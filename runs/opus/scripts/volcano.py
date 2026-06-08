#!/usr/bin/env python
"""Draw labeled volcano plot from a joined DESeq2+ID-map TSV.

Columns expected (1-based):
  1=GeneID(v3), 2=baseMean, 3=log2FC, 4=lfcSE, 5=stat, 6=pvalue, 7=padj,
  8=v3_id, 9=v2_id, 10=gene_name, 11=pident, 12=coverage_pct
"""
import sys, math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from adjustText import adjust_text

LFC_THRESH = 1.0
PADJ_THRESH = 0.05

def load(path):
    rows = []
    with open(path) as f:
        for line in f:
            c = line.rstrip("\n").split("\t")
            if len(c) < 12:
                continue
            try:
                lfc = float(c[2]); padj = float(c[6])
            except Exception:
                continue
            if not math.isfinite(padj) or padj <= 0:
                continue
            gn = c[9].strip() if c[9].strip() not in ("NA",) else ""
            rows.append((c[0], lfc, padj, gn))
    return rows

def draw(rows, title, outpath, ymax=None, xlim=None):
    fig, ax = plt.subplots(figsize=(8, 7.2), dpi=120)
    lfc = np.array([r[1] for r in rows])
    padj = np.array([r[2] for r in rows])
    nlp = -np.log10(padj)
    up = (lfc > LFC_THRESH) & (padj < PADJ_THRESH)
    down = (lfc < -LFC_THRESH) & (padj < PADJ_THRESH)
    ns = ~(up | down)
    ax.scatter(lfc[ns], nlp[ns], s=10, c="#bdbdbd", alpha=0.6, edgecolors="none", label=f"Not Sig (n={ns.sum()})")
    ax.scatter(lfc[down], nlp[down], s=14, c="#3b7dd8", alpha=0.85, edgecolors="none", label=f"Down (n={down.sum()})")
    ax.scatter(lfc[up], nlp[up], s=14, c="#d8453b", alpha=0.85, edgecolors="none", label=f"Up (n={up.sum()})")
    ax.axhline(-math.log10(PADJ_THRESH), ls="--", c="grey", lw=0.7)
    ax.axvline(LFC_THRESH, ls="--", c="grey", lw=0.7)
    ax.axvline(-LFC_THRESH, ls="--", c="grey", lw=0.7)
    if ymax is not None:
        ax.set_ylim(0, ymax)
    if xlim is not None:
        ax.set_xlim(*xlim)

    # Label paper genes
    texts = []
    paper = {"SCF1", "IFF4109", "SWI1", "BCY1", "IFF4892", "ALS4112"}
    for gid, l, p, gn in rows:
        if gn in paper:
            x, y = l, -math.log10(p)
            ax.scatter([x], [y], s=80, facecolors="none", edgecolors="black", lw=1.4, zorder=5)
            txt = ax.text(x, y, gn, fontsize=10, fontweight="bold", zorder=6,
                          bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="black", lw=0.8, alpha=0.92))
            texts.append(txt)
    adjust_text(texts, ax=ax,
                arrowprops=dict(arrowstyle="-", color="black", lw=0.6),
                expand=(1.2, 1.4), force_text=(0.4, 0.6), max_move=30)

    ax.set_xlabel("log2(FoldChange)", fontsize=11)
    ax.set_ylabel("-log10(adjusted p-value)", fontsize=11)
    ax.set_title(title, fontsize=12)
    ax.legend(loc="upper right", fontsize=9, framealpha=0.9)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.savefig(outpath.replace(".png", ".pdf"))
    print(f"wrote {outpath} (+ .pdf)")

if __name__ == "__main__":
    rows1 = load("/tmp/joined_tnSWI1.tsv")
    draw(rows1, "AR0382 tnSWI1 vs WT — Fig. 1D analog",
         "/Users/anton/.loom/analyses/orbit_llm_tests/opus/figures/volcano_Fig1D_tnSWI1_vs_WT.png",
         ymax=25, xlim=(-11, 8))
    rows2 = load("/tmp/joined_AR0387.tsv")
    draw(rows2, "AR0387 vs AR0382 — Fig. 2D/S5 analog",
         "/Users/anton/.loom/analyses/orbit_llm_tests/opus/figures/volcano_Fig2D_AR0387_vs_AR0382.png",
         ymax=25, xlim=(-7, 13))
