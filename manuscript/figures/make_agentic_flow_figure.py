#!/usr/bin/env python3
"""
Generate Figure: The Agentic Flow: From Prompt to Constrained Action.
Illustrates how agentic data analysis operates:
- 1. Scientific Reasoning & Inference (Researcher Prompt + Foundation LLM)
- 2. Client Agent Runtime / Harness (Workstation session, orchestrator, runtimes)
- 3. Operational Funnel (Skills: procedural rules; MCP: typed programmatic endpoints)
- 4. Executed Actions & Targets (Code synthesis, data handling, external APIs, cyberinfrastructure)
- Closed-Loop Feedback (Exit codes, logs, and outputs return to Agent & LLM)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, PathPatch
from matplotlib.path import Path
import matplotlib as mpl

mpl.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]
mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["figure.dpi"] = 300
mpl.rcParams["savefig.dpi"] = 300
mpl.rcParams["pdf.fonttype"] = 42

def draw_pill(ax, x, y, w, h, text, subtext=None, bg="#FFFFFF", border="#CBD5E1", dot_color="#2563EB", text_color="#0F172A", fontsize=8.2):
    """Draw a clean UI pill with an indicator dot."""
    patch = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.003,rounding_size=0.010",
                           facecolor=bg, edgecolor=border, linewidth=1.0, zorder=4)
    ax.add_patch(patch)
    if dot_color:
        dot = Circle((x + 0.014, y + h/2.0), 0.0036, facecolor=dot_color, edgecolor="none", zorder=5)
        ax.add_patch(dot)
        tx = x + 0.024
    else:
        tx = x + w/2.0
    
    if subtext:
        ax.text(tx, y + h*0.65, text, fontsize=fontsize, fontweight="bold", color=text_color, va="center", ha="left" if dot_color else "center", zorder=5)
        ax.text(tx, y + h*0.28, subtext, fontsize=fontsize*0.75, color="#64748B", va="center", ha="left" if dot_color else "center", zorder=5)
    else:
        ax.text(tx, y + h/2.0, text, fontsize=fontsize, fontweight="bold", color=text_color, va="center", ha="left" if dot_color else "center", zorder=5)

def build_agentic_flow_figure():
    fig, ax = plt.subplots(figsize=(16.0, 4.7))
    ax.set_xlim(0.0, 1.60)
    ax.set_ylim(0.0, 0.47)
    ax.axis("off")
    
    # -------------------------------------------------------------
    # 1. SCIENTIFIC REASONING & INFERENCE (Left: x = 0.03 to 0.43)
    # -------------------------------------------------------------
    box1 = FancyBboxPatch((0.03, 0.065), 0.40, 0.385, boxstyle="round,pad=0.006,rounding_size=0.014",
                          facecolor="#FDF2F8", edgecolor="#FBCFE8", linewidth=1.2, zorder=2)
    ax.add_patch(box1)
    
    ax.text(0.048, 0.425, "1. REASONING ENGINE", fontsize=9.2, fontweight="bold", color="#9D174D", va="center")
    ax.text(0.415, 0.425, "Remote LLM", fontsize=7.2, fontweight="bold", color="#BE185D", va="center", ha="right")
    
    # Prompt Card (User input)
    prompt_box = FancyBboxPatch((0.048, 0.14), 0.160, 0.255, boxstyle="round,pad=0.004,rounding_size=0.009",
                                facecolor="#FFFFFF", edgecolor="#F472B6", linewidth=1.1, zorder=3)
    ax.add_patch(prompt_box)
    
    # User chat header
    dot_user = Circle((0.060, 0.368), 0.0035, facecolor="#DB2777", edgecolor="none", zorder=4)
    ax.add_patch(dot_user)
    ax.text(0.068, 0.368, "Researcher Prompt", fontsize=8.0, fontweight="bold", color="#831843", va="center", zorder=4)
    
    # Natural language prompt snippet
    prompt_lines = [
        "\"Download FASTQ files from",
        " SRA, trim low-quality bases,",
        " align with STAR, quantify",
        " gene counts, identify DE",
        " transcripts, and generate",
        " publication volcano plots.\""
    ]
    for p_i, pline in enumerate(prompt_lines):
        ax.text(0.058, 0.335 - p_i * 0.024, pline, fontsize=6.8, color="#475569", style="italic", va="center", zorder=4)
        
    draw_pill(ax, 0.056, 0.155, 0.144, 0.032, "Natural Language Goal", None, bg="#FDF2F8", border="#FBCFE8", dot_color=None, text_color="#9D174D", fontsize=6.5)

    # Arrow from Prompt to LLM
    ax.annotate("", xy=(0.244, 0.270), xytext=(0.212, 0.270),
                arrowprops=dict(arrowstyle="-|>", color="#DB2777", lw=1.5, mutation_scale=10), zorder=5)

    # Foundation LLM Card
    llm_box = FancyBboxPatch((0.246, 0.09), 0.170, 0.305, boxstyle="round,pad=0.005,rounding_size=0.009",
                             facecolor="#FFFFFF", edgecolor="#FDA4AF", linewidth=1.1, zorder=3)
    ax.add_patch(llm_box)
    
    dot_llm = Circle((0.258, 0.368), 0.0035, facecolor="#E11D48", edgecolor="none", zorder=4)
    ax.add_patch(dot_llm)
    ax.text(0.266, 0.368, "Foundation Model", fontsize=8.2, fontweight="bold", color="#9F1239", va="center", zorder=4)
    ax.text(0.266, 0.348, "Cloud / HPC Host", fontsize=6.5, color="#BE185D", va="center", zorder=4)
    
    llm_details = [
        ("Frontier Cloud", "Google, Anthropic, OpenAI"),
        ("Institutional HPC", "Open-weight (Llama, Qwen) on GPUs"),
        ("Analytical Role", "Deconstructs prompt, plans steps,"),
        ("", "and generates structured tool calls")
    ]
    for d_i, (dtitle, ddesc) in enumerate(llm_details):
        dy = 0.315 - d_i * 0.046
        if dtitle:
            dot_sub = Circle((0.258, dy), 0.0025, facecolor="#F43F5E", edgecolor="none", zorder=4)
            ax.add_patch(dot_sub)
            ax.text(0.266, dy + 0.002, dtitle, fontsize=6.8, fontweight="bold", color="#1E293B", va="center", zorder=4)
            ax.text(0.266, dy - 0.016, ddesc, fontsize=6.0, color="#64748B", va="center", zorder=4)
        else:
            ax.text(0.266, dy + 0.016, ddesc, fontsize=6.0, color="#64748B", va="center", zorder=4)

    # -------------------------------------------------------------
    # 2. CLIENT AGENT RUNTIME / HARNESS (Center-Left: x = 0.475 to 0.765)
    # -------------------------------------------------------------
    box2 = FancyBboxPatch((0.475, 0.065), 0.290, 0.385, boxstyle="round,pad=0.006,rounding_size=0.014",
                          facecolor="#FFF7ED", edgecolor="#FED7AA", linewidth=1.2, zorder=2)
    ax.add_patch(box2)
    
    ax.text(0.492, 0.425, "2. CLIENT AGENT HARNESS", fontsize=9.2, fontweight="bold", color="#9A3412", va="center")
    ax.text(0.750, 0.425, "Client Machine", fontsize=7.2, fontweight="bold", color="#C2410C", va="center", ha="right")
    
    # Interaction arrows between LLM and Client Agent
    # Upper arrow: LLM -> Agent (Tool Calls)
    ax.annotate("", xy=(0.475, 0.295), xytext=(0.430, 0.295),
                arrowprops=dict(arrowstyle="-|>", color="#EA580C", lw=1.6, mutation_scale=11), zorder=6)
    ax.text(0.4525, 0.315, "Tool Calls", fontsize=6.4, fontweight="bold", color="#C2410C", ha="center", va="bottom")
    
    # Lower arrow: Agent -> LLM (Feedback)
    ax.annotate("", xy=(0.430, 0.175), xytext=(0.475, 0.175),
                arrowprops=dict(arrowstyle="-|>", color="#2563EB", lw=1.6, mutation_scale=11), zorder=6)
    ax.text(0.4525, 0.155, "Logs / Output", fontsize=6.4, fontweight="bold", color="#1D4ED8", ha="center", va="top")
    
    # Inside Client Agent: 3 functional modules
    draw_pill(ax, 0.492, 0.285, 0.256, 0.075, "Session State & Memory", "Tracks history, variables, active files, context",
              bg="#FFFFFF", border="#FDBA74", dot_color="#F97316", text_color="#7C2D12", fontsize=7.6)
    draw_pill(ax, 0.492, 0.190, 0.256, 0.075, "Execution Orchestrator", "Evaluates instructions & manages subprocesses",
              bg="#FFFFFF", border="#FDBA74", dot_color="#EA580C", text_color="#7C2D12", fontsize=7.6)
    draw_pill(ax, 0.492, 0.095, 0.256, 0.075, "Agent Runtimes", "Orbit (desktop), Claude Code, Antigravity, Codex",
              bg="#FFFFFF", border="#FDBA74", dot_color="#C2410C", text_color="#7C2D12", fontsize=7.6)

    # -------------------------------------------------------------
    # 3. OPERATIONAL FUNNEL: SKILLS & MCP (Center-Right: x = 0.805 to 1.185)
    # -------------------------------------------------------------
    box3 = FancyBboxPatch((0.805, 0.065), 0.380, 0.385, boxstyle="round,pad=0.006,rounding_size=0.014",
                          facecolor="#F0F9FF", edgecolor="#BAE6FD", linewidth=1.2, zorder=2)
    ax.add_patch(box3)
    
    ax.text(0.822, 0.425, "3. GUARDRAILS", fontsize=9.2, fontweight="bold", color="#0369A1", va="center")
    ax.text(1.172, 0.425, "Operational Constraints", fontsize=7.2, fontweight="bold", color="#0284C7", va="center", ha="right")
    
    # Arrow from Agent to Funnel
    ax.annotate("", xy=(0.805, 0.240), xytext=(0.765, 0.240),
                arrowprops=dict(arrowstyle="-|>", color="#0284C7", lw=1.6, mutation_scale=11), zorder=6)
    
    # Sub-card A: Skills (Top)
    skills_card = FancyBboxPatch((0.822, 0.240), 0.346, 0.145, boxstyle="round,pad=0.004,rounding_size=0.009",
                                 facecolor="#FEFCE8", edgecolor="#FDE047", linewidth=1.1, zorder=3)
    ax.add_patch(skills_card)
    
    dot_sk = Circle((0.836, 0.362), 0.0035, facecolor="#CA8A04", edgecolor="none", zorder=4)
    ax.add_patch(dot_sk)
    ax.text(0.844, 0.362, "Domain Skills (Rule Sets)", fontsize=8.0, fontweight="bold", color="#854D0E", va="center", zorder=4)
    ax.text(0.844, 0.342, "Markdown instructions defining domain methodologies", fontsize=6.4, color="#A16207", va="center", zorder=4)
    
    skills_items = [
        ("Conventions:", "Enforces standard parameters, quality thresholds, file formats"),
        ("Decision Briefs:", "Determines tool suitability (e.g., STAR vs HISAT2, DESeq2)"),
        ("Standards:", "Guides structured reasoning and reproducible workflow steps")
    ]
    for s_i, (stitle, sdesc) in enumerate(skills_items):
        sy = 0.315 - s_i * 0.024
        ax.text(0.836, sy, f"• {stitle}", fontsize=6.5, fontweight="bold", color="#713F12", va="center", zorder=4)
        ax.text(0.915, sy, sdesc, fontsize=6.2, color="#475569", va="center", zorder=4)

    # Sub-card B: Model Context Protocol (MCP) (Bottom)
    mcp_card = FancyBboxPatch((0.822, 0.085), 0.346, 0.145, boxstyle="round,pad=0.004,rounding_size=0.009",
                              facecolor="#ECFEFF", edgecolor="#67E8F9", linewidth=1.1, zorder=3)
    ax.add_patch(mcp_card)
    
    dot_mcp = Circle((0.836, 0.207), 0.0035, facecolor="#0891B2", edgecolor="none", zorder=4)
    ax.add_patch(dot_mcp)
    ax.text(0.844, 0.207, "Model Context Protocol (MCP)", fontsize=8.0, fontweight="bold", color="#0E7490", va="center", zorder=4)
    ax.text(0.844, 0.187, "Standardized client-server functions with typed JSON schemas", fontsize=6.4, color="#0891B2", va="center", zorder=4)
    
    mcp_items = [
        ("Typed Endpoints:", "Exposes query_history(), upload_dataset(), run_tool(), check_job()"),
        ("Input Validation:", "Enforces strict argument types & verifies environment states"),
        ("Deterministic I/O:", "Replaces arbitrary terminal commands with schema-validated calls")
    ]
    for m_i, (mtitle, mdesc) in enumerate(mcp_items):
        my = 0.160 - m_i * 0.024
        ax.text(0.836, my, f"• {mtitle}", fontsize=6.5, fontweight="bold", color="#155E75", va="center", zorder=4)
        ax.text(0.925, my, mdesc, fontsize=6.2, color="#475569", va="center", zorder=4)

    # -------------------------------------------------------------
    # 4. EXECUTED ACTIONS & TARGETS (Right: x = 1.225 to 1.575)
    # -------------------------------------------------------------
    box4 = FancyBboxPatch((1.225, 0.065), 0.350, 0.385, boxstyle="round,pad=0.006,rounding_size=0.014",
                          facecolor="#F0FDF4", edgecolor="#BBF7D0", linewidth=1.2, zorder=2)
    ax.add_patch(box4)
    
    ax.text(1.242, 0.425, "4. EXECUTED ACTIONS", fontsize=9.2, fontweight="bold", color="#166534", va="center")
    ax.text(1.562, 0.425, "Targets", fontsize=7.2, fontweight="bold", color="#15803D", va="center", ha="right")
    
    # Arrow from Funnel to Execution
    ax.annotate("", xy=(1.225, 0.240), xytext=(1.185, 0.240),
                arrowprops=dict(arrowstyle="-|>", color="#16A34A", lw=1.6, mutation_scale=11), zorder=6)
    
    actions = [
        ("Code Synthesis & Execution", "Writes & runs ad-hoc Python/R data parsers", "#16A34A"),
        ("Dataset Retrieval & Unpacking", "Downloads, uncompresses, and reformats files", "#0D9488"),
        ("External Web APIs", "Queries NCBI, EBI, UniProt, & Zenodo references", "#0284C7"),
        ("Public Cyberinfrastructure", "Dispatches heavy jobs to Galaxy, UDTs, & HPC", "#7C3AED")
    ]
    
    act_y_start = 0.335
    act_spacing = 0.068
    for a_i, (atitle, adesc, acolor) in enumerate(actions):
        ay = act_y_start - a_i * act_spacing
        draw_pill(ax, 1.242, ay - 0.048, 0.316, 0.058, atitle, adesc,
                  bg="#FFFFFF", border="#86EFAC" if a_i < 3 else "#DDD6FE",
                  dot_color=acolor, text_color="#0F172A", fontsize=7.5)

    # -------------------------------------------------------------
    # FEEDBACK LOOP (Bottom Curved Arrow: Actions back to Client Agent & LLM)
    # -------------------------------------------------------------
    fb_path = Path([(1.40, 0.060), (1.40, 0.018), (0.62, 0.018), (0.62, 0.060)],
                   [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4])
    patch_fb = PathPatch(fb_path, facecolor="none", edgecolor="#64748B", lw=1.3, linestyle="--", zorder=3)
    ax.add_patch(patch_fb)
    
    ax.annotate("", xy=(0.62, 0.065), xytext=(0.62, 0.040),
                arrowprops=dict(arrowstyle="-|>", color="#64748B", lw=1.4, mutation_scale=10), zorder=6)
    
    # Feedback label badge
    badge = FancyBboxPatch((0.71, 0.008), 0.60, 0.024, boxstyle="round,pad=0.002,rounding_size=0.005",
                           facecolor="#F8FAFC", edgecolor="#CBD5E1", linewidth=0.8, zorder=4)
    ax.add_patch(badge)
    ax.text(1.01, 0.020, "Closed-Loop Feedback: exit codes, stderr/stdout, logs, and outputs return to Agent & LLM for evaluation",
            fontsize=6.8, fontweight="bold", color="#334155", ha="center", va="center", zorder=5)
    
    plt.tight_layout()
    plt.savefig("/Users/anton/git/orbit-paper/manuscript/figures/figure1_agentic_flow.png", dpi=300, bbox_inches="tight")
    plt.savefig("/Users/anton/git/orbit-paper/manuscript/figures/figure1_agentic_flow.pdf", bbox_inches="tight")
    print("Agentic Flow Figure generated successfully!")

if __name__ == "__main__":
    build_agentic_flow_figure()
