"""Scorecard metrics with system-level paired bootstrap.

Usage: python -m zcosmo.metrics MODEL1 MODEL2 ... [--split test|train|all] [--ref MODEL]
Reads results/predictions/<model>__<table>__all.csv and writes results/scorecard_<split>.json/.md
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[2]
import os
PRED = Path(os.environ.get("ZC_PRED", ROOT / "results" / "predictions"))
PRED_SPLIT = os.environ.get("ZC_PRED_SPLIT", "all")
N_BOOT = 1000
RNG = np.random.default_rng(7)


def _sys(a, b):
    return np.where(a < b, a + "|" + b, b + "|" + a)


def _load(model, table):
    p = PRED / f"{model}__{table}__{PRED_SPLIT}.csv"
    return pd.read_csv(p) if p.exists() else None


def _subset(df, split):
    if split == "temporal":
        return df[df.temporal]
    if split == "temporal_test":
        return df[df.temporal & (df.split != "train")]
    if split == "test":
        return df[df.split != "train"]
    if split == "test_both":
        return df[df.split == "test_both"]
    if split == "train":
        return df[df.split == "train"]
    return df


# ---- per-row error functions: return (errors array, system ids) ----

def err_idac(df):
    e = (df.pred_ln_gamma_inf - df.ln_gamma_inf).to_numpy()
    return e, _sys(df.solute.to_numpy(str), df.solvent.to_numpy(str))


def err_vle_P(df):
    e = (100 * (df.pred_P - df.P) / df.P).to_numpy()
    return e, _sys(df.c1.to_numpy(str), df.c2.to_numpy(str))


_THREE_PHASE = None


def three_phase_mask(df):
    """True for VLE rows whose x1 lies inside a measured liquid-liquid gap of the same binary (+/- 5 K)."""
    global _THREE_PHASE
    if _THREE_PHASE is None:
        lle = pd.read_csv(Path(os.environ.get("ZC_BENCH", ROOT / "data/benchmark")) / "lle.csv")
        lle["s"] = _sys(lle.c1.to_numpy(str), lle.c2.to_numpy(str))
        # express compositions in the sorted-pair orientation
        lle["xs"] = np.where(lle.c1.to_numpy(str) < lle.c2.to_numpy(str), lle.x1, 1 - lle.x1)
        _THREE_PHASE = {s: g[["T", "xs"]].to_numpy() for s, g in lle.groupby("s")}
    s = _sys(df.c1.to_numpy(str), df.c2.to_numpy(str))
    xs = np.where(df.c1.to_numpy(str) < df.c2.to_numpy(str), df.x1, 1 - df.x1)
    out = np.zeros(len(df), bool)
    for i, (k, T, x) in enumerate(zip(s, df["T"].to_numpy(), xs)):
        a = _THREE_PHASE.get(k)
        if a is None:
            continue
        near = a[np.abs(a[:, 0] - T) <= 5, 1]
        lo, hi = near[near < 0.5], near[near >= 0.5]
        if len(lo) and len(hi) and np.median(lo) < x < np.median(hi):
            out[i] = True
    return out


def err_vle_y(df):
    m = df.y1.notna()
    d = df[m]
    return (d.pred_y1 - d.y1).to_numpy(), _sys(d.c1.to_numpy(str), d.c2.to_numpy(str))


def err_he(df):
    return (df.pred_HE_J - df.HE_J).to_numpy(), _sys(df.c1.to_numpy(str), df.c2.to_numpy(str))


def lle_rows(df):
    """Per binodal point: split predicted? and composition error to nearest branch."""
    split = df.pred_split.astype(bool).to_numpy()
    d = np.minimum(np.abs(df.x1 - df.pred_x1_I), np.abs(df.x1 - df.pred_x1_II)).to_numpy()
    return split, d, _sys(df.c1.to_numpy(str), df.c2.to_numpy(str))


def _boot(stat_fn, sys_ids, *arrays):
    """Bootstrap over systems; stat_fn(*arrays_subset) -> float."""
    u, inv = np.unique(sys_ids, return_inverse=True)
    groups = [np.where(inv == k)[0] for k in range(len(u))]
    vals = []
    for _ in range(N_BOOT):
        pick = RNG.integers(0, len(u), len(u))
        idx = np.concatenate([groups[k] for k in pick])
        vals.append(stat_fn(*[a[idx] for a in arrays]))
    return np.percentile(vals, [2.5, 97.5])


def selectivity_spearman(df, col_pred):
    """Solvent-ranking test: for each solute, rank solvents by ln gamma_inf.

    Per solute, one value per solvent (the row with T closest to 298.15 K); solutes with
    >= 5 solvents and an experimental spread >= 1 ln unit. Returns the median Spearman rho
    of predicted vs experimental ranking, and the number of solutes.
    """
    d = df.dropna(subset=[col_pred]).copy()
    d["dT"] = (d["T"] - 298.15).abs()
    d = d.sort_values("dT").drop_duplicates(["solute", "solvent"])
    rhos = []
    for s, g in d.groupby("solute"):
        if len(g) < 5 or g.ln_gamma_inf.max() - g.ln_gamma_inf.min() < 1.0:
            continue
        rhos.append(spearmanr(g.ln_gamma_inf, g[col_pred]).statistic)
    return (float(np.median(rhos)) if rhos else np.nan), len(rhos)


def scorecard(models, split="test", ref=None):
    out = {"split": split, "models": models, "tables": {}}
    # IDAC
    frames = {m: _load(m, "idac") for m in models}
    base = next(f for f in frames.values() if f is not None)
    base = _subset(base, split)
    ok = np.ones(len(base), bool)
    for m, f in frames.items():
        ok &= _subset(f, split).pred_ln_gamma_inf.notna().to_numpy()
    res = {"n_points": int(ok.sum()), "n_systems": int(len(np.unique(err_idac(base[ok])[1]))), "coverage": {}}
    for m, f in frames.items():
        fs = _subset(f, split)
        res["coverage"][m] = float(fs.pred_ln_gamma_inf.notna().mean())
        e, s = err_idac(fs[ok])
        ae = np.abs(e)
        rho, npairs = selectivity_spearman(fs[ok], "pred_ln_gamma_inf")
        res[m] = {"MAE_ln_gamma_inf": float(ae.mean()), "median_AE": float(np.median(ae)),
                  "frac_within_0.3": float((ae <= 0.3).mean()), "bias": float(e.mean()),
                  "MAE_CI95": _boot(lambda a: np.mean(np.abs(a)), s, e).tolist(),
                  "selectivity_spearman_median": rho, "selectivity_pairs": npairs}
    if ref:
        e_ref, s = err_idac(_subset(frames[ref], split)[ok])
        for m in models:
            if m == ref:
                continue
            e_m, _ = err_idac(_subset(frames[m], split)[ok])
            ci = _boot(lambda a, b: np.mean(np.abs(a)) - np.mean(np.abs(b)), s, e_m, e_ref)
            res[m]["delta_MAE_vs_ref_CI95"] = ci.tolist()
    out["tables"]["idac"] = res

    # VLE
    frames = {m: _load(m, "vle") for m in models}
    if all(f is not None for f in frames.values()):
        base = _subset(next(iter(frames.values())), split)
        ok = np.ones(len(base), bool)
        for f in frames.values():
            ok &= _subset(f, split).pred_P.notna().to_numpy()
        res = {"n_points": int(ok.sum()), "coverage": {}}
        for m, f in frames.items():
            fs = _subset(f, split)
            res["coverage"][m] = float(fs.pred_P.notna().mean())
            e, s = err_vle_P(fs[ok])
            ey, sy = err_vle_y(fs[ok])
            hom = ~three_phase_mask(fs[ok])
            res[m] = {"AAD_P_pct": float(np.mean(np.abs(e))), "median_AD_P_pct": float(np.median(np.abs(e))),
                      "AAD_P_pct_homog": float(np.mean(np.abs(e[hom]))), "n_three_phase": int((~hom).sum()),
                      "AAD_P_homog_CI95": _boot(lambda a: np.mean(np.abs(a)), s[hom], e[hom]).tolist(),
                      "AAD_P_CI95": _boot(lambda a: np.mean(np.abs(a)), s, e).tolist(),
                      "AAD_y": float(np.mean(np.abs(ey))) if len(ey) else None, "n_y": int(len(ey))}
        if ref:
            e_ref, s = err_vle_P(_subset(frames[ref], split)[ok])
            hom = ~three_phase_mask(_subset(frames[ref], split)[ok])
            for m in models:
                if m != ref:
                    e_m, _ = err_vle_P(_subset(frames[m], split)[ok])
                    res[m]["delta_AAD_P_vs_ref_CI95"] = _boot(
                        lambda a, b: np.mean(np.abs(a)) - np.mean(np.abs(b)), s, e_m, e_ref).tolist()
                    res[m]["delta_AAD_P_homog_vs_ref_CI95"] = _boot(
                        lambda a, b: np.mean(np.abs(a)) - np.mean(np.abs(b)), s[hom], e_m[hom], e_ref[hom]).tolist()
        out["tables"]["vle"] = res

    # HE
    frames = {m: _load(m, "he") for m in models}
    if all(f is not None for f in frames.values()):
        base = _subset(next(iter(frames.values())), split)
        ok = np.ones(len(base), bool)
        for f in frames.values():
            ok &= _subset(f, split).pred_HE_J.notna().to_numpy()
        res = {"n_points": int(ok.sum()), "coverage": {}}
        for m, f in frames.items():
            fs = _subset(f, split)
            res["coverage"][m] = float(fs.pred_HE_J.notna().mean())
            d = fs[ok]
            big = d.HE_J.abs() > 20
            e, s = err_he(d)
            res[m] = {"MAE_HE_J": float(np.mean(np.abs(e))),
                      "sign_correct": float((np.sign(d.pred_HE_J[big]) == np.sign(d.HE_J[big])).mean()),
                      "MAE_CI95": _boot(lambda a: np.mean(np.abs(a)), s, e).tolist()}
        out["tables"]["he"] = res

    # LLE
    frames = {m: _load(m, "lle") for m in models}
    if all(f is not None for f in frames.values()):
        res = {}
        for m, f in frames.items():
            fs = _subset(f, split)
            sp, d, s = lle_rows(fs)
            sysdet = pd.DataFrame({"s": s, "sp": sp}).groupby("s").sp.mean()
            res[m] = {"n_points": int(len(fs)), "n_systems": int(len(sysdet)),
                      "gap_found_points": float(sp.mean()), "gap_found_systems": float((sysdet > 0.5).mean()),
                      "MAE_x_when_found": float(np.nanmean(d[sp])) if sp.any() else None}
        out["tables"]["lle"] = res
    return out


def to_markdown(sc):
    lines = [f"# Scorecard ({sc['split']})", ""]
    t = sc["tables"]
    if "idac" in t:
        r = t["idac"]
        lines += [f"## IDAC  ({r['n_points']} points, {r['n_systems']} systems, common subset)", "",
                  "| model | coverage | MAE ln g_inf | 95% CI | median AE | within 0.3 | bias | solvent-rank rho | dMAE vs ref (CI) |",
                  "|---|---|---|---|---|---|---|---|---|"]
        for m in sc["models"]:
            x = r[m]
            ci = x["MAE_CI95"]
            d = x.get("delta_MAE_vs_ref_CI95")
            lines.append(f"| {m} | {r['coverage'][m]:.2f} | {x['MAE_ln_gamma_inf']:.3f} | [{ci[0]:.3f}, {ci[1]:.3f}] | "
                         f"{x['median_AE']:.3f} | {x['frac_within_0.3']:.2f} | {x['bias']:+.3f} | "
                         f"{x['selectivity_spearman_median']:.2f} ({x['selectivity_pairs']}) | "
                         f"{'' if d is None else f'[{d[0]:+.3f}, {d[1]:+.3f}]'} |")
        lines.append("")
    if "vle" in t:
        r = t["vle"]
        lines += [f"## VLE bubble pressure ({r['n_points']} points)", "",
                  "| model | coverage | AAD P % | 95% CI | median AD P % | AAD y | dAAD vs ref (CI) | AAD P % homog. liquid | CI | dAAD homog vs ref (CI) |",
                  "|---|---|---|---|---|---|---|---|---|---|"]
        for m in sc["models"]:
            x = r[m]
            ci = x["AAD_P_CI95"]
            d = x.get("delta_AAD_P_vs_ref_CI95")
            lines.append(f"| {m} | {r['coverage'][m]:.2f} | {x['AAD_P_pct']:.2f} | [{ci[0]:.2f}, {ci[1]:.2f}] | "
                         f"{x['median_AD_P_pct']:.2f} | {x['AAD_y'] if x['AAD_y'] is None else round(x['AAD_y'], 4)} | "
                         f"{'' if d is None else f'[{d[0]:+.2f}, {d[1]:+.2f}]'} | {x['AAD_P_pct_homog']:.2f} | "
                         f"[{x['AAD_P_homog_CI95'][0]:.2f}, {x['AAD_P_homog_CI95'][1]:.2f}] | "
                         f"{'' if x.get('delta_AAD_P_homog_vs_ref_CI95') is None else '[%+.2f, %+.2f]' % tuple(x['delta_AAD_P_homog_vs_ref_CI95'])} |")
        lines.append(f"Three-phase rows excluded from the homogeneous column: {r[sc['models'][0]]['n_three_phase']}")
        lines.append("")
    if "he" in t:
        r = t["he"]
        lines += [f"## Excess enthalpy ({r['n_points']} points)", "", "| model | coverage | MAE J/mol | 95% CI | sign correct |",
                  "|---|---|---|---|---|"]
        for m in sc["models"]:
            x = r[m]
            ci = x["MAE_CI95"]
            lines.append(f"| {m} | {r['coverage'][m]:.2f} | {x['MAE_HE_J']:.0f} | [{ci[0]:.0f}, {ci[1]:.0f}] | {x['sign_correct']:.2f} |")
        lines.append("")
    if "lle" in t:
        r = t["lle"]
        lines += ["## LLE", "", "| model | points | systems | gap found (systems) | MAE x when found |", "|---|---|---|---|---|"]
        for m in sc["models"]:
            x = r[m]
            mx = x["MAE_x_when_found"]
            lines.append(f"| {m} | {x['n_points']} | {x['n_systems']} | {x['gap_found_systems']:.2f} | "
                         f"{'' if mx is None else f'{mx:.3f}'} |")
    return "\n".join(lines)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("models", nargs="+")
    ap.add_argument("--split", default="test")
    ap.add_argument("--ref", default=None)
    ap.add_argument("--tag", default="")
    a = ap.parse_args()
    sc = scorecard(a.models, a.split, a.ref)
    tag = f"_{a.tag}" if a.tag else ""
    (ROOT / "results" / f"scorecard_{a.split}{tag}.json").write_text(json.dumps(sc, indent=1, default=float))
    md = to_markdown(sc)
    (ROOT / "results" / f"scorecard_{a.split}{tag}.md").write_text(md)
    print(md)
