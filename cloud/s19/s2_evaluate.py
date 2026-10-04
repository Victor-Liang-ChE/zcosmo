"""Rule S2 evaluation (PREREGISTRATION.md, entry of 2026-10-04). Usage (repo root, Mac, UD profiles present):
s2_evaluate.py ARTDIR OUTJSON   where ARTDIR holds the s2_<KEY>_<ITEM> artifacts of the s2-profiles run.
Decides each chain by the registered conditions; writes nothing into data/. ln gamma-infinity is evaluated in a separate process per profile set."""
import glob, json, os, subprocess, sys, tempfile
import numpy as np
art, outjson = sys.argv[1:3]
KEYS = ["BTFJIXJJCSYFAL-UHFFFAOYSA-N", "FLIACVVOZYBSBS-UHFFFAOYSA-N", "HPEUJPJOZXNMSJ-UHFFFAOYSA-N", "MVLVMROFTAUDAG-UHFFFAOYSA-N", "OYHQOLUKZRVURQ-HZJYTTRNSA-N", "PYGXAGIECVVIOZ-UHFFFAOYSA-N"]
ROT = [f"r{i}" for i in range(8)]
def f(key, item, ext): 
    g = glob.glob(f"{art}/**/{key}.{item}.{ext}", recursive=True); return g[0] if g else None
def prof(path):
    A = np.array([[float(v) for v in l.split()] for l in open(path) if l.strip() and not l.startswith("#")]); n = len(A) // 3
    return [A[i * n:(i + 1) * n, 1] for i in range(3)]
def dp(a, b): return float(max(np.abs(x - y).max() for x, y in zip(prof(a), prof(b))))
LNG = r'''
import os, sys, glob, shutil, numpy as np, pandas as pd
K, sig, outnpy = sys.argv[1:4]; P = os.getcwd()
D = os.path.join(os.environ["TMPDIR"] if "TMPDIR" in os.environ else "/tmp", "s2ov_" + os.path.basename(outnpy)); shutil.rmtree(D, ignore_errors=True); os.makedirs(D)
for f in glob.glob(f"{P}/data/pyscf_sigma/profiles_v2/*.sigma"): os.symlink(f, f"{D}/{os.path.basename(f)}")
if os.path.lexists(f"{D}/{K}.sigma"): os.remove(f"{D}/{K}.sigma")
shutil.copy(sig, f"{D}/{K}.sigma"); os.environ["ZC_SIGMA_OVERRIDE_DIR"] = D
from zcosmo.evaluate import _smiles
from zcosmo.models import make_model
smi = _smiles(); idac = pd.read_csv("data/benchmark/idac.csv"); rows = idac[(idac.solute == K) | (idac.solvent == K)]
out, cache = [], {}
for r in rows.itertuples():
    k = (r.solute, r.solvent)
    try:
        if k not in cache: cache[k] = make_model("cosmosac_dsp", [r.solute, r.solvent], [smi[r.solute], smi[r.solvent]])
        out.append(cache[k].lngamma_inf(r.T, 0))
    except Exception: out.append(np.nan)
np.save(outnpy, np.array(out, dtype=float))
'''
lngpy = os.path.join(tempfile.mkdtemp(), "lng_one.py"); open(lngpy, "w").write(LNG)
def lng(key, sig, tag):
    o = os.path.join(os.path.dirname(lngpy), f"{key[:10]}_{tag}.npy")
    subprocess.run([sys.executable, lngpy, key, sig, o], check=True, stderr=subprocess.DEVNULL); return np.load(o)
res = []
for k in KEYS:
    r = dict(key=k); paths = {i: f(k, i, "sigma") for i in ["new", "old", "xtb", "pert"] + ROT}
    gj = f(k, "grad", "json")
    missing = [i for i, p in paths.items() if p is None] + ([] if gj else ["grad"])
    if missing: r.update(missing=missing, accepted=False, reason="missing items: " + ",".join(missing)); res.append(r); print(json.dumps(r)); continue
    g = json.load(open(gj)); r.update(grad_max=g["grad_max"], grad_rms=g["grad_rms"], displacement_A=g["displacement_new_vs_old_A"], evaluations_between=100)
    rot = [dp(paths["new"], paths[i]) for i in ROT]
    r.update(dp_rot=rot, T_med=float(np.median(rot)), T_max=float(max(rot)), dp_new_old=dp(paths["new"], paths["old"]),
             dp_new_xtb=dp(paths["new"], paths["xtb"]), dp_new_pert_report_only=dp(paths["new"], paths["pert"]))
    a, b = r["grad_max"] < 4.5e-4 and r["grad_rms"] < 1.5e-4, r["displacement_A"] <= 0.005
    c1, d = r["dp_new_old"] <= r["T_med"], r["dp_new_xtb"] > r["T_max"]
    ln_new, ln_old = lng(k, paths["new"], "new"), lng(k, paths["old"], "old"); ok = np.isfinite(ln_new) & np.isfinite(ln_old)
    r.update(lng_rows=int(len(ln_new)), lng_rows_finite_both=int(ok.sum()), finite_mask_identical=bool((np.isfinite(ln_new) == np.isfinite(ln_old)).all()),
             max_dlng=float(np.abs(ln_new - ln_old)[ok].max()) if ok.any() else None)
    c2 = r["finite_mask_identical"] and (r["max_dlng"] is None or r["max_dlng"] < 0.05)
    r.update(cond_a=bool(a), cond_b=bool(b), cond_c1=bool(c1), cond_c2=bool(c2), cond_d=bool(d), accepted=bool(a and b and c1 and c2 and d))
    res.append(r); print(json.dumps(r), flush=True)
json.dump(res, open(outjson, "w"), indent=1)
print("ACCEPTED:", [x["key"][:10] for x in res if x.get("accepted")], "| NOT:", [x["key"][:10] for x in res if not x.get("accepted")])
