#!/usr/bin/env python3
"""Figure for the Orbit LLM reanalysis: two panels telling the story.

Panel A — LLM cost spread: ~47x range across the six completing runs for the
          SAME scientific answer (lollipop, log x). Two runs aborted (no cost).
Panel B — Result convergence: SCF1 log2FC for both contrasts, direction-
          normalized, every completing run clustering tightly.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

# ---------------------------------------------------------------- shared style
plt.rcParams.update({
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.titleweight": "bold",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#444444",
    "axes.labelcolor": "#222222",
    "text.color": "#222222",
    "xtick.color": "#444444",
    "ytick.color": "#444444",
})

# provider palette (consistent across panels)
PROV = {
    "Anthropic": "#C8643C",
    "OpenAI":    "#10A37F",
    "Google":    "#4285F4",
    "DeepSeek":  "#7C4DD1",
}
MODEL_PROV = {
    "opus": "Anthropic", "sonnet": "Anthropic",
    "gpt-5.5": "OpenAI",
    "gemini 2.5-pro": "Google", "gemini 3.5-flash": "Google",
    "deepseek": "DeepSeek",
}

# --------------------------------------------------------------------- data
# cost (USD, LLM only); only completing runs with a reported figure
cost = {
    "deepseek": 2.82,
    "gemini 2.5-pro": 16.22,
    "gemini 3.5-flash": 17.31,
    "gpt-5.5": 23.46,
    "sonnet": 24.87,
    "opus": 131.83,
}
ratio = max(cost.values()) / min(cost.values())   # ~47x

# SCF1 log2FC, direction-normalized (down-in-mutant / down-in-AR0387 negative)
models = ["opus", "sonnet", "gpt-5.5", "gemini 2.5-pro", "gemini 3.5-flash", "deepseek"]
fig1d = {"opus": -5.83, "sonnet": -6.817, "gpt-5.5": -6.817,
         "gemini 2.5-pro": -6.81, "gemini 3.5-flash": -6.82, "deepseek": -6.82}
fig2d = {"opus": -6.35, "sonnet": -7.346, "gpt-5.5": -7.346,
         "gemini 2.5-pro": -7.34, "gemini 3.5-flash": -7.35, "deepseek": -7.35}
paper_ar0387 = -np.log2(29)   # ~-4.86

# ------------------------------------------------------------------ layout
fig = plt.figure(figsize=(12.5, 5.4))
gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.15], wspace=0.22,
                      left=0.085, right=0.97, top=0.80, bottom=0.16)
axB = fig.add_subplot(gs[0, 0])      # convergence (left, Panel A)
axA = fig.add_subplot(gs[0, 1])      # cost (right, Panel B)

# ---------------------------------------------------- Panel A: cost lollipop
order = sorted(cost, key=cost.get)               # cheap -> expensive
y = np.arange(len(order))
xmin = 2.0
for yi, m in zip(y, order):
    c = PROV[MODEL_PROV[m]]
    axA.hlines(yi, xmin, cost[m], color=c, lw=2.4, alpha=0.55, zorder=1)
    axA.plot(cost[m], yi, "o", ms=11, color=c, zorder=3)
    axA.text(cost[m] * 1.12, yi, f"${cost[m]:,.2f}", va="center", ha="left",
             fontsize=9.5, fontweight="bold", color="#222")
axA.set_xscale("log")
axA.set_xlim(xmin, 320)
axA.set_ylim(-0.7, len(order) - 0.3)
axA.set_yticks(y)
axA.set_yticklabels(order, fontsize=10)
axA.set_xlabel("LLM API cost (USD, log scale) — Galaxy compute was free", fontsize=10)
axA.set_title("B   Same answer, ~47× spread in LLM cost", loc="left")
axA.set_xticks([2, 5, 10, 20, 50, 100, 200])
axA.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(
    lambda v, _: f"${v:g}"))
axA.tick_params(axis="x", labelsize=8.5)
axA.grid(axis="x", color="#dddddd", lw=0.7, zorder=0)
# 47x bracket between cheapest and dearest
yb = len(order) - 0.5
axA.annotate("", xy=(cost["opus"], yb), xytext=(cost["deepseek"], yb),
             arrowprops=dict(arrowstyle="<->", color="#888", lw=1.4))
axA.text(np.sqrt(cost["opus"] * cost["deepseek"]), yb + 0.12,
         f"{ratio:.0f}×", ha="center", va="bottom",
         fontsize=11, fontweight="bold", color="#555")
axA.text(xmin * 1.05, -0.55,
         "two runs (haiku, gpt 1st attempt) aborted at data prep — no result, no cost reported",
         fontsize=8, style="italic", color="#777", ha="left", va="center")

# ------------------------------------------------ Panel B: log2FC convergence
rng = np.random.default_rng(0)
rows = [("Fig. 2D / S5\nAR0387 vs AR0382", fig2d, 1.0),
        ("Fig. 1D\ntnSWI1 vs AR0382", fig1d, 0.0)]
for label, dvals, yc in rows:
    for m in models:
        c = PROV[MODEL_PROV[m]]
        jit = (hash(m) % 7 - 3) / 22.0
        axB.plot(dvals[m], yc + jit, "o", ms=9, color=c,
                 markeredgecolor="white", markeredgewidth=0.8, zorder=3)
axB.set_yticks([0.0, 1.0])
axB.set_yticklabels([r[0] for r in [rows[1], rows[0]]], fontsize=9)
# (set ticks explicitly in display order)
axB.set_yticks([1.0, 0.0])
axB.set_yticklabels([rows[0][0], rows[1][0]], fontsize=9)
axB.set_ylim(-0.6, 1.5)
axB.set_xlim(-8.4, -3.7)
axB.axvline(paper_ar0387, ls="--", lw=1.3, color="#999")
axB.text(-4.72, 0.5, "paper AR0387\nestimate (~29×)",
         ha="left", va="center", fontsize=7.8, color="#888")
axB.annotate("opus: raw MLE\n(unshrunken)", xy=(-5.83, 0.0), xytext=(-5.15, -0.45),
             fontsize=7.4, color="#888", ha="center",
             arrowprops=dict(arrowstyle="-", color="#bbb", lw=0.9))
axB.set_xlabel("SCF1 log₂ fold-change (direction-normalized)", fontsize=9.5)
axB.set_title("A   Every completing run reproduces the SCF1 collapse", loc="left",
              fontsize=11, pad=10)
axB.grid(axis="x", color="#eeeeee", lw=0.7, zorder=0)

# --------------------------------------------------------- legend + titles
prov_handles = [Line2D([0], [0], marker="o", ls="", ms=9, color=PROV[p],
                       markeredgecolor="white", label=p) for p in PROV]
fig.legend(handles=prov_handles, loc="upper right", ncol=4, frameon=False,
           fontsize=9, bbox_to_anchor=(0.97, 0.975), columnspacing=1.3,
           handletextpad=0.3)
fig.suptitle("Eight LLMs reanalyze one C. auris RNA-seq dataset on Galaxy",
             fontsize=14.5, fontweight="bold", x=0.085, ha="left", y=0.965)
fig.text(0.085, 0.90,
         "Santana et al. 2023 (Science) — SCF1 adhesin; reproduced via Orbit on usegalaxy.org",
         fontsize=9.5, color="#666", ha="left")

for ext in ("png", "pdf"):
    fig.savefig(f"/Users/anton/git/orbit-paper/scf1_expression_across_attempts.{ext}",
                dpi=200, bbox_inches="tight")
print(f"wrote figure; cost ratio = {ratio:.1f}x")
