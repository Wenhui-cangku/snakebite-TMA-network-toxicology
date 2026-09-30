# -*- coding: utf-8 -*-
"""Phase 4 - enrichment master table + prior-pathway check table + four-axis colored bubble chart"""
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

# ---------- four-axis assignment (by actual driver-gene membership, not term-name keywords) ----------
GENE_AXIS = {}
for s in ["F2", "F3", "F5", "F7", "F8", "F10", "FGA", "FGB", "F9", "F11",
          "PLG", "PROC", "PROS1", "SERPINE1"]:
    GENE_AXIS[s] = "Axis2 coagulation/fibrinolysis"
GENE_AXIS["GP1BA"] = "Axis1 platelet/vWF"
GENE_AXIS["KDR"] = "Axis4 endothelium/inflammation/kidney"

def axis_of_row(r):
    genes = str(r["intersections"]).split(";")
    axes = [GENE_AXIS[x] for x in genes if x in GENE_AXIS]
    if not axes:
        return "other"
    return max(set(axes), key=axes.count)  # axis of the majority of genes

# ---------- bubble chart Top 20 (g:Profiler, KEGG+REAC+GO:BP) ----------
sel = g[g["source"].isin(["KEGG", "REAC", "GO:BP"])].copy()
sel["axis"] = sel.apply(axis_of_row, axis=1)
top = sel.sort_values("p_value").head(20).iloc[::-1]
top["mlog"] = -np.log10(top["p_value"])

colors = {"Axis1 platelet/vWF": "#1A56C4", "Axis2 coagulation/fibrinolysis": "#B22222",
          "Axis3 complement": "#1E7E34", "Axis4 endothelium/inflammation/kidney": "#B8860B", "other": "#888888"}

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
ax.set_xlabel("-log10(adjusted P, g:SCS)", fontsize=10)
ax.grid(axis="x", alpha=0.3, zorder=0)
size_leg = [plt.scatter([], [], s=n * 45, c="#999999", alpha=0.6, edgecolors="white") for n in (3, 7, 11)]
present = [a for a in colors if a in set(top["axis"])]
axis_handles = [Line2D([0], [0], marker="o", color="none", markerfacecolor=colors[a],
                       markeredgecolor="white", markersize=10, alpha=0.85, label=a) for a in present]
leg1 = ax.legend(handles=axis_handles, loc="lower right", fontsize=8.5,
                 frameon=True, title="four-axis assignment", title_fontsize=9)
ax.add_artist(leg1)
ax.legend(size_leg, ["n=3", "n=7", "n=11"], loc="upper left", bbox_to_anchor=(1.01, 1.0),
          fontsize=8, frameon=True, title="intersection gene count", title_fontsize=8.5,
          labelspacing=1.4, borderpad=1.2)
ax.margins(x=0.06)
ax.set_title("Figure 4  Enrichment Top 20 of the core target set (g:Profiler, g:SCS<0.05)\nGene set = Hub 10 ∪ strict core 10 (15 unique genes); colors by driver-gene four-axis assignment\nNote: KEGG:04610 is named \"complement and coagulation\", but all its 11 driver genes are on the coagulation/fibrinolysis arm (0 complement-arm genes)",
             fontsize=10, weight="bold")
fig.tight_layout(rect=[0, 0, 0.88, 1])
fig.savefig(ENR + r"\figure3_enrichment_bubble.png", bbox_inches="tight")
print("figure3_enrichment_bubble.png saved")

# ---------- prior-pathway check table ----------
prior = pd.DataFrame([
    ["hsa04610 Complement and coagulation cascades", "KEGG p=3.90e-18 ✓", "adj=1.63e-22 ✓", "significant on both platforms ✓✓",
     "all 11 driver genes are on the coagulation/fibrinolysis arm (F2/F3/F5/F7/F8/F10/FGA/PLG/PROC/F11/PROS1); zero genes on the complement arm — key point for H2"],
    ["hsa04611 Platelet activation", "REAC equivalent term p=1.47e-07 ✓", "adj=1.45e-03 ✓", "significant on both platforms ✓✓", "GP1BA/ALB/F2/F5/F8/FGA/PLG/PROS1"],
    ["ECM–receptor interaction", "did not reach g:SCS<0.05", "adj=1.81e-02 ✓", "single platform (Enrichr)", "driven by COL4A1 et al."],
    ["Focal adhesion", "did not reach g:SCS<0.05", "adj=4.68e-02 ✓", "single platform (Enrichr, borderline)", ""],
    ["PI3K–Akt", "not significant", "adj=9.08e-02", "not significant", ""],
    ["NF-κB", "not significant", "no such term", "not significant", "Axis-4 inflammatory dimension has no support on the 15-gene core set; recorded as-is"],
    ["Fluid shear stress & atherosclerosis", "not significant", "adj=1.52e-01", "not significant", ""],
], columns=["prior_pathway", "g:Profiler (platform 1)", "Enrichr (platform 2)", "conclusion", "notes/driver_genes"])
prior.to_csv(ENR + r"\prior_pathway_check.csv", index=False, encoding="utf-8-sig")
print(prior[["prior_pathway", "conclusion"]].to_string(index=False))

# ---------- dual-platform intersection master table ----------
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
print("\nthemes jointly significant on both platforms:", both_terms)
