# -*- coding: utf-8 -*-
"""
v41 robustness / perturbation analysis of the extended toxin-host PPI layer
(54 nodes / 321 edges, STRING score >= 0.7).

Corrections vs the pre-v41 script (robustness_analysis.py):
  1) the curves include k = 0 (no node removed, LCC/N = 1.0) as the first point,
     so removal fraction 0% maps to index 0 and 50% removal (27 of 54 nodes)
     maps to index 27 -- the old script dropped the k=0 point and reported the
     "50%" value at the wrong index;
  2) figure and JSON state the exact convention: static degree order computed
     once on the full network, random removals averaged over 100 shuffles
     (seed 1234).

Outputs (reproducible from this script):
  04_network/robustness_results_v41.json
  04_network/figure3c_robustness_v41.png
"""
import json, random, sys
from pathlib import Path
import numpy as np
import networkx as nx

BASE = Path(__file__).resolve().parents[1]
SEED = 1234
REPEATS = 100
random.seed(SEED)

# --- read extended-layer PPI (score >= 0.7) ---
G = nx.Graph()
with open(BASE / "04_network/ppi_extended61_score700.tsv", encoding="utf-8-sig") as f:
    f.readline()
    for line in f:
        parts = line.strip().split("\t")
        if len(parts) >= 2:
            G.add_edge(parts[0], parts[1])
N0 = G.number_of_nodes()
print(f"network: {N0} nodes, {G.number_of_edges()} edges")

def lcc_frac(g):
    return max((len(c) for c in nx.connected_components(g)), default=0) / N0

# --- 1) targeted attack: static degree order computed once on the full network ---
order = [n for n, _ in sorted(G.degree(), key=lambda x: -x[1])]
targeted = [1.0]  # k = 0
g = G.copy()
for n in order:
    g.remove_node(n)
    targeted.append(lcc_frac(g))

# --- 2) random attack: REPEATS shuffles, mean +/- SD ---
rand_curves = []
for _ in range(REPEATS):
    g = G.copy()
    nodes = list(g.nodes())
    random.shuffle(nodes)
    curve = [1.0]  # k = 0
    for n in nodes:
        g.remove_node(n)
        curve.append(lcc_frac(g))
    rand_curves.append(curve)
rand_mean = np.mean(rand_curves, axis=0)
rand_std = np.std(rand_curves, axis=0)

# --- 3) value at 50% removal (27 of 54 nodes) ---
k50 = N0 // 2  # 27
print(f"at 50% removal (k={k50}): targeted LCC={targeted[k50]:.4f} "
      f"vs random LCC={rand_mean[k50]:.4f}+-{rand_std[k50]:.4f}")

json.dump({
    "n_nodes": N0,
    "n_edges": G.number_of_edges(),
    "k0_included": True,
    "removals_k": list(range(N0 + 1)),
    "targeted_curve": targeted,
    "random_mean": rand_mean.tolist(),
    "random_std": rand_std.tolist(),
    "at_50pct": {"k_removed": k50,
                 "targeted": round(targeted[k50], 4),
                 "random": round(float(rand_mean[k50]), 4),
                 "random_sd": round(float(rand_std[k50]), 4)},
    "seed": SEED,
    "repeats": REPEATS,
    "degree_order": "static, computed once on the full network",
}, open(BASE / "04_network/robustness_results_v41.json", "w", encoding="utf-8"),
    ensure_ascii=False, indent=1)

# --- 4) figure ---
sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot
setup_plot()
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

x = np.arange(N0 + 1) / N0 * 100
fig, ax = plt.subplots(figsize=(7.5, 5.5), dpi=200)
ax.plot(x, targeted, color="#D62728", lw=2.2, label="Targeted removal (static degree order)")
ax.plot(x, rand_mean, color="#1F77B4", lw=2.2,
        label=f"Random removal (mean of {REPEATS} runs, seed {SEED})")
ax.fill_between(x, rand_mean - rand_std, rand_mean + rand_std,
                color="#1F77B4", alpha=0.18, label="Random \u00b11 SD")
ax.axvline(50, color="gray", ls=":", lw=1)
ax.annotate(f"{k50}/{N0} removed (50%):\ntargeted LCC={targeted[k50]:.3f}\n"
            f"random LCC={rand_mean[k50]:.3f}\u00b1{rand_std[k50]:.3f}",
            xy=(50, targeted[k50]), xytext=(57, 0.47), fontsize=10,
            arrowprops=dict(arrowstyle="->", color="gray"))
ax.set_xlabel("Fraction of nodes removed (%)")
ax.set_ylabel("Largest connected component (fraction of N)")
ax.set_title("Connectivity loss of the extended PPI network under node removal")
ax.legend()
ax.set_xlim(0, 100)
ax.set_ylim(0, 1.02)
fig.tight_layout()
out = BASE / "04_network/figure3c_robustness_v41.png"
fig.savefig(out, bbox_inches="tight")
print("figure:", out)
