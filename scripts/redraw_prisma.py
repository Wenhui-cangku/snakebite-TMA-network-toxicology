# -*- coding: utf-8 -*-
"""Redraw the PRISMA Phase 1 two-line flowchart (final version with CTD merged)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot
setup_plot()
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = Path(__file__).resolve().parents[1] / "00_protocol" / "PRISMA_flowchart_phase1_filled.png"

fig, ax = plt.subplots(figsize=(8.6, 10.0), dpi=200)
ax.set_xlim(0, 100); ax.set_ylim(0, 118); ax.axis("off")

def box(x, y, w, h, text, fc, ec, fs=7.8, tc="black"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2",
                                fc=fc, ec=ec, lw=1.2))
    ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=fs, color=tc, linespacing=1.5)

def arrow(x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=13, color="#555555", lw=1.1))

ax.text(50, 116, "Fig. S0-4   Toxin & disease-gene screening workflow (PRISMA-style, Phase 1 two-line final measured version, 2026-09-22)",
        ha="center", fontsize=10.5, weight="bold")

# ---- line A: toxins ----
ax.text(26, 110.5, "A. Toxin library line (completed)", ha="center", fontsize=9.5, weight="bold", color="#8B1A1A")
box(5, 99, 42, 10, "UniProt main retrieval 52 + supplementary 32\n(Kunitz 24 / CRISP 4 / SVMP·Dis 3 / VZ gap-fill 1)\n(siamensis separate export: 28 entries, fully overlapping)", "#FDECEC", "#B22222")
box(5, 86, 42, 9, "Merged & deduplicated (by accession)\nn = 79", "#FDECEC", "#B22222")
box(5, 73, 42, 9, "Removed 16 fragments <30 aa\nexcluded 4 ADAM-like host contaminants", "#E8F0FE", "#1A56C4")
box(5, 59, 42, 10.5, "Archived toxins n = 63, all nine families present\n90% clustering → 40 cluster representatives\nabundance weights back-filled", "#F3E8FD", "#7B1FA2")
arrow(26, 98.6, 26, 95.4); arrow(26, 85.6, 26, 82.4); arrow(26, 72.6, 26, 69.9)

# ---- line B: disease genes ----
ax.text(74, 110.5, "B. Disease gene-set line (completed)", ha="center", fontsize=9.5, weight="bold", color="#1A56C4")
box(53, 97.5, 42, 11.5,
    "GeneCards manual export (6 queries) n = 1356\nOpen Targets (8 MONDO entries) n = 741\nDISEASES curated ∪ DisGeNET (16 CUIs, 46 genes)\nCTD (6-query whitelist) ∪ OMIM (14 phenotypes, 15 genes)",
    "#E8F0FE", "#1A56C4", fs=7.4)
box(53, 85, 42, 8.5, "mygene standardized mapping (human)\nsymbol → UniProt AC", "#E8F0FE", "#1A56C4")
box(53, 72, 42, 9.5, "Merged & deduplicated n = 2190\n(incl. 9 forcibly included by four-axis prior)", "#E8F0FE", "#1A56C4")
box(53, 57.5, 42, 11, "Stratified: core 1042 / wide 1148\n(GeneCards ≥per-query median ∪ OT≥0.3 ∪\n≥3 diseases ∪ curated ∪ CTD direct ∪ prior)\nfour-axis prior 27/27 in core set ✓", "#E6F4EA", "#1E7E34", fs=7.4)
arrow(74, 97.1, 74, 93.9); arrow(74, 84.6, 74, 81.9); arrow(74, 71.6, 74, 68.9)

# ---- merge ----
arrow(26, 58.6, 40, 45.5); arrow(74, 57.1, 60, 45.5)
box(28, 38.5, 44, 7.5, "Toxin predicted targets (L1+L2, n=15) ∩ disease gene core set (n=1042)\nVenn intersection → candidate core target set n = 10 (finalized)\nextension layer 54 nodes (+STRING neighbors ∩ core set)", "#E6F4EA", "#1E7E34")
box(28, 28.5, 44, 7.5, "STRING PPI (score ≥ 0.7, hide isolated nodes)\n→ Cytoscape 3.10\ncytoHubba (MCC/Degree/EPC Top 20) ∩ MCODE", "#E6F4EA", "#1E7E34")
box(28, 19, 44, 6.5, "Hub genes n = 10 (F2/F3/F5/F7/F8/F10/FGA/PLG/PROC/ALB)\n→ enrichment analysis / four-layer heterogeneous network / molecular docking", "#FFF4D6", "#B8860B")
box(28, 10, 44, 6.5, "Triple dry-lab cross-validation\nGEO transcriptomes (GSE121297 / GSE248215)\n+ literature corroboration + clinical-consistency check", "#FFF4D6", "#B8860B")
arrow(50, 38.1, 50, 36.4); arrow(50, 28.1, 50, 25.9); arrow(50, 18.6, 50, 16.9)

ax.text(50, 6.5, "Note: both line counts are final measured values from 2026-09-22/24; Phase 3 intersection and Hub back-filled; downstream n values filled at execution.",
        ha="center", fontsize=7.5, color="#555555")

fig.savefig(OUT, bbox_inches="tight")
print("saved:", OUT)
