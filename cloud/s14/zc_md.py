"""Lean MACE MD engine: feeds the model directly (no ASE per step) with a Verlet neighbour list.

Exactness argument: MACE multiplies every edge by a radial cutoff envelope that is identically 0 for r >= r_max,
so passing a superset of edges (all pairs within r_max + skin at list-build time) gives the same energy and
forces as the exact list. The list stays a valid superset while no atom has moved more than skin/2 since the
build (triangle inequality), so it is rebuilt only then. Positions are kept unwrapped between rebuilds so the
integer image shifts recorded at build time stay correct; shifts = unit_shifts @ cell."""
import numpy as np, torch
from matscipy.neighbours import neighbour_list


class VerletMACE:
    def __init__(self, calc, atoms, skin=1.0, filter=True):
        self.filter = filter
        self.calc, self.model = calc, calc.models[0]
        self.rc = float(self.model.r_max)
        self.skin = skin
        self.atoms = atoms.copy()
        self.dev = next(self.model.parameters()).device
        self.dtype = next(self.model.parameters()).dtype
        base = calc._atoms_to_batch(self.atoms)
        self.bd = {k: v for k, v in base.to_dict().items()}
        self.cell = torch.tensor(np.asarray(self.atoms.cell), dtype=self.dtype, device=self.dev)
        self.n_rebuild = 0
        self._build(torch.tensor(self.atoms.positions, dtype=self.dtype, device=self.dev))

    def _build(self, pos):
        a = self.atoms; a.positions = pos.detach().cpu().double().numpy()
        i, j, S = neighbour_list("ijS", a, self.rc + self.skin)
        self.bd["edge_index"] = torch.tensor(np.stack([i, j]), dtype=torch.long, device=self.dev)  # MACE: sender, receiver
        us = torch.tensor(S, dtype=self.dtype, device=self.dev)
        self.bd["unit_shifts"] = us
        self.bd["shifts"] = us @ self.cell
        self.x_ref = pos.detach().clone()
        self.n_rebuild += 1

    def forces(self, pos):
        """pos: (N,3) tensor, unwrapped. Returns (energy, forces)."""
        if (pos - self.x_ref).norm(dim=1).max() > 0.5 * self.skin:
            self._build(pos)
        bd = dict(self.bd)
        if self.filter:   # keep only edges inside r_max this step (identical result, fewer edges to evaluate)
            s, r = self.bd["edge_index"]
            d = (pos[r] - pos[s] + self.bd["shifts"]).norm(dim=1)
            keep = d < self.rc
            bd["edge_index"] = self.bd["edge_index"][:, keep]
            bd["shifts"] = self.bd["shifts"][keep]
            bd["unit_shifts"] = self.bd["unit_shifts"][keep]
        bd["positions"] = pos.detach().to(self.dtype).requires_grad_(True)
        out = self.model(bd, compute_force=True, training=False)
        return out["energy"].detach(), out["forces"].detach()
