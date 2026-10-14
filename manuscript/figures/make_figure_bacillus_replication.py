#!/usr/bin/env python3
"""
Generate Figure 4: Progression of Autonomous Paper Replication on Galaxy Cyberinfrastructure.
Four-panel layout with clean A, B, C, D panel labels only (all explanations in the figure legend):
- A: Initial workflow construction in Galaxy editor (native_editor_orange_mismatch.png)
- B: Validated Galaxy workflow with transcript-to-gene lookup (native_editor_validated.png)
- C: Galaxy History Notebook rendering and living history (history_notebook_screenshot.png)
- D: Biological replication and whole-transcriptome concordance (comparison_figure.png)
"""

import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image
import matplotlib as mpl

mpl.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]
mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["figure.dpi"] = 300
mpl.rcParams["savefig.dpi"] = 300
mpl.rcParams["pdf.fonttype"] = 42

def build_replication_figure():
    fig_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(fig_dir, "../.."))
    run_dir = os.path.join(repo_root, "bacillus-rnaseq-run")

    img_a_path = os.path.join(run_dir, "real_captures/native_editor_orange_mismatch.png")
    img_b_path = os.path.join(run_dir, "real_captures/native_editor_validated.png")
    img_c_path = os.path.join(run_dir, "history_notebook_screenshot.png")
    img_d_path = os.path.join(run_dir, "comparison_figure.png")

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
        ax.text(x, y + row_h + 0.08, label, fontsize=15, fontweight="bold",
                color="#0F172A", va="bottom", ha="left", zorder=5)
        # Display panel image
        ax.imshow(img, extent=[x, x + col_w, y, y + row_h], aspect="auto", zorder=3)
        # Subtle 0.8pt neutral border around the panel edge
        border = Rectangle((x, y), col_w, row_h, fill=False,
                           edgecolor="#CBD5E1", linewidth=0.8, zorder=4)
        ax.add_patch(border)

    out_pdf = os.path.join(fig_dir, "figure_bacillus_replication.pdf")
    out_png = os.path.join(fig_dir, "figure_bacillus_replication.png")
    plt.tight_layout()
    plt.savefig(out_pdf, bbox_inches="tight", dpi=300)
    plt.savefig(out_png, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Generated {out_pdf} and {out_png} successfully!")

if __name__ == "__main__":
    build_replication_figure()
