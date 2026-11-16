#!/usr/bin/env python3
"""
Generate Supplementary Figure S2 (figure_s2_architecture.{pdf,png}) as a crisp
vector PDF matching the four-part Galactic plane schematic (Agent, MCP Server
& Skills, UI: Validation and Provenance, Public cyberinfrastructure & Tools/Data).
"""
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from PIL import Image

plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42

HERE = Path(__file__).resolve().parent


def draw_shadow_box(
    ax,
    x: float,
    y: float,
    w: float,
    h: float,
    facecolor: str,
    edgecolor: str = "none",
    lw: float = 0.8,
    rounding: float = 0.022,
    zorder: int = 2,
) -> None:
    shadow = FancyBboxPatch(
        (x + 0.004, y - 0.007),
        w,
        h,
        boxstyle=f"round,pad=0,rounding_size={rounding}",
        facecolor="#00000018",
        edgecolor="none",
        zorder=zorder - 1,
    )
    ax.add_patch(shadow)
    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad=0,rounding_size={rounding}",
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=lw,
        zorder=zorder,
    )
    ax.add_patch(box)


def draw_cylinder(ax, cx: float, cy: float, w: float, h: float, zorder: int = 4) -> None:
    top_h = h * 0.28
    y_bot = cy - h / 2 + top_h / 2
    y_top = cy + h / 2 - top_h / 2
    rect = mpatches.Rectangle(
        (cx - w / 2, y_bot),
        w,
        y_top - y_bot,
        facecolor="#cfd4d8",
        edgecolor="none",
        zorder=zorder,
    )
    bot_fill = mpatches.Ellipse(
        (cx, y_bot),
        w,
        top_h,
        facecolor="#cfd4d8",
        edgecolor="none",
        zorder=zorder,
    )
    bot = mpatches.Arc(
        (cx, y_bot),
        w,
        top_h,
        angle=0,
        theta1=180,
        theta2=360,
        edgecolor="#222222",
        linewidth=0.9,
        zorder=zorder + 1,
    )
    ax.add_patch(bot_fill)
    ax.add_patch(rect)
    ax.plot([cx - w / 2, cx - w / 2], [y_bot, y_top], color="#222222", linewidth=0.9, zorder=zorder + 1)
    ax.plot([cx + w / 2, cx + w / 2], [y_bot, y_top], color="#222222", linewidth=0.9, zorder=zorder + 1)
    ax.add_patch(bot)
    top = mpatches.Ellipse(
        (cx, y_top),
        w,
        top_h,
        facecolor="#e2e6ea",
        edgecolor="#222222",
        linewidth=0.9,
        zorder=zorder + 2,
    )
    ax.add_patch(top)
    ax.text(
        cx,
        (y_bot + y_top) / 2 - top_h * 0.08,
        "storage",
        ha="center",
        va="center",
        fontsize=6.6,
        color="#111827",
        zorder=zorder + 3,
    )


def curved_double_arrow(
    ax,
    p1: tuple[float, float],
    p2: tuple[float, float],
    rad: float = 0.0,
    zorder: int = 5,
) -> None:
    arr = FancyArrowPatch(
        p1,
        p2,
        connectionstyle=f"arc3,rad={rad}",
        arrowstyle="<|-|>,head_length=5.5,head_width=3.2",
        linewidth=1.35,
        color="#4b5563",
        zorder=zorder,
    )
    ax.add_patch(arr)


def main() -> None:
    fig, ax = plt.subplots(figsize=(11.2, 6.3), dpi=300)
    fig.patch.set_facecolor("white")
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.0)
    ax.axis("off")

    # 1. Agent (top-left)
    draw_shadow_box(ax, 0.02, 0.70, 0.48, 0.25, facecolor="#dcead3", rounding=0.024)
    ax.text(
        0.26,
        0.855,
        "Agent",
        ha="center",
        va="center",
        fontsize=21,
        fontweight="bold",
        color="#0b0f19",
        zorder=4,
    )
    ax.text(
        0.26,
        0.785,
        "(Orbit, OpenCode, Claude Code, Codex, Agy, ...)",
        ha="center",
        va="center",
        fontsize=11.0,
        color="#111827",
        zorder=4,
    )

    # 2. MCP Server & Skills (middle-left)
    draw_shadow_box(ax, 0.02, 0.41, 0.228, 0.165, facecolor="#f9e2c7", rounding=0.020)
    ax.text(
        0.134,
        0.492,
        "MCP Server",
        ha="center",
        va="center",
        fontsize=12.5,
        fontweight="medium",
        color="#111827",
        zorder=4,
    )

    draw_shadow_box(ax, 0.272, 0.41, 0.228, 0.165, facecolor="#f5c690", rounding=0.020)
    ax.text(
        0.386,
        0.492,
        "Skills",
        ha="center",
        va="center",
        fontsize=12.5,
        fontweight="medium",
        color="#111827",
        zorder=4,
    )

    # 3. UI: Validation and Provenance (top-right)
    draw_shadow_box(ax, 0.57, 0.41, 0.41, 0.54, facecolor="#fae3c6", rounding=0.024)
    ax.text(
        0.775,
        0.902,
        "UI: Validation and Provenance",
        ha="center",
        va="center",
        fontsize=13.2,
        fontweight="bold",
        color="#0b0f19",
        zorder=4,
    )

    # Embed high-resolution Galaxy Workflow Editor capture (1920x1200)
    hi_res_png = HERE / "data" / "bacillus" / "native_editor_orange_mismatch.png"
    if hi_res_png.exists():
        inset = Image.open(hi_res_png)
        ax.imshow(
            inset,
            extent=(0.608, 0.942, 0.448, 0.850),
            aspect="auto",
            interpolation="lanczos",
            zorder=4,
        )
        frame = mpatches.Rectangle(
            (0.608, 0.448),
            0.942 - 0.608,
            0.850 - 0.448,
            fill=False,
            edgecolor="#9ca3af",
            linewidth=0.7,
            zorder=5,
        )
        ax.add_patch(frame)

    # 4. Public cyberinfrastructure (bottom-left)
    draw_shadow_box(ax, 0.02, 0.055, 0.49, 0.215, facecolor="#b8babc", rounding=0.018)
    ax.text(
        0.265,
        0.228,
        "Public cyberinfrastructure",
        ha="center",
        va="center",
        fontsize=12.8,
        color="#0b0f19",
        zorder=4,
    )
    draw_cylinder(ax, 0.090, 0.125, 0.058, 0.090, zorder=4)
    draw_cylinder(ax, 0.162, 0.125, 0.058, 0.090, zorder=4)

    draw_shadow_box(
        ax,
        0.228,
        0.080,
        0.098,
        0.092,
        facecolor="#eeaa61",
        edgecolor="#9a5b13",
        lw=0.8,
        rounding=0.008,
        zorder=4,
    )
    ax.text(
        0.277,
        0.126,
        "CPUs",
        ha="center",
        va="center",
        fontsize=11.5,
        fontweight="medium",
        color="#0b0f19",
        zorder=5,
    )

    draw_shadow_box(
        ax,
        0.356,
        0.080,
        0.098,
        0.092,
        facecolor="#db6863",
        edgecolor="#8f2d2a",
        lw=0.8,
        rounding=0.008,
        zorder=4,
    )
    ax.text(
        0.405,
        0.126,
        "GPUs",
        ha="center",
        va="center",
        fontsize=11.5,
        fontweight="medium",
        color="#0b0f19",
        zorder=5,
    )

    # 5. Tools / Data (bottom-right)
    draw_shadow_box(ax, 0.545, 0.055, 0.435, 0.215, facecolor="#cccccc", rounding=0.018)
    ax.text(
        0.7625,
        0.228,
        "Tools / Data",
        ha="center",
        va="center",
        fontsize=12.8,
        color="#0b0f19",
        zorder=4,
    )

    sub_specs = [
        (0.558, "Tools /\nContainers", "#f7ebc1", "#8c7a3b"),
        (0.665, "Workflows", "#fae194", "#8c7223"),
        (0.772, "Data\n(NCBI ...)", "#e59994", "#8c3f3a"),
        (0.879, "Models", "#9ec4e6", "#376187"),
    ]
    for sx, slabel, sfc, sec in sub_specs:
        draw_shadow_box(
            ax,
            sx,
            0.080,
            0.094,
            0.092,
            facecolor=sfc,
            edgecolor=sec,
            lw=0.75,
            rounding=0.006,
            zorder=4,
        )
        ax.text(
            sx + 0.047,
            0.126,
            slabel,
            ha="center",
            va="center",
            fontsize=8.8,
            color="#0b0f19",
            zorder=5,
        )

    # 6. Connectors
    curved_double_arrow(ax, (0.26, 0.70), (0.134, 0.575), rad=0.14)
    curved_double_arrow(ax, (0.26, 0.70), (0.386, 0.575), rad=-0.14)
    curved_double_arrow(ax, (0.134, 0.41), (0.265, 0.270), rad=-0.16)
    curved_double_arrow(ax, (0.386, 0.41), (0.265, 0.270), rad=0.16)
    curved_double_arrow(ax, (0.265, 0.270), (0.775, 0.41), rad=-0.06)
    curved_double_arrow(ax, (0.510, 0.162), (0.545, 0.162), rad=0.0)

    fig.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99)
    out_pdf = HERE / "figure_s2_architecture.pdf"
    out_png = HERE / "figure_s2_architecture.png"
    plt.savefig(out_pdf, dpi=300, bbox_inches="tight")
    plt.savefig(out_png, dpi=300, bbox_inches="tight")
    print(f"Saved {out_pdf} and {out_png}")


if __name__ == "__main__":
    main()
