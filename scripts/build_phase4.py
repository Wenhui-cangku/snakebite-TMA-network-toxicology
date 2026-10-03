# -*- coding: utf-8 -*-
"""Phase 4 - 富集总表 + 先验通路检验表 + 四轴着色气泡图"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot
setup_plot()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parents[1]  # repo root (snakebite_TMA/)
ENR = str(ROOT / "05_enrichment")

g = pd.read_csv(ENR + r"\gprofiler_raw.csv", encoding="utf-8-sig")
e = pd.read_csv(ENR + r"\enrichr_raw.csv", encoding="utf-8-sig")

# ---------- 四轴归类（按驱动基因实际归属，而非条目名关键词） ----------
GENE_AXIS = {}
for s in ["F2", "F3", "F5", "F7", "F8", "F10", "FGA", "FGB", "F9", "F11",
          "PLG", "PROC", "PROS1", "SERPINE1"]:
    GENE_AXIS[s] = "轴2 凝血/纤溶"
GENE_AXIS["GP1BA"] = "轴1 血小板/vWF"
GENE_AXIS["KDR"] = "轴4 内皮/炎症/肾"

def axis_of_row(r):
    genes = str(r["intersections"]).split(";")
    axes = [GENE_AXIS[x] for x in genes if x in GENE_AXIS]
    if not axes:
        return "其他"
    return max(set(axes), key=axes.count)  # 多数基因归属轴

# ---------- 气泡图 Top 20（g:Profiler, KEGG+REAC+GO:BP） ----------
sel = g[g["source"].isin(["KEGG", "REAC", "GO:BP"])].copy()
sel["axis"] = sel.apply(axis_of_row, axis=1)
top = sel.sort_values("p_value").head(20).iloc[::-1]
top["mlog"] = -np.log10(top["p_value"])

colors = {"轴1 血小板/vWF": "#1A56C4", "轴2 凝血/纤溶": "#B22222",
          "轴3 补体": "#1E7E34", "轴4 内皮/炎症/肾": "#B8860B", "其他": "#888888"}

fig, ax = plt.subplots(figsize=(11.2, 7.6), dpi=200)
ypos = {idx: k for k, idx in enumerate(top.index)}
for axs, c in colors.items():
    sub = top[top["axis"] == axs]
    if len(sub):
        ax.scatter(sub["mlog"], [ypos[i] for i in sub.index], s=sub["intersection_size"] * 45,
                   c=c, alpha=0.75, edgecolors="white", linewidths=0.8,
                   label=axs, zorder=3)
labels = [f"{r['name'][:52]}  [{r['source']}]" for _, r in top.iterrows()]
ax.set_yticks(range(len(top))); ax.set_yticklabels(labels, fontsize=8.2)
ax.set_xlabel("-log10(校正后 P, g:SCS)", fontsize=10)
ax.grid(axis="x", alpha=0.3, zorder=0)
size_leg = [plt.scatter([], [], s=n * 45, c="#999999", alpha=0.6, edgecolors="white") for n in (3, 7, 11)]
present = [a for a in colors if a in set(top["axis"])]
axis_handles = [Line2D([0], [0], marker="o", color="none", markerfacecolor=colors[a],
                       markeredgecolor="white", markersize=10, alpha=0.85, label=a) for a in present]
leg1 = ax.legend(handles=axis_handles, loc="lower right", fontsize=8.5,
                 frameon=True, title="四轴归属", title_fontsize=9)
ax.add_artist(leg1)
ax.legend(size_leg, ["n=3", "n=7", "n=11"], loc="upper left", bbox_to_anchor=(1.01, 1.0),
          fontsize=8, frameon=True, title="交集基因数", title_fontsize=8.5,
          labelspacing=1.4, borderpad=1.2)
ax.margins(x=0.06)
ax.set_title("Figure 4  核心靶点集富集 Top 20（g:Profiler, g:SCS<0.05）\n基因集 = Hub 10 ∪ strict 核心 10（15 唯一基因）；颜色按驱动基因四轴归属\n注：KEGG:04610 条目名含\"补体\"，但其 11 个驱动基因全为凝血/纤溶臂（补体臂 0 基因）",
             fontsize=10, weight="bold")
fig.tight_layout(rect=[0, 0, 0.88, 1])
fig.savefig(ENR + r"\figure3_enrichment_bubble.png", bbox_inches="tight")
print("figure3_enrichment_bubble.png saved")

# ---------- 先验通路检验表 ----------
prior = pd.DataFrame([
    ["hsa04610 补体与凝血级联", "KEGG p=3.90e-18 ✓", "adj=1.63e-22 ✓", "双平台显著 ✓✓",
     "11 驱动基因全为凝血/纤溶臂（F2/F3/F5/F7/F8/F10/FGA/PLG/PROC/F11/PROS1），补体臂 0 基因——H2 关键点"],
    ["hsa04611 血小板激活", "REAC 等效条目 p=1.47e-07 ✓", "adj=1.45e-03 ✓", "双平台显著 ✓✓", "GP1BA/ALB/F2/F5/F8/FGA/PLG/PROS1"],
    ["ECM–receptor interaction", "未达 g:SCS<0.05", "adj=1.81e-02 ✓", "单平台（Enrichr）", "COL4A1 等驱动"],
    ["Focal adhesion", "未达 g:SCS<0.05", "adj=4.68e-02 ✓", "单平台（Enrichr，边缘）", ""],
    ["PI3K–Akt", "未显著", "adj=9.08e-02", "不显著", ""],
    ["NF-κB", "未显著", "无此条目", "不显著", "轴4 炎症维度在 15 基因核心集上无支持，如实记录"],
    ["Fluid shear stress & atherosclerosis", "未显著", "adj=1.52e-01", "不显著", ""],
], columns=["先验通路", "g:Profiler（平台1）", "Enrichr（平台2）", "结论", "备注/驱动基因"])
prior.to_csv(ENR + r"\prior_pathway_check.csv", index=False, encoding="utf-8-sig")
print(prior[["先验通路", "结论"]].to_string(index=False))

# ---------- 双平台交集总表 ----------
e_sig = e[e["adj_p"] < 0.05].copy()
g.to_csv(ENR + r"\enrichment_gprofiler_sig116.csv", index=False, encoding="utf-8-sig")
e_sig.to_csv(ENR + r"\enrichment_enrichr_sig.csv", index=False, encoding="utf-8-sig")
both_terms = []
for kw in ["Complement and coagulation", "Platelet activation", "Fibrin", "Hemostasis",
           "Platelet degranulation", "ECM-receptor", "Focal adhesion", "Intrinsic Pathway",
           "Common Pathway", "Extrinsic Pathway", "Gamma-carboxyl", "AGE-RAGE",
           "Neutrophil extracellular trap"]:
    in_g = g[g["name"].str.contains(kw, case=False, na=False)]
    in_e = e_sig[e_sig["term"].str.contains(kw, case=False, na=False)]
    if len(in_g) and len(in_e):
        both_terms.append(kw)
print("\n双平台共同显著主题:", both_terms)
