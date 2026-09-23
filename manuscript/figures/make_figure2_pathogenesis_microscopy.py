#!/usr/bin/env python3
"""
Generate publication-grade Figure 2:
Cellular Pathogenesis, Microscopy, Rosetting, and Structural Architecture of P. vivax VIR Antigens.

Layout (two rows):
Row 1:
  Panel A: Brightfield Giemsa-stained thin blood smear micrograph (rosetting, Schüffner's dots).
  Panel B: Dual-channel Laser Scanning Confocal Immunofluorescence (DAPI + anti-VIR AlexaFluor 488).
  Panel C: Cellular Export Pathway and Caveola-Vesicle Complexes (CVCs).
Row 2:
  Panel D: Microvascular Endothelial Cytoadherence and Sequestration.
  Panel E: Conserved Mostly-Alpha-Helical PIR Ectodomain Fold (PDB 6ZYV) and 3Di Mapping.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Ellipse, PathPatch, Rectangle
import matplotlib.path as mpath
from PIL import Image
import numpy as np
import matplotlib as mpl

mpl.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]
mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["figure.dpi"] = 300
mpl.rcParams["savefig.dpi"] = 300
mpl.rcParams["pdf.fonttype"] = 42

def build_figure2():
    fig = plt.figure(figsize=(15.0, 9.2))
    
    # Grid specification: 2 rows
    # Row 1: Panels A, B, C
    # Row 2: Panels D, E
    
    # Outer margins
    # x: [0.03, 0.97], y: [0.04, 0.96]
    
    # -------------------------------------------------------------
    # ROW 1 (y: 0.52 to 0.95)
    # -------------------------------------------------------------
    
    # Panel A: Giemsa Light Microscopy (x: 0.03 to 0.33)
    ax_a = fig.add_axes([0.03, 0.52, 0.30, 0.42])
    im_a = Image.open("/Users/anton/git/orbit-paper/manuscript/figures/microscopy_giemsa_rosette.jpg")
    ax_a.imshow(im_a)
    ax_a.axis("off")
    # Title / label
    ax_a.text(0.02, 1.05, "a", transform=ax_a.transAxes, fontsize=15, fontweight="bold", color="#1E3A8A", va="top")
    ax_a.text(0.08, 1.05, "Giemsa-Stained Light Microscopy", transform=ax_a.transAxes,
              fontsize=10.5, fontweight="bold", color="#0F172A", va="top")
    ax_a.text(0.08, 0.99, "P. vivax trophozoite rosetting with uninfected RBCs; Schüffner's dots",
              transform=ax_a.transAxes, fontsize=8.0, fontstyle="italic", color="#475569", va="top")
    
    # Panel B: IFA Confocal Microscopy (x: 0.355 to 0.655)
    ax_b = fig.add_axes([0.355, 0.52, 0.30, 0.42])
    im_b = Image.open("/Users/anton/git/orbit-paper/manuscript/figures/microscopy_ifa_rosette.jpg")
    ax_b.imshow(im_b)
    ax_b.axis("off")
    ax_b.text(0.02, 1.05, "b", transform=ax_b.transAxes, fontsize=15, fontweight="bold", color="#1E3A8A", va="top")
    ax_b.text(0.08, 1.05, "Dual-Channel Confocal IFA", transform=ax_b.transAxes,
              fontsize=10.5, fontweight="bold", color="#0F172A", va="top")
    ax_b.text(0.08, 0.99, "DAPI (nucleus) & anti-VIR (surface puncta concentrated at contact sites)",
              transform=ax_b.transAxes, fontsize=8.0, fontstyle="italic", color="#475569", va="top")
    
    # Panel C: Ultrastructural Export Pathway (x: 0.68 to 0.97)
    ax_c = fig.add_axes([0.68, 0.52, 0.29, 0.42])
    ax_c.set_xlim(0, 1)
    ax_c.set_ylim(0, 1)
    ax_c.axis("off")
    
    box_c = FancyBboxPatch((0.01, 0.01), 0.98, 0.94, boxstyle="round,pad=0.01,rounding_size=0.03",
                           facecolor="#F8FAFC", edgecolor="#CBD5E1", linewidth=1.2, zorder=1)
    ax_c.add_patch(box_c)
    
    ax_c.text(0.03, 1.05, "c", fontsize=15, fontweight="bold", color="#1E3A8A", va="top")
    ax_c.text(0.10, 1.05, "VIR Secretory & Export Pathway", fontsize=10.5, fontweight="bold", color="#0F172A", va="top")
    ax_c.text(0.10, 0.99, "Trafficking via Caveola-Vesicle Complexes (CVCs)", fontsize=8.0, fontstyle="italic", color="#475569", va="top")
    
    # Schematic: Reticulocyte Membrane, CVCs, Parasite
    # Host membrane arc
    arc = patches.Arc((0.5, 0.1), 1.3, 1.3, theta1=45, theta2=135, color="#DC2626", lw=2.2, zorder=2)
    ax_c.add_patch(arc)
    ax_c.text(0.5, 0.77, "Host Reticulocyte Plasma Membrane", fontsize=7.2, fontweight="bold", color="#991B1B", ha="center")
    
    # Parasite boundary (lower)
    ax_c.add_patch(Ellipse((0.5, 0.18), 0.55, 0.24, facecolor="#DBEAFE", edgecolor="#2563EB", lw=1.5, zorder=3))
    ax_c.text(0.5, 0.18, "Intracellular Parasite\n(Trophozoite)", fontsize=7.5, fontweight="bold", color="#1E3A8A", ha="center", va="center", zorder=4)
    ax_c.text(0.5, 0.08, "PVM (Parasitophorous Vacuole Membrane)", fontsize=6.5, color="#1D4ED8", ha="center", zorder=4)
    
    # Caveola-vesicle complexes (Schüffner's dots in cytoplasm)
    np.random.seed(101)
    cvc_coords = [(0.32, 0.40), (0.42, 0.52), (0.50, 0.42), (0.58, 0.55), (0.68, 0.43), (0.38, 0.62), (0.62, 0.64)]
    for cx, cy in cvc_coords:
        ax_c.add_patch(Circle((cx, cy), 0.032, facecolor="#FEF3C7", edgecolor="#D97706", lw=1.2, ls="--", zorder=4))
        # inner vesicle
        ax_c.add_patch(Circle((cx, cy), 0.012, facecolor="#F59E0B", edgecolor="none", zorder=5))
        # VIR cargo dots
        ax_c.add_patch(Circle((cx+0.015, cy+0.015), 0.005, facecolor="#7C3AED", edgecolor="none", zorder=6))
        ax_c.add_patch(Circle((cx-0.015, cy-0.010), 0.005, facecolor="#7C3AED", edgecolor="none", zorder=6))
    
    ax_c.text(0.5, 0.50, "CVCs / Schüffner's Dots\n(Trafficking intermediates)",
              fontsize=7.2, fontweight="bold", color="#B45309", ha="center", va="center", zorder=7,
              bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFBEB", edgecolor="#FCD34D", lw=0.8))
    
    # Exported VIR spikes on host membrane
    for th in np.linspace(58, 122, 11):
        rad = np.radians(th)
        px = 0.5 + 0.65 * np.cos(rad)
        py = 0.1 + 0.65 * np.sin(rad)
        ax_c.add_patch(Circle((px, py), 0.012, facecolor="#7C3AED", edgecolor="#4C1D95", lw=0.9, zorder=8))
    
    ax_c.text(0.82, 0.72, "VIR surface adhesins\n(PIR ectodomains)", fontsize=6.8, fontweight="bold", color="#6D28D9", ha="left")
    
    # Arrow showing trafficking
    ax_c.annotate("", xy=(0.5, 0.72), xytext=(0.5, 0.32),
                  arrowprops=dict(arrowstyle="->", color="#4B5563", lw=1.5, ls=":"))
    
    # -------------------------------------------------------------
    # ROW 2 (y: 0.04 to 0.46)
    # -------------------------------------------------------------
    
    # Panel D: Endothelial Cytoadherence & Sequestration (x: 0.03 to 0.48)
    ax_d = fig.add_axes([0.03, 0.04, 0.45, 0.40])
    ax_d.set_xlim(0, 1)
    ax_d.set_ylim(0, 1)
    ax_d.axis("off")
    
    box_d = FancyBboxPatch((0.01, 0.01), 0.98, 0.94, boxstyle="round,pad=0.01,rounding_size=0.03",
                           facecolor="#F8FAFC", edgecolor="#CBD5E1", linewidth=1.2, zorder=1)
    ax_d.add_patch(box_d)
    
    ax_d.text(0.02, 1.05, "d", fontsize=15, fontweight="bold", color="#1E3A8A", va="top")
    ax_d.text(0.08, 1.05, "Microvascular Cytoadherence & Immune Sequestration",
              fontsize=10.5, fontweight="bold", color="#0F172A", va="top")
    ax_d.text(0.08, 0.99, "Binding endothelial receptors (ICAM-1, CD36) prevents splenic mechanical clearance",
              fontsize=8.0, fontstyle="italic", color="#475569", va="top")
    
    # Endothelial layer
    ey = 0.22
    ax_d.add_patch(Rectangle((0.05, 0.06), 0.90, 0.14, facecolor="#E2E8F0", edgecolor="#94A3B8", lw=1.1, zorder=2))
    for nx in [0.18, 0.42, 0.66, 0.88]:
        ax_d.add_patch(Ellipse((nx, 0.13), 0.12, 0.06, facecolor="#64748B", edgecolor="none", zorder=3))
    ax_d.text(0.50, 0.12, "Vascular Endothelium (Deep Post-Capillary Venule)", fontsize=7.5, fontweight="bold", color="#FFFFFF", ha="center", zorder=4)
    
    # Endothelial receptors
    for rx in np.linspace(0.12, 0.88, 15):
        ax_d.plot([rx, rx], [0.20, 0.28], color="#0284C7", lw=2.2, zorder=4)
        ax_d.add_patch(Circle((rx, 0.28), 0.012, facecolor="#0284C7", edgecolor="none", zorder=5))
    ax_d.text(0.88, 0.32, "Host Receptors\n(ICAM-1 / CD36)", fontsize=7.0, fontweight="bold", color="#0369A1", ha="center", va="bottom", zorder=6)
    
    # Sequestered infected reticulocyte
    ax_d.add_patch(Ellipse((0.45, 0.52), 0.42, 0.26, angle=2, facecolor="#FEF3C7", edgecolor="#D97706", lw=1.6, zorder=5))
    # Trophozoite inside
    ax_d.add_patch(Ellipse((0.44, 0.53), 0.20, 0.12, facecolor="#93C5FD", edgecolor="#2563EB", lw=1.2, zorder=6))
    ax_d.add_patch(Circle((0.46, 0.55), 0.024, facecolor="#DC2626", edgecolor="none", zorder=7))
    ax_d.text(0.44, 0.53, "Sequestered\niRBC", fontsize=7.5, fontweight="bold", color="#1E3A8A", ha="center", va="center", zorder=8)
    
    # Schüffner's dots in sequestered cell
    for _ in range(25):
        sx = 0.45 + np.random.uniform(-0.16, 0.16)
        sy = 0.52 + np.random.uniform(-0.09, 0.09)
        if ((sx-0.45)/0.19)**2 + ((sy-0.52)/0.11)**2 < 0.8:
            ax_d.add_patch(Circle((sx, sy), 0.005, facecolor="#F59E0B", edgecolor="none", zorder=7))
            
    # VIR adhesins engaging endothelial receptors
    for vx in np.linspace(0.32, 0.58, 6):
        ax_d.plot([vx, vx], [0.39, 0.28], color="#7C3AED", lw=2.4, zorder=6)
        ax_d.add_patch(Circle((vx, 0.28), 0.010, facecolor="#7C3AED", edgecolor="none", zorder=7))
        
    ax_d.text(0.10, 0.82, "• Cytoadherence prevents splenic filtration\n• Rosetting causes microvascular hypoperfusion\n• Clinical severity: severe anemia & acute lung injury (ARDS)",
              fontsize=7.4, color="#334155", va="top", zorder=8)
    
    # Panel E: Conserved Fold PDB 6ZYV & 3Di Structural Alphabet (x: 0.52 to 0.97)
    ax_e = fig.add_axes([0.52, 0.04, 0.45, 0.40])
    ax_e.set_xlim(0, 1)
    ax_e.set_ylim(0, 1)
    ax_e.axis("off")
    
    box_e = FancyBboxPatch((0.01, 0.01), 0.98, 0.94, boxstyle="round,pad=0.01,rounding_size=0.03",
                           facecolor="#F8FAFC", edgecolor="#CBD5E1", linewidth=1.2, zorder=1)
    ax_e.add_patch(box_e)
    
    ax_e.text(0.02, 1.05, "e", fontsize=15, fontweight="bold", color="#1E3A8A", va="top")
    ax_e.text(0.08, 1.05, "Conserved PIR Ectodomain Fold & 3Di Structural Alphabet",
              fontsize=10.5, fontweight="bold", color="#0F172A", va="top")
    ax_e.text(0.08, 0.99, "PDB 6ZYV: rigid helical bundle bridges the sequence twilight zone",
              fontsize=8.0, fontstyle="italic", color="#475569", va="top")
    
    # Schematic of 4-helix bundle
    py = 0.46
    helix_coords = [
        (0.12, py - 0.22, 0.12, py + 0.18, "Helix 1"),
        (0.20, py + 0.18, 0.20, py - 0.22, "Helix 2"),
        (0.28, py - 0.22, 0.28, py + 0.18, "Helix 3"),
        (0.36, py + 0.18, 0.36, py - 0.18, "Helix 4")
    ]
    for x1, y1, x2, y2, hname in helix_coords:
        ax_e.add_patch(FancyBboxPatch((x1 - 0.025, min(y1, y2)), 0.050, abs(y2 - y1),
                                     boxstyle="round,pad=0.004,rounding_size=0.015",
                                     facecolor="#D1FAE5", edgecolor="#059669", lw=1.4, zorder=4))
        y_steps = np.linspace(min(y1, y2) + 0.03, max(y1, y2) - 0.03, 7)
        for ys in y_steps:
            ax_e.plot([x1 - 0.020, x1 + 0.020], [ys - 0.015, ys + 0.015], color="#047857", lw=1.4, zorder=5)
            
    # Loops
    ax_e.plot([0.12, 0.16, 0.20], [py + 0.18, py + 0.23, py + 0.18], color="#D97706", lw=1.8, zorder=4)
    ax_e.plot([0.20, 0.24, 0.28], [py - 0.22, py - 0.26, py - 0.22], color="#D97706", lw=1.8, zorder=4)
    ax_e.plot([0.28, 0.32, 0.36], [py + 0.18, py + 0.23, py + 0.18], color="#D97706", lw=1.8, zorder=4)
    
    # Hypervariable loop
    ax_e.add_patch(Ellipse((0.24, py + 0.26), 0.18, 0.08, facecolor="#FEE2E2", edgecolor="#EF4444", lw=1.2, ls="--", zorder=6))
    ax_e.text(0.24, py + 0.26, "Hyper-variable Surface Loops\n(Mutational hotspot / immune evasion)",
              fontsize=6.5, fontweight="bold", color="#B91C1C", ha="center", va="center", zorder=7)
    
    # Explanatory callouts on right
    ax_e.text(0.48, 0.74, "Structural Homology vs Sequence Twilight Zone:", fontsize=8.0, fontweight="bold", color="#0F172A")
    ax_e.text(0.48, 0.58,
              "• Sequence Identity: Median ~32% within FS_001\n"
              "  (indistinguishable from sequence twilight noise)\n"
              "• ProstT5 Transformer: Predicts 20-state 3Di backbone\n"
              "  conformation directly from amino acid FASTA\n"
              "• Foldseek Clustering: Unifies 146 sequence\n"
              "  subfamilies into 73 structural classes\n"
              "• Dominant Fold (FS_001): Encompasses 46% of all\n"
              "  VIRs across Indonesia, Thailand, and Peru",
              fontsize=7.2, color="#334155", va="center")
    
    # Bottom comparison bar
    bar_y = 0.18
    ax_e.add_patch(Rectangle((0.48, bar_y), 0.22, 0.12, facecolor="#EFF6FF", edgecolor="#3B82F6", lw=1.0, zorder=2))
    ax_e.text(0.59, bar_y + 0.08, "Sequence Baseline (MCL)", fontsize=6.8, fontweight="bold", color="#1E40AF", ha="center")
    ax_e.text(0.59, bar_y + 0.03, "146 subfamilies (over-split)", fontsize=6.5, color="#2563EB", ha="center")
    
    ax_e.add_patch(Rectangle((0.73, bar_y), 0.22, 0.12, facecolor="#ECFDF5", edgecolor="#10B981", lw=1.0, zorder=2))
    ax_e.text(0.84, bar_y + 0.08, "Structural Fold (Foldseek)", fontsize=6.8, fontweight="bold", color="#065F46", ha="center")
    ax_e.text(0.84, bar_y + 0.03, "73 classes (50% reduction)", fontsize=6.5, color="#059669", ha="center")
    
    plt.savefig("/Users/anton/git/orbit-paper/manuscript/figures/figure2_pathogenesis_microscopy.png", dpi=300, bbox_inches="tight")
    plt.savefig("/Users/anton/git/orbit-paper/manuscript/figures/figure2_pathogenesis_microscopy.pdf", bbox_inches="tight")
    print("Figure 2 successfully generated!")

if __name__ == "__main__":
    build_figure2()
