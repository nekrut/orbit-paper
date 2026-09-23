#!/usr/bin/env python3
"""
Generate publication-grade Figure 3:
Subtelomeric Compartmentalization and Chromosomal Organization of the VIR Superfamily.

Panel a: Chromosome ideograms across all 14 chromosomes in PvP01, PvW1, and PvPAM colored by Foldseek structural class.
Panel b: Relative chromosomal position density profiles (FS_001 vs other VIRs).
"""

import matplotlib.pyplot as plt
from PIL import Image
import matplotlib as mpl

mpl.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]
mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["figure.dpi"] = 300
mpl.rcParams["savefig.dpi"] = 300
mpl.rcParams["pdf.fonttype"] = 42

def build_figure3():
    fig = plt.figure(figsize=(12.0, 11.5))
    
    # Panel a: Ideograms (top, y: 0.32 to 0.96)
    ax_a = fig.add_axes([0.04, 0.30, 0.92, 0.65])
    im_a = Image.open("/Users/anton/git/orbit-paper/manuscript/figures/fig1_ideogram.png")
    ax_a.imshow(im_a)
    ax_a.axis("off")
    ax_a.text(0.01, 1.03, "a", transform=ax_a.transAxes, fontsize=15, fontweight="bold", color="#1E3A8A", va="top")
    ax_a.text(0.045, 1.03, "Chromosomal Landscapes and Structural Classification Across Continents",
              transform=ax_a.transAxes, fontsize=11, fontweight="bold", color="#0F172A", va="top")
    ax_a.text(0.045, 1.00, "14 chromosomes across PvP01 (Indonesia), PvW1 (Thailand), and PvPAM (Peru) colored by Foldseek structural class",
              transform=ax_a.transAxes, fontsize=8.2, fontstyle="italic", color="#475569", va="top")
    
    # Panel b: Density profile (bottom, y: 0.04 to 0.26)
    ax_b = fig.add_axes([0.04, 0.03, 0.92, 0.24])
    im_b = Image.open("/Users/anton/git/orbit-paper/manuscript/figures/fig2_fs001_density.png")
    ax_b.imshow(im_b)
    ax_b.axis("off")
    ax_b.text(0.01, 1.08, "b", transform=ax_b.transAxes, fontsize=15, fontweight="bold", color="#1E3A8A", va="top")
    ax_b.text(0.045, 1.08, "Relative Chromosomal Distribution and Subtelomeric Enrichment",
              transform=ax_b.transAxes, fontsize=11, fontweight="bold", color="#0F172A", va="top")
    ax_b.text(0.045, 1.01, "Density profiles show sharp accumulation of FS_001 and other VIRs within terminal 10% of chromosomal ends (64.5% of loci)",
              transform=ax_b.transAxes, fontsize=8.2, fontstyle="italic", color="#475569", va="top")
    
    plt.savefig("/Users/anton/git/orbit-paper/manuscript/figures/figure3_genomic_organization.png", dpi=300, bbox_inches="tight")
    plt.savefig("/Users/anton/git/orbit-paper/manuscript/figures/figure3_genomic_organization.pdf", bbox_inches="tight")
    print("Figure 3 successfully generated!")

if __name__ == "__main__":
    build_figure3()
