#!/usr/bin/env python3
"""Compare SCF1 expression results across the 8 orbit LLM reanalysis attempts.

Panel A: SCF1 log2FC per attempt, both contrasts, direction-normalized so that
         down-in-mutant / down-in-AR0387 is negative. Sources: local DESeq2
         tables where present (sonnet, gpt2) + each run's notebook for the rest.
Panel B: SCF1 (B9J08_03708) per-sample normalized counts vs the naive "wrong-ID"
         trap gene (B9J08_01458), from gpt2's protein_matched_key_gene_DE.tsv —
         shows the real expression collapse and why the naive mapping misses it.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# ---- Panel A data: SCF1 log2FC, normalized to mutant/AR0387 relative to AR0382 WT ----
# completing attempts only; haiku & gpt(1st) produced no result.
attempts = ["opus", "sonnet", "gpt2", "gemini\n2.5-pro", "gemini\n3.5-flash", "deepseek"]
# Fig 1D: tnSWI1 vs AR0382
fig1d = [-5.83, -6.817, -6.817, -6.81, -6.82, -6.82]
# Fig 2D/S5: AR0387 vs AR0382
fig2d = [-6.35, -7.346, -7.346, -7.34, -7.35, -7.35]
# runs that reported the inverse sign (WT as numerator) -> normalized here
flipped = {"gemini\n2.5-pro", "gemini\n3.5-flash"}

paper_ar0387 = -np.log2(29)  # ~-4.86, paper's ~29-fold point estimate for AR0387

fig, (axA, axB) = plt.subplots(1, 2, figsize=(14, 6))

x = np.arange(len(attempts))
w = 0.38
b1 = axA.bar(x - w/2, fig1d, w, label="Fig. 1D: tnSWI1 vs AR0382", color="#3b6ea5")
b2 = axA.bar(x + w/2, fig2d, w, label="Fig. 2D/S5: AR0387 vs AR0382", color="#c0504d")
axA.axhline(paper_ar0387, ls="--", lw=1.3, color="grey")
axA.text(len(attempts)-0.5, paper_ar0387+0.12, "paper AR0387 est. (~29x, log2=-4.86)",
         ha="right", va="bottom", fontsize=8, color="grey")
for bars in (b1, b2):
    for bar in bars:
        h = bar.get_height()
        axA.text(bar.get_x()+bar.get_width()/2, h-0.18, f"{h:.2f}",
                 ha="center", va="top", fontsize=7.5, color="white", fontweight="bold")
axA.set_xticks(x)
axA.set_xticklabels(attempts, fontsize=9)
# mark flipped-sign runs
for i, a in enumerate(attempts):
    if a in flipped:
        axA.text(i, 0.15, "*", ha="center", va="bottom", fontsize=14, color="#7a3b9e")
axA.set_ylabel("SCF1 log2 fold-change (direction-normalized)")
axA.set_title("A. SCF1 log2FC across attempts", fontsize=12, loc="left", fontweight="bold")
axA.axhline(0, color="black", lw=0.8)
axA.legend(fontsize=8, loc="upper right")
axA.set_ylim(-8.2, 1.4)

# ---- Panel B: per-sample normalized counts (gpt2) ----
samples = ["AR0382_A", "AR0382_B", "tnSWI1_A", "tnSWI1_B", "AR0387_A", "AR0387_B"]
scf1   = [46988.8, 44890.2, 383.9, 426.6, 231.4, 244.8]          # B9J08_03708 (correct SCF1)
wrong  = [2024.3, 1929.96, 1951.9, 1908.3, 1422.5, 1333.7]       # B9J08_01458 (naive trap)
xb = np.arange(len(samples))
wb = 0.4
axB.bar(xb - wb/2, scf1, wb, label="SCF1 = B9J08_03708 (correct, protein-matched)", color="#3b6ea5")
axB.bar(xb + wb/2, wrong, wb, label="B9J08_01458 (naive zero-strip; wrong gene)", color="#bdbdbd")
axB.set_yscale("log")
axB.set_xticks(xb)
axB.set_xticklabels(samples, rotation=20, fontsize=8.5)
axB.set_ylabel("DESeq2 normalized counts (log scale)")
axB.set_title("B. SCF1 expression collapse vs the naive-ID trap (gpt2 data)",
              fontsize=12, loc="left", fontweight="bold")
axB.legend(fontsize=8, loc="upper right")
# shade condition groups
axB.axvspan(-0.5, 1.5, color="#3b6ea5", alpha=0.05)
axB.axvspan(1.5, 3.5, color="#c0504d", alpha=0.05)
axB.axvspan(3.5, 5.5, color="#c0504d", alpha=0.05)
axB.text(0.5, axB.get_ylim()[1]*0.6, "adhesive WT", ha="center", fontsize=8, color="#3b6ea5")
axB.text(2.5, axB.get_ylim()[1]*0.6, "tnSWI1 mutant", ha="center", fontsize=8, color="#c0504d")
axB.text(4.5, axB.get_ylim()[1]*0.6, "AR0387", ha="center", fontsize=8, color="#c0504d")

fig.suptitle("SCF1 expression across 8 orbit LLM reanalysis attempts (Santana 2023 C. auris)",
             fontsize=13, fontweight="bold")
fig.text(0.01, 0.005,
         "* gemini & gemini-3.5-flash reported the inverse sign (WT as numerator); normalized here so down-in-mutant/AR0387 is negative.   "
         "sonnet & gpt2 are bit-identical (same IWC rnaseq-pe/de workflow).   haiku & gpt (1st attempt) produced no expression result.",
         fontsize=7, color="#444")
fig.tight_layout(rect=[0, 0.035, 1, 0.96])
fig.savefig("/Users/anton/git/orbit-paper/scf1_expression_across_attempts.png", dpi=200)
fig.savefig("/Users/anton/git/orbit-paper/scf1_expression_across_attempts.pdf")
print("wrote scf1_expression_across_attempts.png/.pdf")
