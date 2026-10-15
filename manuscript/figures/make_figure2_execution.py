#!/usr/bin/env python3
"""
Generate publication-grade Figure 2:
Target Enterotoxin Differential Expression and Reference-Assembly Discordance
Across Independent Agent Execution Environments.

Designed at 1:1 full-page width (7.5 in wide) following Nature Methods / Nature
Biotechnology visual standards:
- Panel A: Seamless 3-zone table-forest plot (Target locus & role | DESeq2
  log2FC & Wald 95% CI forest plot | Aligned log2FC [95% CI] and BH-adjusted
  p-value table) across the five target enterotoxin loci (nheB, entFM, nheA,
  nheC, and cytK2).
- Panel B: Library-level transcription of cytotoxin K2 (cytK2, BCE_1209 /
  BCE_RS06135) across the 5 RNA-seq libraries (TSB1-3, GLU1-2) and a graphical
  enterotoxin repertoire concordance matrix contrasting B. pacificus anQ-h4
  against the sequenced isolate B. cereus ATCC 10987.
"""

import os
from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd

mpl.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]
mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["mathtext.fontset"] = "custom"
mpl.rcParams["mathtext.rm"] = "Helvetica"
mpl.rcParams["mathtext.it"] = "Helvetica:italic"
mpl.rcParams["mathtext.bf"] = "Helvetica:bold"
mpl.rcParams["figure.dpi"] = 300
mpl.rcParams["savefig.dpi"] = 300
mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"] = 42


def _format_entry(lfc, lfc_se, pval, padj):
    """Compute 95% CI (lfc +/- 1.96 * lfcSE) and format padj / significance."""
    lfc = float(lfc)
    lfc_se = float(lfc_se)
    ci_l = lfc - 1.96 * lfc_se
    ci_h = lfc + 1.96 * lfc_se
    if pd.isna(padj):
        padj_str = f"NA (p={float(pval):.2f})"
        sig = "n.s."
    else:
        padj_f = float(padj)
        if padj_f < 0.001:
            padj_str = f"{padj_f:.1e}".replace("e-0", "e-")
            sig = "***"
        elif padj_f < 0.01:
            padj_str = f"{padj_f:.4f}"
            sig = "**"
        elif padj_f < 0.05:
            padj_str = f"{padj_f:.4f}"
            sig = "*"
        elif padj_f < 0.10:
            padj_str = f"{padj_f:.4f}"
            sig = "trend"
        else:
            padj_str = f"{padj_f:.4f}"
            sig = "n.s."
    return (lfc, ci_l, ci_h, padj_str, sig)


def _load_execution_data(data_dir: Path):
    df_codex_paper = pd.read_csv(
        data_dir / "codex_paper_enterotoxin_deseq2.tsv", sep="\t"
    ).set_index("gene_name")
    df_cc = pd.read_csv(
        data_dir / "cc_enterotoxin_deseq2.tsv", sep="\t"
    ).set_index("symbol")
    df_codex_atcc = pd.read_csv(
        data_dir / "codex_atcc_enterotoxin_deseq2.tsv", sep="\t"
    ).set_index("gene_name")
    df_agy = pd.read_csv(
        data_dir / "agy_enterotoxin_deseq2.tsv", sep="\t"
    ).set_index("Gene")
    df_cytk_counts = pd.read_csv(data_dir / "cytk2_counts.tsv", sep="\t")

    target_keys = ["nheB", "entFM", "nheA", "nheC", "cytK2"]

    paper_data = {}
    codex_paper_data = {}
    cc_data = {}
    codex_atcc_data = {}
    agy_data = {}

    for k in target_keys:
        if k in df_codex_paper.index:
            r = df_codex_paper.loc[k]
            paper_data[k] = _format_entry(
                r["published_log2FoldChange"],
                r["published_lfcSE"],
                r["published_pvalue"],
                r["published_padj"],
            )
            codex_paper_data[k] = _format_entry(
                r["log2FoldChange"], r["lfcSE"], r["pvalue"], r["padj"]
            )
        else:
            paper_data[k] = None
            codex_paper_data[k] = None

        cc_sym = "cytK" if k == "cytK2" else k
        if cc_sym in df_cc.index:
            r = df_cc.loc[cc_sym]
            cc_data[k] = _format_entry(
                r["log2FoldChange"], r["lfcSE"], r["pvalue"], r["padj"]
            )
        else:
            cc_data[k] = None

        if k in df_codex_atcc.index:
            r = df_codex_atcc.loc[k]
            codex_atcc_data[k] = _format_entry(
                r["log2FoldChange"], r["lfcSE"], r["pvalue"], r["padj"]
            )
        else:
            codex_atcc_data[k] = None

        if k in df_agy.index:
            r = df_agy.loc[k]
            agy_data[k] = _format_entry(
                r["log2FC_replicated"], r["lfcSE"], r["pvalue"], r["padj"]
            )
        else:
            agy_data[k] = None

    cc_cytk_basemean = float(df_cc.loc["cytK", "baseMean"])
    return (
        paper_data,
        cc_data,
        codex_paper_data,
        codex_atcc_data,
        agy_data,
        df_cytk_counts,
        cc_cytk_basemean,
    )


def make_figure():
    base_dir = Path(__file__).resolve().parent
    data_dir = base_dir / "data" / "bacillus"
    (
        paper_data,
        cc_data,
        codex_paper_data,
        codex_atcc_data,
        agy_data,
        df_cytk_counts,
        cc_cytk_basemean,
    ) = _load_execution_data(data_dir)

    # Five execution tracks with Okabe-Ito-harmonized palette matching Figure 1
    models = [
        {
            "id": "paper",
            "name": "Published Benchmark (Vyklická et al., implied anQ-h4)",
            "short": "Published Benchmark (Vyklická et al., implied anQ-h4)",
            "color": "#0f172a",
            "marker": "D",
            "ms": 5.0,
            "data": paper_data,
        },
        {
            "id": "cc",
            "name": "Claude Code / Opus 5.5 (ATCC 10987, ashr-shrunken)",
            "short": "Claude Code (ATCC 10987, ashr-shrunken)",
            "color": "#2563eb",
            "marker": "s",
            "ms": 5.2,
            "data": cc_data,
        },
        {
            "id": "codex_paper",
            "name": "OpenAI Codex / GPT-6 (anQ-h4 RefSeq)",
            "short": "OpenAI Codex (anQ-h4 RefSeq)",
            "color": "#ea580c",
            "marker": "^",
            "ms": 5.6,
            "data": codex_paper_data,
        },
        {
            "id": "codex_atcc",
            "name": "OpenAI Codex / GPT-6 (ATCC 10987)",
            "short": "OpenAI Codex (ATCC 10987)",
            "color": "#b91c1c",
            "marker": "v",
            "ms": 5.6,
            "data": codex_atcc_data,
        },
        {
            "id": "agy",
            "name": "Antigravity / Gemini 3.8 Flash (anQ-h4)",
            "short": "Antigravity / Gemini (anQ-h4)",
            "color": "#0d9488",
            "marker": "o",
            "ms": 5.2,
            "data": agy_data,
        },
    ]

    genes = [
        {
            "key": "nheB",
            "symbol": "nheB",
            "desc": "Enterotoxin Nhe subunit B",
            "locus": "LMD38_RS17200 / BCE_1969",
            "badge": "Catabolite repressed",
            "badge_bg": "#dbeafe",
            "badge_fg": "#1e40af",
        },
        {
            "key": "entFM",
            "symbol": "entFM",
            "desc": "Enterotoxin FM peptidase",
            "locus": "LMD38_RS16820 / BCE_2037",
            "badge": "Growth induced",
            "badge_bg": "#fef3c7",
            "badge_fg": "#92400e",
        },
        {
            "key": "nheA",
            "symbol": "nheA",
            "desc": "Enterotoxin Nhe subunit A",
            "locus": "LMD38_RS17205 / BCE_1968",
            "badge": "Moderate repression",
            "badge_bg": "#e0f2fe",
            "badge_fg": "#0369a1",
        },
        {
            "key": "nheC",
            "symbol": "nheC",
            "desc": "Enterotoxin Nhe subunit C",
            "locus": "LMD38_RS17195 / BCE_1970",
            "badge": "Low basal / neutral",
            "badge_bg": "#f1f5f9",
            "badge_fg": "#475569",
        },
        {
            "key": "cytK2",
            "symbol": "cytK2",
            "desc": "Cytotoxin K2 pore toxin",
            "locus": "BCE_1209 / BCE_RS06135",
            "badge": "Assembly-dependent",
            "badge_bg": "#fce7f3",
            "badge_fg": "#9d174d",
        },
    ]

    # Full-width 1:1 figure (7.5 in wide x 5.05 in high)
    fig = plt.figure(figsize=(7.5, 5.05), dpi=300, facecolor="#ffffff")

    # =========================================================================
    # LEFT MODULE (Panel A): Seamless 3-Zone Forest Plot + Statistical Table
    # =========================================================================
    y_bot, y_height = 0.135, 0.745
    # Touching x-coordinates so row shading flows seamlessly across all 3 columns
    ax_meta = fig.add_axes([0.010, y_bot, 0.165, y_height])
    ax_for = fig.add_axes([0.175, y_bot, 0.230, y_height])
    ax_tab = fig.add_axes([0.405, y_bot, 0.215, y_height])

    y_max = 25.0
    y_min = 0.0
    for ax in (ax_meta, ax_for, ax_tab):
        ax.set_ylim(y_min, y_max)

    ax_meta.set_xlim(0, 1)
    ax_meta.axis("off")

    x_lo, x_hi = -4.2, 3.0
    ax_for.set_xlim(x_lo, x_hi)

    ax_tab.set_xlim(0, 1)
    ax_tab.axis("off")

    # Panel A header (well above column headers)
    fig.text(
        0.010,
        0.968,
        "A",
        fontsize=11.0,
        fontweight="bold",
        color="#0f172a",
        va="top",
        ha="left",
    )
    fig.text(
        0.032,
        0.965,
        "Target enterotoxin differential expression (1% glucose vs. TSB control)",
        fontsize=8.5,
        fontweight="bold",
        color="#0f172a",
        va="top",
        ha="left",
    )

    # Column headers above the 3 zones on an exact shared baseline
    col_hdr_y = y_bot + y_height + 0.014
    fig.text(
        0.014,
        col_hdr_y,
        "Target locus & role",
        fontsize=7.0,
        fontweight="bold",
        color="#334155",
        va="bottom",
        ha="left",
    )
    fig.text(
        0.242,
        col_hdr_y,
        "Repressed (< 0)",
        fontsize=6.7,
        fontweight="bold",
        color="#1d4ed8",
        va="bottom",
        ha="center",
    )
    fig.text(
        0.356,
        col_hdr_y,
        "Induced (> 0)",
        fontsize=6.7,
        fontweight="bold",
        color="#b45309",
        va="bottom",
        ha="center",
    )
    fig.text(
        0.412,
        col_hdr_y,
        r"$\mathbf{log_2FC}$ [95% CI]",
        fontsize=7.0,
        color="#334155",
        va="bottom",
        ha="left",
    )
    fig.text(
        0.614,
        col_hdr_y,
        r"$\mathbf{p_{adj}}$ (sig.)",
        fontsize=7.0,
        color="#334155",
        va="bottom",
        ha="right",
    )

    group_step = 5.0
    row_step = 0.78

    for g_idx, g in enumerate(genes):
        g_top = y_max - g_idx * group_step
        g_bot = g_top - group_step
        bg_col = "#f8fafc" if g_idx % 2 == 0 else "#ffffff"

        # Seamless alternating row band across all three axes
        for ax in (ax_meta, ax_for, ax_tab):
            ax.axhspan(g_bot, g_top, facecolor=bg_col, edgecolor="none", zorder=0)
            if g_idx > 0:
                ax.axhline(g_top, color="#e2e8f0", lw=0.7, zorder=1)

        # Subtle vertical dividers at the boundaries of the forest plot
        ax_for.axvline(x_lo, color="#e2e8f0", lw=0.7, zorder=2)
        ax_for.axvline(x_hi, color="#e2e8f0", lw=0.7, zorder=2)

        # Left column: Gene metadata
        ax_meta.text(
            0.03,
            g_top - 0.80,
            g["symbol"],
            fontsize=8.6,
            fontweight="bold",
            style="italic",
            color="#0f172a",
            va="center",
            ha="left",
        )
        ax_meta.text(
            0.03,
            g_top - 1.70,
            g["desc"],
            fontsize=6.4,
            color="#334155",
            va="center",
            ha="left",
        )
        ax_meta.text(
            0.03,
            g_top - 2.50,
            g["locus"],
            fontsize=5.6,
            color="#64748b",
            va="center",
            ha="left",
            family="monospace",
        )
        # Response badge
        ax_meta.text(
            0.04,
            g_top - 3.55,
            g["badge"],
            fontsize=6.0,
            fontweight="bold",
            color=g["badge_fg"],
            va="center",
            ha="left",
            bbox=dict(
                boxstyle="round,pad=0.22,rounding_size=0.28",
                facecolor=g["badge_bg"],
                edgecolor="none",
            ),
        )

        # Plot each of the 5 execution tracks
        gene_key = g["key"]
        for m_idx, m in enumerate(models):
            y_pos = g_top - 0.72 - m_idx * row_step
            entry = m["data"][gene_key]

            if entry is None:
                # Absent in B. pacificus anQ-h4
                ax_for.plot(
                    [-3.8, 2.6],
                    [y_pos, y_pos],
                    color="#cbd5e1",
                    lw=0.75,
                    linestyle=":",
                    zorder=2,
                )
                ax_for.scatter(
                    [0.0],
                    [y_pos],
                    marker="x",
                    s=18,
                    color="#94a3b8",
                    linewidth=0.9,
                    zorder=3,
                )
                ax_tab.text(
                    0.03,
                    y_pos,
                    "Undetected (anQ-h4)",
                    fontsize=6.1,
                    style="italic",
                    color="#64748b",
                    va="center",
                    ha="left",
                )
                ax_tab.text(
                    0.97,
                    y_pos,
                    "absent",
                    fontsize=6.0,
                    style="italic",
                    color="#94a3b8",
                    va="center",
                    ha="right",
                )
            else:
                lfc, ci_l, ci_h, padj_str, sig = entry
                draw_l = max(ci_l, x_lo + 0.12)
                draw_h = min(ci_h, x_hi - 0.12)

                # Confidence interval bar
                ax_for.plot(
                    [draw_l, draw_h],
                    [y_pos, y_pos],
                    color=m["color"],
                    lw=1.45,
                    solid_capstyle="round",
                    zorder=3,
                )

                # Small end-caps or arrowheads if clipped
                if ci_l < x_lo:
                    ax_for.scatter(
                        [x_lo + 0.12],
                        [y_pos],
                        marker="<",
                        s=15,
                        color=m["color"],
                        zorder=4,
                    )
                else:
                    ax_for.plot(
                        [ci_l, ci_l],
                        [y_pos - 0.13, y_pos + 0.13],
                        color=m["color"],
                        lw=0.95,
                        zorder=3,
                    )

                if ci_h > x_hi:
                    ax_for.scatter(
                        [x_hi - 0.12],
                        [y_pos],
                        marker=">",
                        s=15,
                        color=m["color"],
                        zorder=4,
                    )
                else:
                    ax_for.plot(
                        [ci_h, ci_h],
                        [y_pos - 0.13, y_pos + 0.13],
                        color=m["color"],
                        lw=0.95,
                        zorder=3,
                    )

                # Central point estimate marker
                ax_for.plot(
                    lfc,
                    y_pos,
                    marker=m["marker"],
                    markersize=m["ms"],
                    color=m["color"],
                    markeredgecolor="#0f172a",
                    markeredgewidth=0.55,
                    zorder=5,
                )

                # Right table readout with generous gutter between columns
                is_sig = sig in ("*", "**", "***")
                fw = "bold" if is_sig else "normal"
                ci_txt = f"{lfc:+.2f} [{ci_l:+.2f}, {ci_h:+.2f}]"
                ax_tab.text(
                    0.03,
                    y_pos,
                    ci_txt,
                    fontsize=6.15,
                    fontweight=fw,
                    color=m["color"] if is_sig else "#334155",
                    va="center",
                    ha="left",
                )
                if sig == "n.s.":
                    sig_label = f"{padj_str}"
                elif sig == "trend":
                    sig_label = f"{padj_str} (tr.)"
                else:
                    sig_label = f"{padj_str} ({sig})"
                ax_tab.text(
                    0.97,
                    y_pos,
                    sig_label,
                    fontsize=6.15,
                    fontweight=fw,
                    color=m["color"] if is_sig else "#64748b",
                    va="center",
                    ha="right",
                )

    # Forest plot axis styling
    ax_for.axvline(0, color="#475569", lw=1.0, linestyle="--", zorder=2)
    ax_for.grid(axis="x", color="#e2e8f0", linestyle=":", lw=0.7, zorder=1)
    ax_for.set_axisbelow(True)
    ax_for.set_xticks([-4, -2, 0, 2])
    ax_for.tick_params(axis="x", labelsize=7.0, colors="#334155", length=3, pad=2)
    ax_for.set_yticks([])
    ax_for.set_xlabel(
        r"DESeq2 $\mathbf{log_2FC}$ ($\pm$ 95% CI)",
        fontsize=7.3,
        fontweight="bold",
        color="#1e293b",
        labelpad=3,
    )
    for spine in ("top", "right", "left"):
        ax_for.spines[spine].set_visible(False)
    ax_for.spines["bottom"].set_color("#94a3b8")
    ax_for.spines["bottom"].set_linewidth(0.8)

    # Top and bottom framing lines across Panel A
    for ax in (ax_meta, ax_for, ax_tab):
        ax.axhline(y_max, color="#64748b", lw=0.9, zorder=4)
        ax.axhline(y_min, color="#64748b", lw=0.9, zorder=4)

    # =========================================================================
    # RIGHT MODULE (Panel B): Reference Discordance at cytK2 & Repertoire Matrix
    # =========================================================================
    fig.text(
        0.652,
        0.968,
        "B",
        fontsize=11.0,
        fontweight="bold",
        color="#0f172a",
        va="top",
        ha="left",
    )
    fig.text(
        0.674,
        0.965,
        "Reference-assembly discordance at cytK2",
        fontsize=8.5,
        fontweight="bold",
        color="#0f172a",
        va="top",
        ha="left",
    )

    # Top subplot of Panel B: Per-library raw read pairs for cytK2
    ax_cytk = fig.add_axes([0.695, 0.505, 0.292, 0.365])

    # Compact legend strip above ax_cytk aligned with Panel A column headers
    b_leg_handles = [
        patches.Patch(facecolor="#2563eb", edgecolor="#0f172a", linewidth=0.5, label="Claude Code (ATCC)"),
        patches.Patch(facecolor="#b91c1c", edgecolor="#0f172a", linewidth=0.5, label="Codex (ATCC)"),
        mpl.lines.Line2D([0], [0], marker="D", color="none", markerfacecolor="#0f172a",
                         markeredgecolor="#0f172a", markersize=4.2, label="anQ-h4 (0 reads)"),
    ]
    ax_cytk.legend(
        handles=b_leg_handles,
        loc="lower center",
        bbox_to_anchor=(0.46, 1.02),
        ncol=3,
        fontsize=5.7,
        frameon=False,
        handlelength=1.0,
        handletextpad=0.35,
        columnspacing=0.75,
    )

    samples = df_cytk_counts["sample"].tolist()
    cc_counts = df_cytk_counts["cc_atcc_raw"].astype(int).tolist()
    codex_atcc_counts = df_cytk_counts["codex_atcc_raw"].astype(int).tolist()
    mean_cc = int(round(float(np.mean(cc_counts))))
    basemean_cc = int(round(cc_cytk_basemean))

    x_ind = np.arange(len(samples))
    bar_w = 0.34

    ax_cytk.bar(
        x_ind - bar_w / 2,
        cc_counts,
        width=bar_w,
        color="#2563eb",
        alpha=0.92,
        edgecolor="#0f172a",
        linewidth=0.5,
        label="Claude Code (ATCC 10987)",
        zorder=3,
    )
    ax_cytk.bar(
        x_ind + bar_w / 2,
        codex_atcc_counts,
        width=bar_w,
        color="#b91c1c",
        alpha=0.88,
        edgecolor="#0f172a",
        linewidth=0.5,
        label="Codex (ATCC 10987)",
        zorder=3,
    )

    # Baseline zero markers for anQ-h4 runs
    ax_cytk.scatter(
        x_ind,
        [32] * len(samples),
        marker="D",
        s=16,
        color="#0f172a",
        zorder=4,
        label="anQ-h4 runs (0 reads)",
    )

    # Mean line computed from TSV
    ax_cytk.axhline(mean_cc, color="#1e40af", lw=0.95, linestyle="--", zorder=2)

    # Place mean callout box high in the clean open space above TSB1-TSB3 with leader arrow
    ax_cytk.annotate(
        f"Mean = {mean_cc} pairs/lib\n(DESeq2 baseMean = {basemean_cc})",
        xy=(0.25, mean_cc),
        xytext=(0.12, 1180),
        fontsize=6.1,
        fontweight="bold",
        color="#1e3a8a",
        va="bottom",
        ha="left",
        bbox=dict(
            boxstyle="round,pad=0.22",
            facecolor="#eff6ff",
            edgecolor="#93c5fd",
            linewidth=0.6,
            alpha=0.95,
        ),
        arrowprops=dict(
            arrowstyle="->",
            color="#1e40af",
            lw=0.75,
            shrinkA=1,
            shrinkB=2,
        ),
        zorder=5,
    )

    # Direct value labels above bars (well clear of callout box and top condition banners)
    for idx, (c_val, x_val) in enumerate(zip(cc_counts, codex_atcc_counts)):
        top_val = max(c_val, x_val)
        ax_cytk.text(
            x_ind[idx],
            top_val + 38,
            f"{c_val:,}",
            fontsize=6.1,
            fontweight="bold",
            color="#1e293b",
            ha="center",
            va="bottom",
            zorder=5,
        )

    # Condition group shading and top header strip
    ax_cytk.axvspan(-0.55, 2.5, facecolor="#f8fafc", zorder=0)
    ax_cytk.axvspan(2.5, 4.55, facecolor="#fffbeb", alpha=0.50, zorder=0)
    ax_cytk.axvline(2.5, color="#cbd5e1", lw=0.8, linestyle="-", zorder=1)

    ax_cytk.text(
        1.0,
        1790,
        "TSB Control (n=3)",
        fontsize=6.4,
        fontweight="bold",
        color="#334155",
        ha="center",
        va="top",
    )
    ax_cytk.text(
        3.5,
        1790,
        "1% Glucose (n=2)",
        fontsize=6.4,
        fontweight="bold",
        color="#92400e",
        ha="center",
        va="top",
    )

    ax_cytk.set_xlim(-0.55, 4.55)
    ax_cytk.set_ylim(0, 1880)
    ax_cytk.set_xticks(x_ind)
    ax_cytk.set_xticklabels(samples, fontsize=6.9, fontweight="bold", color="#334155")
    ax_cytk.set_yticks([0, 500, 1000, 1500])
    ax_cytk.tick_params(axis="y", labelsize=6.7, colors="#334155", length=3, pad=2)
    ax_cytk.set_ylabel(
        "cytK2 read pairs / library",
        fontsize=7.1,
        fontweight="bold",
        color="#1e293b",
        labelpad=2,
    )
    ax_cytk.grid(axis="y", color="#e2e8f0", linestyle=":", lw=0.7, zorder=1)
    ax_cytk.spines["top"].set_visible(False)
    ax_cytk.spines["right"].set_visible(False)
    ax_cytk.spines["left"].set_color("#94a3b8")
    ax_cytk.spines["bottom"].set_color("#94a3b8")

    # Bottom subplot of Panel B: Graphical Reference & Toxin Repertoire Matrix
    ax_mat = fig.add_axes([0.652, 0.135, 0.335, 0.315])
    ax_mat.set_xlim(0, 1)
    ax_mat.set_ylim(0, 1)
    ax_mat.axis("off")

    ax_mat.text(
        0.0,
        0.98,
        "Enterotoxin repertoire recovery by reference genome",
        fontsize=7.3,
        fontweight="bold",
        color="#0f172a",
        va="top",
        ha="left",
    )

    # Graphical matrix comparing the 2 reference assemblies across the toxin loci
    loci_cols = [
        ("nheB", "Down **", "#dbeafe", "#1e40af", "Down ***", "#dbeafe", "#1e40af"),
        ("entFM", "Up *", "#fef3c7", "#92400e", "Up */tr.", "#fef3c7", "#92400e"),
        ("nheA", "Down", "#e0f2fe", "#0369a1", "Down *", "#e0f2fe", "#0369a1"),
        ("nheC", "Basal", "#f1f5f9", "#475569", "Basal", "#f1f5f9", "#475569"),
        ("cytK2", "Absent", "#fee2e2", "#991b1b", "Active", "#dcfce7", "#166534"),
        ("hblCDA", "Absent", "#f1f5f9", "#64748b", "Absent", "#f1f5f9", "#64748b"),
    ]

    # Assembly row headers (cleanly separated left species name and right accession)
    assemblies = [
        {
            "name": "B. pacificus anQ-h4",
            "acc": "GCF_020861345.1",
            "runs": "Implied by bpac KEGG | Benchmark, Codex, Antigravity",
            "y_box": 0.46,
            "h_box": 0.37,
            "bg": "#f8fafc",
            "edge": "#cbd5e1",
            "row_idx": 0,
        },
        {
            "name": "B. cereus ATCC 10987",
            "acc": "GCF_000008005.1 / GCA_000008005.1",
            "runs": "Sequenced strain | Claude Code, Codex (ATCC 10987)",
            "y_box": 0.02,
            "h_box": 0.37,
            "bg": "#f0fdf4",
            "edge": "#86efac",
            "row_idx": 1,
        },
    ]

    for asm in assemblies:
        y0 = asm["y_box"]
        h0 = asm["h_box"]
        card = patches.FancyBboxPatch(
            (0.0, y0),
            1.0,
            h0,
            boxstyle="round,pad=0.008,rounding_size=0.03",
            facecolor=asm["bg"],
            edgecolor=asm["edge"],
            linewidth=0.8,
        )
        ax_mat.add_patch(card)

        # Header line inside card (generous whitespace between left title and right accession)
        ax_mat.text(
            0.025,
            y0 + h0 - 0.072,
            asm["name"],
            fontsize=6.1,
            fontweight="bold",
            style="italic",
            color="#0f172a",
            va="center",
            ha="left",
        )
        ax_mat.text(
            0.975,
            y0 + h0 - 0.072,
            asm["acc"],
            fontsize=4.9,
            color="#475569",
            va="center",
            ha="right",
            family="monospace",
        )
        ax_mat.text(
            0.025,
            y0 + h0 - 0.155,
            asm["runs"],
            fontsize=5.75,
            color="#334155",
            va="center",
            ha="left",
        )

        # 6 locus status pills across bottom of card
        n_loci = len(loci_cols)
        cell_w = 0.95 / n_loci
        for c_i, (loc_name, st1, bg1, fg1, st2, bg2, fg2) in enumerate(loci_cols):
            cx = 0.025 + c_i * cell_w + cell_w / 2
            st = st1 if asm["row_idx"] == 0 else st2
            p_bg = bg1 if asm["row_idx"] == 0 else bg2
            p_fg = fg1 if asm["row_idx"] == 0 else fg2

            # Locus label
            ax_mat.text(
                cx,
                y0 + 0.135,
                loc_name,
                fontsize=5.8,
                fontweight="bold",
                style="italic",
                color="#1e293b",
                va="center",
                ha="center",
            )
            # Status pill
            pill = patches.FancyBboxPatch(
                (cx - cell_w * 0.44, y0 + 0.025),
                cell_w * 0.88,
                0.072,
                boxstyle="round,pad=0.004,rounding_size=0.02",
                facecolor=p_bg,
                edgecolor=p_fg if loc_name == "cytK2" else "none",
                linewidth=0.6 if loc_name == "cytK2" else 0.0,
            )
            ax_mat.add_patch(pill)
            ax_mat.text(
                cx,
                y0 + 0.061,
                st,
                fontsize=5.4,
                fontweight="bold",
                color=p_fg,
                va="center",
                ha="center",
            )

    # =========================================================================
    # SHARED UNIFIED LEGEND AT BOTTOM
    # =========================================================================
    leg_handles = []
    leg_labels = []
    for m in models:
        h = mpl.lines.Line2D(
            [0],
            [0],
            color=m["color"],
            marker=m["marker"],
            markersize=5.2,
            lw=1.45,
            markeredgecolor="#0f172a",
            markeredgewidth=0.55,
        )
        leg_handles.append(h)
        leg_labels.append(m["short"])

    fig.legend(
        leg_handles,
        leg_labels,
        loc="lower center",
        bbox_to_anchor=(0.50, 0.008),
        ncol=5,
        fontsize=5.7,
        frameon=True,
        facecolor="#f8fafc",
        edgecolor="#cbd5e1",
        handlelength=1.5,
        handletextpad=0.38,
        columnspacing=0.80,
    )

    output_pdf = base_dir / "figure2_agent_execution.pdf"
    output_png = base_dir / "figure2_agent_execution.png"
    plt.savefig(output_pdf, bbox_inches="tight", pad_inches=0.04)
    plt.savefig(output_png, bbox_inches="tight", pad_inches=0.04, dpi=300)
    plt.close()
    print(f"Generated: {output_pdf}")
    print(f"Generated: {output_png}")


if __name__ == "__main__":
    make_figure()
