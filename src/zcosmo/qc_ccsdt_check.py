"""Check the B3LYP-D4 dimer interaction energies against CCSD(T) at the same (xTB) geometries.

E_int(CP) at CCSD(T)/aug-cc-pVDZ plus an MP2 basis-set correction (aug-cc-pVTZ - aug-cc-pVDZ).
Compared with the B3LYP-D4/def2-TZVP E_int(CP) + D4 dispersion used for Z0.
Writes results/qc/ccsdt_check.csv
"""
import json
import os
import time
from pathlib import Path

import numpy as np
import pandas as pd
from pyscf import gto, scf, mp, cc, lib

ROOT = Path(__file__).resolve().parents[2]
H = 627.509474
lib.num_threads(int(os.environ.get("QC_THREADS", "6")))
MEM = int(os.environ.get("QC_MEM_MB", "8000"))
LABELS = ["water->water", "methanol->water", "water->acetone", "water->acetonitrile", "methylamine->methylamine"]


def energies(sym, x, ghost, basis, do_cc):
    atoms = [(("ghost-" + s) if i in ghost else s, tuple(p)) for i, (s, p) in enumerate(zip(sym, x))]
    mol = gto.M(atom=atoms, basis=basis, unit="Angstrom", verbose=0, max_memory=MEM)
    mf = scf.RHF(mol).density_fit() if not do_cc else scf.RHF(mol)
    mf.conv_tol = 1e-10
    mf.kernel()
    m2 = mp.MP2(mf).run()
    out = {"mp2": m2.e_tot}
    if do_cc:
        c = cc.CCSD(mf).run()
        out["ccsdt"] = c.e_tot + c.ccsd_t()
    return out


def eint(sym, x, nd, basis, do_cc):
    n = len(sym)
    ab = energies(sym, x, set(), basis, do_cc)
    a = energies(sym, x, set(range(nd, n)), basis, do_cc)
    b = energies(sym, x, set(range(nd)), basis, do_cc)
    return {k: (ab[k] - a[k] - b[k]) * H for k in ab}


def main():
    d = pd.read_csv(ROOT / "results/qc/hbond_dimers_b3lyp_def2-tzvp.csv").set_index("label")
    out = ROOT / "results/qc/ccsdt_check.csv"
    done = set(pd.read_csv(out).label) if out.exists() else set()
    from zcosmo.qc_hbond import DIMERS
    nd_map = {}
    for row in DIMERS:
        from rdkit import Chem
        nd_map[row[0]] = Chem.AddHs(Chem.MolFromSmiles(row[1])).GetNumAtoms()
    for lab in LABELS:
        if lab in done:
            continue
        t = time.time()
        g = json.loads(d.loc[lab, "xyz"])
        sym, x, nd = g["sym"], np.array(g["x"]), nd_map[lab]
        dz = eint(sym, x, nd, "aug-cc-pvdz", True)
        tz = eint(sym, x, nd, "aug-cc-pvtz", False)
        e_cc = dz["ccsdt"] + (tz["mp2"] - dz["mp2"])
        e_dft = d.loc[lab, "E_int_cp_kcal"] + d.loc[lab, "E_disp_kcal"]
        r = dict(label=lab, E_int_ccsdt_cbs_kcal=e_cc, E_int_ccsdt_adz=dz["ccsdt"], E_int_mp2_atz=tz["mp2"],
                 E_int_b3lyp_d4=e_dft, diff_kcal=e_dft - e_cc, seconds=round(time.time() - t))
        pd.DataFrame([r]).to_csv(out, mode="a", header=not out.exists(), index=False)
        print(r, flush=True)


if __name__ == "__main__":
    main()
