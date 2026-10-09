# Read-only pairing of archived Figures 1 and 5 with stored inputs (mask counts, hashes, panel values). No model call.
P="$HOME/Projects/BIP Free Predictive Modeling"; cd "$P" || exit 1
source /opt/miniconda3/etc/profile.d/conda.sh; conda activate zcosmo
for f in results/predictions/{cosmosac2010,unifac_do,Z0x,hanna}__idac__all.csv data/benchmark/compounds.csv manuscript/figures/fig1_idac_parity_test.png manuscript/figures/fig5_error_map.png; do
  echo "$(shasum -a 256 "$f" | cut -c1-64) $(stat -f '%Sm' -t '%Y-%m-%dT%H:%M' "$f") $f"; done
git log -1 --format='fig1 committed %h %ad' --date=iso -- manuscript/figures/fig1_idac_parity_test.png
PYTHONPATH=src python - <<'PY'
import numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
P="results/predictions/"; models=["cosmosac2010","unifac_do","Z0x","hanna"]
fr={m:pd.read_csv(f"{P}{m}__idac__all.csv") for m in models}
print("rows per file",{m:len(f) for m,f in fr.items()})
ok=np.ones(len(fr[models[0]]),bool)
for f in fr.values(): ok&=f.pred_ln_gamma_inf.notna().to_numpy()
for m in models:
    d=fr[m][ok&(fr[m].split!="train").to_numpy()]
    sysn=len(set(zip(d.solute,d.solvent))) if "solute" in d else -1
    print(f"fig1 {m} n {len(d)} systems {sysn} MAE {(d.pred_ln_gamma_inf-d.ln_gamma_inf).abs().mean():.4f}")
from zcosmo.error_map import family
comp=pd.read_csv("data/benchmark/compounds.csv"); fam={k:family(s) for k,s in zip(comp.inchikey,comp.smiles)}
a=fr["Z0x"]; b=fr["cosmosac2010"]; ok=a.pred_ln_gamma_inf.notna()&b.pred_ln_gamma_inf.notna()
d=a[ok].copy(); d["dz"]=(a.pred_ln_gamma_inf-a.ln_gamma_inf).abs()[ok]-(b.pred_ln_gamma_inf-b.ln_gamma_inf).abs()[ok]
d["fs"]=d.solute.map(fam); d["fv"]=d.solvent.map(fam)
g=d.groupby(["fs","fv"]).agg(n=("dz","size"),dz=("dz","mean")).reset_index(); g=g[g.n>=10]
print("fig5 rows", int(ok.sum()), "cells>=10", len(g), "dz range", round(g.dz.min(),2), round(g.dz.max(),2))
rows=g.groupby("fs").n.sum().sort_values(ascending=False).index[:9]; cols=g.groupby("fv").n.sum().sort_values(ascending=False).index[:8]
print("fig5 rows", list(rows)); print("fig5 cols", list(cols))
PY
