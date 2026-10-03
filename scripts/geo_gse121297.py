# -*- coding: utf-8 -*-
"""
GSE121297 (GPL570/Affymetrix HG-U133 Plus 2.0) 差异表达
对比: 静态 RCab (GSM3430997-999) vs 静态对照 (GSM3430994-996), 3v3
探针注释: g:Profiler convert API (AFFY_HG_U133_PLUS_2)
统计: Welch t + BH FDR (Python 复现; 报告注明替代 limma)
"""
from pathlib import Path
import pandas as pd
import numpy as np
import urllib.request, json, ssl, time, os
from scipy import stats

DIR = str(Path(__file__).resolve().parents[1] / "06_geo")
ctx = ssl._create_unverified_context()

mat = pd.read_pickle(os.path.join(DIR, "gse121297_gpl570_matrix.pkl"))
CTRL = ["GSM3430994", "GSM3430995", "GSM3430996"]
RCAB = ["GSM3430997", "GSM3430998", "GSM3430999"]

MAP = os.path.join(DIR, "gpl570_probe2symbol.csv")
if os.path.exists(MAP):
    mp = pd.read_csv(MAP)
else:
    probes = list(mat.index)
    rows = []
    for i in range(0, len(probes), 3000):
        batch = probes[i:i+3000]
        body = json.dumps({"organism": "hsapiens", "query": batch,
                           "target": "ENSG", "numeric_ns": "AFFY_HG_U133_PLUS_2"}).encode()
        req = urllib.request.Request("https://biit.cs.ut.ee/gprofiler/api/convert/convert/",
                                     data=body, headers={"Content-Type": "application/json",
                                                         "User-Agent": "Mozilla/5.0"})
        for att in range(3):
            try:
                with urllib.request.urlopen(req, timeout=120, context=ctx) as r:
                    d = json.loads(r.read())
                break
            except Exception as e:
                print("retry", i, att, e); time.sleep(4)
        else:
            continue
        for it in d["result"]:
            rows.append({"probe": it["incoming"], "symbol": it.get("name", ""),
                         "ensg": it.get("converted", "")})
        print(f"converted {i+len(batch)}/{len(probes)}")
        time.sleep(0.4)
    mp = pd.DataFrame(rows)
    mp.to_csv(MAP, index=False)
print("mapping rows:", len(mp))

# 基因级汇总: 每 symbol 取平均表达最高的探针
m = mat.copy()
m["probe"] = m.index
mm = m.melt(id_vars="probe", var_name="sample", value_name="expr")
mm = mm.merge(mp[["probe", "symbol"]], on="probe")
mm = mm[mm["symbol"].notna() & (mm["symbol"] != "")]
gene_sample = mm.groupby(["symbol", "sample"])["expr"].max().unstack()
print("gene-level matrix:", gene_sample.shape)

# Welch t-test
c = gene_sample[CTRL].values
t = gene_sample[RCAB].values
logfc = t.mean(axis=1) - c.mean(axis=1)
pvals = np.array([stats.ttest_ind(t[i], c[i], equal_var=False).pvalue
                  if not (np.allclose(t[i], t[i][0]) and np.allclose(c[i], c[i][0])) else 1.0
                  for i in range(len(gene_sample))])
pvals = np.nan_to_num(pvals, nan=1.0)
order = np.argsort(pvals)
rank = np.empty(len(pvals), dtype=int)
rank[order] = np.arange(1, len(pvals) + 1)
adj = np.minimum.accumulate((pvals[order] * len(pvals) / rank[order])[::-1])[::-1]
adj_full = np.empty(len(pvals))
adj_full[order] = adj

res = pd.DataFrame({"symbol": gene_sample.index, "log2FC": logfc,
                    "p_value": pvals, "adj_p": np.clip(adj_full, 0, 1),
                    "mean_ctrl": c.mean(axis=1), "mean_rcab": t.mean(axis=1)})
res = res.sort_values("adj_p")
res.to_csv(os.path.join(DIR, "GSE121297_deg_static_rcab_vs_ctrl.csv"),
           index=False, encoding="utf-8-sig")
deg = res[(res["adj_p"] < 0.05) & (res["log2FC"].abs() > 1)]
print(f"\nDEG (adj<0.05 & |log2FC|>1): {len(deg)} | 上调 {(deg['log2FC']>0).sum()} 下调 {(deg['log2FC']<0).sum()}")
print(res.head(15).to_string(index=False))

# 先验 27 + Hub 基因核查
watch = ["ADAMTS13","C3","C5","CD46","CFB","CFH","CFI","FGA","GP1BA","HMOX1","IL6",
         "ITGA2B","ITGB3","NOS3","PLG","SERPINE1","TNF","VWF","F2","F5","F10","FGG",
         "PROC","VCAM1","ICAM1","SELE","HAVCR1","F3","F7","F8","F11","PROS1","KDR","COL4A1","ALB"]
sub = res[res["symbol"].isin(watch)].copy()
sub["signif"] = np.where((sub["adj_p"] < 0.05) & (sub["log2FC"].abs() > 1), "DEG",
                np.where(sub["adj_p"] < 0.05, "adj<0.05", "ns"))
print("\n=== 先验/Hub 基因表达核查 ===")
print(sub.sort_values("adj_p").to_string(index=False))
sub.to_csv(os.path.join(DIR, "GSE121297_watchlist.csv"), index=False, encoding="utf-8-sig")
