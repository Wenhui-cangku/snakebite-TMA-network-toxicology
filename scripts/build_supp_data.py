# Repo-portable copy of the workspace builder (paths resolved from this file location).
# -*- coding: utf-8 -*-
"""Generate source tables for Supplementary Tables S4, S6, S10 (v44, 2026-10-02).
Outputs to snakebite_TMA/09_manuscript/supplementary/data/"""
import json, random, sys, time
from pathlib import Path
import numpy as np
import pandas as pd
import networkx as nx

ROOT = Path(__file__).resolve().parents[1]  # repo root
OUT = ROOT / '09_manuscript/supplementary/data'
OUT.mkdir(parents=True, exist_ok=True)

# ---------- shared: load extended-layer network ----------
G = nx.Graph()
with open(ROOT / '04_network/ppi_extended61_score700.tsv', encoding='utf-8-sig') as f:
    f.readline()
    for line in f:
        p = line.strip().split('\t')
        if len(p) >= 2:
            G.add_edge(p[0], p[1])
N0 = G.number_of_nodes()
print(f'network: {N0} nodes, {G.number_of_edges()} edges')

# ---------- S4: full three-algorithm ranking on all 54 nodes ----------
def mcc(G):
    import math
    score = {n: 0.0 for n in G.nodes}
    for c in nx.find_cliques(G):
        w = math.factorial(len(c) - 1)
        for n in c:
            score[n] += w
    return score

def epc(G, sims=1000, p=0.5, seed=42):
    rnd = random.Random(seed)
    el = list(G.edges())
    tot = {n: 0.0 for n in G.nodes}
    for _ in range(sims):
        H = nx.Graph(); H.add_nodes_from(G.nodes)
        H.add_edges_from(e for e in el if rnd.random() < p)
        comp = {}
        for c in nx.connected_components(H):
            for n in c:
                comp[n] = len(c)
        for n in G.nodes:
            tot[n] += comp.get(n, 1)
    return {n: tot[n] / sims for n in G.nodes}

deg = dict(G.degree())
mcc_s = mcc(G)
epc_s = epc(G)
hub = pd.read_csv(ROOT / '04_network/hub_genes.csv', encoding='utf-8-sig')
hub_set = set(hub['基因Symbol'])
strict = set(json.load(open(ROOT / '04_network/intersection_sets.json', encoding='utf-8'))['core_strict'])
axis_map = dict(zip(hub['基因Symbol'], hub['归属病理轴']))
rows = []
for n in G.nodes:
    rows.append({'gene': n, 'degree': deg[n], 'MCC': mcc_s[n], 'EPC': round(epc_s[n], 2),
                 'hub10': n in hub_set, 'strict_core10': n in strict,
                 'pathology_axis': axis_map.get(n, '')})
s4 = pd.DataFrame(rows)
s4['degree_rank'] = s4['degree'].rank(ascending=False, method='min').astype(int)
s4['MCC_rank'] = s4['MCC'].rank(ascending=False, method='min').astype(int)
s4['EPC_rank'] = s4['EPC'].rank(ascending=False, method='min').astype(int)
s4 = s4.sort_values(['degree_rank', 'gene']).reset_index(drop=True)
s4.to_csv(OUT / 'S4_full_three_algorithm_ranking.csv', index=False, encoding='utf-8-sig')
print('S4 ranking rows:', len(s4), '| hub reproduced:', sorted(hub_set & set(s4[s4.degree_rank<=20].gene))[:12])

# ---------- S10: per-run robustness curves (seed 1234, 100 repeats) ----------
random.seed(1234)
def lcc_frac(g):
    return max((len(c) for c in nx.connected_components(g)), default=0) / N0
order = [n for n, _ in sorted(G.degree(), key=lambda x: -x[1])]
targeted = [1.0]
g = G.copy()
for n in order:
    g.remove_node(n); targeted.append(lcc_frac(g))
rand_curves = []
for rep in range(100):
    g = G.copy()
    nodes = list(g.nodes()); random.shuffle(nodes)
    curve = [1.0]
    for n in nodes:
        g.remove_node(n); curve.append(lcc_frac(g))
    rand_curves.append(curve)
mat = np.array(rand_curves)
ref = json.load(open(ROOT / '04_network/robustness_results_v41.json', encoding='utf-8'))
assert np.allclose(mat.mean(axis=0), ref['random_mean']), 'mean mismatch vs archived JSON'
assert np.allclose(targeted, ref['targeted_curve']), 'targeted mismatch'
print('S10 verified vs robustness_results_v41.json (mean & targeted identical)')
runs = pd.DataFrame(mat.T, columns=[f'run_{i+1}' for i in range(100)])
runs.insert(0, 'k_removed', range(N0 + 1))
runs['targeted_static_degree'] = targeted
runs['random_mean'] = mat.mean(axis=0)
runs['random_sd'] = mat.std(axis=0)
runs.to_csv(OUT / 'S10_robustness_per_run_curves.csv', index=False, encoding='utf-8-sig')
pd.DataFrame({'removal_order': range(1, N0 + 1), 'gene': order,
              'degree': [deg[n] for n in order]}).to_csv(
    OUT / 'S10_targeted_removal_order.csv', index=False, encoding='utf-8-sig')
print('S10 per-run curves saved:', runs.shape)

# ---------- S6: g:Profiler sensitivity (15-gene vs 11-gene input) ----------
GENES15 = ['F2','F3','F5','F7','F8','F10','FGA','PLG','PROC','ALB','COL4A1','F11','GP1BA','KDR','PROS1']
FORCED = ['F2','F5','F10','FGG','PROC','VCAM1','ICAM1','SELE','HAVCR1']
GENES11 = [g for g in GENES15 if g not in FORCED]
print('11-gene sensitivity set:', GENES11)

def gost(query, tag):
    import urllib.request
    payload = json.dumps({
        'organism': 'hsapiens', 'query': query,
        'sources': ['GO:BP', 'GO:CC', 'GO:MF', 'KEGG', 'REAC'],
        'user_threshold': 0.05, 'correction_method': 'g_SCS',
        'no_evidences': False}).encode()
    req = urllib.request.Request('https://biit.cs.ut.ee/gprofiler/api/gost/profile/',
                                 data=payload, headers={'Content-Type': 'application/json',
                                                        'User-Agent': 'snakebite-TMA-supplement/1.0'})
    with urllib.request.urlopen(req, timeout=120) as r:
        d = json.loads(r.read().decode())
    rows = []
    for t in d['result']:
        rows.append({'source': t['source'], 'native': t['native'], 'name': t['name'],
                     'p_value': t['p_value'], 'term_size': t['term_size'],
                     'query_size': t['query_size'], 'intersection_size': t['intersection_size'],
                     'intersections': ';'.join(t.get('intersections', [])) if t.get('intersections') else ''})
    df = pd.DataFrame(rows)
    df.to_csv(OUT / f'S6_gprofiler_{tag}.csv', index=False, encoding='utf-8-sig')
    print(f'g:Profiler {tag}: {len(df)} significant terms (g:SCS<0.05)')
    return df

try:
    d15 = gost(GENES15, 'input15_verify')
    time.sleep(2)
    d11 = gost(GENES11, 'input11_no_forced')
    old = pd.read_csv(ROOT / '05_enrichment/gprofiler_raw.csv', encoding='utf-8-sig')
    same = set(old['native']) == set(d15['native'])
    print('15-gene rerun reproduces archived 116 terms:', same,
          f'(archived {len(old)}, rerun {len(d15)})')
    # key terms in the 11-gene sensitivity run
    for nat in ['R-HSA-140877', 'KEGG:04610', 'hsa04610', 'R-HSA-76005', 'R-HSA-76002']:
        hit = d11[d11['native'].str.contains(nat.replace('KEGG:',''), na=False)]
        if len(hit):
            r = hit.iloc[0]
            print(f'  11-gene: {r["native"]} {r["name"][:45]} p={r["p_value"]:.2e} {r["intersection_size"]}/{r["query_size"]}')
        else:
            print(f'  11-gene: {nat} NOT significant')
except Exception as e:
    print('g:Profiler API failed:', e)
