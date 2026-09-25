"""Dimerization thermochemistry for the Z0w association term.

For each H-bond dimer in results/qc/hbond_dimers_b3lyp_def2-tzvp.csv:
  - relax dimer and both monomers with GFN2-xTB (tblite + ASE),
  - harmonic frequencies by finite differences,
  - ideal-gas H and G at 298.15 K, 1 atm, with Grimme's quasi-RRHO entropy (free-rotor interpolation
    for modes below 100 cm-1),
  - dG = dE(B3LYP-D4, counterpoise, incl. deformation) + dG_thermal(xTB), same for dH.
Writes results/qc/assoc_thermo.csv
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from ase import Atoms
from ase.optimize import BFGS
from ase.vibrations import Vibrations
from ase.thermochemistry import IdealGasThermo
from rdkit import Chem

ROOT = Path(__file__).resolve().parents[2]
KB = 1.380649e-23
H_PL = 6.62607015e-34
C_CM = 2.99792458e10
NA = 6.02214076e23
KCAL = 4184.0
EV_KCAL = 23.060548


def _calc():
    from tblite.ase import TBLite
    return TBLite(method="GFN2-xTB", verbosity=0)


def relax(sym, x, fmax=0.005):
    at = Atoms(sym, positions=x)
    at.calc = _calc()
    BFGS(at, logfile=None).run(fmax=fmax, steps=1000)
    return at


def freqs_cm(at, name):
    vib = Vibrations(at, name=str(ROOT / "results/qc/vib" / name), delta=0.005)
    vib.clean()
    vib.run()
    e = vib.get_energies()  # eV, complex for imaginary
    vib.clean()
    f = np.real(e) / (H_PL * C_CM / 1.602176634e-19)  # cm-1
    return f


def qrrho_entropy(freqs, T, nu0=100.0, alpha=4, Bav=1e-44):
    """Vibrational entropy (J/mol/K) with Grimme's quasi-RRHO treatment."""
    S = 0.0
    for nu in freqs:
        if nu <= 1.0:
            continue
        x = H_PL * C_CM * nu / (KB * T)
        Sv = KB * (x / np.expm1(x) - np.log1p(-np.exp(-x)))
        mu = H_PL / (8 * np.pi ** 2 * C_CM * nu)
        mup = mu * Bav / (mu + Bav)
        Sr = KB * (0.5 + np.log(np.sqrt(8 * np.pi ** 3 * mup * KB * T / H_PL ** 2)))
        w = 1 / (1 + (nu0 / nu) ** alpha)
        S += w * Sv + (1 - w) * Sr
    return S * NA


def thermo(at, name, T=298.15, P=101325.0):
    f = freqs_cm(at, name)
    n = len(at)
    linear = n == 2
    nvib = 3 * n - (5 if linear else 6)
    fr = np.sort(f)[-nvib:]
    fr = np.where(fr < 20.0, 20.0, fr)  # floor for numerically soft/imaginary modes
    energies_ev = fr * (H_PL * C_CM / 1.602176634e-19)
    th = IdealGasThermo(vib_energies=energies_ev, geometry="linear" if linear else "nonlinear", atoms=at,
                        symmetrynumber=1, spin=0, potentialenergy=0.0)
    H = th.get_enthalpy(T, verbose=False) * EV_KCAL  # kcal/mol, thermal part (incl. ZPE)
    S_tr_rot = (th.get_entropy(T, P, verbose=False) * EV_KCAL * KCAL
                - th._vib_entropy(T) * EV_KCAL * KCAL if hasattr(th, "_vib_entropy") else None)
    # recompute S = S_trans + S_rot (ASE) + S_vib (qRRHO)
    S_total_ase = th.get_entropy(T, P, verbose=False) * EV_KCAL * KCAL  # J/mol/K
    x = H_PL * C_CM * fr / (KB * T)
    Sv_harm = NA * KB * np.sum(x / np.expm1(x) - np.log1p(-np.exp(-x)))
    S = S_total_ase - Sv_harm + qrrho_entropy(fr, T)
    G = H - T * S / KCAL
    return H, S, G, fr


def main(T=298.15):
    d = pd.read_csv(ROOT / "results/qc/hbond_dimers_b3lyp_def2-tzvp.csv")
    from zcosmo.qc_hbond import DIMERS
    nd = {row[0]: Chem.AddHs(Chem.MolFromSmiles(row[1])).GetNumAtoms() for row in DIMERS}
    (ROOT / "results/qc/vib").mkdir(parents=True, exist_ok=True)
    rows = []
    for r in d.itertuples():
        g = json.loads(r.xyz)
        sym, x = g["sym"], np.array(g["x"])
        k = nd[r.label]
        ab = relax(sym, x)
        a = relax(sym[:k], x[:k])
        b = relax(sym[k:], x[k:])
        tag = r.label.replace("->", "_").replace(" ", "")
        Hab, Sab, Gab, fab = thermo(ab, tag + "_ab", T)
        Ha, Sa, Ga, _ = thermo(a, tag + "_a", T)
        Hb, Sb, Gb, _ = thermo(b, tag + "_b", T)
        dHt, dSt, dGt = Hab - Ha - Hb, Sab - Sa - Sb, Gab - Ga - Gb
        dE = r.E_bind_kcal
        rows.append(dict(label=r.label, donor_prof=r.donor_prof, acceptor_prof=r.acceptor_prof, dE_kcal=dE,
                         dH_thermal_kcal=dHt, dS_J_molK=dSt, dG_thermal_kcal=dGt, dH_kcal=dE + dHt,
                         dG_kcal=dE + dGt, n_soft_modes=int(np.sum(fab < 50))))
        print(rows[-1], flush=True)
    pd.DataFrame(rows).to_csv(ROOT / "results/qc/assoc_thermo.csv", index=False)


if __name__ == "__main__":
    main()
