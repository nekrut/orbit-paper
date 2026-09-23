#!/usr/bin/env python3
"""Standalone render of Panel B (LLM cost spread) for social media.

Extracted from plot_scf1_across_attempts.py — the cost lollipop only, as a
self-contained figure with title, context line, and provider legend.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker
from matplotlib.lines import Line2D
import numpy as np

plt.rcParams.update({
    "font.size": 10,
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#444444",
    "axes.labelcolor": "#222222",
    "text.color": "#222222",
    "xtick.color": "#444444",
    "ytick.color": "#444444",
})

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
cost = {
    "deepseek": 2.82,
    "gemini 2.5-pro": 16.22,
    "gemini 3.5-flash": 17.31,
    "gpt-5.5": 23.46,
    "sonnet": 24.87,
    "opus": 131.83,
}
ratio = max(cost.values()) / min(cost.values())

fig = plt.figure(figsize=(7.6, 5.2))
ax = fig.add_axes([0.22, 0.15, 0.74, 0.58])

order = sorted(cost, key=cost.get)
y = np.arange(len(order))
xmin = 2.0
for yi, m in zip(y, order):
    c = PROV[MODEL_PROV[m]]
    ax.hlines(yi, xmin, cost[m], color=c, lw=2.6, alpha=0.55, zorder=1)
    ax.plot(cost[m], yi, "o", ms=12, color=c, zorder=3)
    ax.text(cost[m] * 1.12, yi, f"${cost[m]:,.2f}", va="center", ha="left",
            fontsize=10, fontweight="bold", color="#222")
ax.set_xscale("log")
ax.set_xlim(xmin, 340)
ax.set_ylim(-0.7, len(order) - 0.3)
ax.set_yticks(y)
ax.set_yticklabels(order, fontsize=10.5)
ax.set_xlabel("LLM API cost (USD, log scale) — Galaxy compute was free", fontsize=10)
ax.set_xticks([2, 5, 10, 20, 50, 100, 200])
ax.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(
    lambda v, _: f"${v:g}"))
ax.tick_params(axis="x", labelsize=9)
ax.grid(axis="x", color="#dddddd", lw=0.7, zorder=0)
yb = len(order) - 0.5
ax.annotate("", xy=(cost["opus"], yb), xytext=(cost["deepseek"], yb),
            arrowprops=dict(arrowstyle="<->", color="#888", lw=1.5))
ax.text(np.sqrt(cost["opus"] * cost["deepseek"]), yb + 0.12,
        f"{ratio:.0f}×", ha="center", va="bottom",
        fontsize=12, fontweight="bold", color="#555")
ax.text(xmin * 1.05, -0.55,
        "two runs (haiku, gpt 1st attempt) aborted at data prep — no result, no cost reported",
        fontsize=8, style="italic", color="#777", ha="left", va="center")

prov_handles = [Line2D([0], [0], marker="o", ls="", ms=9, color=PROV[p],
                       markeredgecolor="white", label=p) for p in PROV]
fig.legend(handles=prov_handles, loc="upper left", ncol=4, frameon=False,
           fontsize=8.5, bbox_to_anchor=(0.22, 0.83), columnspacing=1.1,
           handletextpad=0.3)
fig.suptitle("Same answer, ~47× spread in LLM cost", fontsize=14.5,
             fontweight="bold", x=0.04, ha="left", y=0.96)
fig.text(0.04, 0.90,
         "Eight LLMs reanalyze one C. auris RNA-seq dataset via Orbit on usegalaxy.org",
         fontsize=9.5, color="#666", ha="left")

out = "/Users/anton/git/galaxy-social/posts/images/2026-06-09-llm-cost-spread.png"
fig.savefig(out, dpi=200)
print("wrote", out)
