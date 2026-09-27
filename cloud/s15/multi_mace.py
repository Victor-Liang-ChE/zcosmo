"""MultiMACE: evaluate many independent periodic systems as ONE disjoint MACE graph (exact batching).

Motivation (bench11, L4): one force call costs ~37 ms for 192 atoms and ~72 ms for 5,184 atoms, i.e. the GPU is
launch/overhead bound for small boxes. Stacking G systems into one graph costs about the same wall time as one,
so independent replicas / lambda windows / the full-vs-separated pieces of a decoupling run share one call.

Exactness: MACE message passing only runs along edges, and edges only join nodes of the same system, so each
system's energy (per-graph readout) and forces are identical to evaluating it alone. Neighbour lists are GPU
minimum-image lists per system with a Verlet skin and the per-step r < r_max filter (as in zc_md / fast_md)."""
import numpy as np, torch

NODE_KEYS = {"positions", "node_attrs", "forces", "density_coefficients"}
EDGE_KEYS = {"edge_index", "shifts", "unit_shifts"}


class MultiMACE:
    def __init__(self, calc, systems, skin=1.0):
        """systems: list of ASE Atoms (periodic, cubic, L > 2 (r_max + skin))."""
        self.calc, self.model = calc, calc.models[0]
        self.rc = float(self.model.r_max); self.skin = skin
        p = next(self.model.parameters()); self.dev, self.dtype = p.device, p.dtype
        dicts = [calc._atoms_to_batch(a).to_dict() for a in systems]
        self.n = [len(a) for a in systems]
        self.off = np.concatenate([[0], np.cumsum(self.n)]).astype(int)
        self.G, self.M = len(systems), int(self.off[-1])
        bd = {}
        for k in dicts[0]:
            if k in EDGE_KEYS:
                continue
            vs = [d[k] for d in dicts]
            if k == "ptr":
                bd[k] = torch.tensor(self.off, dtype=vs[0].dtype, device=self.dev)
            elif k == "batch":
                bd[k] = torch.cat([torch.full((n,), g, dtype=vs[0].dtype, device=self.dev) for g, n in enumerate(self.n)])
            elif torch.is_tensor(vs[0]):
                bd[k] = torch.cat([v.to(self.dev) for v in vs], 0)
            else:
                bd[k] = vs[0]
        self.bd = bd
        self.L = torch.tensor([float(a.cell[0, 0]) for a in systems], dtype=self.dtype, device=self.dev)
        self.cells = torch.stack([torch.tensor(np.asarray(a.cell), dtype=self.dtype, device=self.dev) for a in systems])
        self.sys = torch.cat([torch.full((n,), g, device=self.dev, dtype=torch.long) for g, n in enumerate(self.n)])
        self.n_rebuild = 0
        self._build(torch.cat([torch.tensor(a.positions, dtype=self.dtype, device=self.dev) for a in systems]))

    def _build(self, pos):
        rc = self.rc + self.skin
        E, US = [], []
        for g in range(self.G):
            a, b = int(self.off[g]), int(self.off[g + 1]); L = float(self.L[g])
            assert L > 2 * rc, "box too small for the minimum-image GPU list"
            x = pos[a:b]
            d = x[None, :, :] - x[:, None, :]
            S = -torch.round(d / L)
            r = (d + S * L).norm(dim=-1)
            m = torch.triu(r < rc, diagonal=1)
            i, j = m.nonzero(as_tuple=True); Sc = S[i, j]
            E.append(torch.stack([torch.cat([i, j]), torch.cat([j, i])]) + a)
            US.append(torch.cat([Sc, -Sc]))
        self.ei = torch.cat(E, 1); self.us = torch.cat(US, 0).to(self.dtype)
        self.sh = torch.bmm(self.us[:, None, :], self.cells[self.sys[self.ei[0]]])[:, 0]
        self.x_ref = pos.detach().clone(); self.n_rebuild += 1

    def forces(self, pos):
        """pos: (M,3) unwrapped positions of all systems stacked. Returns (energies (G,), forces (M,3))."""
        if (pos - self.x_ref).norm(dim=1).max() > 0.5 * self.skin:
            self._build(pos)
        s, r = self.ei
        keep = (pos[r] - pos[s] + self.sh).norm(dim=1) < self.rc
        bd = dict(self.bd)
        bd["edge_index"], bd["shifts"], bd["unit_shifts"] = self.ei[:, keep], self.sh[keep], self.us[keep]
        bd["positions"] = pos.detach().to(self.dtype).requires_grad_(True)
        out = self.model(bd, compute_force=True, training=False)
        e = out.get("interaction_energy")          # E minus the atomic reference energies: same differences,
        e = out["energy"] if e is None else e      # far smaller magnitude (float32 keeps ~1e-6 eV resolution)
        return e.detach(), out["forces"].detach()
