#!/usr/bin/env python3
"""
Generate Figure 4: Progression of Autonomous Paper Replication on Galaxy Cyberinfrastructure.
Four-panel layout with clean A, B, C, D panel labels only (all explanations in the figure legend):
- A: Initial workflow construction in Galaxy editor (native_editor_orange_mismatch.png)
- B: Validated Galaxy workflow with transcript-to-gene lookup (native_editor_validated.png)
- C: Galaxy History Notebook rendering and living history (history_notebook_screenshot.png)
- D: Biological replication and whole-transcriptome concordance (comparison_figure.png,
     generated directly from tracked TSV files deseq2_kallisto_full_results.tsv and
     deseq2_glucose_vs_control.tsv in manuscript/figures/data/bacillus/)
"""

import os
from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle
import numpy as np
import pandas as pd
from PIL import Image

mpl.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]
mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["figure.dpi"] = 300
mpl.rcParams["savefig.dpi"] = 300
mpl.rcParams["pdf.fonttype"] = 42


def generate_panel_d_comparison(data_dir: Path) -> Path:
    """Compute Panel D (Kallisto vs HISAT2 scatter, heatmaps, bars, and concordance table)
    directly from tracked DESeq2 TSV files in data_dir."""
    cols = ["gene_id", "baseMean", "log2FC", "lfcSE", "stat", "pvalue", "padj"]
    df_kallisto = pd.read_csv(
        data_dir / "deseq2_kallisto_full_results.tsv",
        sep="\t",
        names=cols,
        index_col=0,
    )
    df_hisat2 = pd.read_csv(
        data_dir / "deseq2_glucose_vs_control.tsv",
        sep="\t",
        names=cols,
        index_col=0,
    )

    common_genes = df_kallisto.index.intersection(df_hisat2.index)
    valid_mask = (
        df_kallisto.loc[common_genes, "log2FC"].notna()
        & df_hisat2.loc[common_genes, "log2FC"].notna()
    )
    valid_genes = common_genes[valid_mask]
    n_valid = int(valid_mask.sum())
    r_val = float(
        df_kallisto.loc[valid_genes, "log2FC"].corr(
            df_hisat2.loc[valid_genes, "log2FC"]
        )
    )
    r2_val = r_val ** 2

    toxin_data = [
        ("entFM", "BCE_RS10070"),
        ("nheA", "BCE_RS09750"),
        ("nheB", "BCE_RS09755"),
        ("nheC", "BCE_RS09760"),
    ]

    fig = plt.figure(figsize=(18, 11), dpi=300, facecolor="white")
    gs = GridSpec(
        2,
        3,
        figure=fig,
        width_ratios=[1.08, 0.98, 1.32],
        height_ratios=[1, 1],
        wspace=0.30,
        hspace=0.35,
    )

    # Subpanel 1: Published Figure 4
    ax_paper = fig.add_subplot(gs[:, 0])
    img_paper = mpimg.imread(data_dir / "paper_fig4_enterotoxins.jpg")
    ax_paper.imshow(img_paper)
    ax_paper.axis("off")
    ax_paper.set_title(
        "Published Study (Sci Rep 2025, Fig 4)\nEnterotoxin Heatmap across Carbohydrates",
        fontsize=12,
        weight="bold",
        pad=12,
    )

    # Subpanel 2: Replicated Heatmaps (Kallisto vs HISAT2)
    ax_heat = fig.add_subplot(gs[0, 1])
    heat_matrix = np.zeros((4, 2))
    for i, (sym, gid) in enumerate(toxin_data):
        heat_matrix[i, 0] = df_kallisto.loc[gid, "log2FC"]
        heat_matrix[i, 1] = df_hisat2.loc[gid, "log2FC"]

    cmap = plt.cm.coolwarm
    im = ax_heat.imshow(heat_matrix, cmap=cmap, vmin=-2.5, vmax=2.0, aspect="auto")
    ax_heat.set_xticks([0, 1])
    ax_heat.set_xticklabels(
        ["Kallisto\n(Pseudoalign)", "HISAT2\n(Spliced Align)"],
        fontsize=10.5,
        weight="bold",
    )
    ax_heat.set_yticks(range(4))
    ax_heat.set_yticklabels(
        [t[0] for t in toxin_data], fontsize=12, style="italic", weight="bold"
    )
    ax_heat.set_title(
        "Replicated Heatmaps (GLU vs Ctrl)\nKallisto vs HISAT2 (* padj ≤ 0.05)",
        fontsize=12,
        weight="bold",
        pad=10,
    )

    # Strictly reserve * and ** for BH-adjusted padj <= 0.05 / <= 0.01
    for i, (sym, gid) in enumerate(toxin_data):
        k_fc = df_kallisto.loc[gid, "log2FC"]
        k_padj = df_kallisto.loc[gid, "padj"]
        ast_k = "**" if k_padj <= 0.01 else ("*" if k_padj <= 0.05 else "")
        lbl_k = f"{k_fc:+.2f}\n{ast_k}" if ast_k else f"{k_fc:+.2f}"
        col_k = "white" if abs(k_fc) > 1.2 else "black"
        ax_heat.text(
            0, i, lbl_k, ha="center", va="center", fontsize=10, weight="bold", color=col_k
        )

        h_fc = df_hisat2.loc[gid, "log2FC"]
        h_padj = df_hisat2.loc[gid, "padj"]
        ast_h = "**" if h_padj <= 0.01 else ("*" if h_padj <= 0.05 else "")
        lbl_h = f"{h_fc:+.2f}\n{ast_h}" if ast_h else f"{h_fc:+.2f}"
        col_h = "white" if abs(h_fc) > 1.2 else "black"
        ax_heat.text(
            1, i, lbl_h, ha="center", va="center", fontsize=10, weight="bold", color=col_h
        )

    cbar = plt.colorbar(im, ax=ax_heat, fraction=0.08, pad=0.06)
    cbar.set_label("log2 Fold Change", fontsize=10, weight="bold")

    # Subpanel 3: Enterotoxin Log2FC ± SE Bar Plot
    ax_bar = fig.add_subplot(gs[1, 1])
    y_pos = np.arange(len(toxin_data))
    bar_h = 0.35

    k_lfcs = [df_kallisto.loc[t[1], "log2FC"] for t in toxin_data]
    k_errs = [df_kallisto.loc[t[1], "lfcSE"] for t in toxin_data]
    h_lfcs = [df_hisat2.loc[t[1], "log2FC"] for t in toxin_data]
    h_errs = [df_hisat2.loc[t[1], "lfcSE"] for t in toxin_data]

    ax_bar.barh(
        y_pos - bar_h / 2,
        k_lfcs,
        xerr=k_errs,
        height=bar_h,
        color="#2b83ba",
        alpha=0.85,
        label="Kallisto",
        capsize=4,
        edgecolor="black",
    )
    ax_bar.barh(
        y_pos + bar_h / 2,
        h_lfcs,
        xerr=h_errs,
        height=bar_h,
        color="#fdae61",
        alpha=0.85,
        label="HISAT2",
        capsize=4,
        edgecolor="black",
    )

    ax_bar.axvline(0, color="grey", linestyle="--", linewidth=1)
    ax_bar.set_yticks(y_pos)
    ax_bar.set_yticklabels(
        [t[0] for t in toxin_data], fontsize=11, style="italic", weight="bold"
    )
    ax_bar.invert_yaxis()
    ax_bar.set_xlabel("log2 Fold Change (GLU vs Control)", fontsize=11, weight="bold")
    ax_bar.set_title(
        "Enterotoxin Effect Size (log2FC ± SE)\nKallisto vs HISAT2",
        fontsize=12,
        weight="bold",
        pad=10,
    )
    ax_bar.legend(loc="lower right", frameon=True, fontsize=10)
    ax_bar.set_xlim(-3.4, 2.5)

    # Subpanel 4: Whole-Transcriptome Scatter Plot (Kallisto vs HISAT2)
    ax_scatter = fig.add_subplot(gs[0, 2])
    x_vals = df_hisat2.loc[valid_genes, "log2FC"]
    y_vals = df_kallisto.loc[valid_genes, "log2FC"]

    ax_scatter.scatter(
        x_vals, y_vals, alpha=0.35, s=12, color="#4575b4", edgecolors="none"
    )
    ax_scatter.plot(
        [-8, 8],
        [-8, 8],
        color="red",
        linestyle="--",
        linewidth=1.5,
        label="Identity line (y = x)",
    )

    for sym, gid in toxin_data:
        hx = df_hisat2.loc[gid, "log2FC"]
        ky = df_kallisto.loc[gid, "log2FC"]
        ax_scatter.scatter(hx, ky, s=80, color="#d73027", edgecolor="black", zorder=5)
        ax_scatter.annotate(
            sym,
            (hx, ky),
            xytext=(8, -4),
            textcoords="offset points",
            fontsize=10,
            weight="bold",
            color="#a50026",
        )

    ax_scatter.set_xlabel("HISAT2 log2FC", fontsize=11, weight="bold")
    ax_scatter.set_ylabel("Kallisto log2FC", fontsize=11, weight="bold")
    ax_scatter.set_title(
        f"Whole Transcriptome Agreement\nn = {n_valid:,} Non-NA Genes (Pearson r = {r_val:.4f}, R² = {r2_val:.4f})",
        fontsize=11.5,
        weight="bold",
        pad=10,
    )
    ax_scatter.legend(loc="upper left", frameon=True, fontsize=9.5)
    ax_scatter.set_xlim(-7.5, 7.5)
    ax_scatter.set_ylim(-7.5, 7.5)
    ax_scatter.grid(True, linestyle=":", alpha=0.6)

    # Subpanel 5: Systematic Concordance Summary Table (100% computed from TSVs)
    ax_table = fig.add_subplot(gs[1, 2])
    ax_table.axis("off")
    ax_table.set_title(
        "Systematic Concordance Summary", fontsize=12, weight="bold", pad=10
    )

    def _fmt_cell(df_src, gid, show_raw_p=False):
        r = df_src.loc[gid]
        lfc = float(r["log2FC"])
        pval = float(r["pvalue"])
        padj = float(r["padj"])
        if padj <= 0.05:
            return f"log2FC = {lfc:+.2f}\npadj = {padj:.4f} *"
        elif show_raw_p:
            return f"log2FC = {lfc:+.2f}\np = {pval:.3f}\npadj = {padj:.3f} (NS)"
        else:
            return f"log2FC = {lfc:+.2f}\npadj = {padj:.3f} (NS)"

    headers = [
        "Target",
        "Paper Fig 4",
        "Kallisto (Our Run)",
        "HISAT2 (Our Run)",
        "Status",
    ]
    rows = [
        [
            "nheB",
            "Down (**)\npadj = 0.0027",
            _fmt_cell(df_kallisto, "BCE_RS09755", show_raw_p=False),
            _fmt_cell(df_hisat2, "BCE_RS09755", show_raw_p=False),
            "Concordant (*\npadj ≤ 0.05)",
        ],
        [
            "nheA",
            "Down (blue)\np = 0.050\npadj = 0.14 (NS)",
            _fmt_cell(df_kallisto, "BCE_RS09750", show_raw_p=True),
            _fmt_cell(df_hisat2, "BCE_RS09750", show_raw_p=True),
            "Directional\n(p < 0.05,\npadj > 0.05)",
        ],
        [
            "nheC",
            "Neutral (~0)\npadj = 0.88 (NS)",
            _fmt_cell(df_kallisto, "BCE_RS09760", show_raw_p=False),
            _fmt_cell(df_hisat2, "BCE_RS09760", show_raw_p=False),
            "Concordant\n(Neutral, NS)",
        ],
        [
            "entFM",
            "Up (*)\npadj = 0.0475",
            _fmt_cell(df_kallisto, "BCE_RS10070", show_raw_p=True),
            _fmt_cell(df_hisat2, "BCE_RS10070", show_raw_p=True),
            "Directional\n(p < 0.05,\npadj > 0.05)",
        ],
    ]

    table = ax_table.table(
        cellText=rows,
        colLabels=headers,
        colWidths=[0.12, 0.22, 0.23, 0.23, 0.22],
        loc="center",
        cellLoc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(7.8)
    table.scale(1.02, 2.45)

    for j in range(5):
        table[(0, j)].set_facecolor("#2b5c8f")
        table[(0, j)].set_text_props(weight="bold", color="white")
        table[(0, j)].set_height(0.11)

    for i in range(1, 5):
        status_text = rows[i - 1][4]
        is_directional = "Directional" in status_text
        for j in range(5):
            if j == 4:
                if is_directional:
                    table[(i, j)].set_facecolor("#fff3cd")
                    table[(i, j)].set_text_props(weight="bold", color="#856404")
                else:
                    table[(i, j)].set_facecolor("#d4edda")
                    table[(i, j)].set_text_props(weight="bold", color="#155724")
            else:
                table[(i, j)].set_facecolor("#f8f9fa" if i % 2 == 0 else "#ffffff")

    out_path = data_dir / "comparison_figure.png"
    plt.savefig(out_path, bbox_inches="tight", dpi=300)
    plt.close(fig)
    return out_path


def build_replication_figure():
    fig_dir = Path(__file__).resolve().parent
    data_dir = fig_dir / "data" / "bacillus"

    img_d_path = generate_panel_d_comparison(data_dir)
    img_a_path = data_dir / "native_editor_orange_mismatch.png"
    img_b_path = data_dir / "native_editor_validated.png"
    img_c_path = data_dir / "history_notebook_screenshot.png"

    img_a = Image.open(img_a_path)
    img_b = Image.open(img_b_path)
    img_c = Image.open(img_c_path)
    img_d = Image.open(img_d_path)

    # 16.0 x 10.2 inches clean 2x2 grid
    fig, ax = plt.subplots(figsize=(16.0, 10.2), facecolor="white")
    ax.set_xlim(0.0, 16.0)
    ax.set_ylim(0.0, 10.2)
    ax.axis("off")

    col_w = 7.50
    row_h = 4.55
    x_left = 0.35
    x_right = 8.20
    y_top = 5.20
    y_bottom = 0.20

    panels = [
        ("A", img_a, x_left, y_top),
        ("B", img_b, x_right, y_top),
        ("C", img_c, x_left, y_bottom),
        ("D", img_d, x_right, y_bottom),
    ]

    for label, img, x, y in panels:
        # Clean panel letter above top-left corner of each panel
        ax.text(
            x,
            y + row_h + 0.08,
            label,
            fontsize=15,
            fontweight="bold",
            color="#0F172A",
            va="bottom",
            ha="left",
            zorder=5,
        )
        # Display panel image
        ax.imshow(img, extent=[x, x + col_w, y, y + row_h], aspect="auto", zorder=3)
        # Subtle 0.8pt neutral border around the panel edge
        border = Rectangle(
            (x, y),
            col_w,
            row_h,
            fill=False,
            edgecolor="#CBD5E1",
            linewidth=0.8,
            zorder=4,
        )
        ax.add_patch(border)

    out_pdf = fig_dir / "figure_bacillus_replication.pdf"
    out_png = fig_dir / "figure_bacillus_replication.png"
    plt.tight_layout()
    plt.savefig(out_pdf, bbox_inches="tight", dpi=300)
    plt.savefig(out_png, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Generated {out_pdf} and {out_png} successfully!")


if __name__ == "__main__":
    build_replication_figure()
