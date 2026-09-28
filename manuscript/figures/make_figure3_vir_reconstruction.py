#!/usr/bin/env python3
"""
Generate publication-grade Figure 3 for Section 3.2:
Reconstruction of the VIR Multigene Antigen Family Architecture:
Sequence Twilight Zone Over-Splitting vs. Structure-Aware Global Panmixia.

Layout:
  Two panels side-by-side:
  - Panel a: Sequence Twilight Zone and Family Over-Splitting (Log-scale identity histogram + comparison card)
  - Panel b: Reconstructed Structural Phylogeny and Global Panmixia (Circular tree + parsimony card)
"""

import os
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import FancyBboxPatch
import pandas as pd
import numpy as np
from PIL import Image
import fitz

mpl.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]
mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["figure.dpi"] = 300
mpl.rcParams["savefig.dpi"] = 300
mpl.rcParams["pdf.fonttype"] = 42

def make_figure():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_pdf = os.path.join(base_dir, "figure3_vir_reconstruction.pdf")
    output_png = os.path.join(base_dir, "figure3_vir_reconstruction.png")
    hist_standalone_pdf = os.path.join(base_dir, "identity_histogram.pdf")

    tree_pdf = os.path.join(base_dir, "q2_part_tree.pdf")
    fs_tsv = "/Users/anton/git/phist/data/genomes/alignments/ortho/fs001_rbh.tsv"
    hk_tsv = "/Users/anton/git/phist/data/genomes/alignments/ortho/housekeeping_rbh.tsv"

    if not os.path.exists(tree_pdf):
        raise FileNotFoundError(f"Missing tree vector file: {tree_pdf}")

    fs = pd.read_csv(fs_tsv, sep="\t")
    hk = pd.read_csv(hk_tsv, sep="\t")
    fs_med = fs["pident"].median()
    hk_med = hk["pident"].median()

    # 1. Update standalone identity_histogram.pdf with log y-scale
    fig_hist, ax_h = plt.subplots(figsize=(8, 5), facecolor="white")
    bins = np.linspace(0, 100, 36)
    ax_h.hist(hk["pident"], bins=bins, density=True, alpha=0.55, label=f"Housekeeping RBH (n={len(hk):,})", color="#2563EB", edgecolor="none")
    ax_h.hist(fs["pident"], bins=bins, density=True, alpha=0.65, label=f"FS_001 RBH (n={len(fs):,})", color="#DC2626", edgecolor="none")
    ax_h.axvline(fs_med, color="#DC2626", linestyle="--", linewidth=1.5, label=f"FS_001 median = {fs_med:.1f}%")
    ax_h.axvline(hk_med, color="#2563EB", linestyle="--", linewidth=1.5, label=f"Housekeeping median = {hk_med:.1f}%")
    ax_h.set_yscale("log")
    ax_h.set_ylim(1e-4, 1.0)
    ax_h.set_xlim(0, 100)
    ax_h.set_xlabel("Pairwise Amino Acid Identity (%)", fontsize=10, fontweight="bold", color="#1E293B")
    ax_h.set_ylabel("Density (log scale)", fontsize=10, fontweight="bold", color="#1E293B")
    ax_h.set_title("PvW1 <-> PvPAM ortholog identity\nFS_001 (subtelomeric VIR) vs housekeeping", fontsize=11, fontweight="bold", color="#0F172A")
    ax_h.grid(True, which="both", axis="y", linestyle=":", alpha=0.4, color="#94A3B8")
    ax_h.grid(True, which="major", axis="x", linestyle=":", alpha=0.3, color="#94A3B8")
    ax_h.legend(frameon=True, facecolor="white", edgecolor="#CBD5E1", fontsize=9, loc="upper left")
    plt.tight_layout()
    fig_hist.savefig(hist_standalone_pdf, bbox_inches="tight")
    plt.close(fig_hist)
    print(f"Updated standalone: {hist_standalone_pdf}")

    # 2. Render Tree from vector PDF
    doc_t = fitz.open(tree_pdf)
    pix_t = doc_t[0].get_pixmap(dpi=300)
    im_tree_raw = Image.frombytes("RGB", [pix_t.width, pix_t.height], pix_t.samples)
    im_tree_crop = im_tree_raw.crop((480, 650, 2030, 1860))

    # 3. Create composite figure
    fig = plt.figure(figsize=(14.8, 7.8), facecolor="white")

    # Headers
    fig.text(0.04, 0.955, "a", fontsize=18, fontweight="bold", color="#1E3A8A")
    fig.text(0.065, 0.955, "Sequence Twilight Zone and Family Over-Splitting", fontsize=13.5, fontweight="bold", color="#0F172A")
    fig.text(0.065, 0.922, "Pairwise amino acid identity between continental assemblies (PvW1 vs. PvPAM)", fontsize=9.2, fontstyle="italic", color="#475569")

    fig.text(0.52, 0.955, "b", fontsize=18, fontweight="bold", color="#1E3A8A")
    fig.text(0.545, 0.955, "Reconstructed Structural Phylogeny and Global Panmixia", fontsize=13.5, fontweight="bold", color="#0F172A")
    fig.text(0.545, 0.922, "Circular ML structural phylogeny (FoldMason + IQ-TREE 3) of dominant superfamily FS_001 (n=338)", fontsize=9.2, fontstyle="italic", color="#475569")

    # Panel a: Histogram (top) - Native vector plot with log y-scale
    ax_a_hist = fig.add_axes([0.07, 0.40, 0.40, 0.49])
    ax_a_hist.hist(hk["pident"], bins=bins, density=True, alpha=0.55, label=f"Housekeeping RBH (n={len(hk):,})", color="#2563EB", edgecolor="none")
    ax_a_hist.hist(fs["pident"], bins=bins, density=True, alpha=0.65, label=f"FS_001 RBH (n={len(fs):,})", color="#DC2626", edgecolor="none")

    ax_a_hist.axvline(fs_med, color="#DC2626", linestyle="--", linewidth=1.5, label=f"FS_001 median = {fs_med:.1f}%")
    ax_a_hist.axvline(hk_med, color="#2563EB", linestyle="--", linewidth=1.5, label=f"Housekeeping median = {hk_med:.1f}%")

    ax_a_hist.set_yscale("log")
    ax_a_hist.set_ylim(1e-4, 1.0)
    ax_a_hist.set_xlim(0, 100)
    ax_a_hist.set_xlabel("Pairwise Amino Acid Identity (%)", fontsize=9.5, fontweight="bold", color="#1E293B")
    ax_a_hist.set_ylabel("Density (log scale)", fontsize=9.5, fontweight="bold", color="#1E293B")

    ax_a_hist.grid(True, which="both", axis="y", linestyle=":", alpha=0.4, color="#94A3B8")
    ax_a_hist.grid(True, which="major", axis="x", linestyle=":", alpha=0.3, color="#94A3B8")
    ax_a_hist.legend(frameon=True, facecolor="white", edgecolor="#CBD5E1", fontsize=8.2, loc="upper left")

    # Panel a: Comparison Card (bottom)
    ax_a_card = fig.add_axes([0.04, 0.035, 0.44, 0.28])
    ax_a_card.axis("off")
    box_a = FancyBboxPatch(
        (0.0, 0.0), 1.0, 1.0, boxstyle="round,pad=0.02,rounding_size=0.04",
        facecolor="#F8FAFC", edgecolor="#CBD5E1", linewidth=1.2
    )
    ax_a_card.add_patch(box_a)

    ax_a_card.text(0.04, 0.88, "Repertoire Classification Comparison:", fontsize=10.0, fontweight="bold", color="#0F172A")
    ax_a_card.text(0.04, 0.70, "\u2022 Earlier References: 10\u201312 subfamilies (VIR-A\u2013L; Carlton et al., 2008; Lopez et al., 2013)", fontsize=8.5, color="#334155")
    ax_a_card.text(0.04, 0.52, "\u2022 Sequence-Only Baseline (MCL): 146 fractured subfamilies; median pairwise identity 32%", fontsize=8.5, color="#334155")
    ax_a_card.text(0.04, 0.34, "\u2022 Structure-Aware Model (Foldseek + ProstT5 3Di): Collapses repertoire into 73 structural classes", fontsize=8.5, fontweight="bold", color="#166534")
    ax_a_card.text(0.04, 0.16, "\u2022 Dominant Superfamily FS_001: Unifies 89 sequence subfamilies (1,197 genes, 46% of repertoire)", fontsize=8.5, fontweight="bold", color="#166534")

    # Panel b: Tree (top)
    ax_b_img = fig.add_axes([0.53, 0.38, 0.42, 0.52])
    ax_b_img.imshow(im_tree_crop)
    ax_b_img.axis("off")

    # Legend below tree
    ax_leg = fig.add_axes([0.52, 0.325, 0.44, 0.04])
    ax_leg.axis("off")
    ax_leg.scatter([0.20], [0.5], color="#EF4444", s=50, clip_on=False)
    ax_leg.text(0.23, 0.5, "PvP01 (Indonesia)", fontsize=9.0, fontweight="bold", va="center", color="#0F172A")

    ax_leg.scatter([0.48], [0.5], color="#22C55E", s=50, clip_on=False)
    ax_leg.text(0.51, 0.5, "PvW1 (Thailand)", fontsize=9.0, fontweight="bold", va="center", color="#0F172A")

    ax_leg.scatter([0.76], [0.5], color="#3B82F6", s=50, clip_on=False)
    ax_leg.text(0.79, 0.5, "PvPAM (Peru)", fontsize=9.0, fontweight="bold", va="center", color="#0F172A")
    ax_leg.set_xlim(0, 1)
    ax_leg.set_ylim(0, 1)

    # Panel b: Parsimony Card (bottom)
    ax_b_card = fig.add_axes([0.52, 0.035, 0.44, 0.28])
    ax_b_card.axis("off")
    box_b = FancyBboxPatch(
        (0.0, 0.0), 1.0, 1.0, boxstyle="round,pad=0.02,rounding_size=0.04",
        facecolor="#F0FDF4", edgecolor="#86EFAC", linewidth=1.2
    )
    ax_b_card.add_patch(box_b)

    ax_b_card.text(0.04, 0.88, "Tip-Label Parsimony Permutation Test (Global Panmixia):", fontsize=10.0, fontweight="bold", color="#166534")
    ax_b_card.text(0.04, 0.70, "\u2022 Cross-Continental Sharing: 97.3% of VIR proteins fall into shared clusters (lineage-unique: 2%)", fontsize=8.5, color="#14532D")
    ax_b_card.text(0.04, 0.52, "\u2022 Balanced Repertoire: 118 PvP01 (34.9%) | 110 PvW1 (32.5%) | 110 PvPAM (32.5%) in FS_001", fontsize=8.5, color="#14532D")
    ax_b_card.text(0.04, 0.34, "\u2022 Parsimony Steps: Observed = 160  |  Null Permutation = 159.2 \u00b1 3.8  |  p = 0.55 (Panmictic)", fontsize=8.5, fontweight="bold", color="#14532D")
    ax_b_card.text(0.04, 0.16, "\u2022 Biological Conclusion: Structural fold is ancient and panmictic; sequence divergence is ectopic", fontsize=8.5, color="#14532D")

    fig.savefig(output_png, bbox_inches="tight", dpi=300)
    fig.savefig(output_pdf, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"Generated: {output_png} and {output_pdf}")

if __name__ == "__main__":
    make_figure()
