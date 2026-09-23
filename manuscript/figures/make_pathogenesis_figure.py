#!/usr/bin/env python3
"""
Generate a publication-grade cellular pathogenesis and rosetting schematic
for the Plasmodium vivax PIR/VIR case study in Nature / Nature Biotechnology.
Illustrates:
1. Infected reticulocyte cellular morphology with P. vivax ameboid trophozoite and Schuffner's dots.
2. Export of VIR proteins to the host erythrocyte membrane.
3. Multicellular rosetting (adhesion of uninfected erythrocytes).
4. Endothelial cytoadherence and microvascular sequestration.
5. Conserved mostly-alpha-helical structural ectodomain fold (PDB 6ZYV).
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Ellipse, PathPatch, FancyArrowPatch, Rectangle
import matplotlib.path as mpath
import numpy as np
import matplotlib as mpl

mpl.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]
mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["figure.dpi"] = 300
mpl.rcParams["savefig.dpi"] = 300
mpl.rcParams["pdf.fonttype"] = 42

def generate_pathogenesis_figure():
    fig, ax = plt.subplots(figsize=(13.5, 6.2))
    ax.set_xlim(0.0, 1.35)
    ax.set_ylim(0.0, 0.95)
    ax.axis("off")

    # Background panel frames
    # Left Panel: Cellular Rosetting & VIR Export (x: 0.03 to 0.72)
    # Right Panel: Endothelial Cytoadherence & Structural Fold (x: 0.76 to 1.32)
    
    # -------------------------------------------------------------
    # PANEL A: Cellular Rosetting and Surface Export
    # -------------------------------------------------------------
    f1 = FancyBboxPatch((0.025, 0.03), 0.70, 0.89,
                        boxstyle="round,pad=0.01,rounding_size=0.018",
                        facecolor="#FBFDFF", edgecolor="#BFDBFE", linewidth=1.2, zorder=1)
    ax.add_patch(f1)
    
    # Header A
    ax.text(0.045, 0.885, "A", fontsize=14, fontweight="bold", color="#1E3A8A", va="center")
    ax.text(0.075, 0.885, "Cellular Phenotype: VIR Export & Multicellular Rosetting",
            fontsize=10.5, fontweight="bold", color="#0F172A", va="center")
    ax.text(0.075, 0.860, "Infected erythrocyte binds uninfected red blood cells, driving microvascular obstruction",
            fontsize=7.8, fontstyle="italic", color="#64748B", va="center")

    # Center of Infected Erythrocyte
    cx, cy = 0.36, 0.46
    
    # Draw uninfected RBCs adhering in a rosette around the central infected cell
    rosette_angles = [0.15, 0.95, 1.85, 2.75, 3.65, 4.55, 5.45]
    r_dist = 0.225
    for angle in rosette_angles:
        rx = cx + r_dist * np.cos(angle)
        ry = cy + r_dist * np.sin(angle)
        # Biconcave RBC shape
        rbc = Ellipse((rx, ry), 0.165, 0.125, angle=np.degrees(angle)+90,
                      facecolor="#FCA5A5", edgecolor="#DC2626", linewidth=1.1, alpha=0.85, zorder=2)
        ax.add_patch(rbc)
        # Inner dimple
        dimple = Ellipse((rx, ry), 0.08, 0.055, angle=np.degrees(angle)+90,
                         facecolor="#EF4444", edgecolor="none", alpha=0.35, zorder=3)
        ax.add_patch(dimple)
        ax.text(rx, ry, "Uninfected\nRBC", fontsize=6.2, fontweight="bold", color="#7F1D1D",
                ha="center", va="center", zorder=4)

    # Central Infected Erythrocyte (enlarged reticulocyte, pale stippled)
    irbc = Ellipse((cx, cy), 0.25, 0.21, angle=15,
                   facecolor="#FEF3C7", edgecolor="#D97706", linewidth=1.5, zorder=4)
    ax.add_patch(irbc)

    # Schuffner's dots (stippling / caveola-vesicle complexes)
    np.random.seed(42)
    for _ in range(45):
        sx = cx + np.random.uniform(-0.09, 0.09)
        sy = cy + np.random.uniform(-0.07, 0.07)
        if ((sx - cx)/0.11)**2 + ((sy - cy)/0.09)**2 < 0.85:
            dot = Circle((sx, sy), 0.0022, facecolor="#F59E0B", edgecolor="none", zorder=5)
            ax.add_patch(dot)

    # Ameboid P. vivax trophozoite (irregular cytoplasm with food vacuole & chromatin dot)
    t_path_data = [
        (mpath.Path.MOVETO, (cx - 0.05, cy - 0.01)),
        (mpath.Path.CURVE4, (cx - 0.07, cy + 0.04)),
        (mpath.Path.CURVE4, (cx - 0.02, cy + 0.06)),
        (mpath.Path.CURVE4, (cx + 0.03, cy + 0.04)),
        (mpath.Path.CURVE4, (cx + 0.06, cy + 0.02)),
        (mpath.Path.CURVE4, (cx + 0.05, cy - 0.04)),
        (mpath.Path.CURVE4, (cx + 0.01, cy - 0.05)),
        (mpath.Path.CURVE4, (cx - 0.04, cy - 0.04)),
        (mpath.Path.CLOSEPOLY, (cx - 0.05, cy - 0.01))
    ]
    codes, verts = zip(*t_path_data)
    t_path = mpath.Path(verts, codes)
    t_patch = PathPatch(t_path, facecolor="#93C5FD", edgecolor="#2563EB", linewidth=1.3, zorder=6)
    ax.add_patch(t_patch)

    # Parasite chromatin dot (nucleus)
    chrom = Circle((cx + 0.015, cy + 0.025), 0.013, facecolor="#DC2626", edgecolor="#991B1B", linewidth=0.8, zorder=7)
    ax.add_patch(chrom)
    ax.text(cx + 0.015, cy + 0.025, "N", fontsize=6.5, fontweight="bold", color="#FFFFFF", ha="center", va="center", zorder=8)

    # Pigment granule (hemozoin)
    hz = Circle((cx - 0.02, cy - 0.02), 0.008, facecolor="#78350F", edgecolor="none", zorder=7)
    ax.add_patch(hz)

    # Surface VIR proteins (small spikes/Y-shapes on infected RBC membrane mediating rosetting)
    for ang in np.linspace(0, 2*np.pi, 24, endpoint=False):
        vx = cx + 0.125 * np.cos(ang)
        vy = cy + 0.105 * np.sin(ang)
        spike = Circle((vx, vy), 0.004, facecolor="#7C3AED", edgecolor="#4C1D95", linewidth=0.7, zorder=9)
        ax.add_patch(spike)

    # Labels inside Panel A
    ax.text(cx, cy - 0.075, "P. vivax Infected\nReticulocyte", fontsize=7.2, fontweight="bold",
            color="#92400E", ha="center", va="center", zorder=8)
    
    # Legend Callout for VIR surface antigens
    ax.plot([cx + 0.12, 0.60], [cy + 0.08, cy + 0.14], color="#7C3AED", lw=1.0, ls="--", zorder=10)
    ax.text(0.60, cy + 0.15, "Exported VIR proteins\n(Antigenic Variation & Rosetting)",
            fontsize=7.2, fontweight="bold", color="#6D28D9", va="center", zorder=10)

    # Callout for Schuffner's dots
    ax.plot([cx - 0.06, 0.12], [cy + 0.03, cy + 0.18], color="#D97706", lw=1.0, ls="--", zorder=10)
    ax.text(0.12, cy + 0.19, "Schüffner's dots\n(Caveola-vesicle complexes)",
            fontsize=7.2, fontweight="bold", color="#B45309", ha="right", va="center", zorder=10)

    # Bottom annotation in Panel A
    p_box = FancyBboxPatch((0.05, 0.055), 0.65, 0.075,
                           boxstyle="round,pad=0.004,rounding_size=0.008",
                           facecolor="#FFFFFF", edgecolor="#E2E8F0", linewidth=0.9, zorder=5)
    ax.add_patch(p_box)
    ax.text(0.375, 0.092,
            "Rosetting Frequency: High rosetting strains correlate with severe anemia, respiratory distress (ARDS), and microvascular blockade.",
            fontsize=7.2, color="#334155", ha="center", va="center", zorder=6)

    # -------------------------------------------------------------
    # PANEL B: Endothelial Cytoadherence & Conserved Fold (PDB 6ZYV)
    # -------------------------------------------------------------
    f2 = FancyBboxPatch((0.745, 0.03), 0.58, 0.89,
                        boxstyle="round,pad=0.01,rounding_size=0.018",
                        facecolor="#FBFDFF", edgecolor="#CBD5E1", linewidth=1.2, zorder=1)
    ax.add_patch(f2)

    # Header B
    ax.text(0.765, 0.885, "B", fontsize=14, fontweight="bold", color="#1E3A8A", va="center")
    ax.text(0.795, 0.885, "Pathogenesis & Structural Unification",
            fontsize=10.5, fontweight="bold", color="#0F172A", va="center")
    ax.text(0.795, 0.860, "Conserved mostly-alpha-helical fold mediates receptor cytoadherence",
            fontsize=7.8, fontstyle="italic", color="#64748B", va="center")

    # Sub-panel 1: Endothelial Cytoadherence (Top half of Panel B)
    # Blood vessel lumen and endothelial wall
    ey = 0.53
    # Endothelial cells (base layer)
    ax.add_patch(Rectangle((0.765, ey - 0.04), 0.54, 0.04, facecolor="#E2E8F0", edgecolor="#94A3B8", linewidth=1.0, zorder=2))
    # Nuclei of endothelial cells
    for ex in [0.82, 0.95, 1.08, 1.21]:
        ax.add_patch(Ellipse((ex, ey - 0.02), 0.05, 0.018, facecolor="#64748B", edgecolor="none", zorder=3))
    ax.text(1.035, ey - 0.02, "Vascular Endothelium (Deep Capillary Bed)", fontsize=7.0, fontweight="bold",
            color="#FFFFFF", ha="center", va="center", zorder=4)

    # Endothelial host receptors (ICAM-1, CD36, CSA)
    for rx in np.linspace(0.79, 1.26, 11):
        ax.plot([rx, rx], [ey, ey + 0.025], color="#0284C7", lw=2.0, zorder=3)
        ax.add_patch(Circle((rx, ey + 0.025), 0.005, facecolor="#0284C7", edgecolor="none", zorder=4))
    ax.text(1.27, ey + 0.015, "Host Receptors\n(ICAM-1 / CD36)", fontsize=6.8, fontweight="bold",
            color="#0369A1", va="center", zorder=5)

    # Sequestrated Infected Erythrocyte adhering to endothelium
    ax.add_patch(Ellipse((0.98, ey + 0.09), 0.22, 0.11, angle=-5,
                         facecolor="#FEF3C7", edgecolor="#D97706", linewidth=1.4, zorder=5))
    # Parasite inside adhering cell
    ax.add_patch(Ellipse((0.97, ey + 0.09), 0.09, 0.05, angle=-5, facecolor="#93C5FD", edgecolor="#2563EB", lw=1.0, zorder=6))
    ax.add_patch(Circle((0.98, ey + 0.10), 0.010, facecolor="#DC2626", edgecolor="none", zorder=7))
    ax.text(0.98, ey + 0.09, "Sequestered\niRBC", fontsize=6.8, fontweight="bold", color="#1E3A8A", ha="center", va="center", zorder=8)

    # VIR Ligands engaging host receptors
    for vx in [0.91, 0.94, 0.97, 1.00, 1.03, 1.06]:
        ax.plot([vx, vx], [ey + 0.035, ey + 0.025], color="#7C3AED", lw=2.2, zorder=6)
        ax.add_patch(Circle((vx, ey + 0.025), 0.004, facecolor="#7C3AED", edgecolor="none", zorder=7))

    ax.text(0.77, ey + 0.12, "Cytoadherence prevents splenic filtration\nand triggers microvascular inflammation",
            fontsize=7.2, color="#334155", va="center", zorder=8)

    # Sub-panel 2: PDB 6ZYV Structural Fold Schematic (Bottom half of Panel B)
    py = 0.22
    # Structural Box
    s_box = FancyBboxPatch((0.765, 0.055), 0.54, 0.38,
                           boxstyle="round,pad=0.006,rounding_size=0.010",
                           facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=0.9, zorder=2)
    ax.add_patch(s_box)

    ax.text(0.785, 0.405, "Conserved PIR Ectodomain Fold (Harrison & Higgins, PDB 6ZYV)",
            fontsize=8.0, fontweight="bold", color="#0F172A", va="center", zorder=4)

    # Schematic representation of 6ZYV mostly-alpha-helical bundle
    # Draw 4 canonical antiparallel alpha-helices with connecting loops
    helix_coords = [
        (0.83, py - 0.09, 0.83, py + 0.09, "#059669", "Helix 1"),
        (0.88, py + 0.09, 0.88, py - 0.09, "#059669", "Helix 2"),
        (0.93, py - 0.09, 0.93, py + 0.09, "#059669", "Helix 3"),
        (0.98, py + 0.09, 0.98, py - 0.07, "#059669", "Helix 4")
    ]
    for x1, y1, x2, y2, c, hname in helix_coords:
        # Draw cylinders / coils
        ax.add_patch(FancyBboxPatch((x1 - 0.015, min(y1, y2)), 0.030, abs(y2 - y1),
                                   boxstyle="round,pad=0.002,rounding_size=0.008",
                                   facecolor="#D1FAE5", edgecolor="#059669", linewidth=1.2, zorder=4))
        # Spiral lines representing alpha-helices
        y_steps = np.linspace(min(y1, y2) + 0.02, max(y1, y2) - 0.02, 6)
        for ys in y_steps:
            ax.plot([x1 - 0.012, x1 + 0.012], [ys - 0.01, ys + 0.01], color="#047857", lw=1.2, zorder=5)

    # Connecting loops
    ax.plot([0.83, 0.855, 0.88], [py + 0.09, py + 0.115, py + 0.09], color="#D97706", lw=1.5, zorder=4)
    ax.plot([0.88, 0.905, 0.93], [py - 0.09, py - 0.115, py - 0.09], color="#D97706", lw=1.5, zorder=4)
    ax.plot([0.93, 0.955, 0.98], [py + 0.09, py + 0.115, py + 0.09], color="#D97706", lw=1.5, zorder=4)

    # Variable loop / hyper-variable antigenic tip
    ax.add_patch(Ellipse((0.905, py + 0.125), 0.09, 0.035, facecolor="#FEE2E2", edgecolor="#EF4444", lw=1.1, ls="--", zorder=6))
    ax.text(0.905, py + 0.125, "Hyper-variable Surface Loops\n(Immune Evasion / Divergence)",
            fontsize=6.2, fontweight="bold", color="#B91C1C", ha="center", va="center", zorder=7)

    # Structural Callout text on right of helices
    ax.text(1.03, py + 0.06, "• Rigid $\\alpha$-helical bundle\n  preserved across family",
            fontsize=7.0, fontweight="bold", color="#065F46", va="center", zorder=5)
    ax.text(1.03, py - 0.01, "• 3Di structural alphabet\n  captures backbone states",
            fontsize=7.0, color="#334155", va="center", zorder=5)
    ax.text(1.03, py - 0.07, "• Explains unification:\n  73 structural classes vs\n  146 sequence subfamilies",
            fontsize=7.0, color="#1E40AF", va="center", zorder=5)

    plt.tight_layout()
    plt.savefig("/Users/anton/git/orbit-paper/manuscript/figures/fig_pathogenesis_rosetting.png", dpi=300, bbox_inches="tight")
    plt.savefig("/Users/anton/git/orbit-paper/manuscript/figures/fig_pathogenesis_rosetting.pdf", bbox_inches="tight")
    print("Pathogenesis & rosetting figure created successfully!")

if __name__ == "__main__":
    generate_pathogenesis_figure()
