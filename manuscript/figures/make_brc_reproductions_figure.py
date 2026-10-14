#!/usr/bin/env python3
"""
Generate composite 4-panel figure (figure_brc_reproductions.pdf / .png) for the pathogen
and vector genomics replications on the Galactic plane:
- A: Hokken et al. (2018) A. fumigatus itraconazole time-course RNA-seq log2FC concordance
- B: Chung et al. (2014) A. fumigatus SrbA ChIP-seq target recovery & RNA-seq concordance
- C: Toenhake et al. (2018) P. falciparum 8-timepoint IDC ATAC-seq/RNA-seq stage-by-stage rebuild
- D: Ruiz et al. (2021) A. gambiae ATAC-seq canonical vs. reconstructed region/gene/enhancer counts
"""

import os
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from PIL import Image
import matplotlib as mpl

mpl.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]
mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["figure.dpi"] = 300
mpl.rcParams["savefig.dpi"] = 300
mpl.rcParams["pdf.fonttype"] = 42


def build_brc_figure():
    fig_dir = os.path.dirname(os.path.abspath(__file__))
    panel_dir = os.path.join(fig_dir, "brc_panels")

    img_a = Image.open(os.path.join(panel_dir, "hokken_fig3.png"))
    img_b = Image.open(os.path.join(panel_dir, "chung_recovery.png"))
    img_c = Image.open(os.path.join(panel_dir, "toenhake_fig.png"))
    img_d = Image.open(os.path.join(panel_dir, "ruiz_fig7.png"))

    fig = plt.figure(figsize=(15.5, 9.5), facecolor="white")
    gs = gridspec.GridSpec(
        2, 2,
        figure=fig,
        height_ratios=[1.0, 1.15],
        width_ratios=[1.0, 1.0],
        hspace=0.14,
        wspace=0.08,
    )

    panels = [
        (gs[0, 0], img_a, "A"),
        (gs[0, 1], img_b, "B"),
        (gs[1, 0], img_c, "C"),
        (gs[1, 1], img_d, "D"),
    ]

    for spec, img, label in panels:
        ax = fig.add_subplot(spec)
        ax.imshow(img)
        ax.axis("off")
        ax.text(
            -0.02, 1.04, label,
            transform=ax.transAxes,
            fontsize=16,
            fontweight="bold",
            color="#0F172A",
            va="top",
            ha="left",
        )

    out_pdf = os.path.join(fig_dir, "figure_brc_reproductions.pdf")
    out_png = os.path.join(fig_dir, "figure_brc_reproductions.png")
    fig.savefig(out_pdf, bbox_inches="tight", facecolor="white")
    fig.savefig(out_png, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"Saved {out_pdf} and {out_png}")


if __name__ == "__main__":
    build_brc_figure()
