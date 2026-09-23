#!/usr/bin/env python3
"""
Generate publication-grade Figure 5:
Panmictic Structural Phylogenomics of the Dominant VIR Fold Across Continents.

Panel a: Circular maximum-likelihood structural phylogenetic tree (IQ-TREE 3) of 338 FS_001 representatives.
Panel b: Quantitative tip-label parsimony testing results (AA, 3Di, and partitioned models vs 1,000 permutations).
"""

import matplotlib.pyplot as plt
from PIL import Image
import matplotlib as mpl

mpl.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]
mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["figure.dpi"] = 300
mpl.rcParams["savefig.dpi"] = 300
mpl.rcParams["pdf.fonttype"] = 42

def build_figure5():
    fig = plt.figure(figsize=(13.0, 7.5))
    
    # Left: Panel a (Tree, x: 0.04 to 0.58, y: 0.05 to 0.92)
    ax_a = fig.add_axes([0.04, 0.04, 0.54, 0.88])
    im_a = Image.open("/Users/anton/git/orbit-paper/manuscript/figures/fig5_q2_tree.png")
    ax_a.imshow(im_a)
    ax_a.axis("off")
    ax_a.text(0.01, 1.05, "a", transform=ax_a.transAxes, fontsize=15, fontweight="bold", color="#1E3A8A", va="top")
    ax_a.text(0.06, 1.05, "Maximum-Likelihood Structural Phylogeny (FoldMason + IQ-TREE)",
              transform=ax_a.transAxes, fontsize=11, fontweight="bold", color="#0F172A", va="top")
    ax_a.text(0.06, 1.01, "338 representative sequences from dominant structural class FS_001; tips colored by genome",
              transform=ax_a.transAxes, fontsize=8.2, fontstyle="italic", color="#475569", va="top")
    
    # Right: Panel b (Quantitative statistics and biological interpretation, x: 0.61 to 0.96)
    ax_b = fig.add_axes([0.61, 0.04, 0.35, 0.88])
    ax_b.axis("off")
    
    b_box = mpl.patches.FancyBboxPatch((0.02, 0.02), 0.96, 0.94, boxstyle="round,pad=0.02,rounding_size=0.03",
                                       facecolor="#F8FAFC", edgecolor="#CBD5E1", linewidth=1.2)
    ax_b.add_patch(b_box)
    
    ax_b.text(0.02, 1.05, "b", fontsize=15, fontweight="bold", color="#1E3A8A", va="top")
    ax_b.text(0.09, 1.05, "Quantitative Parsimony & Panmixia Analysis",
              fontsize=11, fontweight="bold", color="#0F172A", va="top")
    ax_b.text(0.09, 1.01, "Statistical test of geographic lineage segregation",
              fontsize=8.2, fontstyle="italic", color="#475569", va="top")
    
    # Summary of parsimony tests
    ax_b.text(0.07, 0.90, "Continental Tip Distribution:", fontsize=9.5, fontweight="bold", color="#1E3A8A")
    ax_b.text(0.07, 0.81,
              "• PvP01 (Indonesia): 118 tips (34.9%)\n"
              "• PvW1 (Thailand): 110 tips (32.5%)\n"
              "• PvPAM (Peru): 110 tips (32.5%)\n"
              "Total tips: n = 338 (balanced representation)",
              fontsize=8.2, color="#334155")
    
    ax_b.text(0.07, 0.69, "Phylogenetic Permutation Tests (1,000 Shuffles):", fontsize=9.5, fontweight="bold", color="#1E3A8A")
    
    # Table of scores
    table_y = 0.50
    ax_b.text(0.07, table_y + 0.12, "Model Partition", fontsize=8.0, fontweight="bold", color="#0F172A")
    ax_b.text(0.48, table_y + 0.12, "Obs. Score", fontsize=8.0, fontweight="bold", color="#0F172A")
    ax_b.text(0.72, table_y + 0.12, "Null p-value", fontsize=8.0, fontweight="bold", color="#0F172A")
    ax_b.plot([0.07, 0.92], [table_y + 0.10, table_y + 0.10], color="#94A3B8", lw=0.8)
    
    rows = [
        ("Partitioned (AA + 3Di)", "160", "p = 0.55 (NS)"),
        ("Amino Acid Alone (VT+F+R6)", "162", "p = 0.69 (NS)"),
        ("3Di Alone (Garg-Hochberg)", "156", "p = 0.26 (NS)")
    ]
    for i, (m, s, p) in enumerate(rows):
        ry = table_y + 0.05 - i * 0.055
        ax_b.text(0.07, ry, m, fontsize=7.8, color="#334155")
        ax_b.text(0.52, ry, s, fontsize=7.8, fontweight="bold", color="#0F172A")
        ax_b.text(0.72, ry, p, fontsize=7.8, fontweight="bold", color="#059669")
        
    ax_b.plot([0.07, 0.92], [table_y - 0.10, table_y - 0.10], color="#94A3B8", lw=0.8)
    
    ax_b.text(0.07, 0.32, "Decisive Biological Conclusions:", fontsize=9.5, fontweight="bold", color="#0F172A")
    ax_b.text(0.07, 0.16,
              "1. Evolutionary Interleaving: Isolates from Asia\n"
              "   and South America are completely interspersed\n"
              "   throughout the structural tree.\n\n"
              "2. Ancient Pre-Radiation Origin: VIR diversity\n"
              "   diversified prior to modern continental spread.\n\n"
              "3. Global Panmictic Repertoire: Subtelomeric\n"
              "   ectopic recombination and gene conversion\n"
              "   maintain cross-continental antigenic breadth.",
              fontsize=8.0, color="#334155")
    
    plt.savefig("/Users/anton/git/orbit-paper/manuscript/figures/figure5_structural_phylogeny.png", dpi=300, bbox_inches="tight")
    plt.savefig("/Users/anton/git/orbit-paper/manuscript/figures/figure5_structural_phylogeny.pdf", bbox_inches="tight")
    print("Figure 5 successfully generated!")

if __name__ == "__main__":
    build_figure5()
