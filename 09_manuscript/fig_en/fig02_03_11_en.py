# -*- coding: utf-8 -*-
"""Fig 2 Venn (EN) / Fig 3 PPI (EN) / Fig 11 robustness (EN) -> assets_en"""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot
setup_plot()
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

BASE = Path(__file__).resolve().parents[2]
NET = BASE / "04_network"
OUT = BASE / "09_manuscript" / "assets_en"
OUT.mkdir(exist_ok=True)

# ---------------- Fig 2 Venn (EN) ----------------
from matplotlib.patches import Circle
fig, ax = plt.subplots(figsize=(8.2, 5.6), dpi=200)
ax.set_xlim(0, 10); ax.set_ylim(0, 6.9); ax.axis("off"); ax.set_aspect("equal")
big = Circle((6.1, 3.3), 2.55, fc="#1A56C4", ec="#12408F", alpha=0.30, lw=1.5)
small = Circle((3.15, 3.3), 1.05, fc="#7B1FA2", ec="#5A1480", alpha=0.35, lw=1.5)
ax.add_patch(big); ax.add_patch(small)
inter = Circle((6.1, 3.3), 2.55, fc="#1E7E34", ec="none", alpha=0.55, lw=0)
inter.set_clip_path(Circle((3.15, 3.3), 1.05, transform=ax.transData))
ax.add_patch(inter)
ax.text(2.62, 3.3, "5", ha="center", va="center", fontsize=15, weight="bold", color="#5A1480")
ax.text(3.87, 3.3, "10", ha="center", va="center", fontsize=13, weight="bold", color="#0E3D1F")
ax.text(6.6, 3.3, "1032", ha="center", va="center", fontsize=15, weight="bold", color="#12408F")
ax.annotate("L2 literature-curated\ntargets (n = 15)", xy=(2.75, 4.15), xytext=(0.55, 5.35),
            fontsize=9.5, color="#5A1480", weight="bold",
            arrowprops=dict(arrowstyle="-", color="#5A1480", lw=0.9))
ax.annotate("Core disease-gene set\n(6 sources)  n = 1042", xy=(7.9, 5.1), xytext=(7.0, 5.45),
            fontsize=9.5, color="#12408F", weight="bold",
            arrowprops=dict(arrowstyle="-", color="#12408F", lw=0.9))
ax.annotate("Strict core target set  n = 10", xy=(3.9, 2.62), xytext=(5.6, 1.15),
            fontsize=9.5, color="#0E3D1F", weight="bold",
            arrowprops=dict(arrowstyle="-", color="#145A32", lw=0.9))
ax.text(5, 6.65, "Figure 2  L2 literature-curated targets ∩ core disease-gene set", ha="center",
        fontsize=11.5, weight="bold")
fig.savefig(OUT / "figure2a_venn.png", bbox_inches="tight")
plt.close(fig)
print("fig2 en saved")

# ---------------- Fig 3 PPI (EN) ----------------
df = pd.read_csv(NET / "ppi_extended61_score700.tsv", sep="\t")
topo = json.load(open(NET / "phase3_topology.json", encoding="utf-8"))
hub = set(topo["extended61"]["hub"])
core = {"COL4A1", "F10", "F11", "F5", "FGA", "GP1BA", "KDR", "PLG", "PROC", "PROS1"}
G = nx.Graph()
G.add_edges_from(zip(df["node1"], df["node2"]))
others = sorted([n for n in G.nodes if n not in core and n not in hub])
core_only = sorted([n for n in G.nodes if n in core and n not in hub])
hub_core = sorted([n for n in G.nodes if n in core and n in hub])
hub_ext = sorted([n for n in G.nodes if n in hub and n not in core])
pos = nx.shell_layout(G, [hub_core, hub_ext + core_only, others])
R = [1.35, 2.7, 4.6]
for i, ring in enumerate([hub_core, hub_ext + core_only, others]):
    for n in ring:
        x, y = pos[n]
        r = (x**2 + y**2) ** 0.5
        if r > 0:
            pos[n] = (x / r * R[i], y / r * R[i])
fig, ax = plt.subplots(figsize=(10.5, 10.5), dpi=200)
ax.set_xlim(-5.6, 5.6); ax.set_ylim(-5.6, 5.6); ax.set_aspect("equal")
nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.18, width=0.6, edge_color="#888888")
nx.draw_networkx_nodes(G, pos, nodelist=others, node_size=1350, node_color="#9FB8E8",
                       edgecolors="#5B7DBF", linewidths=0.8, ax=ax)
nx.draw_networkx_nodes(G, pos, nodelist=core_only, node_size=2100, node_color="#7BC47F",
                       edgecolors="#1E7E34", linewidths=1.4, ax=ax)
nx.draw_networkx_nodes(G, pos, nodelist=hub_core, node_size=2600, node_color="#F0B429",
                       edgecolors="#8A5A00", linewidths=2.0, ax=ax)
nx.draw_networkx_nodes(G, pos, nodelist=hub_ext, node_size=2100, node_color="#E8862E",
                       edgecolors="#8A3B00", linewidths=2.0, ax=ax)
for n in G.nodes:
    if n in hub_core:
        fs, fw, tc = 9.5, "bold", "#3D2B00"
    elif n in hub:
        fs, fw, tc = 8.5, "bold", "white"
    elif n in core:
        fs, fw, tc = 8.5, "bold", "#0E3D1F"
    else:
        fs, fw, tc = 6.8, "normal", "#1B2A4A"
    ax.text(pos[n][0], pos[n][1], n, fontsize=fs, ha="center", va="center", weight=fw, color=tc)
from matplotlib.lines import Line2D
_leg = [("#F0B429", "#8A5A00", "Hub ∩ core"), ("#E8862E", "#8A3B00", "Hub (extended)"),
        ("#7BC47F", "#1E7E34", "strict core"), ("#9FB8E8", "#5B7DBF", "Extended neighbors")]
ax.legend([Line2D([0], [0], marker="o", ls="", markersize=11,
                  markerfacecolor=c, markeredgecolor=e, markeredgewidth=1.4) for c, e, _ in _leg],
          [t for _, _, t in _leg], loc="upper left", fontsize=9, frameon=True)
ax.set_title("Figure 3  Extended-layer PPI network of candidate targets (STRING combined score ≥ 0.7; 54 nodes / 321 edges)\n"
             "Hub = MCC ∩ Degree ∩ EPC Top-20 consensus (orange); green = L2 direct-intersection core",
             fontsize=10, weight="bold")
ax.axis("off")
fig.savefig(OUT / "figure2b_ppi.png", bbox_inches="tight")
plt.close(fig)
print("fig3 en saved")

# ---------------- Fig 11 robustness (EN, from saved json) ----------------
res = json.load(open(NET / "robustness_results.json", encoding="utf-8"))
targeted = res["targeted_curve"]; rand_mean = np.array(res["random_mean"]); rand_std = np.array(res["random_std"])
N0 = res["n_nodes"]; i50 = int(N0 * 0.5)
fig, ax = plt.subplots(figsize=(7.5, 5.5), dpi=200)
x = np.arange(N0) / N0 * 100
ax.plot(x, targeted, color="#D62728", lw=2.2, label="Targeted attack (descending degree)")
ax.plot(x, rand_mean, color="#1F77B4", lw=2.2, label="Random attack (mean of 100 runs)")
ax.fill_between(x, rand_mean - rand_std, rand_mean + rand_std, color="#1F77B4", alpha=0.18)
ax.axvline(50, color="gray", ls=":", lw=1)
ax.annotate(f"50% removed: targeted LCC={targeted[i50]:.2f} vs random LCC={rand_mean[i50]:.2f}",
            xy=(50, targeted[i50]), xytext=(42, 0.62), fontsize=10,
            arrowprops=dict(arrowstyle="->", color="gray"))
ax.set_xlabel("Nodes removed (%)"); ax.set_ylabel("Largest connected component (LCC/N)")
ax.set_title("Figure 11  Robustness of the toxin–host PPI network:\ntargeted attack on coagulation hubs vs random attack", fontsize=11)
ax.legend(); ax.set_xlim(0, 100); ax.set_ylim(0, 1.02)
fig.tight_layout()
fig.savefig(OUT / "figure3c_robustness.png", bbox_inches="tight")
plt.close(fig)
print("fig11 en saved")
