# -*- coding: utf-8 -*-
"""Render Fig. 5 four-layer heterogeneous network from Cytoscape cyjs layout (EN labels)."""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

CYJS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figure4_hetero_network.cyjs")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "09_manuscript", "assets_en", "figure5_network.png")

d = json.load(open(CYJS, encoding="utf-8"))
els = d["elements"]
nodes = {n["data"]["id"]: n for n in els["nodes"]}
edges = els["edges"]

fig, ax = plt.subplots(figsize=(13.2, 8.4), dpi=300)

EDGE_STYLE = {
    "direct":     dict(color="#B22222", lw=1.6, ls="-",  alpha=0.85, z=2),
    "membership": dict(color="#9E9E9E", lw=0.7, ls="-",  alpha=0.45, z=1),
    "mechanism":  dict(color="#757575", lw=1.1, ls="--", alpha=0.75, z=1),
    "progression":dict(color="#7B1FA2", lw=1.4, ls=":",  alpha=0.9,  z=2),
}
for e in edges:
    dd = e["data"]
    s, t = nodes[dd["source"]]["position"], nodes[dd["target"]]["position"]
    st = EDGE_STYLE.get(dd["interaction"], EDGE_STYLE["membership"])
    ax.plot([s["x"], t["x"]], [-s["y"], -t["y"]], color=st["color"], lw=st["lw"],
            ls=st["ls"], alpha=st["alpha"], zorder=st["z"])

def en_label(txt):
    return txt.split("\n")[0]

for nid, n in nodes.items():
    dd, pos = n["data"], n["position"]
    x, y = pos["x"], -pos["y"]
    nt = dd["node_type"]
    hub = "Hub" in (dd.get("hub_status") or "")
    if nt == "toxin":
        ax.scatter(x, y, marker="h", s=950, c=dd["fill_color"], edgecolors="black",
                   linewidths=1.0, zorder=4)
        ax.text(x - 26, y, en_label(dd["label"]), ha="right", va="center",
                fontsize=9, weight="bold", color="#333333", zorder=5)
    elif nt == "target":
        ax.scatter(x, y, marker="o", s=820, c=dd["fill_color"],
                   edgecolors="black" if hub else "#0D3B66",
                   linewidths=2.2 if hub else 0.9, zorder=4)
        ax.text(x, y, dd["label"], ha="center", va="center", fontsize=6.6,
                weight="bold", color="white", zorder=5)
    elif nt == "pathway":
        lines = dd["label"].split("\n")
        w = 340
        box = FancyBboxPatch((x - w/2, y - 46), w, 92,
                             boxstyle="round,pad=6,rounding_size=12",
                             fc="#E8F5E9", ec="#2CA02C", lw=1.4, zorder=3)
        ax.add_patch(box)
        ax.text(x, y + 17, lines[0], ha="center", va="center", fontsize=8.4,
                weight="bold", color="#1B5E20", zorder=5)
        ax.text(x, y - 19, lines[1] if len(lines) > 1 else "", ha="center",
                va="center", fontsize=7.2, color="#33691E", zorder=5)
    elif nt == "phenotype":
        ax.scatter(x, y, marker="D", s=1250, c=dd["fill_color"], edgecolors="black",
                   linewidths=1.0, zorder=4)
        ax.text(x + 80, y, en_label(dd["label"]), ha="left", va="center", fontsize=9,
                weight="bold", color="#4A148C", zorder=5)

# column headers
for x, t in [(-640, "Toxins"), (-215, "Host targets"), (230, "Pathways"), (700, "Phenotypes")]:
    ax.text(x, -640, t, ha="center", fontsize=11.5, weight="bold", color="#37474F")

# legend
from matplotlib.lines import Line2D
handles = [
    Line2D([], [], marker="h", ls="", markersize=11, markerfacecolor="#D62728", markeredgecolor="black", label="Toxin"),
    Line2D([], [], marker="o", ls="", markersize=10, markerfacecolor="#1F77B4", markeredgecolor="black", markeredgewidth=2, label="Target (hub candidate)"),
    Line2D([], [], marker="o", ls="", markersize=10, markerfacecolor="#1F77B4", markeredgecolor="#0D3B66", label="Target"),
    Line2D([], [], marker="s", ls="", markersize=10, markerfacecolor="#E8F5E9", markeredgecolor="#2CA02C", label="Pathway"),
    Line2D([], [], marker="D", ls="", markersize=10, markerfacecolor="#9467BD", markeredgecolor="black", label="Phenotype"),
    Line2D([], [], color="#B22222", lw=1.6, label="Literature-curated edge"),
    Line2D([], [], color="#9E9E9E", lw=0.9, label="Pathway membership (enrichment)"),
    Line2D([], [], color="#757575", lw=1.1, ls="--", label="Mechanistic inference"),
    Line2D([], [], color="#7B1FA2", lw=1.4, ls=":", label="Phenotype progression"),
]
ax.legend(handles=handles, loc="lower center", ncol=3, fontsize=8, frameon=True,
          bbox_to_anchor=(0.5, -0.02))

ax.set_xlim(-1000, 1000)
ax.set_ylim(-720, 720)
ax.axis("off")
fig.tight_layout()
fig.savefig(OUT, bbox_inches="tight", facecolor="white")
print("saved", OUT)
