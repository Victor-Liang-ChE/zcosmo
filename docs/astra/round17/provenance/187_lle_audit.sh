# Audit (Astra round-1 finding): evaluate.binodal returns None ("no split") when the model cannot be evaluated
# (missing profile -> NaN, or an exception), so failures are counted as miscible. Count failures per model on the LLE
# test rows (positives) and the LLE negatives, and recompute recall / false-positive / balanced accuracy on rows where the
# model actually evaluates. Diagnostic only: the registered scorecard is not changed by this job.
P="$HOME/Projects/BIP Free Predictive Modeling"; cd "$P" || exit 1
source /opt/miniconda3/etc/profile.d/conda.sh; conda activate zcosmo
PYTHONPATH=src python - <<'PY'
import numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from zcosmo.models import make_model
from zcosmo.evaluate import _smiles
smi = _smiles()
neg = pd.read_csv("results/predictions/lle_negatives.csv"); print("negatives cols:", list(neg.columns)[:14], len(neg))
def evaluable(m, a, b, T):
    try:
        mod = make_model(m, [a, b], [smi[a], smi[b]])
        v = [mod.lngamma(T, np.array([x, 1 - x])) for x in (1e-4, 0.5, 1 - 1e-4)]
        return bool(np.all(np.isfinite(v)))
    except Exception:
        return False
for m in ["unifac_do", "cosmosac2010", "Z0x", "Z0w"]:
    try: d = pd.read_csv(f"results/predictions/{m}__lle__all.csv")
    except FileNotFoundError: print(m, "no predictions"); continue
    d = d[d.split != "train"]
    s = np.where(d.c1 < d.c2, d.c1 + "|" + d.c2, d.c2 + "|" + d.c1); d = d.assign(pair=s)
    ok = {}
    for (p, T), g in d.groupby(["pair", "T"]):
        a, b = p.split("|"); ok[(p, T)] = evaluable(m, a, b, float(T))
    d["ok"] = [ok[(p, T)] for p, T in zip(d.pair, d["T"])]
    rec_all = (d.groupby("pair").pred_split.mean() > 0.5).mean()
    dd = d[d.ok]; rec_ok = (dd.groupby("pair").pred_split.mean() > 0.5).mean()
    n = neg[neg.split != "train"] if "split" in neg else neg
    ca, cb = [c for c in n.columns if c.lower() in ("c1", "solute", "comp1")][0], [c for c in n.columns if c.lower() in ("c2", "solvent", "comp2")][0]
    tcol = "T" if "T" in n.columns else None
    nok = np.array([evaluable(m, a, b, float(t) if tcol else 298.15) for a, b, t in zip(n[ca], n[cb], n[tcol] if tcol else [298.15] * len(n))])
    fp_all = n[f"fp_{m}"].mean(); fp_ok = n[f"fp_{m}"][nok].mean()
    print(f"{m:13s} positives: {d.pair.nunique()} pairs, not evaluable {d[~d.ok].pair.nunique()} | recall all {rec_all:.3f} evaluable-only {rec_ok:.3f} || negatives: {len(n)}, not evaluable {int((~nok).sum())} | fp all {fp_all:.3f} evaluable-only {fp_ok:.3f} | bal all {(rec_all+1-fp_all)/2:.3f} evaluable-only {(rec_ok+1-fp_ok)/2:.3f}")
PY
