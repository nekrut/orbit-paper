#!/usr/bin/env python3
"""
Generate Figure 1: The Flow: Agent -> Infrastructure -> Result.
Faithfully rendered from the user's architectural schematic in Untitled drawing.pdf:
- Left: Autonomous Agents & Interface Layer (Galaxy MCP, Galaxy skills, Foundry Skills).
- Center: Branching Decision Node: "If local compute available?"
  - YES: Assemble all tools / Prototype / Test -> Local compute -> Deploy Tools & Workflows / Run everything -> Galaxy.
  - NO: Assemble all tools / Prototype / Test / Run everything -> Galaxy.
- Galaxy -> Notebook (Living Epistemic Record & Provenance by Construction).
- Right: Provenance & Epistemic Properties summary.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Polygon, Rectangle
import numpy as np
import matplotlib as mpl

mpl.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]
mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["figure.dpi"] = 300
mpl.rcParams["savefig.dpi"] = 300
mpl.rcParams["pdf.fonttype"] = 42

def draw_pill(ax, x, y, w, h, text, subtext=None, bg="#FFFFFF", border="#CBD5E1", dot_color="#2563EB", text_color="#0F172A", fontsize=9.0):
    """Draw a clean UI pill with an indicator dot."""
    patch = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.005,rounding_size=0.012",
                           facecolor=bg, edgecolor=border, linewidth=1.1, zorder=4)
    ax.add_patch(patch)
    if dot_color:
        dot = Circle((x + 0.015, y + h/2.0), 0.0042, facecolor=dot_color, edgecolor="none", zorder=5)
        ax.add_patch(dot)
        tx = x + 0.026
    else:
        tx = x + w/2.0
    
    if subtext:
        ax.text(tx, y + h*0.65, text, fontsize=fontsize, fontweight="bold", color=text_color, va="center", ha="left" if dot_color else "center", zorder=5)
        ax.text(tx, y + h*0.28, subtext, fontsize=fontsize*0.75, color="#64748B", va="center", ha="left" if dot_color else "center", zorder=5)
    else:
        ax.text(tx, y + h/2.0, text, fontsize=fontsize, fontweight="bold", color=text_color, va="center", ha="left" if dot_color else "center", zorder=5)

def build_figure1():
    fig, ax = plt.subplots(figsize=(15.6, 8.8))
    ax.set_xlim(0.0, 1.56)
    ax.set_ylim(0.0, 0.88)
    ax.axis("off")
    
    # -------------------------------------------------------------
    # TOP STAGE HEADERS (The Flow: Agent -> Infrastructure -> Result)
    # -------------------------------------------------------------
    # Stage 1: AGENT
    h1 = FancyBboxPatch((0.04, 0.80), 0.44, 0.055, boxstyle="round,pad=0.003,rounding_size=0.010",
                        facecolor="#EFF6FF", edgecolor="#BFDBFE", linewidth=1.2, zorder=2)
    ax.add_patch(h1)
    ax.text(0.06, 0.827, "1. AGENT LAYER", fontsize=10.5, fontweight="bold", color="#1E40AF", va="center")
    ax.text(0.46, 0.827, "Reasoning, MCP & Skills", fontsize=8.2, color="#3B82F6", va="center", ha="right")
    
    # Stage 2: INFRASTRUCTURE
    h2 = FancyBboxPatch((0.51, 0.80), 0.65, 0.055, boxstyle="round,pad=0.003,rounding_size=0.010",
                        facecolor="#F0FDF4", edgecolor="#BBF7D0", linewidth=1.2, zorder=2)
    ax.add_patch(h2)
    ax.text(0.53, 0.827, "2. INFRASTRUCTURE LAYER", fontsize=10.5, fontweight="bold", color="#166534", va="center")
    ax.text(1.14, 0.827, "Hybrid Execution & Supercompute", fontsize=8.2, color="#15803D", va="center", ha="right")
    
    # Stage 3: RESULT
    h3 = FancyBboxPatch((1.19, 0.80), 0.33, 0.055, boxstyle="round,pad=0.003,rounding_size=0.010",
                        facecolor="#F5F3FF", edgecolor="#DDD6FE", linewidth=1.2, zorder=2)
    ax.add_patch(h3)
    ax.text(1.21, 0.827, "3. RESULT LAYER", fontsize=10.5, fontweight="bold", color="#6D28D9", va="center")
    ax.text(1.50, 0.827, "Living Record & Provenance", fontsize=8.2, color="#7C3AED", va="center", ha="right")

    # -------------------------------------------------------------
    # LEFT CONTAINER: AGENTS & SKILLS (x: 0.04 to 0.48, y: 0.06 to 0.76)
    # -------------------------------------------------------------
    box_agents = FancyBboxPatch((0.04, 0.06), 0.44, 0.70, boxstyle="round,pad=0.008,rounding_size=0.018",
                                facecolor="#F8FAFC", edgecolor="#94A3B8", linewidth=1.3, zorder=2)
    ax.add_patch(box_agents)
    
    # Inner sub-box 1: Autonomous Agents (Left column)
    ax.text(0.065, 0.725, "Autonomous Agents", fontsize=10.0, fontweight="bold", color="#1E293B", va="center")
    
    agent_names = [
        ("Orbit", "Scientific research workbench"),
        ("Claude Code", "Command-line agentic assistant"),
        ("Codex", "Autonomous code & task engine"),
        ("Antigravity", "Multimodal pair-programmer"),
        ("Pi.dev", "Headless agent runtime"),
        ("...", "Universal agentic surface")
    ]
    
    ay_start = 0.670
    card_h = 0.075
    spacing = 0.098
    for i, (aname, adesc) in enumerate(agent_names):
        ay = ay_start - i * spacing
        draw_pill(ax, 0.065, ay - card_h + 0.01, 0.175, card_h, aname, adesc if i < 5 else "Open to any MCP client",
                  bg="#FFFFFF", border="#BFDBFE" if i < 5 else "#CBD5E1", dot_color="#2563EB" if i < 5 else "#94A3B8",
                  fontsize=8.8)
    
    # Inner sub-box 2: Protocols & Skills (Right column)
    ax.text(0.275, 0.725, "Protocols & Skills", fontsize=10.0, fontweight="bold", color="#1E293B", va="center")
    
    skill_items = [
        ("Galaxy MCP", "44 tool endpoints, stdio & HTTP", "#D97706", "#FFFBEB", "#FDE68A"),
        ("Galaxy Skills", "Curated domain guides & idioms", "#059669", "#ECFDF5", "#A7F3D0"),
        ("Foundry Skills", "Workflow casting & schema checks", "#C2410C", "#FFF7ED", "#FED7AA")
    ]
    
    sy_start = 0.610
    s_h = 0.105
    s_spacing = 0.148
    for j, (sname, sdesc, scol, sbg, sbor) in enumerate(skill_items):
        sy = sy_start - j * s_spacing
        draw_pill(ax, 0.275, sy - s_h + 0.01, 0.180, s_h, sname, sdesc,
                  bg=sbg, border=sbor, dot_color=scol, fontsize=9.0)

    # Connecting bracket / dashed lines from Agents to Protocols
    for k in range(5):
        y_from = ay_start - k * spacing - card_h/2.0 + 0.01
        ax.plot([0.245, 0.265], [y_from, 0.41], color="#CBD5E1", lw=0.9, ls=":", zorder=3)
    ax.plot([0.265, 0.270], [0.41, 0.41], color="#94A3B8", lw=1.2, zorder=3)
    
    # -------------------------------------------------------------
    # DECISION NODE: If local compute available?
    # Center at (0.61, 0.41)
    # -------------------------------------------------------------
    # Arrow from Left box to Diamond
    ax.annotate("", xy=(0.540, 0.41), xytext=(0.480, 0.41),
                arrowprops=dict(arrowstyle="-|>", color="#1E293B", lw=1.8, mutation_scale=14), zorder=5)

    dcx, dcy = 0.620, 0.41
    dw, dh = 0.080, 0.085
    diamond_pts = np.array([
        [dcx, dcy + dh],
        [dcx + dw, dcy],
        [dcx, dcy - dh],
        [dcx - dw, dcy]
    ])
    diamond_poly = Polygon(diamond_pts, facecolor="#F0F9FF", edgecolor="#0284C7", linewidth=1.5, zorder=4)
    ax.add_patch(diamond_poly)
    
    ax.text(dcx, dcy + 0.020, "If local\ncompute", fontsize=8.6, fontweight="bold", color="#0369A1",
            ha="center", va="center", zorder=6)
    ax.text(dcx, dcy - 0.022, "available?", fontsize=8.6, fontweight="bold", color="#0369A1",
            ha="center", va="center", zorder=6)
    
    # -------------------------------------------------------------
    # BRANCH 1: YES (Local Compute Available) - Upper Route
    # -------------------------------------------------------------
    # Arrow going UP from diamond top
    ax.plot([dcx, dcx], [dcy + dh, 0.65], color="#1E293B", lw=1.6, zorder=3)
    ax.text(dcx - 0.015, 0.54, "Yes", fontsize=9.2, fontweight="bold", color="#15803D", ha="right", va="center")
    
    # Horizontal line to Local compute box
    lc_x = 0.96
    lc_y = 0.65
    ax.annotate("", xy=(lc_x, lc_y), xytext=(dcx, 0.65),
                arrowprops=dict(arrowstyle="-|>", color="#1E293B", lw=1.6, mutation_scale=14), zorder=3)
    
    # Annotation badge along upper horizontal path
    badge_yes = FancyBboxPatch((0.68, 0.665), 0.22, 0.036, boxstyle="round,pad=0.002,rounding_size=0.006",
                               facecolor="#FFFFFF", edgecolor="#86EFAC", lw=1.0, zorder=5)
    ax.add_patch(badge_yes)
    ax.text(0.79, 0.683, "Assemble all tools / Prototype / Test", fontsize=7.6, fontweight="bold",
            color="#166534", ha="center", va="center", zorder=6)
    
    # Node: Local compute
    lc_box = FancyBboxPatch((lc_x, 0.580), 0.160, 0.140, boxstyle="round,pad=0.006,rounding_size=0.015",
                            facecolor="#FEF3C7", edgecolor="#D97706", linewidth=1.4, zorder=4)
    ax.add_patch(lc_box)
    ax.text(lc_x + 0.080, 0.685, "Local Compute", fontsize=10.0, fontweight="bold", color="#92400E", ha="center", zorder=5)
    ax.text(lc_x + 0.080, 0.635, "• Local Docker / Podman\n• Conda environments\n• Unit tests & mock data",
            fontsize=7.2, color="#78350F", ha="center", va="center", zorder=5)
    
    # -------------------------------------------------------------
    # GALAXY PUBLIC CYBERINFRASTRUCTURE (Center/Bottom Right)
    # -------------------------------------------------------------
    gx_x = 0.96
    gx_y = 0.24
    gx_w = 0.160
    gx_h = 0.170
    
    gx_box = FancyBboxPatch((gx_x, gx_y), gx_w, gx_h, boxstyle="round,pad=0.008,rounding_size=0.018",
                            facecolor="#ECFDF5", edgecolor="#059669", linewidth=1.5, zorder=4)
    ax.add_patch(gx_box)
    
    ax.text(gx_x + gx_w/2.0, gx_y + gx_h - 0.025, "Galaxy", fontsize=11.5, fontweight="bold", color="#065F46", ha="center", zorder=5)
    ax.text(gx_x + gx_w/2.0, gx_y + 0.075,
            "• Public Supercompute\n• Tools & Workflows\n• Bioconda & Containers\n• Unprivileged UDTs\n• GPU Accelerators",
            fontsize=7.2, color="#047857", ha="center", va="center", zorder=5)
    
    # Downward arrow from Local compute to Galaxy
    ax.annotate("", xy=(gx_x + gx_w/2.0, gx_y + gx_h), xytext=(lc_x + 0.080, 0.580),
                arrowprops=dict(arrowstyle="-|>", color="#1E293B", lw=1.6, mutation_scale=14), zorder=3)
    
    # Annotation on the Local compute -> Galaxy vertical arrow (placed neatly to the left)
    lbl_box1 = FancyBboxPatch((0.74, 0.465), 0.20, 0.045, boxstyle="round,pad=0.002,rounding_size=0.006",
                              facecolor="#FFFFFF", edgecolor="#CBD5E1", lw=0.9, zorder=5)
    ax.add_patch(lbl_box1)
    ax.text(0.84, 0.488, "Deploy Tools & Workflows\n/ Run everything", fontsize=7.2, fontweight="bold",
            color="#334155", ha="center", va="center", zorder=6)
    
    # -------------------------------------------------------------
    # BRANCH 2: NO (No Local Compute Available) - Lower Direct Route
    # -------------------------------------------------------------
    # Arrow going DOWN from diamond bottom
    ax.plot([dcx, dcx], [dcy - dh, 0.27], color="#1E293B", lw=1.6, zorder=3)
    ax.text(dcx - 0.015, 0.31, "No", fontsize=9.2, fontweight="bold", color="#DC2626", ha="right", va="center")
    
    # Horizontal line from bottom of diamond to Galaxy box
    ax.annotate("", xy=(gx_x, 0.27), xytext=(dcx, 0.27),
                arrowprops=dict(arrowstyle="-|>", color="#1E293B", lw=1.6, mutation_scale=14), zorder=3)
    
    # Annotation badge along lower horizontal path
    badge_no = FancyBboxPatch((0.645, 0.215), 0.29, 0.038, boxstyle="round,pad=0.002,rounding_size=0.006",
                              facecolor="#FFFFFF", edgecolor="#FCA5A5", lw=1.0, zorder=5)
    ax.add_patch(badge_no)
    ax.text(0.790, 0.234, "Assemble all tools / Prototype / Test / Run everything",
            fontsize=7.4, fontweight="bold", color="#991B1B", ha="center", va="center", zorder=6)

    # -------------------------------------------------------------
    # RESULT: NOTEBOOK (Living Record & Provenance)
    # Straight down below Galaxy (matching user sketch)
    # -------------------------------------------------------------
    nb_x = 0.96
    nb_y = 0.04
    nb_w = 0.160
    nb_h = 0.135
    
    # Downward arrow from Galaxy to Notebook
    ax.annotate("", xy=(nb_x + nb_w/2.0, nb_y + nb_h), xytext=(gx_x + gx_w/2.0, gx_y),
                arrowprops=dict(arrowstyle="-|>", color="#1E293B", lw=1.8, mutation_scale=15), zorder=3)
    
    nb_box = FancyBboxPatch((nb_x, nb_y), nb_w, nb_h, boxstyle="round,pad=0.008,rounding_size=0.018",
                            facecolor="#F5F3FF", edgecolor="#7C3AED", linewidth=1.5, zorder=4)
    ax.add_patch(nb_box)
    
    ax.text(nb_x + nb_w/2.0, nb_y + nb_h - 0.024, "Notebook", fontsize=11.5, fontweight="bold", color="#5B21B6", ha="center", zorder=5)
    ax.text(nb_x + nb_w/2.0, nb_y + 0.055,
            "• Living Epistemic Record\n• Immutable DAG Provenance\n• Verifiable by Construction\n• Machine-Checkable Results",
            fontsize=7.2, color="#6D28D9", ha="center", va="center", zorder=5)
            
    # -------------------------------------------------------------
    # EXTRA SUMMARY PANEL ON FAR RIGHT (x: 1.19 to 1.52, y: 0.06 to 0.76)
    # -------------------------------------------------------------
    summary_box = FancyBboxPatch((1.19, 0.06), 0.33, 0.70, boxstyle="round,pad=0.008,rounding_size=0.018",
                                 facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1.2, zorder=2)
    ax.add_patch(summary_box)
    
    ax.text(1.215, 0.725, "Key Architectural Properties", fontsize=10.0, fontweight="bold", color="#0F172A", va="center")
    
    prop_items = [
        ("Decoupled Execution",
         "Agents reason and plan independently;\ncomputational workloads execute\nremotely across distributed clusters.", "#2563EB"),
        ("Universal Public Access",
         "Researchers lacking local supercompute\nor GPU resources run heavy transformer\nmodels and structural aligners on Galaxy.", "#059669"),
        ("Dual-Mode Flexibility",
         "Rapid local prototyping and unit-testing\nwhen workstations allow; direct remote\nassembly when local resources are absent.", "#D97706"),
        ("Extensibility via UDTs",
         "Unprivileged User-Defined Tools allow\nagents to cast custom containerized\nsoftware dynamically at runtime.", "#C2410C"),
        ("Provenance by Construction",
         "Every executed job automatically seals\ninput digests, exact tool versions, and\noutputs into an immutable DAG ledger.", "#7C3AED")
    ]
    
    py_start = 0.650
    p_spacing = 0.125
    for m, (ptitle, pdesc, pcol) in enumerate(prop_items):
        py = py_start - m * p_spacing
        dot = Circle((1.220, py + 0.016), 0.0042, facecolor=pcol, edgecolor="none", zorder=4)
        ax.add_patch(dot)
        ax.text(1.235, py + 0.016, ptitle, fontsize=8.6, fontweight="bold", color="#0F172A", va="center", zorder=4)
        ax.text(1.235, py - 0.024, pdesc, fontsize=7.2, color="#475569", va="center", zorder=4)
    
    plt.tight_layout()
    plt.savefig("/Users/anton/git/orbit-paper/manuscript/figures/figure1_architecture.png", dpi=300, bbox_inches="tight")
    plt.savefig("/Users/anton/git/orbit-paper/manuscript/figures/figure1_architecture.pdf", bbox_inches="tight")
    print("New Figure 1 regenerated successfully!")

if __name__ == "__main__":
    build_figure1()
