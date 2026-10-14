#!/usr/bin/env python3
"""
Generate Figure 4: Progression of Autonomous Paper Replication on Galaxy Cyberinfrastructure.
Four-panel progression:
- a: Initial Workflow Construction & Canvas Type Enforcement (native_editor_orange_mismatch.png)
- b: Autonomous Triage to Validated Galaxy Workflow (native_editor_validated.png)
- c: Supercomputing Execution & History Provenance (native_history_view.png)
- d: 100% Biological Replication of Published Benchmark (comparison_figure.png)
"""

import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from PIL import Image
import matplotlib as mpl

mpl.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]
mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["figure.dpi"] = 300
mpl.rcParams["savefig.dpi"] = 300
mpl.rcParams["pdf.fonttype"] = 42

def draw_pill(ax, x, y, w, h, text, bg="#FFFFFF", border="#CBD5E1", text_color="#0F172A", fontsize=7.2):
    """Draw a compact label badge pill."""
    patch = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.004,rounding_size=0.03",
                           facecolor=bg, edgecolor=border, linewidth=1.0, zorder=6)
    ax.add_patch(patch)
    ax.text(x + w/2.0, y + h/2.0, text, fontsize=fontsize, fontweight="bold", color=text_color,
            va="center", ha="center", zorder=7)

def build_replication_figure():
    fig_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(fig_dir, "../.."))
    run_dir = os.path.join(repo_root, "bacillus-rnaseq-run")
    
    img_a_path = os.path.join(run_dir, "real_captures/native_editor_orange_mismatch.png")
    img_b_path = os.path.join(run_dir, "real_captures/native_editor_validated.png")
    img_c_path = os.path.join(run_dir, "real_captures/native_history_view.png")
    img_d_path = os.path.join(run_dir, "comparison_figure.png")

    img_a = Image.open(img_a_path)
    img_b = Image.open(img_b_path)
    img_c = Image.open(img_c_path)
    img_d = Image.open(img_d_path)

    # 16.0 x 10.4 inches: high-resolution two-row grid
    fig, ax = plt.subplots(figsize=(16.0, 10.4))
    ax.set_xlim(0.0, 16.0)
    ax.set_ylim(0.0, 10.4)
    ax.axis("off")

    # Layout coordinates
    col_w = 7.42
    row_h = 4.65
    x_left = 0.40
    x_right = 8.18
    y_top = 5.35
    y_bottom = 0.35

    # =========================================================
    # Panel a: Initial Workflow Construction & Type Mismatch
    # =========================================================
    p_a = FancyBboxPatch((x_left, y_top), col_w, row_h, boxstyle="round,pad=0.01,rounding_size=0.05",
                         facecolor="#FFFBEB", edgecolor="#FDE68A", linewidth=1.2, zorder=2)
    ax.add_patch(p_a)

    h_a = FancyBboxPatch((x_left + 0.08, y_top + row_h - 0.38), col_w - 0.16, 0.32,
                         boxstyle="round,pad=0.01,rounding_size=0.03",
                         facecolor="#FEF3C7", edgecolor="#F59E0B", linewidth=0.9, zorder=3)
    ax.add_patch(h_a)
    ax.text(x_left + 0.20, y_top + row_h - 0.22, "a", fontsize=12.5, fontweight="bold", color="#78350F", va="center", zorder=4)
    ax.text(x_left + 0.52, y_top + row_h - 0.22, "Workflow Construction & Canvas Type Enforcement",
            fontsize=9.5, fontweight="bold", color="#92400E", va="center", zorder=4)
    draw_pill(ax, x_left + col_w - 2.50, y_top + row_h - 0.34, 2.35, 0.24,
              "Type Mismatch: Collection Input", bg="#FEF3C7", border="#D97706", text_color="#B45309", fontsize=6.8)

    # Image A
    ax.imshow(img_a, extent=[x_left + 0.08, x_left + col_w - 0.08, y_top + 0.08, y_top + row_h - 0.44],
              aspect='auto', zorder=3)

    # =========================================================
    # Panel b: Autonomous Triage to Validated Workflow
    # =========================================================
    p_b = FancyBboxPatch((x_right, y_top), col_w, row_h, boxstyle="round,pad=0.01,rounding_size=0.05",
                         facecolor="#F0FDF4", edgecolor="#BBF7D0", linewidth=1.2, zorder=2)
    ax.add_patch(p_b)

    h_b = FancyBboxPatch((x_right + 0.08, y_top + row_h - 0.38), col_w - 0.16, 0.32,
                         boxstyle="round,pad=0.01,rounding_size=0.03",
                         facecolor="#DCFCE7", edgecolor="#22C55E", linewidth=0.9, zorder=3)
    ax.add_patch(h_b)
    ax.text(x_right + 0.20, y_top + row_h - 0.22, "b", fontsize=12.5, fontweight="bold", color="#064E3B", va="center", zorder=4)
    ax.text(x_right + 0.52, y_top + row_h - 0.22, "Autonomous Triage to Validated Workflow (ea7670a8)",
            fontsize=9.5, fontweight="bold", color="#166534", va="center", zorder=4)
    draw_pill(ax, x_right + col_w - 2.55, y_top + row_h - 0.34, 2.40, 0.24,
              "Integrated tximport: Validated", bg="#DCFCE7", border="#16A34A", text_color="#15803D", fontsize=6.8)

    # Image B
    ax.imshow(img_b, extent=[x_right + 0.08, x_right + col_w - 0.08, y_top + 0.08, y_top + row_h - 0.44],
              aspect='auto', zorder=3)

    # =========================================================
    # Panel c: Supercomputing Execution & History Provenance
    # =========================================================
    p_c = FancyBboxPatch((x_left, y_bottom), col_w, row_h, boxstyle="round,pad=0.01,rounding_size=0.05",
                         facecolor="#F0F9FF", edgecolor="#BAE6FD", linewidth=1.2, zorder=2)
    ax.add_patch(p_c)

    h_c = FancyBboxPatch((x_left + 0.08, y_bottom + row_h - 0.38), col_w - 0.16, 0.32,
                         boxstyle="round,pad=0.01,rounding_size=0.03",
                         facecolor="#E0F2FE", edgecolor="#0284C7", linewidth=0.9, zorder=3)
    ax.add_patch(h_c)
    ax.text(x_left + 0.20, y_bottom + row_h - 0.22, "c", fontsize=12.5, fontweight="bold", color="#0C4A6E", va="center", zorder=4)
    ax.text(x_left + 0.52, y_bottom + row_h - 0.22, "Supercomputing Execution & Living History (bbd44e69)",
            fontsize=9.5, fontweight="bold", color="#0369A1", va="center", zorder=4)
    draw_pill(ax, x_left + col_w - 2.50, y_bottom + row_h - 0.34, 2.35, 0.24,
              "UseGalaxy.org | Zero Host Disk Used", bg="#E0F2FE", border="#0284C7", text_color="#0369A1", fontsize=6.8)

    # Image C
    ax.imshow(img_c, extent=[x_left + 0.08, x_left + col_w - 0.08, y_bottom + 0.08, y_bottom + row_h - 0.44],
              aspect='auto', zorder=3)

    # =========================================================
    # Panel d: Biological Replication of Published Benchmark
    # =========================================================
    p_d = FancyBboxPatch((x_right, y_bottom), col_w, row_h, boxstyle="round,pad=0.01,rounding_size=0.05",
                         facecolor="#FAFAFA", edgecolor="#E2E8F0", linewidth=1.2, zorder=2)
    ax.add_patch(p_d)

    h_d = FancyBboxPatch((x_right + 0.08, y_bottom + row_h - 0.38), col_w - 0.16, 0.32,
                         boxstyle="round,pad=0.01,rounding_size=0.03",
                         facecolor="#F1F5F9", edgecolor="#64748B", linewidth=0.9, zorder=3)
    ax.add_patch(h_d)
    ax.text(x_right + 0.20, y_bottom + row_h - 0.22, "d", fontsize=12.5, fontweight="bold", color="#0F172A", va="center", zorder=4)
    ax.text(x_right + 0.52, y_bottom + row_h - 0.22, "Biological Replication of Published Study (Sci Rep 2025, Fig 4)",
            fontsize=9.5, fontweight="bold", color="#1E293B", va="center", zorder=4)
    draw_pill(ax, x_right + col_w - 2.65, y_bottom + row_h - 0.34, 2.50, 0.24,
              "Pearson r = 0.9622 across 5,472 Genes", bg="#F1F5F9", border="#475569", text_color="#334155", fontsize=6.8)

    # Image D
    ax.imshow(img_d, extent=[x_right + 0.08, x_right + col_w - 0.08, y_bottom + 0.08, y_bottom + row_h - 0.44],
              aspect='auto', zorder=3)

    # Connecting horizontal arrow between a and b
    ax.annotate("", xy=(8.16, y_top + row_h/2.0), xytext=(7.84, y_top + row_h/2.0),
                arrowprops=dict(arrowstyle="-|>", color="#059669", lw=2.2, mutation_scale=13), zorder=5)

    # Save PDF and PNG
    out_pdf = os.path.join(fig_dir, "figure_bacillus_replication.pdf")
    out_png = os.path.join(fig_dir, "figure_bacillus_replication.png")
    plt.tight_layout()
    plt.savefig(out_pdf, bbox_inches='tight', dpi=300)
    plt.savefig(out_png, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Generated {out_pdf} and {out_png} successfully!")

if __name__ == "__main__":
    build_replication_figure()
