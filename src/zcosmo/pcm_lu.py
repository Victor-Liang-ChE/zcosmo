"""PySCF 2.14.0 PCM: one LU factorization per surface, unchanged equations."""
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
