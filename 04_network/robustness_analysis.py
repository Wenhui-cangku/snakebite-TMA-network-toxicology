# -*- coding: utf-8 -*-
"""网络鲁棒性/扰动分析: 扩展层54节点PPI 随机攻击 vs 靶向攻击 + 致命节点识别"""
import json, random, sys
from pathlib import Path
import networkx as nx

BASE = Path(__file__).resolve().parents[1]
random.seed(1234)

# 读扩展层 PPI (score>=0.7)
G = nx.Graph()
with open(BASE/"04_network/ppi_extended61_score700.tsv", encoding="utf-8-sig") as f:
    header = f.readline().strip().split("\t")
    for line in f:
        parts = line.strip().split("\t")
        if len(parts) >= 2:
            G.add_edge(parts[0], parts[1])
print(f"网络: {G.number_of_nodes()} 节点, {G.number_of_edges()} 边")

N0 = G.number_of_nodes()
def lcc_size(g):
    return max((len(c) for c in nx.connected_components(g)), default=0)

# 1) 靶向攻击: 按 degree 降序逐个移除
order = [n for n, _ in sorted(G.degree(), key=lambda x: -x[1])]
targeted = []
g = G.copy()
for n in order:
    g.remove_node(n)
    targeted.append(lcc_size(g) / N0)

# 2) 随机攻击: 100 次平均
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

# 3) 致命节点: 单独移除后 LCC 下降幅度排名
base = lcc_size(G) / N0
impact = []
for n in G.nodes():
    g = G.copy(); g.remove_node(n)
    impact.append((n, G.degree(n), base - lcc_size(g)/N0,
                   nx.connected_components(g) and len(list(nx.connected_components(g))) or 0))
impact.sort(key=lambda x: -x[2])
print("\n致命节点 Top10 (移除后LCC损失):")
for n, d, loss, ncomp in impact[:10]:
    print(f"  {n}: degree={d}, LCC损失={loss:.3f}, 剩余连通分量={ncomp}")

# 移除比例达50%时的LCC对比
i50 = int(N0*0.5)
print(f"\n移除50%节点后 LCC 占比: 靶向={targeted[i50]:.3f} vs 随机={rand_mean[i50]:.3f}±{rand_std[i50]:.3f}")

# 保存结果
json.dump({
    "n_nodes": N0, "n_edges": G.number_of_edges(),
    "targeted_curve": targeted, "random_mean": rand_mean.tolist(), "random_std": rand_std.tolist(),
    "lethal_top10": [(n, d, round(loss,4)) for n, d, loss, _ in impact[:10]],
    "at_50pct": {"targeted": round(targeted[i50],4), "random": round(float(rand_mean[i50]),4)},
}, open(BASE/"04_network/robustness_results.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)

# 出图
sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot
setup_plot()
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(7.5, 5.5), dpi=200)
x = np.arange(N0) / N0 * 100
ax.plot(x, targeted, color="#D62728", lw=2.2, label="靶向攻击 (按degree降序移除)")
ax.plot(x, rand_mean, color="#1F77B4", lw=2.2, label="随机攻击 (100次均值)")
ax.fill_between(x, rand_mean-rand_std, rand_mean+rand_std, color="#1F77B4", alpha=0.18)
ax.axvline(50, color="gray", ls=":", lw=1)
ax.annotate(f"50%移除: 靶向LCC={targeted[i50]:.2f} vs 随机LCC={rand_mean[i50]:.2f}",
            xy=(50, targeted[i50]), xytext=(42, 0.62), fontsize=10,
            arrowprops=dict(arrowstyle="->", color="gray"))
ax.set_xlabel("移除节点比例 (%)"); ax.set_ylabel("最大连通子图占比 (LCC/N)")
ax.set_title("毒素–宿主 PPI 网络鲁棒性：凝血枢纽靶向脆弱性显著高于随机攻击", fontsize=11)
ax.legend(); ax.set_xlim(0,100); ax.set_ylim(0,1.02)
fig.tight_layout()
out = BASE/"04_network/figure3c_robustness.png"
fig.savefig(out, bbox_inches="tight")
print("\n图:", out)
