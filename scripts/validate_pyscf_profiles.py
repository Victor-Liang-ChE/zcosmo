"""Registered acceptance test for pyscf_cosmo profiles (see PREREGISTRATION.md)."""
import numpy as np
import pandas as pd
from zcosmo.cosmosac import Mixture, Params, load_fluid

PD = "data/pyscf_sigma/profiles"
val = pd.read_csv("data/pyscf_sigma/validation_set.csv")
idac = pd.read_csv("data/benchmark/idac.csv")
idac = idac[idac.has_sigma]
rows = []
for k in val.inchikey:
    try:
        fp = load_fluid(k, PD)
    except FileNotFoundError:
        continue
    fu = load_fluid(k)
    sub = idac[(idac.solute == k) | (idac.solvent == k)]
    for r in sub.itertuples():
        other = r.solvent if r.solute == k else r.solute
        try:
            fo = load_fluid(other)
        except FileNotFoundError:
            continue
        pair_u = [fu, fo] if r.solute == k else [fo, fu]
        pair_p = [fp, fo] if r.solute == k else [fo, fp]
        mu = Mixture(None, Params(), fluids=pair_u)
        mp_ = Mixture(None, Params(), fluids=pair_p)
        lu, lp = mu.lngamma_inf(r.T, 0), mp_.lngamma_inf(r.T, 0)
        rows.append(dict(key=k, T=r.T, ud=lu, pyscf=lp, exp=r.ln_gamma_inf))
d = pd.DataFrame(rows)
d["diff"] = (d.pyscf - d.ud).abs()
per = d.groupby("key").agg(n=("diff", "size"), med=("diff", "median"),
                           mae_ud=("ud", lambda s: np.nan), )
per["mae_ud"] = d.groupby("key").apply(lambda g: (g.ud - g.exp).abs().mean())
per["mae_pyscf"] = d.groupby("key").apply(lambda g: (g.pyscf - g.exp).abs().mean())
names = dict(zip(val.inchikey, val.smiles))
per["smiles"] = per.index.map(names)
print(per.round(3).to_string())
print("molecules", d.key.nunique(), "rows", len(d))
print("MEDIAN |dlnγ∞| over rows:", round(d["diff"].median(), 4), " mean:", round(d["diff"].mean(), 4))
print("exp MAE ud:", round((d.ud - d.exp).abs().mean(), 3), " pyscf:", round((d.pyscf - d.exp).abs().mean(), 3))
print("ACCEPT" if d["diff"].median() < 0.15 and d.key.nunique() >= 20 else "REJECT")
d.to_csv("results/pyscf_profile_validation.csv", index=False)
