#!/usr/bin/env python3
"""
Generate publication-grade Figure 4:
The Sequence Twilight Zone and Breakdown of Syntenic Orthology in Multigene Antigen Families.

Panel a: Pairwise amino acid sequence identity histogram comparing 5,120 housekeeping genes vs 194 FS_001 pairs.
Panel b: Whole-genome ribbon synteny map between PvW1 (Thailand) and PvPAM (Peru).
"""

import matplotlib.pyplot as plt
from PIL import Image
import matplotlib as mpl

mpl.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]
mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["figure.dpi"] = 300
mpl.rcParams["savefig.dpi"] = 300
mpl.rcParams["pdf.fonttype"] = 42

def build_figure4():
    fig = plt.figure(figsize=(13.0, 10.0))
    
    # Panel a: Identity histogram (left/top, x: 0.04 to 0.44, y: 0.52 to 0.94)
    # Wait, let's look at aspect ratios:
    # fig3_identity_hist is 1579 x 982 (aspect ~1.6)
    # fig4_ribbon_synteny is 3550 x 1380 (aspect ~2.57)
    # We can place Panel a at top or left, and Panel b across bottom!
    
    # Top row: Panel a (Identity histogram) with an explanatory text box on the right
    ax_a = fig.add_axes([0.04, 0.52, 0.46, 0.41])
    im_a = Image.open("/Users/anton/git/orbit-paper/manuscript/figures/fig3_identity_hist.png")
    ax_a.imshow(im_a)
    ax_a.axis("off")
    ax_a.text(0.01, 1.05, "a", transform=ax_a.transAxes, fontsize=15, fontweight="bold", color="#1E3A8A", va="top")
    ax_a.text(0.08, 1.05, "Sequence Identity in the Twilight Zone",
              transform=ax_a.transAxes, fontsize=11, fontweight="bold", color="#0F172A", va="top")
    ax_a.text(0.08, 1.00, "Pairwise amino acid identity of housekeeping core (n=5,120) vs VIR FS_001 (n=194)",
              transform=ax_a.transAxes, fontsize=8.2, fontstyle="italic", color="#475569", va="top")
    
    # Top right: Explanatory summary panel
    ax_desc = fig.add_axes([0.53, 0.52, 0.43, 0.41])
    ax_desc.axis("off")
    desc_box = mpl.patches.FancyBboxPatch((0.02, 0.02), 0.96, 0.94, boxstyle="round,pad=0.02,rounding_size=0.03",
                                          facecolor="#F8FAFC", edgecolor="#CBD5E1", linewidth=1.2)
    ax_desc.add_patch(desc_box)
    ax_desc.text(0.07, 0.88, "Key Orthology Findings:", fontsize=10.5, fontweight="bold", color="#0F172A")
    ax_desc.text(0.07, 0.54,
                 "• Housekeeping Backbone: Mean identity ~98%,\n"
                 "  establishing high cross-continental assembly fidelity.\n\n"
                 "• VIR Antigens in the Twilight Zone: Median identity\n"
                 "  is only ~32% within FS_001, where sequence alignment\n"
                 "  methods lose statistical sensitivity.\n\n"
                 "• Pseudogene Rescue: Translating unannotated GFF3\n"
                 "  pseudogenes rescued 145 loci, restoring syntenic\n"
                 "  landmarks in Peru and Indonesia.\n\n"
                 "• Syntenic Filtering: Out of 194 reciprocal best-hit\n"
                 "  (RBH) pairs between Thailand and Peru, only 11\n"
                 "  possess conserved flanking microsynteny.",
                 fontsize=8.5, color="#334155", va="center")
    
    # Bottom row: Panel b (Ribbon synteny map across whole width, x: 0.04 to 0.96, y: 0.04 to 0.45)
    ax_b = fig.add_axes([0.04, 0.03, 0.92, 0.44])
    im_b = Image.open("/Users/anton/git/orbit-paper/manuscript/figures/fig4_ribbon_synteny.png")
    ax_b.imshow(im_b)
    ax_b.axis("off")
    ax_b.text(0.01, 1.05, "b", transform=ax_b.transAxes, fontsize=15, fontweight="bold", color="#1E3A8A", va="top")
    ax_b.text(0.04, 1.05, "Cross-Continental Ribbon Synteny Map Between PvW1 (Thailand) and PvPAM (Peru)",
              transform=ax_b.transAxes, fontsize=11, fontweight="bold", color="#0F172A", va="top")
    ax_b.text(0.04, 1.00, "Conserved internal chromosomal backbone (grey ribbons) flanked by highly scrambled, non-syntenic subtelomeric VIR clusters",
              transform=ax_b.transAxes, fontsize=8.2, fontstyle="italic", color="#475569", va="top")
    
    plt.savefig("/Users/anton/git/orbit-paper/manuscript/figures/figure4_synteny_twilight.png", dpi=300, bbox_inches="tight")
    plt.savefig("/Users/anton/git/orbit-paper/manuscript/figures/figure4_synteny_twilight.pdf", bbox_inches="tight")
    print("Figure 4 successfully generated!")

if __name__ == "__main__":
    build_figure4()
