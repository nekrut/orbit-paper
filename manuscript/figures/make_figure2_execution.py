#!/usr/bin/env python3
"""
Generate publication-grade Figure 2:
Target Enterotoxin Differential Expression (log2FC vs. TSB Control).
Forest plot comparing differential expression effect sizes (log2FC and 95% CIs)
for target enterotoxin genes (nheB, entFM, nheA, nheC) across independent agent
execution environments (Claude Code, OpenAI Codex, Antigravity/Gemini) against
the published benchmark (PMC12804731).
"""

import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

mpl.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]
mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["figure.dpi"] = 300
mpl.rcParams["savefig.dpi"] = 300
mpl.rcParams["pdf.fonttype"] = 42

def make_figure():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    genes = [
        {"name": "nheB (Enterotoxin subunit B)", "key": "nheB", "note": "Primary virulence factor (marked repression in glucose)"},
        {"name": "entFM (Enterotoxin FM)", "key": "entFM", "note": "Cell-wall peptidase (marked induction in glucose)"},
        {"name": "nheA (Enterotoxin subunit A)", "key": "nheA", "note": "Operon subunit (moderate repression in glucose)"},
        {"name": "nheC (Enterotoxin subunit C)", "key": "nheC", "note": "Low basal expression (non-significant shift)"},
    ]

    models = [
        {
            "id": "paper",
            "name": "Published Benchmark (Vyklická et al. 2026)",
            "short": "Published Benchmark",
            "color": "#0f172a",
            "marker": "D",
            "data": {
                "nheB": (-1.98, -2.75, -1.21, "padj = 0.0027", "**"),
                "entFM": (1.13, 0.32, 1.94, "padj = 0.0475", "*"),
                "nheA": (-1.06, -1.95, -0.17, "padj = 0.1407", "n.s."),
                "nheC": (-0.11, -1.15, 0.93, "padj = 0.8772", "n.s."),
            }
        },
        {
            "id": "cc",
            "name": "Anthropic Claude Opus 5.5 (Claude Code)",
            "short": "Claude Code (Opus 5.5)",
            "color": "#2563eb",
            "marker": "s",
            "data": {
                "nheB": (-2.08, -2.86, -1.30, "padj = 0.0002", "***"),
                "entFM": (1.08, 0.25, 1.91, "padj = 0.0620", "trend"),
                "nheA": (-1.23, -2.12, -0.34, "padj = 0.0520", "trend"),
                "nheC": (-0.21, -1.45, 1.03, "padj = 0.8100", "n.s."),
            }
        },
        {
            "id": "codex_paper",
            "name": "OpenAI Codex / GPT-6 (anQ-h4 RefSeq)",
            "short": "Codex (anQ-h4)",
            "color": "#ea580c",
            "marker": "^",
            "data": {
                "nheB": (-2.16, -3.10, -1.22, "padj = 9.3e-5", "***"),
                "entFM": (1.32, 0.45, 2.19, "padj = 0.0145", "*"),
                "nheA": (-1.19, -2.23, -0.16, "padj = 0.0754", "trend"),
                "nheC": (-0.95, -3.20, 1.80, "p = 0.659", "n.s."),
            }
        },
        {
            "id": "codex_atcc",
            "name": "OpenAI Codex / GPT-6 (ATCC 10987 GenBank)",
            "short": "Codex (ATCC 10987)",
            "color": "#c2410c",
            "marker": "v",
            "data": {
                "nheB": (-2.46, -3.50, -1.41, "padj = 5.5e-5", "***"),
                "entFM": (1.35, 0.41, 2.30, "padj = 0.0220", "*"),
                "nheA": (-1.52, -2.65, -0.39, "padj = 0.0331", "*"),
                "nheC": (-0.27, -1.71, 1.17, "padj = 0.8097", "n.s."),
            }
        },
        {
            "id": "agy",
            "name": "Google Gemini 3.8 Flash (Antigravity)",
            "short": "Gemini (Antigravity)",
            "color": "#0d9488",
            "marker": "o",
            "data": {
                "nheB": (-2.41, -3.25, -1.57, "padj = 0.0021", "**"),
                "entFM": (1.42, 0.58, 2.26, "padj = 0.0658", "trend"),
                "nheA": (-1.49, -2.48, -0.50, "padj = 0.1012", "n.s."),
                "nheC": (-0.62, -2.05, 0.81, "padj = 0.5129", "n.s."),
            }
        },
    ]

    fig = plt.figure(figsize=(11.0, 7.2), dpi=300)
    ax = fig.add_axes([0.08, 0.12, 0.84, 0.80])

    y_total_span = 26.0

    for g_idx, g in enumerate(genes):
        gene_key = g["key"]
        group_base = y_total_span - 1.5 - g_idx * 6.2

        # Alternating background shading
        ax.axhspan(group_base - 3.4, group_base + 1.2, facecolor="#f8fafc" if g_idx % 2 == 0 else "#ffffff", zorder=0)

        # Gene header and annotation
        ax.text(-3.85, group_base + 0.6, g["name"], fontsize=10.0, fontweight="bold", color="#0f172a", va="center")
        ax.text(-3.85, group_base - 0.15, g["note"], fontsize=7.8, color="#64748b", va="center", style="italic")

        for m_idx, m in enumerate(models):
            y_pos = group_base - 0.85 - m_idx * 0.52
            lfc, ci_l, ci_h, padj_txt, sig = m["data"][gene_key]

            # 95% Confidence Interval error bar
            ax.plot([ci_l, ci_h], [y_pos, y_pos], color=m["color"], lw=1.8, zorder=3)
            # Central estimate marker
            ax.scatter([lfc], [y_pos], color=m["color"], marker=m["marker"], s=55, zorder=4, edgecolor="#0f172a", linewidth=0.6)

            # Right-aligned effect size and significance callout
            ax.text(2.65, y_pos, f"{lfc:+.2f} ({sig})", fontsize=7.8, color=m["color"],
                    fontweight="bold" if sig in ["*", "**", "***"] else "normal", va="center", ha="left")

    ax.text(2.65, y_total_span - 0.5, "log2FC (sig)", fontsize=8.2, fontweight="bold", color="#475569", va="bottom", ha="left")
    ax.axvline(0, color="#94a3b8", lw=1.2, linestyle="--", zorder=2)
    ax.set_xlim(-4.0, 3.8)
    ax.set_ylim(0.5, y_total_span + 0.5)
    ax.set_xlabel("log2 Fold Change (0.5% Glucose vs. TSB Control)", fontsize=9.5, fontweight="bold", color="#334155")
    ax.set_yticks([])

    ax.grid(axis="x", color="#e2e8f0", linestyle=":", lw=0.8, zorder=1)
    ax.set_axisbelow(True)

    ax.set_title("Target Enterotoxin Differential Expression (log2FC vs. TSB Control)", fontsize=11.5, fontweight="bold", color="#0f172a", pad=14)

    leg_handles = []
    leg_labels = []
    for m in models:
        line = mpl.lines.Line2D([0], [0], color=m["color"], marker=m["marker"], markersize=7, lw=1.8, markeredgecolor="#0f172a", markeredgewidth=0.6)
        leg_handles.append(line)
        leg_labels.append(m["short"])

    ax.legend(leg_handles, leg_labels, loc="lower center", bbox_to_anchor=(0.5, -0.12),
              ncol=5, fontsize=8.2, frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1")

    output_pdf = os.path.join(base_dir, "figure2_agent_execution.pdf")
    output_png = os.path.join(base_dir, "figure2_agent_execution.png")
    plt.savefig(output_pdf, bbox_inches="tight", pad_inches=0.05)
    plt.savefig(output_png, bbox_inches="tight", pad_inches=0.05, dpi=300)
    plt.close()
    print(f"Generated: {output_pdf}")
    print(f"Generated: {output_png}")

if __name__ == "__main__":
    make_figure()
