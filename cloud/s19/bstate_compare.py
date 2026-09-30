"""Compare the three gate arms. Usage: bstate_compare.py ROOT KEY1,KEY2  (ROOT/{full,state,geom}/KEY.sigma + gate.json)"""
import json, sys
import numpy as np
root, keys = sys.argv[1], sys.argv[2].split(",")
def prof(p):
    return np.loadtxt(p)[:, 1]
for k in keys:
    g = {m: json.load(open(f"{root}/{m}/{k}/gate.json")) for m in ("full", "state", "geom")}
    x = {m: np.array(json.load(open(f"{root}/{m}/{k}/{k}.xyz.json"))["x"]) for m in g}
    p = {m: prof(f"{root}/{m}/{k}/{k}.sigma") for m in g}
    meta = {m: json.loads(open(f"{root}/{m}/{k}/{k}.sigma").readline()[len("# meta: "):]) for m in g}
    for m in ("state", "geom"):
        print(k, m, "passes", g[m]["passes"], "evals", g[m]["gradient_evaluations"], "vs full evals", g["full"]["gradient_evaluations"],
              "| max|dx| A %.2e" % np.abs(x[m] - x["full"]).max(),
              "| dE Eh %.2e" % abs(meta[m]["E_scf_Eh"] - meta["full"]["E_scf_Eh"]),
              "| max|dp| %.2e" % np.abs(p[m] - p["full"]).max())
