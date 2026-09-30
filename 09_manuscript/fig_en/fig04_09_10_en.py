# -*- coding: utf-8 -*-
"""Fig 4 enrichment bubble (EN) / Fig 9 volcano (EN) / Fig 10 watchlist (EN) -> assets_en"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot
setup_plot()
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

BASE = Path(__file__).resolve().parents[2]
ENR = BASE / "05_enrichment"
GEO = BASE / "06_geo"
OUT = BASE / "09_manuscript" / "assets_en"
OUT.mkdir(exist_ok=True)

# ---------------- Fig 4 enrichment bubble (EN) ----------------
g = pd.read_csv(ENR / "gprofiler_raw.csv", encoding="utf-8-sig")
GENE_AXIS = {}
for s in ["F2", "F3", "F5", "F7", "F8", "F10", "FGA", "FGB", "F9", "F11",
          "PLG", "PROC", "PROS1", "SERPINE1"]:
    GENE_AXIS[s] = "Axis 2 Coagulation/Fibrinolysis"
GENE_AXIS["GP1BA"] = "Axis 1 Platelet/vWF"
GENE_AXIS["KDR"] = "Axis 4 Endothelium/Inflammation/Kidney"

def axis_of_row(r):
    genes = str(r["intersections"]).split(";")
    axes = [GENE_AXIS[x] for x in genes if x in GENE_AXIS]
    if not axes:
        return "Other"
    return max(set(axes), key=axes.count)

sel = g[g["source"].isin(["KEGG", "REAC", "GO:BP"])].copy()
sel["axis"] = sel.apply(axis_of_row, axis=1)
top = sel.sort_values("p_value").head(20).iloc[::-1]
top["mlog"] = -np.log10(top["p_value"])

colors = {"Axis 1 Platelet/vWF": "#1A56C4", "Axis 2 Coagulation/Fibrinolysis": "#B22222",
          "Axis 3 Complement": "#1E7E34", "Axis 4 Endothelium/Inflammation/Kidney": "#B8860B", "Other": "#888888"}

fig, ax = plt.subplots(figsize=(11.6, 7.6), dpi=200)
ypos = {idx: k for k, idx in enumerate(top.index)}
for axs, c in colors.items():
    sub = top[top["axis"] == axs]
    if len(sub):
        ax.scatter(sub["mlog"], [ypos[i] for i in sub.index], s=sub["intersection_size"] * 45,
                   c=c, alpha=0.75, edgecolors="white", linewidths=0.8, zorder=3)
labels = [f"{r['name'][:52]}  [{r['source']}]" for _, r in top.iterrows()]
ax.set_yticks(range(len(top))); ax.set_yticklabels(labels, fontsize=8.2)
ax.set_xlabel("-log10(adjusted P, g:SCS)", fontsize=10)
ax.grid(axis="x", alpha=0.3, zorder=0)
size_leg = [plt.scatter([], [], s=n * 45, c="#999999", alpha=0.6, edgecolors="white") for n in (3, 7, 11)]
present = [a for a in colors if a in set(top["axis"])]
axis_handles = [Line2D([0], [0], marker="o", color="none", markerfacecolor=colors[a],
                       markeredgecolor="white", markersize=10, alpha=0.85, label=a) for a in present]
leg1 = ax.legend(handles=axis_handles, loc="lower right", fontsize=8.5,
                 frameon=True, title="Axis assignment", title_fontsize=9)
ax.add_artist(leg1)
ax.legend(size_leg, ["n=3", "n=7", "n=11"], loc="upper left", bbox_to_anchor=(1.01, 1.0),
          fontsize=8, frameon=True, title="Intersecting genes", title_fontsize=8.5,
          labelspacing=1.4, borderpad=1.2)
ax.margins(x=0.06)
ax.set_title("Figure 4  Top-20 enrichment of the core target set (g:Profiler, g:SCS < 0.05)\n"
             "Gene set = Hub 10 ∪ strict core 10 (15 unique genes); color = four-axis assignment of driver genes\n"
             "Note: KEGG:04610 is named 'Complement and coagulation', but all 11 driver genes are in the coagulation/fibrinolysis arm (0 complement)",
             fontsize=9.5, weight="bold")
fig.tight_layout(rect=[0, 0, 0.86, 1])
fig.savefig(OUT / "figure3_enrichment_bubble.png", bbox_inches="tight")
plt.close(fig)
print("fig4 en saved")

# ---------------- Fig 9 volcano (EN) + Fig 10 watchlist (EN) ----------------
WATCH = {
    "Axis 1": ["ADAMTS13", "GP1BA", "ITGA2B", "ITGB3", "VWF"],
    "Axis 2": ["F2", "F3", "F5", "F7", "F8", "F10", "FGA", "FGG", "PLG", "PROC", "PROS1", "SERPINE1", "F11"],
    "Axis 3": ["C3", "C5", "CD46", "CFB", "CFH", "CFI"],
    "Axis 4": ["HMOX1", "IL6", "NOS3", "TNF", "VCAM1", "ICAM1", "SELE", "HAVCR1", "KDR"],
}
AXC = {"Axis 1": "#1A56C4", "Axis 2": "#B22222", "Axis 3": "#1E7E34", "Axis 4": "#B8860B"}
g2ax = {gg: a for a, gs in WATCH.items() for gg in gs}

d1 = pd.read_csv(GEO / "GSE121297_deg_static_rcab_vs_ctrl.csv", encoding="utf-8-sig")
d2 = pd.read_csv(GEO / "GSE248215_deg_DR24h_vs_ctrl.csv", encoding="utf-8-sig")

fig, axes = plt.subplots(1, 2, figsize=(13.5, 6.2), dpi=200)
for ax, df, title in [
    (axes[0], d1, "Figure 9a  GSE121297 (human HUVEC × snaclec RCαβ)\nstatic RCαβ vs static control (3 vs 3)"),
    (axes[1], d2, "Figure 9b  GSE248215 (mouse muscle × D. russelii venom)\n24 h vs PBS control (3 vs 2)"),
]:
    x = df["log2FC"].clip(-8, 8)
    y = -np.log10(df["p_value"].clip(1e-10, 1))
    ax.scatter(x, y, s=6, c="#BBBBBB", alpha=0.5, zorder=1)
    wl = df[df["symbol"].isin(g2ax)]
    for _, r in wl.iterrows():
        a = g2ax[r["symbol"]]
        ax.scatter(min(max(r["log2FC"], -8), 8), -np.log10(max(r["p_value"], 1e-10)),
                   s=42, c=AXC[a], edgecolors="black", linewidths=0.5, zorder=3)
    for _, r in wl[(wl["p_value"] < 0.05) & (wl["log2FC"].abs() > 0.58)].iterrows():
        ax.annotate(r["symbol"], (min(max(r["log2FC"], -8), 8), -np.log10(max(r["p_value"], 1e-10))),
                    textcoords="offset points", xytext=(5, 4), fontsize=8, weight="bold")
    ax.axhline(-np.log10(0.05), ls="--", lw=0.8, c="#555555")
    ax.axvline(1, ls=":", lw=0.8, c="#999999"); ax.axvline(-1, ls=":", lw=0.8, c="#999999")
    ax.set_xlabel("log2FC"); ax.set_ylabel("-log10(nominal P)")
    ax.set_title(title, fontsize=10, weight="bold")
handles = [plt.Line2D([], [], marker="o", ls="", color=c, markeredgecolor="black", markersize=8)
           for c in AXC.values()]
fig.legend(handles, [f"{a} ({'/'.join(gs[:3])}…)" for a, gs in WATCH.items()],
           loc="lower center", ncol=4, fontsize=8.5, frameon=True, title="4-axis watchlist", title_fontsize=9)
fig.tight_layout(rect=[0, 0.08, 1, 1])
fig.savefig(OUT / "figure4_volcano.png", bbox_inches="tight")
plt.close(fig)
print("fig9 en saved")

rows = []
for gg, a in g2ax.items():
    v1 = d1[d1["symbol"] == gg]
    v2 = d2[d2["symbol"] == gg]
    rows.append({"gene": gg, "axis": a,
                 "fc1": v1["log2FC"].iloc[0] if len(v1) else np.nan,
                 "p1": v1["p_value"].iloc[0] if len(v1) else np.nan,
                 "fc2": v2["log2FC"].iloc[0] if len(v2) else np.nan,
                 "p2": v2["p_value"].iloc[0] if len(v2) else np.nan})
w = pd.DataFrame(rows)
w["fc1s"] = w["fc1"].clip(-3, 7)
w["fc2s"] = w["fc2"].clip(-3, 7)
w = w.sort_values(["axis", "fc1s"], ascending=[True, False]).reset_index(drop=True)

fig, ax = plt.subplots(figsize=(10.5, 8.5), dpi=200)
y = np.arange(len(w))
ax.barh(y + 0.21, w["fc1s"], height=0.38, color="#3B6FC4", label="GSE121297 HUVEC×snaclec (human)")
ax.barh(y - 0.21, w["fc2s"], height=0.38, color="#C46A3B", label="GSE248215 muscle×D. russelii (mouse)")
for i, r in w.iterrows():
    if pd.notna(r["p1"]) and r["p1"] < 0.05:
        ax.text(r["fc1s"] + (0.08 if r["fc1s"] >= 0 else -0.08), i + 0.21, "*",
                va="center", ha="left" if r["fc1s"] >= 0 else "right", fontsize=11, weight="bold", color="#1A3E72")
    if pd.notna(r["p2"]) and r["p2"] < 0.05:
        ax.text(r["fc2s"] + (0.08 if r["fc2s"] >= 0 else -0.08), i - 0.21, "*",
                va="center", ha="left" if r["fc2s"] >= 0 else "right", fontsize=11, weight="bold", color="#7A3A14")
ax.set_yticks(y)
ax.set_yticklabels([f"{r['gene']}  [{r['axis']}]" for _, r in w.iterrows()], fontsize=8)
ax.invert_yaxis()
ax.axvline(0, c="black", lw=0.8)
ax.axvline(1, ls=":", lw=0.7, c="#999999"); ax.axvline(-1, ls=":", lw=0.7, c="#999999")
ax.set_xlabel("log2FC (display clipped at ±3/7; * = nominal p < 0.05; missing = not measured)")
ax.legend(loc="lower right", fontsize=9)
ax.set_title("Figure 10  Expression changes of the a priori four-axis watchlist in two GEO datasets", fontsize=10.5, weight="bold")
fig.tight_layout()
fig.savefig(OUT / "figure4c_watchlist.png", bbox_inches="tight")
plt.close(fig)
print("fig10 en saved")
