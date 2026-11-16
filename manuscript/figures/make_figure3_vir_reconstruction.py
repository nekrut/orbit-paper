#!/usr/bin/env python3
"""
Generate Figure 7 (figure3_vir_reconstruction.{pdf,png}) exclusively from
tracked in-repo files under manuscript/figures/data/vir/.
"""
from io import BytesIO
from pathlib import Path

import fitz  # PyMuPDF
import matplotlib.gridspec as gridspec
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
from scipy.stats import mannwhitneyu

plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["axes.edgecolor"] = "#333333"
plt.rcParams["axes.linewidth"] = 0.8
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE / "data" / "vir"


def main() -> None:
    hk_path = DATA_DIR / "housekeeping_rbh.tsv"
    vir_path = DATA_DIR / "fs001_rbh.tsv"
    tree_pdf_path = DATA_DIR / "q2_part_tree.pdf"

    df_hk = pd.read_csv(hk_path, sep="\t")
    df_vir = pd.read_csv(vir_path, sep="\t")

    hk_pident = (
        df_hk["pident"] * 100.0 if df_hk["pident"].max() <= 1.0 else df_hk["pident"]
    )
    vir_pident = (
        df_vir["pident"] * 100.0 if df_vir["pident"].max() <= 1.0 else df_vir["pident"]
    )

    hk_med = float(np.median(hk_pident))
    hk_iqr = float(np.percentile(hk_pident, 75) - np.percentile(hk_pident, 25))
    vir_med = float(np.median(vir_pident))
    vir_iqr = float(np.percentile(vir_pident, 75) - np.percentile(vir_pident, 25))
    _, mw_p = mannwhitneyu(vir_pident, hk_pident, alternative="two-sided")
    mw_exp = int(np.floor(np.log10(mw_p)))
    mw_mant = mw_p / (10.0 ** mw_exp)
    sup_map = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
    mw_p_label = f"{mw_mant:.1f} × 10{str(mw_exp).translate(sup_map)}"

    fig = plt.figure(figsize=(13.6, 6.1), dpi=300)
    fig.patch.set_facecolor("white")
    gs = gridspec.GridSpec(1, 2, width_ratios=[1.12, 1.18], wspace=0.12)

    # Panel A: Sequence vs. Structural Divergence
    ax1 = fig.add_subplot(gs[0])
    data = [vir_pident.values, hk_pident.values]
    colors = ["#2563eb", "#d97706"]
    labels = [
        f"VIR Core Fold\n(FS_001 RBH, n = {len(vir_pident)})",
        f"Housekeeping Control\n(Single-Copy RBH, n = {len(hk_pident)})",
    ]

    bp = ax1.boxplot(
        data,
        vert=False,
        patch_artist=True,
        tick_labels=labels,
        widths=0.38,
        boxprops=dict(linewidth=1.2, alpha=0.82),
        medianprops=dict(color="#111827", linewidth=2.2),
        whiskerprops=dict(linewidth=1.2, color="#374151"),
        capprops=dict(linewidth=1.2, color="#374151"),
        flierprops=dict(marker="o", markersize=2.8, alpha=0.32),
    )

    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_edgecolor("#1e293b")

    np.random.seed(42)
    for i, (d, c) in enumerate(zip(data, colors), start=1):
        y = np.random.normal(i, 0.06, size=len(d))
        ax1.scatter(
            d,
            y,
            alpha=0.35,
            color=c,
            edgecolors="none",
            s=15,
            zorder=3,
        )

    ax1.set_xlabel(
        "Pairwise Cross-Strain Sequence Identity (%)",
        fontsize=10.5,
        fontweight="bold",
        labelpad=8,
    )
    ax1.set_title(
        "A  Sequence vs. Structural Divergence (2,592 VIR proteins)",
        fontsize=11.5,
        fontweight="bold",
        loc="left",
        pad=12,
        color="#111827",
    )
    ax1.set_xlim(15, 104)
    ax1.set_ylim(0.18, 2.65)
    ax1.grid(axis="x", linestyle="--", alpha=0.5, color="#cbd5e1")
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.tick_params(axis="y", labelsize=9.5)
    ax1.tick_params(axis="x", labelsize=9.5)

    # Annotate medians and IQRs
    ax1.annotate(
        f"VIR FS_001 Median: {vir_med:.1f}% (IQR {vir_iqr:.1f}%)\nMann–Whitney U p = {mw_p_label} vs. Housekeeping",
        xy=(vir_med, 1.20),
        xytext=(vir_med - 14, 1.46),
        arrowprops=dict(arrowstyle="->", color="#1e40af", lw=1.2),
        fontsize=8.6,
        fontweight="bold",
        color="#1e3a8a",
        bbox=dict(
            boxstyle="round,pad=0.35",
            facecolor="#eff6ff",
            edgecolor="#93c5fd",
            lw=0.9,
        ),
    )

    ax1.annotate(
        f"Housekeeping Median: {hk_med:.1f}% (IQR {hk_iqr:.1f}%)",
        xy=(hk_med, 2.20),
        xytext=(48, 2.40),
        arrowprops=dict(arrowstyle="->", color="#92400e", lw=1.2),
        fontsize=8.6,
        fontweight="bold",
        color="#92400e",
        bbox=dict(
            boxstyle="round,pad=0.35",
            facecolor="#fffbeb",
            edgecolor="#fcd34d",
            lw=0.9,
        ),
    )

    # Explicit structural vs sequence clustering consolidation box
    consolidation_text = (
        "Repertoire-Wide Structural Consolidation (2,592 VIR proteins):\n"
        "• Sequence (MMseqs2/MCL): 203 clusters (146 with ≥3 members)\n"
        "• Structure (Foldseek 3Di+AA): 73 CPU classes (24 with ≥3; 76 Galaxy)\n"
        "• Universal core: 21 classes in all 3 strains (97.3%, 2,523/2,592 proteins)"
    )
    ax1.text(
        0.02,
        0.025,
        consolidation_text,
        transform=ax1.transAxes,
        fontsize=8.1,
        va="bottom",
        ha="left",
        color="#1f2937",
        linespacing=1.3,
        bbox=dict(
            boxstyle="round,pad=0.38",
            facecolor="#f8fafc",
            edgecolor="#cbd5e1",
            lw=0.9,
        ),
    )

    # Panel B: Core-Fold Structural Phylogeny (FS_001, n = 338)
    ax2 = fig.add_subplot(gs[1])
    doc = fitz.open(tree_pdf_path)
    page = doc.load_page(0)
    pix = page.get_pixmap(dpi=300)
    img_tree = Image.open(BytesIO(pix.tobytes("png")))
    w, h = img_tree.size
    # Tighter crop around the circular phylogeny to maximize tree legibility
    img_tree_cropped = img_tree.crop(
        (int(w * 0.14), int(h * 0.14), int(w * 0.88), int(h * 0.86))
    )

    ax2.imshow(np.array(img_tree_cropped))
    ax2.set_title(
        "B  Core-Fold Structural Phylogeny (FS_001, n = 338)",
        fontsize=11.5,
        fontweight="bold",
        loc="left",
        pad=12,
        color="#111827",
    )
    ax2.axis("off")

    # Match exact ggtree palette from plot_and_test.R:
    # scale_color_manual(values=c(PvP01="#E41A1C", PvW1="#377EB8", PvPAM="#4DAF4A"))
    p_pvp01 = mlines.Line2D(
        [],
        [],
        color="#E41A1C",
        marker="o",
        linestyle="None",
        markersize=6.5,
        label="PvP01 (Indonesia, n = 118)",
    )
    p_pvw1 = mlines.Line2D(
        [],
        [],
        color="#377EB8",
        marker="o",
        linestyle="None",
        markersize=6.5,
        label="PvW1 (Thailand, n = 110)",
    )
    p_pvpam = mlines.Line2D(
        [],
        [],
        color="#4DAF4A",
        marker="o",
        linestyle="None",
        markersize=6.5,
        label="PvPAM (Peru, n = 110)",
    )
    ax2.legend(
        handles=[p_pvp01, p_pvw1, p_pvpam],
        loc="upper left",
        bbox_to_anchor=(0.0, 0.99),
        title="Geographical Isolate",
        frameon=True,
        facecolor="white",
        edgecolor="#cbd5e1",
        fontsize=8.2,
        title_fontsize=8.6,
    )

    ax2.text(
        0.99,
        0.02,
        "Fitch Parsimony Permutation Test:\nObserved score = 160 vs. null 160\n(mean 159.2 ± 3.8, p = 0.55; pan-mixed)",
        transform=ax2.transAxes,
        fontsize=8.2,
        va="bottom",
        ha="right",
        color="#1f2937",
        linespacing=1.3,
        bbox=dict(
            boxstyle="round,pad=0.38",
            facecolor="#f8fafc",
            edgecolor="#cbd5e1",
            lw=0.9,
        ),
    )

    fig.subplots_adjust(left=0.06, right=0.98, bottom=0.12, top=0.91, wspace=0.14)
    out_pdf = HERE / "figure3_vir_reconstruction.pdf"
    out_png = HERE / "figure3_vir_reconstruction.png"
    plt.savefig(out_pdf, dpi=300, bbox_inches="tight")
    plt.savefig(out_png, dpi=300, bbox_inches="tight")
    print(
        f"Saved {out_pdf} and {out_png} "
        f"(VIR median={vir_med:.1f}%, IQR={vir_iqr:.1f}%; HK median={hk_med:.1f}%, IQR={hk_iqr:.1f}%)"
    )


if __name__ == "__main__":
    main()
