"""E-class regression: cached C-PCM paths (P1 LU reuse, P9 surface-integral cache) reproduce stock pyscf 2.14."""
import numpy as np
import pytest

pyscf = pytest.importorskip("pyscf")
from pyscf import dft, gto
from pyscf.data import elements

from zcosmo.pcm_lu import cache_pcm, cache_pcm3c
from zcosmo.pyscf_cosmo import BOHR, RADII


def _run(wrap, spin, atoms):
    mol = gto.M(atom=atoms, unit="Angstrom", basis="def2-svp", spin=spin, verbose=0)
    mf = (dft.UKS(mol) if spin else dft.RKS(mol)).density_fit().PCM()
    if wrap:
        mf = wrap(mf)
    mf.xc = "b88,p86"; mf.grids.level = 2; mf.conv_tol = 1e-9
    s = mf.with_solvent; s.method = "C-PCM"; s.eps = 1e9; s.lebedev_order = 17
    tb = np.zeros(120)
    for el, r in RADII.items():
        tb[elements.charge(el)] = r / BOHR
    s.radii_table = tb
    e = mf.kernel()
    return e, np.asarray(mf.nuc_grad_method().kernel()), np.asarray(mf.with_solvent._intermediates["q"])


@pytest.mark.parametrize("label,atoms,spin", [("water", "O 0 0 0; H 0 .76 .59; H 0 -.76 .59", 0),
                                              ("oxygen", "O 0 0 0; O 0 0 1.21", 2)])
@pytest.mark.parametrize("wrap", [cache_pcm, cache_pcm3c])
def test_cached_pcm_matches_stock(label, atoms, spin, wrap):
    ref, cand = _run(None, spin, atoms), _run(wrap, spin, atoms)
    assert abs(cand[0] - ref[0]) < 1e-8
    assert abs(cand[1] - ref[1]).max() < 1e-6
    assert abs(cand[2] - ref[2]).max() < 1e-8


def test_partial_cache_matches(monkeypatch):
    monkeypatch.setenv("ZC_PCM3C_MB", "0.05")   # forces uncached tail blocks
    atoms = "O 0 0 0; H 0 .76 .59; H 0 -.76 .59"
    ref, cand = _run(None, 0, atoms), _run(cache_pcm3c, 0, atoms)
    assert abs(cand[0] - ref[0]) < 1e-8 and abs(cand[1] - ref[1]).max() < 1e-6
