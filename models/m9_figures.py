"""Figures for the decentralized-AI lever test (reads results/lever_grid.json). Run: python models/m9_figures.py"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "results"); FIG = os.path.join(ROOT, "figures")
INK, INK2, MUTED, SURF = "#0b0b0b", "#52514e", "#898781", "#fcfcfb"
SER = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]
BLUES = LinearSegmentedColormap.from_list("b", ["#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"])
GX = [0.05, 0.10, 0.20, 0.25, 0.50]; GY = [2028, 2030, 2032, 2035, 2040]


def style(ax):
    ax.set_facecolor(SURF)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    for s in ["left", "bottom"]:
        ax.spines[s].set_color(MUTED)
    ax.tick_params(colors=INK2, labelsize=9)


def heat(res):
    base = res["baseline_NO"]["metrics"]["nt_UC"]["mean"]
    fig, axs = plt.subplots(1, 1, figsize=(8.5, 6.2), facecolor=SURF)
    axs = [axs]
    for ax, enc in zip(axs, [0.0]):
        M = np.full((len(GX), 5), np.nan); D = M.copy(); L = M.copy(); U = M.copy()
        for i, X in enumerate(GX):
            for j, Y in enumerate(GY):
                r = res["grid"].get(f"X={X:g}|Y={Y}|enc={enc:g}")
                if r:
                    M[i, j] = r["metrics"]["nt_UC"]["mean"]; d = r["delta_vs_baseline"]["nt_UC"]
                    D[i, j] = d["delta"]; L[i, j], U[i, j] = d["ci95"]
        im = ax.imshow(D, cmap=BLUES.reversed(), vmin=min(np.nanmin(D), -0.01), vmax=0, aspect="auto")
        for i in range(len(GX)):
            for j in range(5):
                if np.isfinite(M[i, j]):
                    dark = D[i, j] < 0.6 * np.nanmin(D)
                    ax.text(j, i, f"{M[i, j]:.3f}\n{D[i, j]:+.3f}\n[{L[i, j]:+.3f}, {U[i, j]:+.3f}]", ha="center", va="center",
                            fontsize=7.5, color="#ffffff" if dark else INK)
        ax.set_xticks(range(5)); ax.set_xticklabels([str(y) for y in GY]); ax.set_yticks(range(len(GX)))
        ax.set_yticklabels([f"{x:.0%}" for x in GX]); ax.set_xlabel("year Y the adoption level is reached (US bloc)", color=INK2)
        ax.set_ylabel("adoption level X (share of economic activity)", color=INK2)
        for s in ax.spines.values():
            s.set_visible(False)
        ax.tick_params(colors=INK2, labelsize=9)
        cb = fig.colorbar(im, ax=ax, fraction=0.04); cb.set_label("change vs baseline", color=INK2); cb.ax.tick_params(colors=INK2, labelsize=8)
    fig.suptitle(f"P(>=99.9% deliberate depopulation, US or China, by 2075)\ncell value, change vs baseline {base:.3f}, paired 95% CI (lever round 3: U1-U4)",
                 color=INK, fontsize=11)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "lever_deadline_heatmap.png"), dpi=150, facecolor=SURF); plt.close(fig)


def channels(res):
    cells = sorted({k.split("|")[0] + "|" + k.split("|")[1] for k in res["decomp"]})
    fig, axs = plt.subplots(1, len(cells), figsize=(15, 14), facecolor=SURF, sharey=True)
    axs = np.atleast_1d(axs)
    for ax, cell in zip(axs, cells):
        rows = [(k.split("|", 2)[2], v["delta_vs_baseline"]["nt_UC"]) for k, v in res["decomp"].items() if k.startswith(cell + "|")]
        names = [r[0] for r in rows][::-1]; d = np.array([r[1]["delta"] for r in rows])[::-1]
        lo = np.array([r[1]["ci95"][0] for r in rows])[::-1]; hi = np.array([r[1]["ci95"][1] for r in rows])[::-1]
        y = np.arange(len(names))
        col = [MUTED if (n.startswith("round-") or n.startswith("lever round-")) else (SER[1] if "minus" in n else (SER[2] if n.startswith("closure channels only") else (SER[3] if n.startswith("S:") else SER[0]))) for n in names]
        ax.barh(y, d, color=col, height=0.6)
        ax.errorbar(d, y, xerr=[d - lo, hi - d], fmt="none", ecolor=INK2, lw=1, capsize=2)
        ax.axvline(0, color=MUTED, lw=1)
        for yi, v in zip(y, d):
            ax.text(v - 0.001 if v < 0 else v + 0.001, yi, f"{v:+.3f}", va="center", ha="right" if v < 0 else "left", fontsize=8, color=INK)
        ax.set_yticks(y); ax.set_yticklabels(names, fontsize=8.5)
        X, Y = cell.split("|"); ax.set_title(f"{float(X[2:]):.0%} adoption by {Y[2:]}", color=INK, fontsize=11)
        ax.set_xlabel("change in P(near-total, US or China) vs baseline", color=INK2); style(ax)
        xmin = min(lo.min(), -0.01); ax.set_xlim(xmin * 1.35, max(hi.max(), 0) + abs(xmin) * 0.3)
    fig.text(0.01, 0.01, "blue: all channels / variants;  grey: earlier specifications (incl. lever round 2, U1-U4 off);  aqua: closure channels alone;  orange: all channels minus one;  yellow: alternative readings (S:). Bars: paired 95% bootstrap CI over epistemic draws.",
             color=INK2, fontsize=8.5)
    fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(FIG, "lever_channels.png"), dpi=150, facecolor=SURF); plt.close(fig)


def crackdown(res):
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.6), facecolor=SURF)
    sel = [("X=0.1|Y=2030|enc=0", ":"), ("X=0.25|Y=2030|enc=0", "-"), ("X=0.5|Y=2035|enc=0", "--")]
    for key, ls in sel:
        r = res["grid"].get(key)
        if not r:
            continue
        c = r["diag"]["curves"]; yrs = c["years"]
        lab = f"{r['cfg']['X']:.0%} by {int(r['cfg']['Y'])}"
        for b, nm in enumerate(["US", "China", "Europe"]):
            axs[0].plot(yrs, c["P_crackdown_cum"][nm], color=SER[b], ls=ls, lw=2, label=f"{nm}, {lab}")
            axs[1].plot(yrs, c["a_mean"][nm], color=SER[b], ls=ls, lw=2, label=f"{nm}, {lab}")
    axs[0].set_title("P(at least one state crackdown by year)", color=INK, fontsize=11); axs[0].set_ylim(0, 1.02)
    axs[1].set_title("mean realised adoption (target path x crackdown suppression)", color=INK, fontsize=11)
    for ax in axs:
        style(ax); ax.set_xlim(2027, 2076); ax.grid(axis="y", color="#e8e7e3", lw=0.8)
    axs[1].legend(fontsize=7.5, frameon=False, ncol=1, loc="center right", labelcolor=INK2)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "lever_crackdown.png"), dpi=150, facecolor=SURF); plt.close(fig)


def closure(res):
    """paired mean shift of the first closure year (capped at 2076) vs baseline, per grid cell (L2/L4/L5 act here)"""
    fig, axs = plt.subplots(1, 3, figsize=(14, 4.4), facecolor=SURF)
    for ax, nm in zip(axs, ["US", "China", "Europe"]):
        M = np.full((len(GX), 5), np.nan)
        for i, X in enumerate(GX):
            for j, Y in enumerate(GY):
                r = res["grid"].get(f"X={X:g}|Y={Y}|enc=0")
                if r and r["diag"].get("closure_delay"):
                    M[i, j] = r["diag"]["closure_delay"][nm]["mean_shift_years_capped2076"]
        im = ax.imshow(M, cmap=BLUES, vmin=0, vmax=max(np.nanmax(M), 0.1), aspect="auto")
        for i in range(len(GX)):
            for j in range(5):
                if np.isfinite(M[i, j]):
                    ax.text(j, i, f"{M[i, j]:+.2f}", ha="center", va="center", fontsize=8.5,
                            color="#ffffff" if M[i, j] > 0.6 * np.nanmax(M) else INK)
        ax.set_xticks(range(5)); ax.set_xticklabels([str(y) for y in GY]); ax.set_yticks(range(len(GX)))
        ax.set_yticklabels([f"{x:.0%}" for x in GX]); ax.set_title(f"{nm}: closure delay (years)", color=INK, fontsize=11)
        ax.set_xlabel("year Y", color=INK2)
        for sp in ax.spines.values():
            sp.set_visible(False)
        ax.tick_params(colors=INK2, labelsize=9)
    axs[0].set_ylabel("adoption level X", color=INK2)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "lever_closure.png"), dpi=150, facecolor=SURF); plt.close(fig)


if __name__ == "__main__":
    p = os.path.join(RES, "lever_grid.json")
    if not os.path.exists(p):
        p = os.path.join(RES, "lever_grid_partial.json")
    res = json.load(open(p))
    heat(res); channels(res); crackdown(res); closure(res)
    print("figures written")
