# -*- coding: utf-8 -*-
"""Figure 2b 扩展层 PPI 网络图（score>=0.7, 54 节点）"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot
setup_plot()
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import json

NET = str(Path(__file__).resolve().parents[1] / "04_network")
df = pd.read_csv(NET + r"\ppi_extended61_score700.tsv", sep="\t")
topo = json.load(open(NET + r"\phase3_topology.json", encoding="utf-8"))
hub = set(topo["extended61"]["hub"])
core = {"COL4A1", "F10", "F11", "F5", "FGA", "GP1BA", "KDR", "PLG", "PROC", "PROS1"}

G = nx.Graph()
G.add_edges_from(zip(df["node1"], df["node2"]))

# 同心正圆布局：内环 Hub∩核心，中环 Hub扩展+strict核心，外环 扩展邻居
others = sorted([n for n in G.nodes if n not in core and n not in hub])
core_only = sorted([n for n in G.nodes if n in core and n not in hub])
hub_core = sorted([n for n in G.nodes if n in core and n in hub])
hub_ext = sorted([n for n in G.nodes if n in hub and n not in core])

pos = nx.shell_layout(G, [hub_core, hub_ext + core_only, others])
R = [1.35, 2.7, 4.6]  # 三环半径
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
                       edgecolors="#5B7DBF", linewidths=0.8, ax=ax, label="扩展邻居层")
nx.draw_networkx_nodes(G, pos, nodelist=core_only, node_size=2100, node_color="#7BC47F",
                       edgecolors="#1E7E34", linewidths=1.4, ax=ax, label="strict 核心")
nx.draw_networkx_nodes(G, pos, nodelist=hub_core, node_size=2600, node_color="#F0B429",
                       edgecolors="#8A5A00", linewidths=2.0, ax=ax, label="Hub ∩ 核心")
nx.draw_networkx_nodes(G, pos, nodelist=hub_ext, node_size=2100, node_color="#E8862E",
                       edgecolors="#8A3B00", linewidths=2.0, ax=ax, label="Hub（扩展层）")

# 基因名置于圆圈中心
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

# 图例：固定小圆点（避免 networkx 把节点大小带进图例）
from matplotlib.lines import Line2D
_leg = [("#F0B429", "#8A5A00", "Hub ∩ 核心"), ("#E8862E", "#8A3B00", "Hub（扩展层）"),
        ("#7BC47F", "#1E7E34", "strict 核心"), ("#9FB8E8", "#5B7DBF", "扩展邻居层")]
ax.legend([Line2D([0], [0], marker="o", ls="", markersize=11,
                  markerfacecolor=c, markeredgecolor=e, markeredgewidth=1.4) for c, e, _ in _leg],
          [t for _, _, t in _leg], loc="upper left", fontsize=9, frameon=True)
ax.set_title("Figure 3  候选靶点扩展层 PPI 网络（STRING combined score ≥ 0.7，54 节点 / 321 边）\n"
             "Hub = MCC ∩ Degree ∩ EPC 三榜 Top20（橙）；绿 = L2 直接交集核心",
             fontsize=10.5, weight="bold")
ax.axis("off")
fig.savefig(NET + r"\figure2b_ppi.png", bbox_inches="tight")
print("saved figure2b_ppi.png")
