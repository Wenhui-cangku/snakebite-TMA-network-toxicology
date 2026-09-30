# -*- coding: utf-8 -*-
"""Figure 1 workflow + Figure 7 AOP mechanism diagram
Output PNG (300 dpi) + SVG to 09_manuscript/assets/"""
import sys, os
from pathlib import Path
sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot
setup_plot()

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets")
os.makedirs(OUT, exist_ok=True)

C_DATA = ("#ECEFF1", "#546E7A")   # gray-blue: data layer
C_NET  = ("#E3F2FD", "#1565C0")   # blue: network layer
C_VAL  = ("#FFF3E0", "#E65100")   # orange: validation layer
C_INT  = ("#E8F5E9", "#2E7D32")   # green: integration layer
C_TOX  = ("#FDECEA", "#C62828")   # red: toxins
C_TGT  = ("#E3F2FD", "#1565C0")   # blue: targets
C_KE   = ("#E8F5E9", "#2E7D32")   # green: KE
C_AO   = ("#F3E5F5", "#6A1B9A")   # purple: AO
C_NEG  = ("#F5F5F5", "#9E9E9E")   # gray: negative/secondary

def box(ax, x, y, w, h, text, fc, ec, fs=9.5, bold=False, ls="-", tc="black"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
                                fc=fc, ec=ec, lw=1.6, ls=ls, mutation_aspect=1))
    ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=fs,
            color=tc, fontweight="bold" if bold else "normal", linespacing=1.35)

def arrow(ax, x1, y1, x2, y2, color="#455A64", lw=1.6, ls="-", label=None, fs=8, lab_off=(0, 0.06)):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=13,
                                 color=color, lw=lw, ls=ls, shrinkA=2, shrinkB=2, zorder=5))
    if label:
        ax.text((x1+x2)/2 + lab_off[0], (y1+y2)/2 + lab_off[1], label,
                ha="center", va="bottom", fontsize=fs, color=color)

# ================= Figure 1 workflow =================
fig, ax = plt.subplots(figsize=(9.2, 10.2))
ax.set_xlim(0, 10); ax.set_ylim(0, 11.4); ax.axis("off")

rows = [
    (10.15, "Data sources", C_DATA, 1.9, 1.06),
    (7.95,  "Curated libraries", C_DATA, 1.9, 1.06),
    (5.75,  "Network construction", C_NET, 1.9, 1.06),
    (3.35,  "Multi-layer validation", C_VAL, 2.35, 1.21),
    (0.95,  "Integration & output", C_INT, 1.9, 1.06),
]
for y, name, (fc, ec), bh, ldy in rows:
    ax.add_patch(FancyBboxPatch((0.15, y + 1.28 - bh), 9.7, bh, boxstyle="round,pad=0.02,rounding_size=0.05",
                                fc=fc, ec="none", alpha=0.45, zorder=0))
    ax.text(0.55, y+ldy, name, fontsize=9, color=ec, fontweight="bold", va="center")

# Row1 data sources
box(ax, 0.55, 9.55, 4.1, 1.1, "UniProtKB + VenomZone\n(keyword: Toxin, reviewed;\nD. russelii / D. siamensis)", *C_DATA, fs=9)
box(ax, 5.35, 9.55, 4.1, 1.1, "6 disease-gene sources\nGeneCards · Open Targets · DISEASES\nDisGeNET · CTD · OMIM", *C_DATA, fs=9)
# Row2 libraries
box(ax, 0.55, 7.35, 4.1, 1.1, "Toxin library\n63 sequences / 40 clusters\n(CD-HIT 90%, 5 families)", *C_DATA, fs=9, bold=False)
box(ax, 5.35, 7.35, 4.1, 1.1, "Disease gene set\n2,190 total / 1,042 core\n(4-axis prior 27/27 covered)", *C_DATA, fs=9)
# Row3 network
box(ax, 0.55, 5.15, 4.1, 1.1, "Toxin–host target edges\n4-tier evidence\n(L2 literature score=1.0)", *C_NET)
box(ax, 5.35, 5.15, 4.1, 1.1, "Intersection & topology\nstrict core 10 ∩ | Hub 10\n(MCC∩Degree∩EPC)", *C_NET)
# Row4 validation (two columns, four blocks)
box(ax, 0.55, 3.40, 4.1, 0.92, "Enrichment\n(g:Profiler + Enrichr,\nprior pathway tests)", *C_VAL, fs=8.2)
box(ax, 5.35, 3.40, 4.1, 0.92, "Structure validation\n7 pairs × ClusPro/HADDOCK/HDock\n+ 3 repurposed drugs (Vina)", *C_VAL, fs=8.2)
box(ax, 0.55, 2.50, 4.1, 0.82, "Transcriptome cross-check\nGSE121297 (HUVEC×snaclec)\nGSE248215 (mouse×venom)", *C_VAL, fs=8.2)
box(ax, 5.35, 2.50, 4.1, 0.82, "Network robustness\ntargeted vs random attack\n(54 nodes / 321 edges)", *C_VAL, fs=8.2)
# Row5 integration
box(ax, 2.35, 0.35, 5.3, 1.1, "AOP framework integration\nMIE → KE → AO\nHypothesis list + repurposing leads", *C_INT, fs=9.5, bold=True)

# arrows
arrow(ax, 2.6, 9.55, 2.6, 8.45); arrow(ax, 7.4, 9.55, 7.4, 8.45)
arrow(ax, 2.6, 7.35, 2.6, 6.25); arrow(ax, 7.4, 7.35, 7.4, 6.25)
arrow(ax, 2.6, 5.15, 2.6, 4.34)
arrow(ax, 7.4, 5.15, 7.4, 4.34)
arrow(ax, 2.6, 4.60, 7.4, 5.15, color="#90A4AE", lw=1.1)   # enrichment gene set comes from Hub
arrow(ax, 5.0, 2.42, 5.0, 1.50, color="#78909C", lw=2.2)    # validation layer → integration layer

ax.set_title("Figure 1. Study workflow: from venom toxins to host targets — a multi-layer computational pipeline",
             fontsize=11, fontweight="bold", pad=12)
fig.savefig(os.path.join(OUT, "figure1_workflow.png"), dpi=300, bbox_inches="tight")
fig.savefig(os.path.join(OUT, "figure1_workflow.svg"), bbox_inches="tight")
plt.close(fig)

# ================= Figure 7 AOP mechanism diagram =================
fig, ax = plt.subplots(figsize=(12.6, 7.4))
ax.set_xlim(0, 14); ax.set_ylim(0, 8.2); ax.axis("off")

# column titles
for x, t, sub in [(1.55, "MIE ★★★", "toxin–target binding (structure-verified)"),
                  (5.75, "Host targets", "direct targets (literature-curated)"),
                  (9.55, "KE ★★", "key events (enrichment + transcriptome)"),
                  (12.85, "AO ★", "adverse outcome (clinical triad)")]:
    ax.text(x, 7.85, t, ha="center", fontsize=12, fontweight="bold", color="#37474F")
    ax.text(x, 7.5, sub, ha="center", fontsize=8, color="#78909C")

toxins = ["RVV-X\n(SVMP+snaclec)", "RVV-Vγ\n(SVSP)", "daborhagin-K\n(SVMP P-III)",
          "snaclec\nQ38L02", "PLA2\nVRV-PL-VIIIa", "Kunitz\nH6VC06", "svVEGF\nP67861"]
targets = ["FXa\n(F10)", "FV\n(F5)", "Fibrinogen-Aα\n(FGA)", "GP1BA\n(VWF receptor)",
           "Plasmin\n(PLG)", "VEGFR2\n(KDR)"]
pairs = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 0), (5, 4), (6, 5)]  # toxin i → target j

tys = [6.6, 5.65, 4.7, 3.75, 2.8, 1.85, 0.9]
for i, name in enumerate(toxins):
    box(ax, 0.5, tys[i]-0.36, 2.1, 0.72, name, *C_TOX, fs=8.6)

gys = {0: 6.05, 1: 5.1, 2: 4.15, 3: 3.2, 4: 2.25, 5: 1.3}
for j, name in enumerate(targets):
    box(ax, 4.75, gys[j]-0.36, 2.0, 0.72, name, *C_TGT, fs=8.6)

for i, j in pairs:
    arrow(ax, 2.62, tys[i], 4.73, gys[j], color="#C62828", lw=1.5)

# KE layer
kes = [(7.85, 5.55, "KE1  Coagulation activation\n& consumption\n(F2/F3/F5/F7/F8/F10/FGA)"),
       (7.85, 3.85, "KE2  Platelet dysfunction &\nendothelial activation\n(GP1BA · VEGFR2 · SELE/VCAM1)"),
       (7.85, 2.15, "KE3  Fibrinolysis imbalance\n(Kunitz inhibits plasmin;\nSERPINE1 up)")]
for x, y, t in kes:
    box(ax, x, y-0.55, 2.7, 1.1, t, *C_KE, fs=8.0)
# complement (secondary, gray dashed)
box(ax, 7.85, 0.45, 2.7, 0.8, "Complement: host secondary\n(no direct toxin edge)", *C_NEG, fs=8.2, ls="--", tc="#616161")

# AO layer
box(ax, 11.85, 4.55, 2.0, 1.9, "TMA triad\n• Thrombocytopenia\n• MAHA\n• AKI (HAVCR1↑)", *C_AO, fs=9, bold=True)
box(ax, 11.85, 3.15, 2.0, 0.85, "Capillary leak /\nhypotension", *C_AO, fs=8.4)

# target→KE arrows
arrow(ax, 6.77, gys[0], 7.83, 5.55, color="#1565C0")
arrow(ax, 6.77, gys[1], 7.83, 5.45, color="#1565C0")
arrow(ax, 6.77, gys[2], 7.83, 5.30, color="#1565C0")
arrow(ax, 6.77, gys[3], 7.83, 3.90, color="#1565C0")
arrow(ax, 6.77, gys[5], 7.83, 3.70, color="#1565C0")
arrow(ax, 6.77, gys[4], 7.83, 2.20, color="#1565C0")

# KE→AO
arrow(ax, 10.57, 5.30, 11.83, 5.60, color="#2E7D32")
arrow(ax, 10.57, 3.85, 11.83, 5.05, color="#2E7D32")
arrow(ax, 10.57, 2.15, 11.83, 4.75, color="#2E7D32")
arrow(ax, 10.57, 0.85, 11.83, 3.35, color="#9E9E9E", ls="--")   # right edge of complement box → capillary leak, avoiding the KE3 box

# caption bar
ax.text(0.5, 0.12, "Solid red arrows: structure-verified direct binding (7/7).  Dashed grey: host secondary response (no direct evidence).  "
                   "★ evidence level: ★★★ structural, ★★ curated/enriched, ★ inferred.",
        fontsize=8, color="#607D8B", va="bottom")
ax.set_title("Figure 12. Mechanistic model of Russell's viper envenomation-associated TMA (AOP framework)",
             fontsize=11.5, fontweight="bold", pad=10)
fig.savefig(os.path.join(OUT, "figure7_aop_mechanism.png"), dpi=300, bbox_inches="tight")
fig.savefig(os.path.join(OUT, "figure7_aop_mechanism.svg"), bbox_inches="tight")
plt.close(fig)

print("done:", os.listdir(OUT))
