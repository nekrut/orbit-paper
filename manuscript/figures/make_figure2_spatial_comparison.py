#!/usr/bin/env python3
"""
Generate Figure 2 (figure2_spatial_comparison.{pdf,png}) exclusively from
tracked in-repo data and image assets under manuscript/figures/data/spatial/.

Compares Paper2Agent Extended Data Fig. 1c (run on the 1,000-cell tutorial
subset, 96 KB, r = 0.0861) against the full 5,613-cell Zenodo Dataset 15
reference archive cited in Data Availability (405 MB, r = 0.2553).
"""
import csv
import json
from pathlib import Path

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["axes.edgecolor"] = "#333333"
plt.rcParams["axes.linewidth"] = 0.8
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE / "data" / "spatial"


def load_per_cell(csv_path: Path):
    xs, ys, actual, pred, pi_log = [], [], [], [], []
    with open(csv_path, newline="") as f:
        for row in csv.DictReader(f):
            xs.append(float(row["x_coord"]))
            ys.append(float(row["y_coord"]))
            actual.append(float(row["actual_expression"]))
            pred.append(float(row["predicted_expression"]))
            pi_log.append(float(row["pi_width_log1p"]))
    return (
        np.array(xs),
        np.array(ys),
        np.array(actual),
        np.array(pred),
        np.array(pi_log),
    )


def load_cv_metrics(csv_path: Path) -> dict[str, float]:
    out = {}
    with open(csv_path, newline="") as f:
        for row in csv.DictReader(f):
            out[row["gene"]] = float(row["pearson_r"])
    return out


def plot_spatial_panel(
    ax,
    fig,
    x: np.ndarray,
    y: np.ndarray,
    vals: np.ndarray,
    title: str,
    subtitle: str,
    cbar_label: str | None = None,
    title_color: str = "#111827",
    clip_p95: bool = True,
):
    v = vals.copy()
    if clip_p95:
        p95 = np.percentile(v, 95)
        v[v > p95] = p95
    im = ax.scatter(
        x,
        y,
        s=2.2,
        c=v,
        cmap="viridis",
        rasterized=True,
        edgecolors="none",
    )
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")
    ax.set_title(
        title,
        fontsize=10.5,
        fontweight="bold",
        loc="left",
        pad=16,
        color=title_color,
    )
    ax.text(
        0.0,
        1.015,
        subtitle,
        transform=ax.transAxes,
        fontsize=8.5,
        color="#4b5563",
        ha="left",
        va="bottom",
    )
    cbar = fig.colorbar(im, ax=ax, fraction=0.042, pad=0.015, shrink=0.82)
    cbar.ax.tick_params(labelsize=7.8)
    if cbar_label:
        cbar.set_label(cbar_label, fontsize=8.0, rotation=270, labelpad=11)


def main() -> None:
    paper_img_path = DATA_DIR / "Fig5_ESM.jpg"
    tut_csv = DATA_DIR / "galaxy_smoke_per_cell_results.csv"
    full_csv = DATA_DIR / "full_dataset15_galaxy_per_cell_results.csv"
    tut_cv_csv = DATA_DIR / "tutorial_cv_eval_per_gene_metrics.csv"
    full_cv_csv = DATA_DIR / "full_dataset15_cv_eval_per_gene_metrics.csv"

    with open(DATA_DIR / "galaxy_smoke_summary.json") as f:
        gal_tut = json.load(f)
    with open(DATA_DIR / "full_dataset15_galaxy_summary.json") as f:
        gal_full = json.load(f)

    x_t, y_t, act_t, pred_t, pi_t = load_per_cell(tut_csv)
    x_f, y_f, act_f, pred_f, pi_f = load_per_cell(full_csv)
    cv_tut = load_cv_metrics(tut_cv_csv)
    cv_full = load_cv_metrics(full_cv_csv)

    img_pap_full = Image.open(paper_img_path)
    w, h = img_pap_full.size
    crop_box = (int(w * 0.575), int(h * 0.325), int(w * 0.998), int(h * 0.72))
    img_pap_cropped = np.array(img_pap_full.crop(crop_box))

    fig = plt.figure(figsize=(16.0, 9.2), dpi=300, facecolor="white")
    outer_gs = gridspec.GridSpec(
        2,
        1,
        figure=fig,
        height_ratios=[1.05, 1.0],
        hspace=0.28,
    )

    # =========================================================================
    # ROW 1: Published Paper2Agent vs 1,000-cell Unit-Test vs 5,613-cell Full
    # =========================================================================
    gs_top = gridspec.GridSpecFromSubplotSpec(
        1, 3, subplot_spec=outer_gs[0], width_ratios=[1.05, 1.0, 1.0], wspace=0.18
    )

    axA = fig.add_subplot(gs_top[0, 0])
    axA.imshow(img_pap_cropped)
    axA.axis("off")
    axA.set_title(
        "A  Published Paper2Agent Example",
        fontsize=10.5,
        fontweight="bold",
        loc="left",
        pad=16,
        color="#991b1b",
    )
    axA.text(
        0.0,
        1.015,
        "Miao et al. Ext. Data Fig. 1c (colorbar cap = 2.36)",
        transform=axA.transAxes,
        fontsize=8.5,
        color="#4b5563",
        ha="left",
        va="bottom",
    )

    axB = fig.add_subplot(gs_top[0, 1])
    plot_spatial_panel(
        axB,
        fig,
        x_t,
        y_t,
        pi_t,
        title="B  PI Width: 1,000-Cell Tutorial Subset",
        subtitle=f"96 KB tutorial subset (1,000 × 33) • P95 = {gal_tut['p95_pi_width_log1p']:.2f}, Cov = {gal_tut['empirical_coverage']*100:.1f}%",
        cbar_label="log(1 + PI Width)",
        title_color="#991b1b",
    )

    axC = fig.add_subplot(gs_top[0, 2])
    plot_spatial_panel(
        axC,
        fig,
        x_f,
        y_f,
        pi_f,
        title="C  PI Width: Cited 5,613-Cell Reference",
        subtitle=f"405 MB Dataset 15 (5,613 × 30,527) • P95 = {gal_full['p95_pi_width_log1p']:.2f}, Cov = {gal_full['empirical_coverage']*100:.1f}%",
        cbar_label="log(1 + PI Width)",
        title_color="#065f46",
    )

    # =========================================================================
    # ROW 2: Ground Truth vs Wrong-Dataset Imputation vs Full Imputation + 33-Gene CV
    # =========================================================================
    gs_bot = gridspec.GridSpecFromSubplotSpec(
        1,
        5,
        subplot_spec=outer_gs[1],
        width_ratios=[1.0, 1.0, 1.0, 0.16, 1.12],
        wspace=0.14,
    )

    axD = fig.add_subplot(gs_bot[0, 0])
    plot_spatial_panel(
        axD,
        fig,
        x_f,
        y_f,
        np.log1p(np.maximum(0, act_f)),
        title="D  Measured Acta2 (osmFISH)",
        subtitle="Held-out ground truth (3,405 spatial cells)",
        cbar_label=None,
        title_color="#1f2937",
    )

    axE = fig.add_subplot(gs_bot[0, 1])
    plot_spatial_panel(
        axE,
        fig,
        x_t,
        y_t,
        np.log1p(np.maximum(0, pred_t)),
        title="E  Imputed: 1,000-Cell Tutorial Subset",
        subtitle=f"Tutorial subset (1,000 / 5,613 cells) • r = {gal_tut['pearson_r']:.4f}",
        cbar_label=None,
        title_color="#991b1b",
    )

    axF = fig.add_subplot(gs_bot[0, 2])
    plot_spatial_panel(
        axF,
        fig,
        x_f,
        y_f,
        np.log1p(np.maximum(0, pred_f)),
        title="F  Imputed: 5,613-Cell Reference",
        subtitle=f"Full Dataset 15 reference • r = {gal_full['pearson_r']:.4f} (3.0×)",
        cbar_label="log(1 + Expression)",
        title_color="#065f46",
    )

    # Panel G: Dumbbell / delta plot of key cortical markers & 33-gene summary
    axG = fig.add_subplot(gs_bot[0, 4])
    highlight_genes = [
        ("sox10", "Sox10"),
        ("plp1", "Plp1"),
        ("vip", "Vip"),
        ("pthlh", "Pthlh"),
        ("anln", "Anln"),
        ("acta2", "Acta2*"),
        ("gfap", "Gfap"),
        ("lamp5", "Lamp5"),
        ("serpinf1", "Serpinf1"),
        ("kcnip2", "Kcnip2"),
    ]
    y_pos = np.arange(len(highlight_genes))[::-1]
    tut_vals = [cv_tut[g] for g, _ in highlight_genes]
    full_vals = [cv_full[g] for g, _ in highlight_genes]
    labels = [lbl for _, lbl in highlight_genes]

    axG.axvline(0.0, color="#9ca3af", linestyle="--", linewidth=0.8, zorder=1)
    for yi, tv, fv, (gkey, _) in zip(y_pos, tut_vals, full_vals, highlight_genes):
        lw = 2.4 if gkey == "acta2" else 1.6
        col = "#2563eb" if gkey == "acta2" else "#94a3b8"
        axG.plot([tv, fv], [yi, yi], color=col, linewidth=lw, zorder=2)

    axG.scatter(
        tut_vals,
        y_pos,
        color="#dc2626",
        s=38,
        zorder=3,
        label="1,000-cell tutorial subset",
    )
    axG.scatter(
        full_vals,
        y_pos,
        color="#059669",
        s=38,
        zorder=4,
        label="5,613-cell Dataset 15",
    )

    axG.set_yticks(y_pos)
    axG.set_yticklabels(labels, fontsize=8.5, fontstyle="italic")
    for ticklbl, (gkey, _) in zip(axG.get_yticklabels(), highlight_genes):
        if gkey == "acta2":
            ticklbl.set_fontweight("bold")
            ticklbl.set_color("#1e3a8a")

    axG.set_xlabel("10-Fold CV Pearson r", fontsize=8.8)
    axG.set_xlim(-0.20, 0.72)
    axG.tick_params(axis="x", labelsize=8.2)
    axG.spines["top"].set_visible(False)
    axG.spines["right"].set_visible(False)
    axG.grid(axis="x", linestyle=":", alpha=0.5)

    axG.set_title(
        "G  33-Gene Panel Accuracy",
        fontsize=10.5,
        fontweight="bold",
        loc="left",
        pad=16,
        color="#111827",
    )
    axG.text(
        0.0,
        1.015,
        "27/33 genes improve (mean r: 0.18 → 0.27)",
        transform=axG.transAxes,
        fontsize=8.5,
        color="#4b5563",
        ha="left",
        va="bottom",
    )
    axG.legend(
        loc="lower right",
        fontsize=7.8,
        frameon=True,
        facecolor="white",
        edgecolor="#d1d5db",
        handletextpad=0.3,
        borderpad=0.35,
    )

    out_pdf = HERE / "figure2_spatial_comparison.pdf"
    out_png = HERE / "figure2_spatial_comparison.png"
    plt.savefig(out_pdf, dpi=300, bbox_inches="tight")
    plt.savefig(out_png, dpi=300, bbox_inches="tight")
    print(f"Saved {out_pdf} and {out_png}")


if __name__ == "__main__":
    main()
