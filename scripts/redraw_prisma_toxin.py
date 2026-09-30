# -*- coding: utf-8 -*-
"""Redraw the PRISMA toxin-line flowchart (Fig. S0-2, toxin line filled with measured counts) — English version"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot
setup_plot()
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = Path(__file__).resolve().parents[1] / "00_protocol" / "PRISMA_flowchart_toxin_filled.png"

fig, ax = plt.subplots(figsize=(8.6, 10.2), dpi=200)
ax.set_xlim(0, 100); ax.set_ylim(0, 122); ax.axis("off")

def box(x, y, w, h, text, fc, ec, fs=7.8, tc="black"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2",
                                fc=fc, ec=ec, lw=1.2))
    ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=fs, color=tc, linespacing=1.5)

def arrow(x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=13, color="#555555", lw=1.1))

ax.text(50, 119.5, "Fig. S0-2   Toxin & disease-gene screening workflow (PRISMA-style, toxin line filled with measured counts, 2026-09-22)",
        ha="center", fontsize=10, weight="bold")

# ---- line A: toxins (completed) ----
ax.text(26, 113.5, "A. Toxin library line (completed)", ha="center", fontsize=9.5, weight="bold", color="#8B1A1A")
box(5, 100, 42, 12, "UniProt main retrieval (two species combined, reviewed)\nn = 52 (D. siamensis 28 + D. russelii 24)\nSupplementary: Kunitz 24 + CRISP 4 + SVMP/Dis 3\n(note: siamensis separate export, 28 entries, fully overlapping)",
    "#FDECEC", "#B22222", fs=7.2)
box(5, 88, 42, 8, "Merged & deduplicated (by accession)\nn = 78", "#FDECEC", "#B22222")
box(5, 75, 42, 9.5, "Removed 16 fragment sequences <30 aa\nExcluded 4 ADAM-like host-protein contaminants\n(not archived)   removed n = 16", "#E8F0FE", "#1A56C4", fs=7.4)
box(5, 60.5, 42, 11.5, "Archived toxins n = 62\nAll nine families present (Kunitz 21 / PLA2 15 / snaclec 8 /\nSVMP·Dis 5 / SVSP 4 / CRISP 4 / LAAO 2 / VEGF 2 / NGF 1)",
    "#F3E8FD", "#7B1FA2", fs=7.2)
box(5, 47.5, 42, 10, "90%-identity clustering (CD-HIT-equivalent algorithm)\nclusters n = 40 (40 representative sequences)\nAbundance weights back-filled from Sri Lanka\npopulation proteomics", "#F3E8FD", "#7B1FA2", fs=7.2)
arrow(26, 99.6, 26, 96.4); arrow(26, 87.6, 26, 84.9); arrow(26, 74.6, 26, 72.4); arrow(26, 60.1, 26, 57.9)

# ---- line B: disease genes (pending Phase 1B) ----
ax.text(74, 113.5, "B. Disease gene-set line (pending Phase 1B)", ha="center", fontsize=9.5, weight="bold", color="#1A56C4")
box(53, 98.5, 42, 13.5, "GeneCards (core-set score ≥ median or ≥10)\nDisGeNET (≥0.1) / OMIM / CTD\nQuery terms: TMA, snakebite, VICC,\nMAHA, aHUS, TTP\nn = ___", "#E8F0FE", "#1A56C4", fs=7.4)
box(53, 86, 42, 9, "UniProt ID standardization\n(official symbol + UniProt AC)\nhuman genes only", "#E8F0FE", "#1A56C4")
box(53, 75.5, 42, 7.5, "Disease gene set after merge & dedup\nn = ___", "#E8F0FE", "#1A56C4")
box(53, 63.5, 42, 9, "Four-axis prior-molecule completeness check\n(ADAMTS13/VWF/F2/C3/VCAM1 etc.)", "#E8F0FE", "#1A56C4")
arrow(74, 98.1, 74, 95.4); arrow(74, 85.6, 74, 83.4); arrow(74, 75.1, 74, 72.9)

# ---- merge ----
arrow(26, 47.1, 40, 42.5); arrow(74, 63.1, 60, 42.5)
box(28, 34.5, 44, 8, "Toxin predicted targets (L1+L2 evidence) ∩ disease gene set\nVenn intersection → candidate core target set\nn = ___  (pending Phase 2–3)", "#E6F4EA", "#1E7E34")
box(28, 25, 44, 7.5, "STRING PPI (score ≥ 0.7, hide isolated nodes)\n→ Cytoscape 3.10\ncytoHubba (MCC/Degree/EPC Top 20) ∩ MCODE", "#E6F4EA", "#1E7E34")
box(28, 16, 44, 6.5, "Hub genes (expected 8–15)\n→ enrichment analysis / four-layer heterogeneous network / molecular docking", "#FFF4D6", "#B8860B")
box(28, 6.5, 44, 7, "Triple dry-lab cross-validation\nGEO transcriptomes (GSE121297 / GSE248215)\n+ literature corroboration + clinical-consistency check", "#FFF4D6", "#B8860B")
arrow(50, 34.1, 50, 32.9); arrow(50, 24.6, 50, 22.9); arrow(50, 15.6, 50, 13.9)

ax.text(50, 2.8, "Note: toxin-line counts measured 2026-09-22; gene-line and downstream n values to be filled at Phase 1B–3 execution.",
        ha="center", fontsize=7.5, color="#555555")

fig.savefig(OUT, bbox_inches="tight")
print("saved:", OUT)
