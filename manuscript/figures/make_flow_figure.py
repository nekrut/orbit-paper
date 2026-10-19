#!/usr/bin/env python3
"""
Generate Figure 3: The Flow of Verifiable Agentic Science.
Horizontal 3-panel pipeline:
- 1. Agent Layer (Interactive reasoning, prompt, Orbit desktop / CLI)
- 2. Guardrails & Protocols (Domain skills & Model Context Protocol)
- 3. Public Compute Infrastructure (UseGalaxy.org, ACCESS-CI supercomputing, verifiable results)
- Bottom closed-loop feedback: Living Provenance & Immutable DAG Notebook
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, PathPatch
from matplotlib.path import Path
from PIL import Image
import matplotlib as mpl

mpl.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]
mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["figure.dpi"] = 300
mpl.rcParams["savefig.dpi"] = 300
mpl.rcParams["pdf.fonttype"] = 42

def draw_pill(ax, x, y, w, h, text, bg="#FFFFFF", border="#CBD5E1", text_color="#0F172A", fontsize=6.2):
    """Draw a compact label badge pill."""
    patch = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.004,rounding_size=0.03",
                           facecolor=bg, edgecolor=border, linewidth=0.9, zorder=6)
    ax.add_patch(patch)
    ax.text(x + w/2.0, y + h/2.0, text, fontsize=fontsize, fontweight="bold", color=text_color,
            va="center", ha="center", zorder=7)

def build_flow_figure():
    fig_dir = os.path.dirname(os.path.abspath(__file__))
    orbit_path = os.path.join(fig_dir, "orbit_screenshot.png")
    galaxy_path = os.path.join(fig_dir, "galaxy_screenshot.png")

    orbit_img = Image.open(orbit_path)
    galaxy_img = Image.open(galaxy_path)

    fig, ax = plt.subplots(figsize=(16.0, 6.05))
    ax.set_xlim(0.0, 16.0)
    ax.set_ylim(0.0, 6.05)
    ax.axis("off")

    # ---------------------------------------------------------
    # Panel 1: Agent Layer (Two Modes of Agentic Use)
    # ---------------------------------------------------------
    p1 = FancyBboxPatch((0.25, 0.40), 5.40, 5.45, boxstyle="round,pad=0.01,rounding_size=0.08",
                         facecolor="#FDF2F8", edgecolor="#FBCFE8", linewidth=1.3, zorder=2)
    ax.add_patch(p1)

    h1 = FancyBboxPatch((0.35, 5.38), 5.20, 0.36, boxstyle="round,pad=0.01,rounding_size=0.04",
                         facecolor="#FCE7F3", edgecolor="#F472B6", linewidth=1.0, zorder=3)
    ax.add_patch(h1)
    ax.text(0.50, 5.56, "1. Agent Layer", fontsize=11.0, fontweight="bold", color="#9D174D", va="center", zorder=4)
    ax.text(5.45, 5.56, "Two Modes of Agentic Use", fontsize=8.5, fontweight="bold", color="#BE185D", va="center", ha="right", zorder=4)

    # Mode 1 Card: Generic Agents
    m1_card = FancyBboxPatch((0.35, 4.40), 2.48, 0.88, boxstyle="round,pad=0.01,rounding_size=0.04",
                              facecolor="#FFFFFF", edgecolor="#F9A8D4", linewidth=1.0, zorder=3)
    ax.add_patch(m1_card)
    ax.text(0.47, 5.13, "Mode 1: Any Generic Agent", fontsize=7.8, fontweight="bold", color="#9D174D", va="center", zorder=4)
    ax.text(0.47, 4.91, "• CLI / IDE agents (Claude Code, Codex, Agy)", fontsize=6.5, color="#334155", va="center", zorder=4)
    ax.text(0.47, 4.72, "• Connects via community Skills & Galaxy MCP", fontsize=6.5, color="#334155", va="center", zorder=4)
    ax.text(0.47, 4.53, "• Standard terminal or editor interface", fontsize=6.5, color="#334155", va="center", zorder=4)

    # Mode 2 Card: Opinionated Agent (Orbit)
    m2_card = FancyBboxPatch((2.93, 4.40), 2.62, 0.88, boxstyle="round,pad=0.01,rounding_size=0.04",
                              facecolor="#FFF1F2", edgecolor="#E11D48", linewidth=1.2, zorder=3)
    ax.add_patch(m2_card)
    ax.text(3.05, 5.13, "Mode 2: Opinionated Agent (Orbit)", fontsize=7.8, fontweight="bold", color="#9F1239", va="center", zorder=4)
    ax.text(3.05, 4.91, "• Lightweight Pi.dev app + agent harness logic", fontsize=6.5, color="#334155", va="center", zorder=4)
    ax.text(3.05, 4.72, "• Direct notebook export, UDTs & job tracking", fontsize=6.5, color="#334155", va="center", zorder=4)
    ax.text(3.05, 4.53, "• Commercial, public API & local LLMs", fontsize=6.5, color="#334155", va="center", zorder=4)

    # Orbit Screenshot below the two mode cards
    ax.imshow(orbit_img, extent=[0.35, 5.55, 0.50, 4.30], aspect='auto', zorder=3)

    # ---------------------------------------------------------
    # Panel 2: Guardrails & Protocols (Skills & MCP)
    # ---------------------------------------------------------
    p2 = FancyBboxPatch((6.35, 0.40), 3.30, 5.45, boxstyle="round,pad=0.01,rounding_size=0.08",
                         facecolor="#F8FAFC", edgecolor="#CBD5E1", linewidth=1.3, zorder=2)
    ax.add_patch(p2)

    h2 = FancyBboxPatch((6.45, 5.38), 3.10, 0.36, boxstyle="round,pad=0.01,rounding_size=0.04",
                         facecolor="#F1F5F9", edgecolor="#94A3B8", linewidth=1.0, zorder=3)
    ax.add_patch(h2)
    ax.text(6.60, 5.56, "2. Guardrails", fontsize=11.0, fontweight="bold", color="#0F172A", va="center", zorder=4)
    ax.text(9.45, 5.56, "Skills & MCP Protocols", fontsize=8.5, fontweight="bold", color="#475569", va="center", ha="right", zorder=4)

    # Subcard 2A: Skills
    c_skills = FancyBboxPatch((6.45, 2.98), 3.10, 2.28, boxstyle="round,pad=0.01,rounding_size=0.05",
                              facecolor="#FEFCE8", edgecolor="#FDE047", linewidth=1.1, zorder=3)
    ax.add_patch(c_skills)
    dot_sk = Circle((6.65, 4.98), 0.05, facecolor="#CA8A04", edgecolor="none", zorder=4)
    ax.add_patch(dot_sk)
    ax.text(6.78, 4.98, "Domain Skills", fontsize=10.0, fontweight="bold", color="#854D0E", va="center", zorder=4)
    ax.text(9.40, 4.98, "Rule Sets", fontsize=7.2, fontweight="bold", color="#A16207", va="center", ha="right", zorder=4)
    ax.text(6.65, 4.72, "Procedural domain rules & analysis design", fontsize=7.2, color="#A16207", style="italic", va="center", zorder=4)

    skill_lines = [
        ("• Analysis Standards:", "Encodes QC thresholds & formats"),
        ("• Decision Briefs:", "Guides tool selection (STAR, etc.)"),
        ("• Reference Data:", "Prompts assembly & strand checks"),
        ("• Verification:", "Pre-execution plan sanity checks")
    ]
    for i, (stitle, sdesc) in enumerate(skill_lines):
        sy = 4.38 - i * 0.31
        ax.text(6.65, sy, stitle, fontsize=7.3, fontweight="bold", color="#713F12", va="center", zorder=4)
        ax.text(7.75, sy, sdesc, fontsize=7.0, color="#475569", va="center", zorder=4)

    # Subcard 2B: MCP
    c_mcp = FancyBboxPatch((6.45, 0.50), 3.10, 2.28, boxstyle="round,pad=0.01,rounding_size=0.05",
                           facecolor="#F0F9FF", edgecolor="#BAE6FD", linewidth=1.1, zorder=3)
    ax.add_patch(c_mcp)
    dot_mcp = Circle((6.65, 2.50), 0.05, facecolor="#0284C7", edgecolor="none", zorder=4)
    ax.add_patch(dot_mcp)
    ax.text(6.78, 2.50, "Model Context Protocol", fontsize=10.0, fontweight="bold", color="#0369A1", va="center", zorder=4)
    ax.text(9.40, 2.50, "Typed APIs", fontsize=7.2, fontweight="bold", color="#0284C7", va="center", ha="right", zorder=4)
    ax.text(6.65, 2.24, "Structured endpoints & environment APIs", fontsize=7.2, color="#0284C7", style="italic", va="center", zorder=4)

    mcp_lines = [
        ("• Typed Schemas:", "run_tool(), get_history_contents()"),
        ("• Data Streaming:", "Upload, query & download files"),
        ("• Job Polling:", "Real-time state & resource tracking"),
        ("• Guardrails:", "Replaces ad-hoc Galaxy scripting")
    ]
    for i, (mtitle, mdesc) in enumerate(mcp_lines):
        my = 1.90 - i * 0.31
        ax.text(6.65, my, mtitle, fontsize=7.3, fontweight="bold", color="#075985", va="center", zorder=4)
        ax.text(7.62, my, mdesc, fontsize=7.0, color="#475569", va="center", zorder=4)

    # ---------------------------------------------------------
    # Panel 3: Public Compute Infrastructure
    # ---------------------------------------------------------
    p3 = FancyBboxPatch((10.35, 0.40), 5.40, 5.45, boxstyle="round,pad=0.01,rounding_size=0.08",
                         facecolor="#F0FDF4", edgecolor="#BBF7D0", linewidth=1.3, zorder=2)
    ax.add_patch(p3)

    h3 = FancyBboxPatch((10.45, 5.38), 5.20, 0.36, boxstyle="round,pad=0.01,rounding_size=0.04",
                         facecolor="#DCFCE7", edgecolor="#86EFAC", linewidth=1.0, zorder=3)
    ax.add_patch(h3)
    ax.text(10.60, 5.56, "3. Public Compute Infrastructure", fontsize=11.0, fontweight="bold", color="#166534", va="center", zorder=4)
    ax.text(15.55, 5.56, "Galaxy / ACCESS-CI / Supercomputing", fontsize=8.5, fontweight="bold", color="#15803D", va="center", ha="right", zorder=4)

    # Galaxy Screenshot: exact aspect ratio preservation
    ax.imshow(galaxy_img, extent=[10.45, 15.65, 0.50, 5.28], aspect='auto', zorder=3)

    # ---------------------------------------------------------
    # Flow Arrows & Badges in Gaps
    # ---------------------------------------------------------
    # Gap 1: x = 5.65 to 6.35 (Center = 6.00)
    # Upper Arrow: Agent -> Skills
    ax.annotate("", xy=(6.35, 4.10), xytext=(5.65, 4.10),
                arrowprops=dict(arrowstyle="-|>", color="#9D174D", lw=2.0, mutation_scale=13), zorder=5)
    draw_pill(ax, 5.68, 4.26, 0.64, 0.21, "Domain Rules", bg="#FDF2F8", border="#F472B6", text_color="#9D174D", fontsize=6.2)

    # Lower Arrow: Agent -> MCP
    ax.annotate("", xy=(6.35, 1.64), xytext=(5.65, 1.64),
                arrowprops=dict(arrowstyle="-|>", color="#0284C7", lw=2.0, mutation_scale=13), zorder=5)
    draw_pill(ax, 5.68, 1.80, 0.64, 0.21, "Tool Calls", bg="#F0F9FF", border="#7DD3FC", text_color="#0369A1", fontsize=6.2)

    # Gap 2: x = 9.65 to 10.35 (Center = 10.00)
    # Upper Arrow: Skills -> Infrastructure
    ax.annotate("", xy=(10.35, 4.10), xytext=(9.65, 4.10),
                arrowprops=dict(arrowstyle="-|>", color="#CA8A04", lw=2.0, mutation_scale=13), zorder=5)
    draw_pill(ax, 9.68, 4.26, 0.64, 0.21, "Validated", bg="#FEFCE8", border="#FDE047", text_color="#854D0E", fontsize=6.2)

    # Lower Arrow: MCP -> Infrastructure
    ax.annotate("", xy=(10.35, 1.64), xytext=(9.65, 1.64),
                arrowprops=dict(arrowstyle="-|>", color="#059669", lw=2.0, mutation_scale=13), zorder=5)
    draw_pill(ax, 9.68, 1.80, 0.64, 0.21, "Dispatch", bg="#F0FDF4", border="#86EFAC", text_color="#166534", fontsize=6.2)

    # ---------------------------------------------------------
    # Bottom Feedback Loop
    # ---------------------------------------------------------
    fb_path = Path([(13.05, 0.40), (13.05, 0.12), (2.95, 0.12), (2.95, 0.40)],
                   [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4])
    patch_fb = PathPatch(fb_path, facecolor="none", edgecolor="#64748B", lw=1.4, linestyle="--", zorder=3)
    ax.add_patch(patch_fb)
    ax.annotate("", xy=(2.95, 0.40), xytext=(2.95, 0.22),
                arrowprops=dict(arrowstyle="-|>", color="#64748B", lw=1.5, mutation_scale=11), zorder=5)

    # Feedback badge
    fbadge = FancyBboxPatch((5.30, 0.02), 5.40, 0.20, boxstyle="round,pad=0.004,rounding_size=0.03",
                            facecolor="#FFFFFF", edgecolor="#94A3B8", linewidth=1.0, zorder=5)
    ax.add_patch(fbadge)
    ax.text(8.00, 0.12, "Living Provenance: the history records the DAG; the notebook ties it to the plan",
            fontsize=7.2, fontweight="bold", color="#334155", ha="center", va="center", zorder=6)

    plt.tight_layout()
    out_png = os.path.join(fig_dir, "flow.png")
    out_pdf = os.path.join(fig_dir, "flow.pdf")
    plt.savefig(out_png, dpi=300, bbox_inches="tight")
    plt.savefig(out_pdf, bbox_inches="tight")
    print(f"Compact flow figure saved to {out_pdf} and {out_png}")

if __name__ == "__main__":
    build_flow_figure()
