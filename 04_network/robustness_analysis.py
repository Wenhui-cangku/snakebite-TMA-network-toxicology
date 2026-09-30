# -*- coding: utf-8 -*-
"""Network robustness/perturbation analysis: 54-node extension-layer PPI, random vs targeted attack + lethal-node identification"""
import json, random, sys
from pathlib import Path
import networkx as nx

BASE = Path(__file__).resolve().parents[1]
random.seed(1234)

# read extension-layer PPI (score>=0.7)
G = nx.Graph()
with open(BASE/"04_network/ppi_extended61_score700.tsv", encoding="utf-8-sig") as f:
    header = f.readline().strip().split("\t")
    for line in f:
        parts = line.strip().split("\t")
        if len(parts) >= 2:
            G.add_edge(parts[0], parts[1])
print(f"network: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

N0 = G.number_of_nodes()
def lcc_size(g):
    return max((len(c) for c in nx.connected_components(g)), default=0)

# 1) targeted attack: remove nodes one by one in descending degree order
order = [n for n, _ in sorted(G.degree(), key=lambda x: -x[1])]
targeted = []
g = G.copy()
for n in order:
    g.remove_node(n)
    targeted.append(lcc_size(g) / N0)

# 2) random attack: averaged over 100 runs
import numpy as np
rand_curves = []
for rep in range(100):
    g = G.copy()
    nodes = list(g.nodes())
    random.shuffle(nodes)
    curve = []
    for n in nodes:
        g.remove_node(n)
        curve.append(lcc_size(g) / N0)
    rand_curves.append(curve)
rand_mean = np.mean(rand_curves, axis=0)
rand_std = np.std(rand_curves, axis=0)

# 3) lethal nodes: ranked by LCC drop after individual removal
base = lcc_size(G) / N0
impact = []
for n in G.nodes():
    g = G.copy(); g.remove_node(n)
    impact.append((n, G.degree(n), base - lcc_size(g)/N0,
                   nx.connected_components(g) and len(list(nx.connected_components(g))) or 0))
impact.sort(key=lambda x: -x[2])
print("\nLethal nodes Top10 (LCC loss after removal):")
for n, d, loss, ncomp in impact[:10]:
    print(f"  {n}: degree={d}, LCC loss={loss:.3f}, remaining components={ncomp}")

# LCC comparison at 50% node removal
i50 = int(N0*0.5)
print(f"\nLCC fraction after 50% node removal: targeted={targeted[i50]:.3f} vs random={rand_mean[i50]:.3f}±{rand_std[i50]:.3f}")

# save results
json.dump({
    "n_nodes": N0, "n_edges": G.number_of_edges(),
    "targeted_curve": targeted, "random_mean": rand_mean.tolist(), "random_std": rand_std.tolist(),
    "lethal_top10": [(n, d, round(loss,4)) for n, d, loss, _ in impact[:10]],
    "at_50pct": {"targeted": round(targeted[i50],4), "random": round(float(rand_mean[i50]),4)},
}, open(BASE/"04_network/robustness_results.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)

# plotting
sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot
setup_plot()
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(7.5, 5.5), dpi=200)
x = np.arange(N0) / N0 * 100
ax.plot(x, targeted, color="#D62728", lw=2.2, label="targeted attack (degree-descending removal)")
ax.plot(x, rand_mean, color="#1F77B4", lw=2.2, label="random attack (mean of 100 runs)")
ax.fill_between(x, rand_mean-rand_std, rand_mean+rand_std, color="#1F77B4", alpha=0.18)
ax.axvline(50, color="gray", ls=":", lw=1)
ax.annotate(f"50% removed: targeted LCC={targeted[i50]:.2f} vs random LCC={rand_mean[i50]:.2f}",
            xy=(50, targeted[i50]), xytext=(42, 0.62), fontsize=10,
            arrowprops=dict(arrowstyle="->", color="gray"))
ax.set_xlabel("fraction of nodes removed (%)"); ax.set_ylabel("largest connected component (LCC/N)")
ax.set_title("Toxin–host PPI network robustness: targeted vulnerability at coagulation hubs markedly exceeds random attack", fontsize=11)
ax.legend(); ax.set_xlim(0,100); ax.set_ylim(0,1.02)
fig.tight_layout()
out = BASE/"04_network/figure3c_robustness.png"
fig.savefig(out, bbox_inches="tight")
print("\nfigure:", out)
