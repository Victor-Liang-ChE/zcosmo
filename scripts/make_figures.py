"""Manuscript figures (static PNG, light theme)."""
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from zcosmo.error_map import family

C = {"cosmosac2010": "#2a78d6", "Z0x": "#eb6834", "unifac_do": "#1baf7a", "hanna": "#4a3aa7",
     "Z0": "#e87ba4", "Z0e": "#eda100", "Z0s": "#008300", "cosmosac_dsp": "#52514e"}
NAME = {"cosmosac2010": "COSMO-SAC 2010", "cosmosac_dsp": "COSMO-SAC-dsp", "unifac_do": "Mod. UNIFAC",
        "Z0": "Z0", "Z0e": "Z0e", "Z0s": "Z0s", "Z0x": "Z0x", "hanna": "HANNA"}
INK, INK2, GRID, BG = "#0b0b0b", "#52514e", "#e6e5e0", "#fcfcfb"
plt.rcParams.update({"font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.facecolor": BG, "figure.facecolor": BG, "axes.grid": True,
                     "grid.color": GRID, "grid.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False})
P = "results/predictions/"
OUT = "manuscript/figures/"

# Fig 1: IDAC parity on held-out molecules
models = ["cosmosac2010", "unifac_do", "Z0x", "hanna"]
fr = {m: pd.read_csv(f"{P}{m}__idac__all.csv") for m in models}
ok = np.ones(len(fr[models[0]]), bool)
for f in fr.values():
    ok &= f.pred_ln_gamma_inf.notna().to_numpy()
fig, axs = plt.subplots(1, 4, figsize=(11, 3), sharex=True, sharey=True)
for ax, m in zip(axs, models):
    d = fr[m][ok & (fr[m].split != "train").to_numpy()]
    ax.plot([-3, 14], [-3, 14], color=INK2, lw=1)
    ax.scatter(d.ln_gamma_inf, d.pred_ln_gamma_inf, s=8, color=C[m], alpha=0.6, lw=0)
    mae = (d.pred_ln_gamma_inf - d.ln_gamma_inf).abs().mean()
    ax.set_title(f"{NAME[m]}  (MAE {mae:.2f})", color=INK, fontsize=9)
    ax.set_xlabel("experimental ln γ∞")
axs[0].set_ylabel("predicted ln γ∞")
axs[0].set_xlim(-3, 14); axs[0].set_ylim(-3, 14)
fig.tight_layout(); fig.savefig(OUT + "fig1_idac_parity_test.png", dpi=200)

# Fig 2: hydrogen-bond constants
hb = pd.read_csv("results/qc/hb_constants_per_dimer.csv")
fit = {"OH-OH": 4013.78, "OH-OT": 3016.43, "OT-OT": 932.31}
fig, ax = plt.subplots(figsize=(4.6, 3))
for i, cls in enumerate(["OH-OH", "OH-OT", "OT-OT"]):
    v = hb[hb.cls == cls].c_hb
    ax.scatter(np.full(len(v), i) + np.linspace(-0.12, 0.12, len(v)), v, s=22, color=C["Z0x"], zorder=3,
               label="DFT dimers (this work)" if i == 0 else None)
    ax.hlines(v.mean(), i - 0.25, i + 0.25, color=C["Z0x"], lw=2)
    ax.hlines(fit[cls], i - 0.25, i + 0.25, color=C["cosmosac2010"], lw=2,
              label="fitted COSMO-SAC 2010" if i == 0 else None)
ax.set_xticks([0, 1, 2]); ax.set_xticklabels(["OH–OH", "OH–OT", "OT–OT"])
ax.set_ylabel("c_hb (kcal Å⁴ mol⁻¹ e⁻²)"); ax.set_ylim(0, 9000)
ax.legend(frameon=False, fontsize=8, loc="lower left")
fig.tight_layout(); fig.savefig(OUT + "fig2_hbond_constants.png", dpi=200)

# Fig 3: accuracy trade-off (test split scorecard)
sc = json.load(open("results/scorecard_test_main7.json"))
fig, ax = plt.subplots(figsize=(4.6, 3.4))
for m in sc["models"]:
    x = sc["tables"]["idac"][m]["MAE_ln_gamma_inf"]; y = sc["tables"]["vle"][m]["AAD_P_pct"]
    ax.scatter(x, y, s=60, color=C[m], zorder=3, edgecolor=BG, lw=2)
    ax.annotate(NAME[m], (x, y), xytext=(6, 4), textcoords="offset points", fontsize=8, color=INK)
ax.set_xlabel("IDAC MAE in ln γ∞ (held-out molecules)")
ax.set_ylabel("VLE bubble-pressure AAD (%)")
fig.tight_layout(); fig.savefig(OUT + "fig3_tradeoff.png", dpi=200)

# Fig 4: LLE split detection
neg = pd.read_csv(P + "lle_negatives.csv"); neg = neg[neg.split != "train"]
fig, ax = plt.subplots(figsize=(4.6, 3.4))
for m in ["unifac_do", "cosmosac2010", "cosmosac_dsp", "Z0", "Z0s", "Z0x", "hanna"]:
    try:
        d = pd.read_csv(f"{P}{m}__lle__all.csv")
    except FileNotFoundError:
        continue
    d = d[d.split != "train"]
    s = np.where(d.c1 < d.c2, d.c1 + "|" + d.c2, d.c2 + "|" + d.c1)
    rec = (d.groupby(s).pred_split.mean() > 0.5).mean()
    fp = neg[f"fp_{m}"].mean()
    ax.scatter(fp, rec, s=60, color=C[m], zorder=3, edgecolor=BG, lw=2)
    off = {"Z0": (-8, 6, "right"), "Z0x": (8, -12, "left"), "cosmosac2010": (4, -14, "left"),
           "cosmosac_dsp": (6, 6, "left")}.get(m, (6, 4, "left"))
    ax.annotate(NAME[m], (fp, rec), xytext=off[:2], textcoords="offset points", fontsize=8, color=INK, ha=off[2])
ax.set_xlabel("false splits on miscible systems"); ax.set_ylabel("real splits found")
ax.set_xlim(-0.01, 0.1); ax.set_ylim(0.3, 1.0)
fig.tight_layout(); fig.savefig(OUT + "fig4_lle_detection.png", dpi=200)

# Fig 5: error map Z0x minus COSMO-SAC 2010 (all data, IDAC)
comp = pd.read_csv("data/benchmark/compounds.csv"); fam = {k: family(s) for k, s in zip(comp.inchikey, comp.smiles)}
a = pd.read_csv(P + "Z0x__idac__all.csv"); b = pd.read_csv(P + "cosmosac2010__idac__all.csv")
ok = a.pred_ln_gamma_inf.notna() & b.pred_ln_gamma_inf.notna()
d = a[ok].copy(); d["dz"] = (a.pred_ln_gamma_inf - a.ln_gamma_inf).abs()[ok] - (b.pred_ln_gamma_inf - b.ln_gamma_inf).abs()[ok]
d["fs"] = d.solute.map(fam); d["fv"] = d.solvent.map(fam)
g = d.groupby(["fs", "fv"]).agg(n=("dz", "size"), dz=("dz", "mean")).reset_index()
g = g[g.n >= 10]
rows = g.groupby("fs").n.sum().sort_values(ascending=False).index[:9]
cols = g.groupby("fv").n.sum().sort_values(ascending=False).index[:8]
M = g.pivot(index="fs", columns="fv", values="dz").reindex(index=rows, columns=cols)
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
cmap = LinearSegmentedColormap.from_list("div", ["#2a78d6", "#f0efec", "#eb6834"])
fig, ax = plt.subplots(figsize=(6.4, 4.4))
ax.grid(False)
im = ax.imshow(M.to_numpy(float), cmap=cmap, norm=TwoSlopeNorm(0, -1.5, 1.5))
ax.set_xticks(range(len(cols))); ax.set_xticklabels(cols, rotation=40, ha="right")
ax.set_yticks(range(len(rows))); ax.set_yticklabels(rows)
ax.set_xlabel("solvent family"); ax.set_ylabel("solute family")
cb = fig.colorbar(im, ax=ax, shrink=0.8); cb.set_label("Z0x error minus COSMO-SAC error (ln γ∞)")
fig.tight_layout(); fig.savefig(OUT + "fig5_error_map.png", dpi=200)
print("figures written")
