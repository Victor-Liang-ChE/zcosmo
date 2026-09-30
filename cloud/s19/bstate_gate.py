"""E-gate runner for pyberny state persistence (PREREGISTRATION.md, 2026-09-30).
Usage: bstate_gate.py MODE KEY OUTDIR
  full : uninterrupted registered path (cap 100 steps, no state)
  state: per-pass cap 5 steps, ZC_BERNY_STATE=1 (optimiser state restored on every resume)
  geom : per-pass cap 5 steps, geometry-only resume (today's behaviour)
Loops the registered run_one() until the profile exists; writes OUTDIR/gate.json with the pass and gradient-evaluation counts."""
import json, os, sys, time
from pathlib import Path
import pandas as pd
mode, key, out = sys.argv[1:4]
CAP = 100 if mode == "full" else 5
os.environ["ZC_MAXSTEPS"] = str(CAP)
os.environ["ZC_BERNY_STATE"] = "1" if mode == "state" else "0"
import zcosmo.pyscf_cosmo_v2 as _m
from zcosmo.pyscf_cosmo_v2 import run_one
_orig, CYC = _m.dft_geometry, []
def _counted(*a, **k):  # run_one deletes the checkpoint on success, so read the cycle count before it does
    try:
        return _orig(*a, **k)
    finally:
        pp = k.get("partial")
        if pp is not None and Path(pp).exists():
            CYC.append(json.loads(Path(pp).read_text())["cycle"] + 1)
_m.dft_geometry = _counted
d = pd.read_csv("data/benchmark/compounds.csv"); row = d[d.inchikey == key].iloc[0].to_dict()
Path(out).mkdir(parents=True, exist_ok=True)
t0, passes, evals = time.time(), 0, 0
partial = Path(out) / f"{key}.partial.json"
while True:
    passes += 1
    k, st, dt = run_one(row, out)
    c = CYC[-1] if CYC else -1
    evals += c
    print(mode, key, "pass", passes, st[:60], f"{dt:.0f}s", "cycles_in_pass", c, flush=True)
    if st in ("ok", "exists"): break
    if not st.startswith("fail: RuntimeError('Berny did not converge") or passes >= 60:
        raise SystemExit("gate run aborted: " + st)
Path(out, "gate.json").write_text(json.dumps({"mode": mode, "key": key, "cap": CAP, "passes": passes,
                                              "gradient_evaluations": evals, "evals_valid": True, "seconds": round(time.time() - t0)}))
print("GATE", mode, key, "passes", passes, "evals", evals, flush=True)
