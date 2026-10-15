#!/usr/bin/env python3
"""
Generate Figure 5 (figure2_spatial_comparison.{pdf,png}) exclusively from
tracked in-repo data and image assets under manuscript/figures/data/spatial/.
"""
import json
from pathlib import Path

import matplotlib.image as mpimg
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


def main() -> None:
    galaxy_img_path = DATA_DIR / "galaxy_smoke_pi_width.png"
    paper_img_path = DATA_DIR / "Fig5_ESM.jpg"
    galaxy_summary_path = DATA_DIR / "galaxy_smoke_summary.json"
    local_summary_path = DATA_DIR / "smoke_acta2_sklearn15_summary.json"
    full_summary_path = DATA_DIR / "full_dataset15_galaxy_summary.json"

    with open(galaxy_summary_path) as f:
        gal = json.load(f)
    with open(local_summary_path) as f:
        loc = json.load(f)
    with open(full_summary_path) as f:
        full = json.load(f)

    img_gal = mpimg.imread(galaxy_img_path)

    img_pap_full = Image.open(paper_img_path)
    w, h = img_pap_full.size
    # Clean crop around Extended Data Fig. 1c (SpatialDM Acta2 prediction interval width panel)
    crop_box = (int(w * 0.575), int(h * 0.325), int(w * 0.998), int(h * 0.72))
    img_pap_cropped = np.array(img_pap_full.crop(crop_box))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.0, 6.2), dpi=300)
    fig.patch.set_facecolor("white")

    ax1.imshow(img_gal)
    ax1.set_title(
        "A  Orbit Galaxy UDT Execution (1,000-cell tutorial subset)",
        fontsize=11.5,
        fontweight="bold",
        pad=10,
        loc="left",
        color="#1a1a1a",
    )
    ax1.axis("off")

    ax2.imshow(img_pap_cropped)
    ax2.set_title(
        "B  Published Paper2Agent Benchmark (Miao et al. Extended Data Fig. 1c)",
        fontsize=11.5,
        fontweight="bold",
        pad=10,
        loc="left",
        color="#1a1a1a",
    )
    ax2.axis("off")

    gal_cov = gal["empirical_coverage"] * 100.0
    loc_cov = loc["empirical_coverage"] * 100.0
    gal_mean = gal["mean_pi_width_log1p"]
    loc_mean = loc["mean_pi_width_log1p"]
    full_cov = full["empirical_coverage"] * 100.0
    full_mean = full["mean_pi_width_log1p"]
    full_r = full["pearson_r"]
    full_n = full["num_cells"]

    metrics_text = (
        f"Quantitative Verification & Calibration Provenance (Target gene: Acta2, 77% nominal conformal level, α = 0.23):\n"
        f"• Calibration gene filter: 31 calibration genes after 1% minimum expression filter (drops Flt1; 32 unfiltered)\n"
        f"• Tutorial Subset (1,000 cells, 33 genes): Galaxy UDT coverage = {gal_cov:.2f}% vs. {loc_cov:.2f}% local reference  |  "
        f"Mean log(1 + PI width) = {gal_mean:.4f} (Galaxy) vs. {loc_mean:.4f} (local)\n"
        f"• Numerical Reproducibility: Identical cross-platform splits yield $\\Delta_{{\\mathrm{{max}}}} < 10^{{-15}}$ ($r = 1.0000$); "
        f"full Dataset 15 ({full_n:,} cells) achieves {full_cov:.2f}% coverage, mean width {full_mean:.4f}, $r = {full_r:.4f}$"
    )

    fig.text(
        0.5,
        0.025,
        metrics_text,
        ha="center",
        va="bottom",
        fontsize=9.2,
        color="#1f2937",
        linespacing=1.4,
        bbox=dict(
            boxstyle="round,pad=0.55",
            facecolor="#f8fafc",
            edgecolor="#cbd5e1",
            linewidth=1.0,
        ),
    )

    plt.tight_layout(rect=[0, 0.16, 1, 0.98])

    out_pdf = HERE / "figure2_spatial_comparison.pdf"
    out_png = HERE / "figure2_spatial_comparison.png"
    plt.savefig(out_pdf, dpi=300, bbox_inches="tight")
    plt.savefig(out_png, dpi=300, bbox_inches="tight")
    print(f"Saved {out_pdf} and {out_png}")


if __name__ == "__main__":
    main()
