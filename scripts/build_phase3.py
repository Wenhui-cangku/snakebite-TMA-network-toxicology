# -*- coding: utf-8 -*-
"""
Phase 3 - 交集、PPI 与拓扑分析
1) L2 毒素靶点 ∩ 疾病主集 -> 候选核心靶点集(strict 10; extended +51 STRING邻居层)
2) Figure 2a 韦恩图
3) STRING PPI (0.7 / 0.4 双阈值, 导出 TSV)
4) MCC / Degree / EPC 三算法 Top20, Hub = 三榜交集 (Python 复现 cytoHubba)
5) 四轴映射 + QC 核查点
"""
import pandas as pd
import os, json, time, urllib.request, urllib.parse
import networkx as nx
from itertools import combinations

ROOT = Path(__file__).resolve().parents[1]  # repo root (snakebite_TMA/)
NET = os.path.join(ROOT, r"04_network")
os.makedirs(NET, exist_ok=True)
TODAY = "2026-09-24"

edges = pd.read_csv(os.path.join(ROOT, r"03_target_prediction\toxin_target_edges.csv"), encoding="utf-8-sig")
master = pd.read_csv(os.path.join(ROOT, r"02_disease_genes\disease_gene_master.csv"), encoding="utf-8-sig")

lit_t = sorted(set(edges.loc[edges["evidence_type"] == "literature", "target_symbol"]))
main = set(master.loc[master["纳入主集(是/否)"] == "是", "基因Symbol"].str.upper())
core = sorted(set(lit_t) & main)
ext_nb = sorted(set(edges.loc[edges["evidence_type"] == "string", "target_symbol"]) & main)
extended = sorted(set(core) | set(ext_nb))
print(f"strict core: {len(core)} {core}")
print(f"extended: {len(extended)}")

# ---------------- Figure 2a Venn ----------------
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot
setup_plot()
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn2_circles

fig, ax = plt.subplots(figsize=(7.2, 5.2), dpi=200)
v = venn2(subsets=(len(set(lit_t) - main), len(main - set(lit_t)), len(core)),
          set_labels=("毒素预测靶点\n(L1+L2, n=15)", "疾病基因主集\n(六源, n=1042)"), ax=ax)
v.get_patch_by_id("10").set_color("#7B1FA2"); v.get_patch_by_id("10").set_alpha(0.55)
v.get_patch_by_id("01").set_color("#1A56C4"); v.get_patch_by_id("01").set_alpha(0.45)
v.get_patch_by_id("11").set_color("#1E7E34"); v.get_patch_by_id("11").set_alpha(0.75)
venn2_circles(subsets=(len(set(lit_t) - main), len(main - set(lit_t)), len(core)), ax=ax, lw=1.0)
ax.text(0, -0.62, "交集 n = 10：COL4A1, F10, F11, F5, FGA,\nGP1BA, KDR, PLG, PROC, PROS1",
        ha="center", fontsize=8.5, color="#1E7E34", weight="bold")
ax.set_title("Figure 2a  毒素预测靶点（L1+L2）∩ 疾病基因主集", fontsize=11, weight="bold")
fig.savefig(os.path.join(NET, "figure2a_venn.png"), bbox_inches="tight")
plt.close(fig)
print("figure2a_venn.png saved")

# ---------------- STRING PPI ----------------
def string_network(genes, score):
    u = ("https://string-db.org/api/tsv/network?identifiers=" +
         urllib.parse.quote("%0d".join(genes)) +
         f"&species=9606&required_score={score}")
    req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
    for att in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                txt = r.read().decode()
            break
        except Exception as e:
            print("  STRING retry", att + 1, e); time.sleep(4)
    else:
        return pd.DataFrame()
    from io import StringIO
    df = pd.read_csv(StringIO(txt), sep="\t")
    return df[["preferredName_A", "preferredName_B", "score"]].rename(
        columns={"preferredName_A": "node1", "preferredName_B": "node2"})

ppi = {}
for tag, genes in [("core10", core), ("extended61", extended)]:
    for sc in (700, 400):
        df = string_network(genes, sc)
        df = df[df["node1"] != df["node2"]]
        ppi[(tag, sc)] = df
        df.to_csv(os.path.join(NET, f"ppi_{tag}_score{sc}.tsv"), sep="\t", index=False)
        connected = set(df["node1"]) | set(df["node2"])
        iso = sorted(set(genes) - connected)
        print(f"PPI {tag} score>={sc}: 边 {len(df)} | 孤立节点 {len(iso)} {iso if len(iso)<=8 else iso[:8]}")
        time.sleep(1)

# ---------------- 拓扑三算法 ----------------
def mcc(G):
    score = {n: 0.0 for n in G.nodes}
    import math
    for c in nx.find_cliques(G):
        w = math.factorial(len(c) - 1)
        for n in c:
            score[n] += w
    return score

def epc(G, sims=1000, p=0.5, seed=42):
    import random
    rnd = random.Random(seed)
    el = list(G.edges())
    tot = {n: 0.0 for n in G.nodes}
    for _ in range(sims):
        H = nx.Graph()
        H.add_nodes_from(G.nodes)
        H.add_edges_from(e for e in el if rnd.random() < p)
        comp = {}
        for c in nx.connected_components(H):
            for n in c:
                comp[n] = len(c)
        for n in G.nodes:
            tot[n] += comp.get(n, 1)
    return {n: tot[n] / sims for n in G.nodes}

def topn(score, n=20):
    return [g for g, _ in sorted(score.items(), key=lambda x: (-x[1], x[0]))[:n]]

results = {}
for tag, genes in [("core10", core), ("extended61", extended)]:
    df = ppi[(tag, 700)]
    G = nx.Graph()
    G.add_nodes_from(genes)
    G.add_edges_from(zip(df["node1"], df["node2"]))
    deg = dict(G.degree())
    m = mcc(G) if len(G.edges) else {n: 0 for n in G.nodes}
    e = epc(G) if len(G.edges) else {n: 0 for n in G.nodes}
    t_deg, t_mcc, t_epc = topn(deg), topn(m), topn(e)
    hub = sorted(set(t_deg) & set(t_mcc) & set(t_epc))
    results[tag] = {"deg": deg, "mcc": m, "epc": e,
                    "top_deg": t_deg, "top_mcc": t_mcc, "top_epc": t_epc, "hub": hub}
    print(f"\n[{tag}] 节点 {len(G.nodes)} 边 {len(G.edges)}")
    print("  Hub (三榜交集):", hub)

# ---------------- Hub 表 + 四轴 ----------------
ax_map = dict(zip(master["基因Symbol"].str.upper(), master["归属病理轴(1-4)"]))
rows = []
for g in results["extended61"]["hub"]:
    rows.append({"基因Symbol": g,
                 "Degree": results["extended61"]["deg"].get(g, 0),
                 "MCC": results["extended61"]["mcc"].get(g, 0),
                 "EPC": round(results["extended61"]["epc"].get(g, 0), 2),
                 "归属病理轴": ax_map.get(g, ""),
                 "strict核心": "是" if g in core else "否（扩展层）"})
hub_df = pd.DataFrame(rows).sort_values(["strict核心", "Degree"], ascending=[True, False])
hub_df.to_csv(os.path.join(NET, "hub_genes.csv"), index=False, encoding="utf-8-sig")
print("\nhub_genes.csv:")
print(hub_df.to_string(index=False))

# QC 核查点
qc_targets = ["ADAMTS13", "VWF", "F2", "F10", "C3", "VCAM1"]
print("\nQC H1/H2 核查:")
for g in qc_targets:
    loc = ("strict" if g in core else
           "hub" if g in results["extended61"]["hub"] else
           "extended" if g in extended else "缺失")
    print(f"  {g}: {loc}")

json.dump({t: {k: v for k, v in r.items() if k in ("top_deg", "top_mcc", "top_epc", "hub")}
           for t, r in results.items()},
          open(os.path.join(NET, "phase3_topology.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("\nphase3_topology.json saved")
