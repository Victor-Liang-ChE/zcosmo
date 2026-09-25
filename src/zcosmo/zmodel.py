"""Build the Z0 parameter set (no experimental input) and its ablations.

Z0 recipe (fixed in PREREGISTRATION.md before any Z0 result was computed):
  a_eff     = pi * r_av^2 with the r_av used to average the sigma profiles (7.25 A^2);
              a geometric identity, not a new constant.
  c_ES      = alpha'/2 with Klamt's electrostatic estimate alpha' = 0.3 a_eff^1.5 / eps0,
              conductor limit (f_pol = 1), temperature independent (B_ES = 0).
  c_hb      = one constant per class (OH-OH, OH-OT, OT-OT) from B3LYP-D4/def2-TZVP
              counterpoise dimer energies (dispersion part removed, since dispersion
              has its own term), matched to one contacting segment pair:
                  E_HB = c_ES (sD + sA)^2 - c_hb (sD - sA)^2
              sD = mean sigma of the most negative a_eff of the donor-type profile,
              sA = mean sigma of the most positive a_eff of the acceptor-type profile.
  dispersion = London term from D4 molecular C6 and polarizabilities, weight 1.
Z1 = Z0 with one global scale s on every interaction energy, fitted on the train
split IDAC only.
"""
from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

import numpy as np
import pandas as pd

from zcosmo.cosmosac import Params, load_fluid, SIG

ROOT = Path(__file__).resolve().parents[2]
ZP = ROOT / "results" / "z_params"
EPS0 = 2.395e-4  # e^2 / (kcal/mol * A), vacuum permittivity in COSMO units
PROF = {"NHB": 0, "OH": 1, "OT": 2}


def c_es_theory(aeff=7.25, fpol=1.0):
    return fpol * 0.3 * aeff ** 1.5 / EPS0 / 2.0


def tail_sigma(key, prof, side, aeff=7.25):
    """Area-weighted mean sigma of the most extreme a_eff of one side of a profile."""
    f = load_fluid(key)
    p = f.psigA[PROF[prof]].copy()
    order = np.argsort(SIG) if side == "neg" else np.argsort(-SIG)
    mask = (SIG < 0) if side == "neg" else (SIG > 0)
    acc, num = 0.0, 0.0
    for i in order:
        if not mask[i] or p[i] <= 0:
            continue
        take = min(p[i], aeff - acc)
        num += take * SIG[i]
        acc += take
        if acc >= aeff - 1e-12:
            break
    return num / acc if acc > 0 else np.nan


def hb_constants(dimer_csv, c_es, use_disp_free=True):
    d = pd.read_csv(dimer_csv)
    rows = []
    for r in d.itertuples():
        sD = tail_sigma(r.donor_key, r.donor_prof, "neg")
        sA = tail_sigma(r.acceptor_key, r.acceptor_prof, "pos")
        E = r.E_bind_kcal - (r.E_disp_kcal if use_disp_free else 0.0)
        c = (c_es * (sD + sA) ** 2 - E) / (sD - sA) ** 2
        cls = "-".join(sorted([r.donor_prof, r.acceptor_prof]))
        rows.append(dict(label=r.label, cls=cls, sigma_D=sD, sigma_A=sA, E_HB_kcal=E, c_hb=c))
    t = pd.DataFrame(rows)
    by = t.groupby("cls").c_hb.agg(["mean", "std", "count"])
    return t, by


def write(name, prm: Params, note, extra=None):
    ZP.mkdir(parents=True, exist_ok=True)
    d = {"name": name, "note": note, "params": asdict(prm)}
    if extra:
        d.update(extra)
    (ZP / f"{name}.json").write_text(json.dumps(d, indent=1, default=float))


def build(dimer_csv=ROOT / "results/qc/hbond_dimers_b3lyp_def2-tzvp.csv"):
    ces = c_es_theory()
    t, by = hb_constants(dimer_csv, ces)
    t.to_csv(ROOT / "results/qc/hb_constants_per_dimer.csv", index=False)
    by.to_csv(ROOT / "results/qc/hb_constants_by_class.csv")
    c = by["mean"].to_dict()
    hb = dict(c_OH_OH=c["OH-OH"], c_OH_OT=c["OH-OT"], c_OT_OT=c["OT-OT"])
    fitted = Params()
    z0 = Params(A_ES=ces, B_ES=0.0, disp_mode="london", w_dsp=1.0, **hb)
    extra = {"c_ES_theory": ces, "hb_by_class": by.reset_index().to_dict("records")}
    write("Z0", z0, "all constants from theory / quantum chemistry", extra)
    # single-replacement ablations starting from the fitted COSMO-SAC-dsp
    write("abl_es", fitted.with_(A_ES=ces, B_ES=0.0), "fitted model, electrostatics from theory")
    write("abl_hb", fitted.with_(**hb), "fitted model, H-bond constants from DFT dimers")
    write("abl_disp", fitted.with_(disp_mode="london", w_dsp=1.0), "fitted model, London dispersion")
    write("Z0_nodisp", z0.with_(disp_mode="none"), "Z0 without any dispersion term")
    print(by)
    print("c_ES theory:", ces, " fitted at 298 K:", fitted.A_ES + fitted.B_ES / 298.15 ** 2)
    return z0


def scaled(z0: Params, s: float) -> Params:
    return z0.with_(A_ES=z0.A_ES * s, B_ES=z0.B_ES * s, c_OH_OH=z0.c_OH_OH * s, c_OT_OT=z0.c_OT_OT * s,
                    c_OH_OT=z0.c_OH_OT * s, w_dsp=z0.w_dsp * s)


if __name__ == "__main__":
    build()
