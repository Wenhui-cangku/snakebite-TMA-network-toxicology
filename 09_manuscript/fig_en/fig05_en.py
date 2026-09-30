# -*- coding: utf-8 -*-
"""Fig 5 four-layer heterogeneous network preview (EN) -> assets_en/figure4_preview.png
matplotlib preview part only (node/edge definitions identical to build_figure4_network.py, labels in English)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot
setup_plot()
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

OUT = Path(__file__).resolve().parents[1] / "assets_en"
OUT.mkdir(exist_ok=True)

# (id, label, layer, type, hub)
NODES = [
    ("RVVX",  "RVV-X",        1, "toxin", ""),
    ("RVVV",  "RVV-Vγ",       1, "toxin", ""),
    ("DABK",  "daborhagin-K", 1, "toxin", ""),
    ("SNAC",  "snaclec Q38L02",1,"toxin", ""),
    ("PLA2",  "PLA2 VRV-PL-VIIIa",1,"toxin",""),
    ("KUN",   "Kunitz H6VC06", 1, "toxin",""),
    ("SVVEGF","svVEGF",       1, "toxin", ""),
    ("F10",   "F10",    2, "target", "Hub+strict"),
    ("F9",    "F9",     2, "target", ""),
    ("PROS1", "PROS1",  2, "target", "strict"),
    ("F5",    "F5",     2, "target", "Hub+strict"),
    ("FGA",   "FGA",    2, "target", "Hub+strict"),
    ("FN1",   "FN1",    2, "target", ""),
    ("COL4A1","COL4A1", 2, "target", "strict"),
    ("GP1BA", "GP1BA",  2, "target", "strict"),
    ("PLG",   "PLG",    2, "target", "Hub+strict"),
    ("F11",   "F11",    2, "target", "strict"),
    ("PRSS1", "PRSS1",  2, "target", ""),
    ("KDR",   "KDR",    2, "target", "strict"),
    ("PW_FIB",  "Formation of Fibrin Clot\n(REAC 140877, p=9.7e-23)", 3, "pathway", ""),
    ("PW_COAG", "Complement & Coagulation\n(KEGG 04610, p=3.9e-18)",  3, "pathway", ""),
    ("PW_PLT",  "Platelet Activation\n(REAC 76002, p=1.5e-07)",       3, "pathway", ""),
    ("PW_ECM",  "ECM-Receptor Interaction\n(KEGG 04512, adj=0.018)",  3, "pathway", ""),
    ("PW_FA",   "Focal Adhesion\n(KEGG 04510, adj=0.047)",            3, "pathway", ""),
    ("PW_VEGF", "VEGFR2 Signaling\n(REAC 195399, adj=0.023)",         3, "pathway", ""),
    ("PH_VICC", "VICC\nconsumption coagulopathy",        4, "phenotype", ""),
    ("PH_THR",  "Thrombocytopenia",                      4, "phenotype", ""),
    ("PH_MAHA", "MAHA\nmicroangiopathic hemolytic anemia",4, "phenotype", ""),
    ("PH_AKI",  "AKI\nacute kidney injury",              4, "phenotype", ""),
    ("PH_LEAK", "Capillary Leak /\nhypotension",         4, "phenotype", ""),
]
EDGES = [
    ("RVVX","F10","direct"),("RVVX","F9","direct"),("RVVX","PROS1","direct"),
    ("RVVV","F5","direct"),("DABK","FGA","direct"),("DABK","FN1","direct"),
    ("DABK","COL4A1","direct"),("SNAC","GP1BA","direct"),("PLA2","F10","direct"),
    ("KUN","PLG","direct"),("KUN","F11","direct"),("KUN","F10","direct"),
    ("KUN","PRSS1","direct"),("SVVEGF","KDR","direct"),
    ("F10","PW_FIB","membership"),("F5","PW_FIB","membership"),("FGA","PW_FIB","membership"),
    ("F11","PW_FIB","membership"),("GP1BA","PW_FIB","membership"),("PROS1","PW_FIB","membership"),
    ("F10","PW_COAG","membership"),("FGA","PW_COAG","membership"),("PLG","PW_COAG","membership"),
    ("F11","PW_COAG","membership"),("PROS1","PW_COAG","membership"),
    ("FGA","PW_PLT","membership"),("PLG","PW_PLT","membership"),("GP1BA","PW_PLT","membership"),
    ("PROS1","PW_PLT","membership"),("COL4A1","PW_ECM","membership"),("GP1BA","PW_ECM","membership"),
    ("COL4A1","PW_FA","membership"),("KDR","PW_FA","membership"),("KDR","PW_VEGF","membership"),
    ("PW_FIB","PH_VICC","mechanism"),("PW_FIB","PH_MAHA","mechanism"),("PW_FIB","PH_THR","mechanism"),
    ("PW_COAG","PH_VICC","mechanism"),("PW_COAG","PH_MAHA","mechanism"),("PW_COAG","PH_AKI","mechanism"),
    ("PW_PLT","PH_THR","mechanism"),("PW_PLT","PH_MAHA","mechanism"),("PW_ECM","PH_AKI","mechanism"),
    ("PW_VEGF","PH_LEAK","mechanism"),("PW_VEGF","PH_AKI","mechanism"),
    ("PH_VICC","PH_THR","progression"),("PH_VICC","PH_MAHA","progression"),
    ("PH_VICC","PH_AKI","progression"),("PH_LEAK","PH_AKI","progression"),
]
LAYERS_X = {1: -640, 2: -215, 3: 230, 4: 700}
ORDER = {
    1: ["RVVV","RVVX","PLA2","KUN","DABK","SNAC","SVVEGF"],
    2: ["F5","F10","F9","F11","PROS1","PLG","PRSS1","FGA","FN1","COL4A1","GP1BA","KDR"],
    3: ["PW_FIB","PW_COAG","PW_PLT","PW_ECM","PW_FA","PW_VEGF"],
    4: ["PH_VICC","PH_THR","PH_MAHA","PH_AKI","PH_LEAK"],
}
GAP = {1: 150, 2: 105, 3: 170, 4: 175}
pos = {}
for layer, ids in ORDER.items():
    n = len(ids)
    y0 = (n - 1) * GAP[layer] / 2
    for i, nid in enumerate(ids):
        pos[nid] = (LAYERS_X[layer], y0 - i * GAP[layer])

fig, ax = plt.subplots(figsize=(16, 12), dpi=200)
edge_style = {"direct": dict(color="#333", lw=2.2, ls="-"),
              "membership": dict(color="#AAAAAA", lw=1.0, ls="-"),
              "mechanism": dict(color="#777", lw=1.6, ls="--"),
              "progression": dict(color="#9467BD", lw=1.6, ls=":")}
for s, t, inter in EDGES:
    x1, y1 = pos[s]; x2, y2 = pos[t]
    ax.plot([x1, x2], [y1, y2], zorder=1, **edge_style[inter])
marker = {"toxin": "h", "target": "o", "pathway": "s", "phenotype": "D"}
size = {"toxin": 1500, "target": 900, "pathway": 2200, "phenotype": 1800}
ncolor = {"toxin": "#D62728", "target": "#1F77B4", "pathway": "#2CA02C", "phenotype": "#9467BD"}
for nid, label, layer, nt, hub in NODES:
    x, y = pos[nid]
    ax.scatter(x, y, s=size[nt], c=ncolor[nt], marker=marker[nt], zorder=3,
               edgecolors="black" if "Hub" in hub else "#333",
               linewidths=2.2 if "Hub" in hub else 0.8)
    parts = label.split("\n")
    if layer == 1:
        ax.annotate(parts[0], (x+70, y), ha="left", va="center", zorder=4, fontsize=9.5, weight="bold", color="#7F1919")
    elif layer == 2:
        ax.annotate(parts[0], (x, y), ha="center", va="center", zorder=4, fontsize=8.5, color="white", weight="bold")
    elif layer == 3:
        ax.annotate(parts[0], (x+120, y+18), ha="left", va="center", zorder=4, fontsize=8.5, weight="bold", color="#1E5A1E")
        if len(parts) > 1:
            ax.annotate(parts[1], (x+120, y-20), ha="left", va="center", zorder=4, fontsize=7.5, color="#555")
    else:
        ax.annotate(parts[0], (x+95, y+18), ha="left", va="center", zorder=4, fontsize=9.5, weight="bold", color="#4B2A6B")
        if len(parts) > 1:
            ax.annotate(parts[1], (x+95, y-22), ha="left", va="center", zorder=4, fontsize=8, color="#555")
for layer, name in [(1, "Layer 1  Toxins"), (2, "Layer 2  Host Direct Targets"),
                    (3, "Layer 3  Enriched Pathways"), (4, "Layer 4  TMA Phenotypes")]:
    ax.text(LAYERS_X[layer], 640, name, ha="center", fontsize=13, weight="bold")
handles = [Line2D([0], [0], color="#333", lw=2.2, label="Direct interaction (literature)"),
           Line2D([0], [0], color="#AAAAAA", lw=1.0, label="Pathway membership"),
           Line2D([0], [0], color="#777", lw=1.6, ls="--", label="Mechanistic inference"),
           Line2D([0], [0], color="#9467BD", lw=1.6, ls=":", label="Phenotype progression")]
ax.legend(handles=handles, loc="lower left", fontsize=10, framealpha=0.9)
ax.set_xlim(-800, 1350); ax.set_ylim(-700, 720); ax.axis("off")
ax.set_title("Figure 5  Four-layer heterogeneous network: toxins → host targets → pathways → TMA phenotypes",
             fontsize=12, weight="bold")
fig.tight_layout()
fig.savefig(OUT / "figure4_preview.png", bbox_inches="tight")
print("fig5 en saved")
