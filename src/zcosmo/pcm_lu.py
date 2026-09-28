"""PySCF 2.14.0 PCM: one LU factorization per surface, unchanged equations."""
import os
import numpy as np
import pyscf
from scipy.linalg import lu_factor, lu_solve
from pyscf.solvent.pcm import PCM


class CachedPCM(PCM):
    def _get_vind(self, dms):
        if not self._intermediates:
            self.build()
        it = self._intermediates
        K, R = it["K"], it["R"]
        cached = it.get("_zc_lu")
        if cached is None or cached[0] is not K:
            cached = (K, lu_factor(np.array(K, order="F", copy=True),
                                  overwrite_a=True, check_finite=True))
            it["_zc_lu"] = cached
        nao = dms.shape[-1]
        dms = dms.reshape(-1, nao, nao)
        if len(dms) == 2:
            dms = (dms[0] + dms[1]).reshape(-1, nao, nao)
        v = self.v_grids_n - self._get_v(dms)
        q = lu_solve(cached[1], R @ v.T, check_finite=True).T
        vK = lu_solve(cached[1], v.T, trans=1, check_finite=True)
        qt = (R.T @ vK).T
        qs = (q + qt) / 2.0
        vmat = self._get_vmat(qs)
        it.update(q=q[0], q_sym=qs[0], v_grids=v[0], dm=dms)
        return 0.5 * np.dot(qs[0], v[0]), vmat[0]


def cache_pcm(mf):
    if pyscf.__version__ != "2.14.0":
        raise RuntimeError("Revalidate CachedPCM before changing PySCF 2.14.0")
    old = mf.with_solvent
    if type(old) is not PCM:
        raise TypeError("Expected an unmodified CPU PCM object")
    new = CachedPCM(old.mol)
    new.__dict__.update(old.__dict__)
    mf.with_solvent = new
    return mf


# ---- P9 (E candidate, 2026-09-28): cache the surface 3-centre integrals once per surface -------------------------
# pyscf 2.14 PCM._get_v and ._get_vmat recompute int3c2e(AO pair, surface point) with aosym='s1' on EVERY SCF
# iteration (measured: ~45% of one BP86/SVP C-PCM Berny cycle for 1-octanol and decanoic acid on 4 cores). The
# integrals depend only on the geometry and the surface, so they are computed once (packed lower triangle, 's2ij')
# and contracted by matrix products afterwards. Same integrals, same equations; only summation order changes.
from pyscf import gto, lib, df


class CachedPCM3c(CachedPCM):
    def _zc_blocks(self):
        it = self._intermediates if self._intermediates is not None else {}
        grid = self.surface["grid_coords"]
        c = it.get("_zc_3c")
        if c is not None and c[0] is grid:
            return c[1]
        mol = self.mol
        nao = mol.nao
        npair = nao * (nao + 1) // 2
        exps = self.surface["charge_exp"]
        ngrids = grid.shape[0]
        budget = float(os.environ.get("ZC_PCM3C_MB", "4000")) * 1e6 / 8     # doubles allowed in the cache
        blk = int(max(min(budget / max(npair, 1), ngrids), 1))
        int3c2e = mol._add_suffix("int3c2e")
        cintopt = gto.moleintor.make_cintopt(mol._atm, mol._bas, mol._env, int3c2e)
        blocks = []
        for p0, p1 in lib.prange(0, ngrids, blk):
            if p0 >= blk:                       # beyond the memory budget: those blocks stay uncached
                blocks.append((p0, p1, None)); continue
            fm = gto.fakemol_for_charges(grid[p0:p1], expnt=exps[p0:p1] ** 2)
            fm.cart = mol.cart
            blocks.append((p0, p1, df.incore.aux_e2(mol, fm, intor=int3c2e, aosym="s2ij", cintopt=cintopt)))
        if self._intermediates is not None:
            self._intermediates["_zc_3c"] = (grid, blocks)
        return blocks

    def _zc_block(self, p0, p1, v):
        if v is not None:
            return v
        mol = self.mol
        fm = gto.fakemol_for_charges(self.surface["grid_coords"][p0:p1], expnt=self.surface["charge_exp"][p0:p1] ** 2)
        fm.cart = mol.cart
        return df.incore.aux_e2(mol, fm, intor=mol._add_suffix("int3c2e"), aosym="s2ij")

    def _get_v(self, dms):
        nao = dms.shape[-1]
        nset = dms.shape[0]
        # sum_ij V_ij D_ij = sum_{i>=j} V_ij (D_ij + D_ji) - diagonal counted once
        dt = []
        for i in range(nset):
            d = dms[i] + dms[i].T
            d[np.diag_indices(nao)] *= 0.5
            dt.append(lib.pack_tril(d))
        dt = np.asarray(dt)
        out = np.empty((nset, self.surface["grid_coords"].shape[0]))
        for p0, p1, v in self._zc_blocks():
            out[:, p0:p1] = dt @ self._zc_block(p0, p1, v)
        return out

    def _get_vmat(self, q):
        nao = self.mol.nao
        ng = self.surface["grid_coords"].shape[0]
        q = q.reshape(-1, ng)
        acc = np.zeros((q.shape[0], nao * (nao + 1) // 2))
        for p0, p1, v in self._zc_blocks():
            acc += q[:, p0:p1] @ self._zc_block(p0, p1, v).T
        return -np.asarray([lib.unpack_tril(a) for a in acc])


def cache_pcm3c(mf):
    mf = cache_pcm(mf)
    new = CachedPCM3c(mf.with_solvent.mol)
    new.__dict__.update(mf.with_solvent.__dict__)
    mf.with_solvent = new
    return mf
