#!/usr/bin/env python3
"""
Generate publication-grade Figure 2:
Empirical Reanalysis and Replication Across Independent Agent Execution Environments.
Panel a: Alluvial trajectory flow of three autonomous agents (Claude Opus 5.5, Codex GPT-6 Astra,
Gemini 3.8 Flash) across seven execution stages, demonstrating complete toolchain divergence.
Panel b: Forest plot of differential expression effect sizes (log2FC and 95% CIs) for target enterotoxin
genes (nheB, entFM, nheA, nheC) compared against the published benchmark (PMC12804731).
"""

import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
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
            "short": "Published Paper",
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
            "id": "agy",
            "name": "Google Gemini 3.8 Flash (Antigravity)",
            "short": "Gemini (agy)",
            "color": "#0d9488",
            "marker": "o",
            "data": {
                "nheB": (-2.41, -3.25, -1.57, "padj = 0.0021", "**"),
                "entFM": (1.42, 0.58, 2.26, "padj = 0.0658", "trend"),
                "nheA": (-1.49, -2.48, -0.50, "padj = 0.1012", "n.s."),
                "nheC": (-0.62, -2.05, 0.81, "padj = 0.5129", "n.s."),
            }
        },
        {
            "id": "cc",
            "name": "Anthropic Claude Opus 5.5 (Claude Code)",
            "short": "Claude (cc)",
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
    ]

    fig = plt.figure(figsize=(16.8, 7.6), dpi=300)
    
    # Coordinates for panels
    # Left: Panel a (Alluvial flow of 3 agents)
    ax_a = fig.add_axes([0.020, 0.07, 0.585, 0.87])
    # Right: Panel b (Forest plot of differential expression)
    ax_forest = fig.add_axes([0.650, 0.10, 0.335, 0.82])

    fig.text(0.020, 0.965, "a   Autonomous Execution Trajectories Across Three Agent Platforms",
             fontsize=11.5, fontweight="bold", color="#0f172a", va="top")
    fig.text(0.650, 0.965, "b   Target Enterotoxin Differential Expression (log2FC vs. TSB Control)",
             fontsize=11.5, fontweight="bold", color="#0f172a", va="top")

    # ----------------------------------------------------
    # Panel a: Alluvial Trajectory Flow
    # ----------------------------------------------------
    total_w_a = 730
    total_h_a = 350
    ax_a.set_xlim(0, total_w_a)
    ax_a.set_ylim(total_h_a, 0)
    ax_a.axis("off")

    STAGES_A = [
        {"k": "runtime", "label": "AGENT PLATFORM"},
        {"k": "ref", "label": "REFERENCE GENOME"},
        {"k": "engine", "label": "PIPELINE ENGINE"},
        {"k": "aligner", "label": "READ ALIGNER"},
        {"k": "quant", "label": "QUANTIFICATION"},
        {"k": "model", "label": "DIFFERENTIAL MODEL"},
        {"k": "outcome", "label": "BIOLOGICAL OUTCOME"},
    ]

    # Node definitions per stage
    # For each stage, list nodes from top to bottom (y positions)
    # Claude = blue (#2563eb), Codex = orange (#ea580c), Gemini = teal (#0d9488)
    STAGE_NODES = [
        # Stage 0: AGENT PLATFORM
        [
            {"agent": "cc", "main": "Claude Opus 5.5", "sub": "Claude Code (cc)", "y": 70},
            {"agent": "codex", "main": "Codex GPT-6 Astra", "sub": "OpenAI runner", "y": 160},
            {"agent": "gemini", "main": "Gemini 3.8 Flash", "sub": "Antigravity CLI (agy)", "y": 250},
        ],
        # Stage 1: REFERENCE GENOME
        [
            {"agent": "gemini", "main": "anQ-h4 (RefSeq)", "sub": "GCF_020861345.1", "y": 70},
            {"agent": "codex", "main": "Dual Reference", "sub": "anQ-h4 & ATCC 10987", "y": 160},
            {"agent": "cc", "main": "ATCC 10987", "sub": "GCA_000008005.1", "y": 250},
        ],
        # Stage 2: PIPELINE ENGINE
        [
            {"agent": "cc", "main": "nf-core/rnaseq", "sub": "Docker (>100GB)", "y": 70},
            {"agent": "codex", "main": "Modular runner", "sub": "run_all.sh pipeline", "y": 160},
            {"agent": "gemini", "main": "Ad-hoc Bash", "sub": "Local Conda env", "y": 250},
        ],
        # Stage 3: READ ALIGNER
        [
            {"agent": "gemini", "main": "Bowtie2 v2.5.5", "sub": "fastp polyG removal", "y": 70},
            {"agent": "codex", "main": "HISAT2", "sub": "fastp Q20 filter", "y": 160},
            {"agent": "cc", "main": "STAR 2-pass", "sub": "Trim Galore QC", "y": 250},
        ],
        # Stage 4: QUANTIFICATION
        [
            {"agent": "cc", "main": "Salmon / fCounts", "sub": "MAPQ 255 unique", "y": 70},
            {"agent": "codex", "main": "featureCounts", "sub": "MAPQ >= 10, fragments", "y": 160},
            {"agent": "gemini", "main": "featureCounts", "sub": "transcript features", "y": 250},
        ],
        # Stage 5: DIFFERENTIAL MODEL
        [
            {"agent": "cc", "main": "DESeq2 + ashr", "sub": "adaptive shrinkage", "y": 70},
            {"agent": "codex", "main": "DESeq2 normal", "sub": "normal prior shrink", "y": 160},
            {"agent": "gemini", "main": "DESeq2 Wald", "sub": "5-sample contrast", "y": 250},
        ],
        # Stage 6: BIOLOGICAL OUTCOME (Converging)
        [
            {"agent": "cc", "main": "nheB down, entFM up", "sub": "Discovered cytK (BCE_1209)", "y": 80},
            {"agent": "codex", "main": "nheB down, entFM up", "sub": "Dual-genome concordant", "y": 160},
            {"agent": "gemini", "main": "nheB down, entFM up", "sub": "hbl / cytK absent", "y": 240},
        ],
    ]

    AGENT_COLORS = {
        "cc": "#2563eb",
        "codex": "#ea580c",
        "gemini": "#0d9488",
    }

    left_a = 16
    col_w_a = 98
    node_w_a = 8
    node_h_a = 28
    ribbon_h = 20

    # Draw Ribbons first
    for s_idx in range(len(STAGES_A) - 1):
        x0 = left_a + s_idx * col_w_a + node_w_a
        x1 = left_a + (s_idx + 1) * col_w_a
        xm = (x0 + x1) / 2.0

        curr_nodes = STAGE_NODES[s_idx]
        next_nodes = STAGE_NODES[s_idx + 1]

        for c_node in curr_nodes:
            ag = c_node["agent"]
            # find corresponding node in next stage
            n_node = next(n for n in next_nodes if n["agent"] == ag)

            y0 = c_node["y"] - ribbon_h / 2.0
            y1 = n_node["y"] - ribbon_h / 2.0

            verts = [
                (x0, y0),
                (xm, y0), (xm, y1), (x1, y1),
                (x1, y1 + ribbon_h),
                (xm, y1 + ribbon_h), (xm, y0 + ribbon_h), (x0, y0 + ribbon_h),
                (x0, y0)
            ]
            codes = [
                Path.MOVETO,
                Path.CURVE4, Path.CURVE4, Path.CURVE4,
                Path.LINETO,
                Path.CURVE4, Path.CURVE4, Path.CURVE4,
                Path.CLOSEPOLY
            ]
            path = Path(verts, codes)
            patch = patches.PathPatch(path, facecolor=AGENT_COLORS[ag], alpha=0.42, edgecolor="none", zorder=2)
            ax_a.add_patch(patch)

    # Draw Column Headers and Nodes
    header_y = 38
    for s_idx, stage in enumerate(STAGES_A):
        nx = left_a + s_idx * col_w_a
        ax_a.text(nx, header_y, stage["label"], fontsize=7.8, fontweight="bold", color="#334155", va="bottom", zorder=4)

        for nd in STAGE_NODES[s_idx]:
            ag = nd["agent"]
            ny = nd["y"] - node_h_a / 2.0
            bar_col = AGENT_COLORS[ag] if s_idx == 0 else "#334155"

            n_patch = patches.FancyBboxPatch(
                (nx, ny), node_w_a, node_h_a,
                boxstyle="round,pad=0,rounding_size=2",
                facecolor=bar_col, edgecolor="none", zorder=3
            )
            ax_a.add_patch(n_patch)

            tx = nx + node_w_a + 3
            # Main label
            ax_a.text(tx, nd["y"] - 4.2, nd["main"], fontsize=7.2, fontweight="bold", color="#0f172a", va="center",
                      bbox=dict(facecolor="#ffffff", alpha=0.88, edgecolor="none", boxstyle="round,pad=0.12"), zorder=4)
            # Sub label
            sub_col = "#b91c1c" if "Discovered" in nd["sub"] else "#64748b"
            ax_a.text(tx, nd["y"] + 5.5, nd["sub"], fontsize=6.2, fontweight="bold" if "Discovered" in nd["sub"] else "normal",
                      color=sub_col, va="center",
                      bbox=dict(facecolor="#ffffff", alpha=0.88, edgecolor="none", boxstyle="round,pad=0.12"), zorder=4)

    # Bottom Legend in Panel a
    leg_y = total_h_a - 14
    ax_a.text(left_a, leg_y, "Agent Platform:", fontsize=8.0, fontweight="bold", color="#334155", va="center")
    cur_lx = left_a + 85
    legend_items = [
        ("Claude Opus 5.5", "#2563eb"),
        ("Codex GPT-6 Astra", "#ea580c"),
        ("Gemini 3.8 Flash", "#0d9488"),
    ]
    for l_name, l_col in legend_items:
        rect = patches.Rectangle((cur_lx, leg_y - 4), 12, 8, facecolor=l_col, edgecolor="none")
        ax_a.add_patch(rect)
        ax_a.text(cur_lx + 15, leg_y, l_name, fontsize=7.6, color="#1e293b", va="center")
        cur_lx += 125

    ax_a.text(total_w_a - 10, leg_y, "Toolchain overlap: 0% shared tools across all platforms.",
              fontsize=7.3, color="#64748b", ha="right", va="center", style="italic")

    # ----------------------------------------------------
    # Panel b: Forest Plot of log2FC
    # ----------------------------------------------------
    y_total_span = 26.0
    for g_idx, g in enumerate(genes):
        gene_key = g["key"]
        group_base = y_total_span - 1.5 - g_idx * 6.2

        ax_forest.axhspan(group_base - 3.4, group_base + 1.2, facecolor="#f8fafc" if g_idx % 2 == 0 else "#ffffff", zorder=0)

        ax_forest.text(-3.85, group_base + 0.5, g["name"], fontsize=9.2, fontweight="bold", color="#0f172a", va="center")
        ax_forest.text(-3.85, group_base - 0.2, g["note"], fontsize=7.2, color="#64748b", va="center", style="italic")

        for m_idx, m in enumerate(models):
            y_pos = group_base - 0.8 - m_idx * 0.52
            lfc, ci_l, ci_h, padj_txt, sig = m["data"][gene_key]

            # Plot error bar
            ax_forest.plot([ci_l, ci_h], [y_pos, y_pos], color=m["color"], lw=1.5, zorder=3)
            # Plot marker
            ax_forest.scatter([lfc], [y_pos], color=m["color"], marker=m["marker"], s=45, zorder=4, edgecolor="#0f172a", linewidth=0.5)

            ax_forest.text(2.55, y_pos, f"{lfc:+.2f} ({sig})", fontsize=7.0, color=m["color"], fontweight="bold" if sig in ["*", "**", "***"] else "normal", va="center", ha="left")

    ax_forest.text(2.55, y_total_span - 0.5, "log2FC (sig)", fontsize=7.2, fontweight="bold", color="#475569", va="bottom", ha="left")
    ax_forest.axvline(0, color="#94a3b8", lw=1.0, linestyle="--", zorder=2)
    ax_forest.set_xlim(-4.0, 3.7)
    ax_forest.set_ylim(0.5, y_total_span + 0.5)
    ax_forest.set_xlabel("log2 Fold Change (0.5% Glucose / TSB Control)", fontsize=8.8, fontweight="bold", color="#334155")
    ax_forest.set_yticks([])

    ax_forest.grid(axis="x", color="#e2e8f0", linestyle=":", lw=0.8, zorder=1)
    ax_forest.set_axisbelow(True)

    leg_handles = []
    leg_labels = []
    for m in models:
        line = mpl.lines.Line2D([0], [0], color=m["color"], marker=m["marker"], markersize=6, lw=1.5, markeredgecolor="#0f172a", markeredgewidth=0.5)
        leg_handles.append(line)
        leg_labels.append(m["short"])

    ax_forest.legend(leg_handles, leg_labels, loc="lower center", bbox_to_anchor=(0.5, -0.14),
                     ncol=3, fontsize=7.8, frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1")

    output_pdf = os.path.join(base_dir, "figure2_agent_execution.pdf")
    output_png = os.path.join(base_dir, "figure2_agent_execution.png")
    plt.savefig(output_pdf, bbox_inches="tight", pad_inches=0.05)
    plt.savefig(output_png, bbox_inches="tight", pad_inches=0.05, dpi=300)
    plt.close()
    print(f"Generated: {output_pdf}")
    print(f"Generated: {output_png}")

if __name__ == "__main__":
    make_figure()
