#!/usr/bin/env python3
"""
Generate Figure 6 (figure_brc_reproductions.{pdf,png}) directly from tracked
in-repo data files under manuscript/figures/data/brc/ at publication width (7.5 in).

Panel A: Hokken et al. (2018) A. fumigatus itraconazole time-course RNA-seq
         reproduction across all 4 post-exposure timepoints (t30, t60, t120, t240).
Panel B: Ruiz et al. (2021) A. gambiae ATAC-seq chromatin accessibility
         reproduction comparing published Table S3 against unfitted 51% reciprocal
         overlap and post-hoc fitted either_frac = 0.851 across Midguts and Salivary Glands.
"""
from pathlib import Path

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["axes.edgecolor"] = "#334155"
plt.rcParams["axes.linewidth"] = 0.8
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE / "data" / "brc"


def main() -> None:
    hokken_df = pd.read_csv(DATA_DIR / "hokken_deseq2_vs_published_degs.tsv", sep="\t")
    ruiz_df = pd.read_csv(DATA_DIR / "ruiz_atacseq_track_comparison.tsv", sep="\t")
    recov_df = pd.read_csv(DATA_DIR / "ruiz_coordinate_recovery_vs_excel.tsv", sep="\t")

    fig = plt.figure(figsize=(7.5, 6.7), dpi=300)
    fig.patch.set_facecolor("white")

    outer = gridspec.GridSpec(
        2, 1, height_ratios=[1.0, 1.48], hspace=0.62
    )

    # =========================================================================
    # PANEL A: Hokken et al. (4 timepoints: t30, t60, t120, t240)
    # =========================================================================
    gs_a = gridspec.GridSpecFromSubplotSpec(1, 4, subplot_spec=outer[0], wspace=0.22)

    timepoints = [
        ("t30", "30 min vs. 0 min", 3922),
        ("t60", "60 min vs. 0 min", 3393),
        ("t120", "120 min vs. 0 min", 1191),
        ("t240", "240 min vs. 0 min", 1098),
    ]

    for idx, (tp, title_str, total_called) in enumerate(timepoints):
        ax = fig.add_subplot(gs_a[idx])
        sub = hokken_df[hokken_df["timepoint"] == tp]
        x = sub["log2FoldChange_paper"].values
        y = sub["log2FoldChange_ours"].values
        n = len(sub)

        r = float(np.corrcoef(x, y)[0, 1])
        slope, _ = np.polyfit(x, y, 1)

        up = y >= 1.0
        down = ~up

        ax.plot([-7.5, 10.5], [-7.5, 10.5], ls="--", lw=0.8, color="#64748b", zorder=1)
        ax.axhline(0, lw=0.5, color="#cbd5e1", zorder=0)
        ax.axvline(0, lw=0.5, color="#cbd5e1", zorder=0)

        ax.scatter(
            x[down],
            y[down],
            s=4.5,
            alpha=0.45,
            color="#2563eb",
            edgecolors="none",
            rasterized=True,
            zorder=2,
        )
        ax.scatter(
            x[up],
            y[up],
            s=4.5,
            alpha=0.45,
            color="#dc2626",
            edgecolors="none",
            rasterized=True,
            zorder=2,
        )

        ax.set_xlim(-7.5, 10.5)
        ax.set_ylim(-7.5, 10.5)
        ax.set_xticks([-5, 0, 5, 10])
        ax.set_yticks([-5, 0, 5, 10])
        ax.tick_params(labelsize=7.5, pad=2)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_title(title_str, fontsize=8.5, fontweight="bold", pad=5, color="#0f172a")

        n_str = f"n = {n:,}/{total_called:,}" if n != total_called else f"n = {n:,}"
        stats_box = f"r = {r:.4f}\nslope = {slope:.3f}\n{n_str}"
        ax.text(
            0.05,
            0.95,
            stats_box,
            transform=ax.transAxes,
            fontsize=6.8,
            va="top",
            ha="left",
            color="#0f172a",
            linespacing=1.22,
            bbox=dict(
                boxstyle="round,pad=0.25",
                facecolor="white",
                edgecolor="#cbd5e1",
                alpha=0.92,
                lw=0.6,
            ),
        )

        ax.set_xlabel("Published $\\log_2$FC", fontsize=8.0, labelpad=3)
        if idx == 0:
            ax.set_ylabel("Orbit Galaxy $\\log_2$FC", fontsize=8.2, fontweight="bold", labelpad=3)
        else:
            ax.set_yticklabels([])

    fig.text(
        0.01,
        0.965,
        "A  A. fumigatus Itraconazole Time-Course RNA-seq (Hokken et al., 30-Sample Pooled DESeq2 Model)",
        fontsize=9.5,
        fontweight="bold",
        color="#0f172a",
        ha="left",
        va="top",
    )

    # =========================================================================
    # PANEL B: Ruiz et al. (Horizontal Grouped Bars for Zero Label Collision)
    # =========================================================================
    gs_b = gridspec.GridSpecFromSubplotSpec(1, 2, subplot_spec=outer[1], wspace=0.14)

    fig.text(
        0.01,
        0.562,
        "B  A. gambiae ATAC-seq Chromatin Accessibility (Ruiz et al., Unfitted 51% Reciprocal vs. Post-Hoc Fitted Rules)",
        fontsize=9.5,
        fontweight="bold",
        color="#0f172a",
        ha="left",
        va="top",
    )

    metrics = [
        ("total_regions", "Total\nRegions"),
        ("enhancers", "Candidate\nEnhancers"),
        ("promoters", "Promoters\n(≤1 kb)"),
        ("unique_genes", "Assigned\nGenes"),
    ]
    series_cfg = [
        ("canonical_ruiz_excel", "Published (Ruiz Table S3)", "#1e293b", None),
        ("unfitted_macs212_recip0.51", "Unfitted 51% Recip. (MACS2 2.1.2)", "#0284c7", None),
        ("fitted_macs212_either0.851", "Post-Hoc Fitted either_frac = 0.851", "#d97706", "///"),
    ]

    tissues = [
        ("Midguts", "Midguts (I1,I2 Shared Peak Rows)", 72000),
        ("Salivary glands", "Salivary Glands (I1,I2 Shared Peak Rows)", 110000),
    ]

    for t_idx, (tissue_key, tissue_title, xmax) in enumerate(tissues):
        ax = fig.add_subplot(gs_b[t_idx])
        t_sub = ruiz_df[ruiz_df["tissue"] == tissue_key].set_index("track_id")
        m211_row = t_sub.loc["unfitted_macs211_recip0.51"]
        pub_row = t_sub.loc["canonical_ruiz_excel"]

        y_pos = np.arange(len(metrics))
        height = 0.255

        for s_idx, (track_id, s_label, color, hatch) in enumerate(series_cfg):
            row = t_sub.loc[track_id]
            vals = [float(row[m_col]) for m_col, _ in metrics]
            offsets = y_pos + (s_idx - 1) * height

            bars = ax.barh(
                offsets,
                vals,
                height=height * 0.88,
                label=s_label if t_idx == 0 else None,
                color=color,
                edgecolor="#0f172a" if hatch else "none",
                linewidth=0.5 if hatch else 0,
                hatch=hatch,
                alpha=0.92,
                zorder=3,
            )

            for m_idx, (bar, val) in enumerate(zip(bars, vals)):
                pub_val = float(pub_row[metrics[m_idx][0]])
                if track_id == "canonical_ruiz_excel":
                    lbl = f"{int(val):,}"
                else:
                    pct = (val - pub_val) / pub_val * 100.0
                    sign = "+" if pct >= 0 else ""
                    lbl = f"{int(val):,} ({sign}{pct:.1f}%)"

                ax.text(
                    bar.get_width() + xmax * 0.012,
                    bar.get_y() + bar.get_height() / 2.0,
                    lbl,
                    ha="left",
                    va="center",
                    fontsize=6.5,
                    fontweight="bold" if m_idx == 0 else "normal",
                    color="#0f172a",
                )

        ax.set_yticks(y_pos)
        if t_idx == 0:
            ax.set_yticklabels([m_lbl for _, m_lbl in metrics], fontsize=7.8, fontweight="bold")
        else:
            ax.set_yticklabels([])
        ax.invert_yaxis()
        ax.set_xlim(0, xmax)
        ax.xaxis.set_major_formatter(
            plt.FuncFormatter(lambda v, _: f"{int(v/1000)}k" if v > 0 else "0")
        )
        ax.tick_params(axis="x", labelsize=7.5, pad=2)
        ax.grid(axis="x", ls="--", lw=0.6, alpha=0.5, color="#cbd5e1", zorder=0)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_title(tissue_title, fontsize=8.5, fontweight="bold", pad=7, color="#0f172a")
        ax.set_xlabel("Count (Regions or Assigned Genes)", fontsize=8.0, labelpad=3)

        rec_rows = recov_df[recov_df["tissue"] == tissue_key]
        rec_min = rec_rows["pct_excel_I1I2_hit"].min()
        rec_max = rec_rows["pct_excel_I1I2_hit"].max()
        m211_reg = int(m211_row["total_regions"])
        m211_pct = (
            (m211_reg - float(pub_row["total_regions"]))
            / float(pub_row["total_regions"])
            * 100.0
        )

        prov_text = (
            f"Unfitted coordinate recovery: {rec_min:.1f}–{rec_max:.1f}%\n"
            f"MACS2 2.1.1 wrapper (51%): {m211_reg:,} ({m211_pct:.1f}%)"
        )
        ax.text(
            0.985,
            0.03,
            prov_text,
            transform=ax.transAxes,
            fontsize=6.1,
            va="bottom",
            ha="right",
            color="#1e293b",
            linespacing=1.2,
            bbox=dict(
                boxstyle="round,pad=0.25",
                facecolor="#f8fafc",
                edgecolor="#cbd5e1",
                lw=0.6,
            ),
            zorder=5,
        )

    handles, labels = fig.axes[4].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.51, 0.530),
        ncol=3,
        frameon=True,
        facecolor="#f8fafc",
        edgecolor="#cbd5e1",
        fontsize=7.2,
        handlelength=1.4,
        columnspacing=1.1,
    )

    fig.subplots_adjust(left=0.11, right=0.98, top=0.90, bottom=0.07)

    out_pdf = HERE / "figure_brc_reproductions.pdf"
    out_png = HERE / "figure_brc_reproductions.png"
    plt.savefig(out_pdf, dpi=300, bbox_inches="tight")
    plt.savefig(out_png, dpi=300, bbox_inches="tight")
    print(f"Saved {out_pdf} and {out_png}")


if __name__ == "__main__":
    main()
