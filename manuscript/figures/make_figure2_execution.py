#!/usr/bin/env python3
"""
Generate publication-grade Figure 2:
Empirical Reanalysis and Replication Across Independent Agent Execution Environments.
Compares the concrete execution workflows, reference genomes, and differential expression
effect sizes (log2FC) of three autonomous agents (Google Gemini via Antigravity, Anthropic
Claude via Claude Code, OpenAI Codex via GPT-6 Astra) against published benchmarks for
Bacillus cereus enterotoxin expression (PMC12804731).
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

    fig = plt.figure(figsize=(15.2, 8.4), dpi=300)
    
    ax_banner = fig.add_axes([0.025, 0.90, 0.95, 0.085])
    ax_table = fig.add_axes([0.025, 0.08, 0.47, 0.79])
    ax_forest = fig.add_axes([0.54, 0.12, 0.435, 0.75])

    # 1. Top Banner
    ax_banner.axis("off")
    banner_rect = patches.FancyBboxPatch(
        (0, 0), 1, 1, transform=ax_banner.transAxes,
        boxstyle="round,pad=0,rounding_size=0.08",
        facecolor="#f8fafc", edgecolor="#cbd5e1", linewidth=1.0
    )
    ax_banner.add_patch(banner_rect)
    ax_banner.text(0.015, 0.64, "Empirical Reanalysis and Biological Signal Replication Across Three Agent Platforms",
                   fontsize=12.5, fontweight="bold", color="#0f172a", va="center")
    ax_banner.text(0.015, 0.28, "Re-analysis of Glucose vs. TSB contrast (PMC12804731) across Gemini 3.8 Flash, Claude Opus 5.5, and Codex GPT-6 Astra",
                   fontsize=8.5, color="#475569", va="center")

    summary_badges = [
        ("Biological Concordance", "100% Direction (nhe down, entFM up)", "#15803d"),
        ("Toolchain Overlap", "0% Shared (Bowtie2 vs nf-core vs HISAT2)", "#b91c1c"),
        ("Provenance Tracking", "0% Archived (ephemeral terminal scripts)", "#c2410c"),
    ]
    for idx, (b_title, b_sub, b_col) in enumerate(summary_badges):
        bx = 0.58 + idx * 0.138
        b_patch = patches.FancyBboxPatch(
            (bx, 0.12), 0.132, 0.76, transform=ax_banner.transAxes,
            boxstyle="round,pad=0,rounding_size=0.06",
            facecolor="#ffffff", edgecolor="#e2e8f0", linewidth=0.8
        )
        ax_banner.add_patch(b_patch)
        ax_banner.text(bx + 0.066, 0.60, b_title, fontsize=7.8, fontweight="bold", color=b_col, ha="center", va="center")
        ax_banner.text(bx + 0.066, 0.28, b_sub, fontsize=6.6, color="#64748b", ha="center", va="center")

    # 2. Left Column: Architecture & Execution Matrix
    ax_table.axis("off")
    ax_table.text(0.0, 0.99, "a  Autonomous Execution Architecture and Toolchain Matrix",
                  fontsize=11.0, fontweight="bold", color="#0f172a", va="top")

    harnesses = [
        {
            "name": "Google Gemini 3.8 Flash",
            "runtime": "Antigravity CLI (agy)",
            "color": "#0d9488",
            "ref": "anQ-h4 (GCF_020861345.1)\nRefSeq LMD38_RS* locus tags",
            "pipeline": "Ad-hoc Bash + R scripts\nLocal Conda environment",
            "align": "fastp v1.4.0 -> bowtie2 v2.5.5\nsubread featureCounts v2.1.1",
            "stats": "DESeq2 v1.50.2 (5-sample fit)\nStandard Wald test",
            "toxins": "nheB down, entFM up, hbl/cytK absent\n(cytK absent in anQ-h4 annotation)",
            "verdict": "Concordant biological trend\nEphemeral bash script"
        },
        {
            "name": "Anthropic Claude Opus 5.5",
            "runtime": "Claude Code (cc)",
            "color": "#2563eb",
            "ref": "ATCC 10987 (GCA_000008005.1)\nGenBank BCE_* locus tags + tblastn",
            "pipeline": "nf-core/rnaseq 3.14.0 +\nnf-core/differentialabundance 1.4.0",
            "align": "Trim Galore -> STAR 2-pass -> Salmon\nfeatureCounts (MAPQ 255 unique)",
            "stats": "DESeq2 v1.34.0 (ashr shrinkage)\nGLU vs TSB Wald test",
            "toxins": "nheB down, entFM up, hbl absent\nDiscovered cytK present (BCE_1209)",
            "verdict": "Concordant biological trend\nHeavy disk footprint (>100GB)"
        },
        {
            "name": "OpenAI Codex / GPT-6 Astra",
            "runtime": "Codex exec (--ephemeral)",
            "color": "#ea580c",
            "ref": "Dual: anQ-h4 (GCF_020861345.1) &\nATCC 10987 (GCA_000008005.1)",
            "pipeline": "Modular Bash runner (run_all.sh)\nConda with explicit package URLs",
            "align": "fastp (Q20) -> HISAT2 (unspliced)\nfeatureCounts (MAPQ>=10, fragments)",
            "stats": "DESeq2 (5-sample, no outlier replace)\nWald intervals + normal prior shrink",
            "toxins": "nheB down, entFM up, hbl absent\nSensitivity analysis across 2 genomes",
            "verdict": "Concordant biological trend\nStrict statistics, isolated code"
        },
    ]

    card_y = 0.94
    card_h = 0.29
    card_gap = 0.025

    categories = [
        ("Reference Genome:", "ref"),
        ("Software Stack:", "pipeline"),
        ("Alignment & Quant:", "align"),
        ("Differential Model:", "stats"),
        ("Toxin Findings:", "toxins"),
    ]

    for h_idx, h in enumerate(harnesses):
        y_pos = card_y - h_idx * (card_h + card_gap) - card_h
        card_box = patches.FancyBboxPatch(
            (0.0, y_pos), 1.0, card_h,
            boxstyle="round,pad=0,rounding_size=0.03",
            facecolor="#ffffff", edgecolor=h["color"], linewidth=1.4
        )
        ax_table.add_patch(card_box)

        tag_rect = patches.FancyBboxPatch(
            (0.0, y_pos + card_h - 0.052), 1.0, 0.052,
            boxstyle="round,pad=0,rounding_size=0.03",
            facecolor=h["color"], edgecolor="none"
        )
        ax_table.add_patch(tag_rect)
        ax_table.text(0.025, y_pos + card_h - 0.026, h["name"], fontsize=9.2, fontweight="bold", color="#ffffff", va="center")
        ax_table.text(0.975, y_pos + card_h - 0.026, f"Runtime: {h['runtime']}", fontsize=8.0, color="#ffffff", ha="right", va="center")

        cx1, cx2 = 0.025, 0.52
        rows = [
            (categories[0], categories[1]),
            (categories[2], categories[3]),
            (categories[4], None)
        ]
        
        row_y = y_pos + card_h - 0.086
        for r_idx, (col1, col2) in enumerate(rows):
            lbl1, key1 = col1
            ax_table.text(cx1, row_y, lbl1, fontsize=7.2, fontweight="bold", color="#475569", va="top")
            ax_table.text(cx1 + 0.17, row_y, h[key1], fontsize=7.2, color="#0f172a", va="top")

            if col2:
                lbl2, key2 = col2
                ax_table.text(cx2, row_y, lbl2, fontsize=7.2, fontweight="bold", color="#475569", va="top")
                ax_table.text(cx2 + 0.17, row_y, h[key2], fontsize=7.2, color="#0f172a", va="top")
            
            row_y -= 0.066

    # 3. Right Column: Forest Plot of log2FC
    ax_forest.text(0.0, 1.04, "b  Target Enterotoxin Differential Expression (log2FC vs. TSB Control)",
                   fontsize=11.0, fontweight="bold", color="#0f172a", va="top", transform=ax_forest.transAxes)

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

    ax_forest.legend(leg_handles, leg_labels, loc="lower center", bbox_to_anchor=(0.5, -0.16),
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
