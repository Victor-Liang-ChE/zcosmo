"""Exact speed-ups on top of zc_md.VerletMACE:
 (a) GPU neighbour list (minimum image; exact when the cubic box L > 2 (r_max + skin)),
 (b) half-edge symmetry: edges stored as [canonical ; reversed]; spherical harmonics of the reversed edge equal
     (-1)^l times the canonical ones and the per-edge radial MLP weights are identical, so only half are computed,
 (c) optional static-shape padding (dummy edges longer than r_max contribute exactly zero) for CUDA graphs."""
import math, numpy as np, torch
from zc_md import VerletMACE


class _Half(torch.nn.Module):
    def __init__(self, mod, sign=None):
        super().__init__(); self.mod = mod; self.register_buffer("sign", sign) if sign is not None else setattr(self, "sign", None)
    def forward(self, x, *a, **k):
        K = x.shape[0] // 2
        h = self.mod(x[:K], *a, **k)
        return torch.cat([h, h * self.sign if self.sign is not None else h], 0)


def sh_sign(sh_mod, dev, dtype):
    irreps = getattr(sh_mod, "irreps_out", None)
    s = []
    for mul, ir in irreps:
        s += [(-1.0) ** ir.l] * (mul * (2 * ir.l + 1))
    return torch.tensor(s, device=dev, dtype=dtype)


def patch_half(model):
    """Wrap spherical harmonics and every interaction's radial MLP. Returns list of what was wrapped."""
    done = []
    p = next(model.parameters())
    if hasattr(model, "spherical_harmonics"):
        model.spherical_harmonics = _Half(model.spherical_harmonics, sh_sign(model.spherical_harmonics, p.device, p.dtype)); done.append("sh")
    for i, blk in enumerate(getattr(model, "interactions", [])):
        if hasattr(blk, "conv_tp_weights"):
            blk.conv_tp_weights = _Half(blk.conv_tp_weights); done.append(f"radial{i}")
    return done


class FastMACE(VerletMACE):
    def __init__(self, calc, atoms, skin=1.0, gpu_nl=True, half=False, pad_to=None):
        self.gpu_nl, self.half, self.pad_to = gpu_nl, half, pad_to
        super().__init__(calc, atoms, skin=skin, filter=True)

    def _build(self, pos):
        if not self.gpu_nl:
            return super()._build(pos)
        L = float(self.cell[0, 0]); rc = self.rc + self.skin
        assert L > 2 * rc, "box too small for minimum-image GPU list"
        d = pos[None, :, :] - pos[:, None, :]                    # d[i, j] = x_j - x_i
        S = -torch.round(d / L)
        r = (d + S * L).norm(dim=-1)
        m = (r < rc); m.fill_diagonal_(False)
        m = torch.triu(m, diagonal=1)                            # canonical i < j
        i, j = m.nonzero(as_tuple=True); Sc = S[i, j]
        ei = torch.stack([torch.cat([i, j]), torch.cat([j, i])])
        us = torch.cat([Sc, -Sc])
        self.bd["edge_index"], self.bd["unit_shifts"] = ei, us.to(self.dtype)
        self.bd["shifts"] = self.bd["unit_shifts"] @ self.cell
        self.x_ref = pos.detach().clone(); self.n_rebuild += 1

    def forces(self, pos):
        if (pos - self.x_ref).norm(dim=1).max() > 0.5 * self.skin:
            self._build(pos)
        bd = dict(self.bd)
        K = bd["edge_index"].shape[1] // 2
        s, r = bd["edge_index"][:, :K]
        dd = (pos[r] - pos[s] + bd["shifts"][:K]).norm(dim=1)
        keep = torch.nonzero(dd < self.rc).flatten()
        idx = torch.cat([keep, keep + K])
        ei, sh, us = bd["edge_index"][:, idx], bd["shifts"][idx], bd["unit_shifts"][idx]
        if self.pad_to:                                           # dummy edges: node 0 -> node 0 shifted by n*L (> r_max)
            npad = self.pad_to - keep.numel()
            assert npad >= 0
            L = float(self.cell[0, 0]); far = torch.zeros(npad, 3, device=pos.device, dtype=self.dtype); far[:, 0] = math.ceil(self.rc / L + 1)
            z = torch.zeros(npad, dtype=torch.long, device=pos.device)
            ei = torch.cat([torch.cat([ei[:, :keep.numel()], torch.stack([z, z])], 1), torch.cat([ei[:, keep.numel():], torch.stack([z, z])], 1)], 1)
            us = torch.cat([us[:keep.numel()], far, us[keep.numel():], -far]); sh = us @ self.cell
        bd["edge_index"], bd["shifts"], bd["unit_shifts"] = ei, sh, us
        bd["positions"] = pos.detach().to(self.dtype).requires_grad_(True)
        out = self.model(bd, compute_force=True, training=False)
        return out["energy"].detach(), out["forces"].detach()
