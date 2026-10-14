#!/usr/bin/env python3
"""
Generate publication-grade Figure 1:
Combinatorial Divergence in Autonomous Agent Planning and Execution Trajectories.
Visualizes the alluvial flow of 30 independent LLM agent plans (10 Claude Opus,
10 OpenAI Codex, 10 Google Gemini) across 8 analytical decisions, with the three
empirically executed agent workflows highlighted as bold ribbons.
"""

import json
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path

mpl.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]
mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["figure.dpi"] = 300
mpl.rcParams["savefig.dpi"] = 300
mpl.rcParams["pdf.fonttype"] = 42

def make_figure():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.expanduser(
        "~/.gemini/antigravity-cli/brain/ca9cf8af-8540-4356-977f-e501aa2d1a93/scratch/bacillus/choices/artifact_data.json"
    )
    if not os.path.exists(data_path):
        data_path = os.path.abspath(os.path.join(base_dir, "../../../scratch/bacillus/choices/artifact_data.json"))
    
    with open(data_path) as f:
        DATA = json.load(f)

    WFMAP = {
        "Nextflow": "Custom Nextflow",
        "custom Nextflow": "Custom Nextflow",
        "scripts": "Bash/R scripts",
        "Snakemake": "Snakemake",
        "nf-core/rnaseq": "nf-core/rnaseq",
    }
    for d in DATA:
        d["wf"] = WFMAP.get(d["wf"], d["wf"])

    FAM_INFO = {
        "opus": {"name": "Claude Opus 5.5", "color": "#2563eb", "badge": "Anthropic", "marker": "s"},
        "codex": {"name": "Codex (GPT-6 Astra)", "color": "#ea580c", "badge": "OpenAI", "marker": "^"},
        "gemini": {"name": "Gemini 3.8 Flash", "color": "#0d9488", "badge": "Google", "marker": "o"},
    }
    FAMS = ["opus", "codex", "gemini"]
    famRank = {"opus": 0, "codex": 1, "gemini": 2}

    STAGES = [
        {"k": "fam", "label": "AGENT FAMILY", "fmt": lambda v: FAM_INFO[v]["name"]},
        {"k": "ref", "label": "REFERENCE GENOME", "fmt": lambda v: v},
        {"k": "wf", "label": "PIPELINE ENGINE", "fmt": lambda v: v},
        {"k": "trim", "label": "READ TRIMMING", "fmt": lambda v: v},
        {"k": "rRNA", "label": "rRNA FILTERING", "fmt": lambda v: v},
        {"k": "aligner", "label": "READ ALIGNER", "fmt": lambda v: v},
        {"k": "feature", "label": "COUNTED FEATURE", "fmt": lambda v: v},
        {"k": "model", "label": "DE MODEL SCOPE", "fmt": lambda v: v},
        {"k": "shrink", "label": "LFC SHRINKAGE", "fmt": lambda v: v},
    ]

    keyOrder = [s["k"] for s in STAGES]
    plans = sorted(DATA, key=lambda p: [famRank[p["fam"]] if k == "fam" else p[k] for k in keyOrder])

    colW = 164
    left = 32
    top = 34
    unit = 15.0
    gap = 22.0
    nodeW = 10.0

    layout = []
    for i, s in enumerate(STAGES):
        groups = {}
        for idx, p in enumerate(plans):
            val = p[s["k"]]
            groups.setdefault(val, []).append(idx)
        
        if s["k"] == "fam":
            opts = FAMS
        else:
            opts = sorted(groups.keys(), key=lambda g: sum(groups[g]) / len(groups[g]))
        
        y = top
        nodes = {}
        for o in opts:
            n = len(groups[o])
            nodes[o] = {"y": y, "n": n, "members": []}
            y += n * unit + gap
        layout.append({"x": left + i * colW, "nodes": nodes, "h": y - gap})

    # Slot assignments
    slotY = [[] for _ in plans]
    for i, L in enumerate(layout):
        s = STAGES[i]
        order = list(range(len(plans))) if i == 0 else sorted(range(len(plans)), key=lambda idx: slotY[idx][i-1])
        fill = {}
        for idx in order:
            o = plans[idx][s["k"]]
            nd = L["nodes"][o]
            fill[o] = fill.get(o, 0)
            slotY[idx].append(nd["y"] + fill[o] * unit)
            fill[o] += 1
            nd["members"].append(idx)

    max_h = max(L["h"] for L in layout)
    total_w = left + (len(STAGES) - 1) * colW + nodeW + 185
    total_h = max_h + 46

    fig = plt.figure(figsize=(16.2, 6.8), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, total_w)
    ax.set_ylim(total_h, 0)
    ax.axis("off")

    # 1. Background Ribbons (30 plans, transparent alpha=0.18)
    for p_idx, p in enumerate(plans):
        fam_col = FAM_INFO[p["fam"]]["color"]
        for i in range(len(STAGES) - 1):
            x0 = layout[i]["x"] + nodeW
            x1 = layout[i+1]["x"]
            xm = (x0 + x1) / 2.0
            y0 = slotY[p_idx][i] + 1.0
            y1 = slotY[p_idx][i+1] + 1.0
            h = unit - 2.0

            verts = [
                (x0, y0),
                (xm, y0), (xm, y1), (x1, y1),
                (x1, y1 + h),
                (xm, y1 + h), (xm, y0 + h), (x0, y0 + h),
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
            patch = patches.PathPatch(path, facecolor=fam_col, alpha=0.18, edgecolor="none", zorder=2)
            ax.add_patch(patch)

    # 2. Highlighted Representative Planning Trajectories (1 per family, alpha=0.92, bold outline)
    executed_trajectories = [
        {
            "id": "opus",
            "name": "Claude Opus 5.5",
            "badge": "Plan: Claude Opus 5.5",
            "color": "#2563eb",
            "marker": "s",
            "steps": [(s["k"], plans[4][s["k"]], slotY[4][i]) for i, s in enumerate(STAGES)],
        },
        {
            "id": "codex",
            "name": "OpenAI Codex (GPT-6 Astra)",
            "badge": "Plan: Codex (GPT-6 Astra)",
            "color": "#ea580c",
            "marker": "^",
            "steps": [(s["k"], plans[12][s["k"]], slotY[12][i]) for i, s in enumerate(STAGES)],
        },
        {
            "id": "gemini",
            "name": "Gemini 3.8 Flash",
            "badge": "Plan: Gemini 3.8 Flash",
            "color": "#0d9488",
            "marker": "o",
            "steps": [(s["k"], plans[20][s["k"]], slotY[20][i]) for i, s in enumerate(STAGES)],
        },
    ]

    ribbon_h = unit - 2.0

    for traj in executed_trajectories:
        t_col = traj["color"]
        steps = traj["steps"]
        for i in range(len(STAGES) - 1):
            x0 = layout[i]["x"] + nodeW
            x1 = layout[i+1]["x"]
            xm = (x0 + x1) / 2.0
            y0 = steps[i][2] + 1.0
            y1 = steps[i+1][2] + 1.0

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

            # White glow outline underneath
            glow = patches.PathPatch(path, facecolor=t_col, alpha=1.0, edgecolor="#ffffff", linewidth=3.6, zorder=5)
            ax.add_patch(glow)

            # Bold colored ribbon on top
            patch = patches.PathPatch(path, facecolor=t_col, alpha=0.92, edgecolor="#0f172a", linewidth=1.2, zorder=6)
            ax.add_patch(patch)

    # 3. Stage Column Headers & Nodes
    for i, s in enumerate(STAGES):
        L = layout[i]
        ax.text(L["x"], top - 14, s["label"], fontsize=8.5, fontweight="bold", color="#334155", va="bottom", zorder=8)

        for opt_key, nd in L["nodes"].items():
            nh = nd["n"] * unit
            node_x = L["x"]
            node_y = nd["y"]

            if s["k"] == "fam":
                bar_col = FAM_INFO[opt_key]["color"]
            else:
                bar_col = "#334155"

            n_patch = patches.FancyBboxPatch(
                (node_x, node_y + 0.5), nodeW, nh - 1.0,
                boxstyle="round,pad=0,rounding_size=2",
                facecolor=bar_col, edgecolor="none", zorder=7
            )
            ax.add_patch(n_patch)

            label_text = s["fmt"](opt_key)
            count_str = f"n={nd['n']}"
            
            tx = node_x + nodeW + 6
            ty = node_y + nh / 2.0

            is_fork = (s["k"] == "ref" and opt_key in ["anQ-h4", "ATCC 10987"]) or \
                      (s["k"] == "model" and opt_key in ["All samples (pooled)", "5 samples only"])

            if nh <= 20:
                disp_str = f"{label_text} ({count_str})"
                ax.text(tx, ty, disp_str, fontsize=7.8, fontweight="medium", color="#0f172a", va="center",
                        bbox=dict(facecolor="#ffffff", alpha=0.88, edgecolor="none", boxstyle="round,pad=0.2"), zorder=8)
            else:
                if is_fork:
                    ax.text(tx, ty - 4.5, label_text, fontsize=8.2, fontweight="bold", color="#0f172a", va="center",
                            bbox=dict(facecolor="#ffffff", alpha=0.90, edgecolor="none", boxstyle="round,pad=0.15"), zorder=8)
                    ax.text(tx, ty + 6.2, f"{count_str} (Major Fork)", fontsize=7.2, fontweight="medium", color="#b91c1c", va="center",
                            bbox=dict(facecolor="#ffffff", alpha=0.90, edgecolor="none", boxstyle="round,pad=0.15"), zorder=8)
                else:
                    ax.text(tx, ty - 4.0, label_text, fontsize=8.0, fontweight="medium", color="#1e293b", va="center",
                            bbox=dict(facecolor="#ffffff", alpha=0.88, edgecolor="none", boxstyle="round,pad=0.15"), zorder=8)
                    ax.text(tx, ty + 6.0, count_str, fontsize=7.0, color="#64748b", va="center",
                            bbox=dict(facecolor="#ffffff", alpha=0.88, edgecolor="none", boxstyle="round,pad=0.15"), zorder=8)

    # 4. Markers and end badges for the 3 executed trajectories
    for traj in executed_trajectories:
        start_y = traj["steps"][0][2] + ribbon_h / 2.0
        start_x = layout[0]["x"] + nodeW / 2.0
        ax.scatter([start_x], [start_y], marker=traj["marker"], s=45, color="#ffffff", edgecolor="#0f172a", linewidth=1.0, zorder=10)

    exit_x = layout[8]["x"] + nodeW + 65
    for traj in executed_trajectories:
        exit_y = traj["steps"][8][2] + ribbon_h / 2.0
        
        # Draw connecting leader line from ribbon exit to badge
        ax.plot([layout[8]["x"] + nodeW, exit_x - 12], [exit_y, exit_y], color=traj["color"], lw=1.5, linestyle=":", zorder=9)
        ax.scatter([exit_x - 12], [exit_y], marker=traj["marker"], s=50, color=traj["color"], edgecolor="#0f172a", linewidth=0.8, zorder=10)
        ax.text(exit_x - 2, exit_y, traj["badge"], fontsize=7.6, fontweight="bold", color="#ffffff", va="center", ha="left",
                bbox=dict(facecolor=traj["color"], edgecolor="#0f172a", boxstyle="round,pad=0.25", linewidth=0.8), zorder=9)

    # 5. Enhanced Legend at bottom
    leg_x = left
    leg_y = total_h - 20

    ax.text(leg_x, leg_y, "Planning Cohort (n=30):", fontsize=8.2, fontweight="bold", color="#334155", va="center")
    cur_lx = leg_x + 135
    for f_key in FAMS:
        f_info = FAM_INFO[f_key]
        leg_rect = patches.Rectangle((cur_lx, leg_y - 4), 12, 8, facecolor=f_info["color"], alpha=0.25, edgecolor="none")
        ax.add_patch(leg_rect)
        ax.text(cur_lx + 16, leg_y, f"{f_info['name']} (10 plans)", fontsize=7.8, color="#475569", va="center")
        cur_lx += 165

    cur_lx += 15
    ax.text(cur_lx, leg_y, "Highlighted Plans (n=3):", fontsize=8.2, fontweight="bold", color="#0f172a", va="center")
    cur_lx += 125
    leg_rect_exec = patches.Rectangle((cur_lx, leg_y - 4), 16, 8, facecolor="#2563eb", alpha=0.92, edgecolor="#0f172a", linewidth=1.0)
    ax.add_patch(leg_rect_exec)
    ax.text(cur_lx + 22, leg_y, "Bold ribbons trace one representative planning trajectory per model family", fontsize=7.8, fontweight="bold", color="#0f172a", va="center")

    output_pdf = os.path.join(base_dir, "figure1_agent_trajectories.pdf")
    output_png = os.path.join(base_dir, "figure1_agent_trajectories.png")
    plt.savefig(output_pdf, bbox_inches="tight", pad_inches=0.05)
    plt.savefig(output_png, bbox_inches="tight", pad_inches=0.05, dpi=300)
    plt.close()
    print(f"Generated: {output_pdf}")
    print(f"Generated: {output_png}")

if __name__ == "__main__":
    make_figure()
