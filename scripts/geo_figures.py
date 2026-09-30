# -*- coding: utf-8 -*-
"""GEO validation-layer figures: dual volcano plots + watchlist two-dataset comparison bar chart"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot
setup_plot()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

DIR = str(Path(__file__).resolve().parents[1] / "06_geo")
WATCH = {
    "Axis1": ["ADAMTS13", "GP1BA", "ITGA2B", "ITGB3", "VWF"],
    "Axis2": ["F2", "F3", "F5", "F7", "F8", "F10", "FGA", "FGG", "PLG", "PROC", "PROS1", "SERPINE1", "F11"],
    "Axis3": ["C3", "C5", "CD46", "CFB", "CFH", "CFI"],
    "Axis4": ["HMOX1", "IL6", "NOS3", "TNF", "VCAM1", "ICAM1", "SELE", "HAVCR1", "KDR"],
}
AXC = {"Axis1": "#1A56C4", "Axis2": "#B22222", "Axis3": "#1E7E34", "Axis4": "#B8860B"}
g2ax = {g: a for a, gs in WATCH.items() for g in gs}

d1 = pd.read_csv(DIR + r"\GSE121297_deg_static_rcab_vs_ctrl.csv", encoding="utf-8-sig")
d2 = pd.read_csv(DIR + r"\GSE248215_deg_DR24h_vs_ctrl.csv", encoding="utf-8-sig")

fig, axes = plt.subplots(1, 2, figsize=(13.5, 6.2), dpi=200)
for ax, df, title, xlab in [
    (axes[0], d1, "Figure 9a  GSE121297 (human HUVEC × snaclec RCαβ)\nstatic RCαβ vs static control (3v3)", "log2FC"),
    (axes[1], d2, "Figure 9b  GSE248215 (mouse muscle × D. russelii venom)\n24h vs PBS control (3v2)", "log2FC"),
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
    ax.set_xlabel(xlab); ax.set_ylabel("-log10(nominal P)")
    ax.set_title(title, fontsize=10, weight="bold")
handles = [plt.Line2D([], [], marker="o", ls="", color=c, markeredgecolor="black", markersize=8)
           for c in AXC.values()]
fig.legend(handles, [f"{a}（{'/'.join(gs[:3])}…）" for a, gs in WATCH.items()],
           loc="lower center", ncol=4, fontsize=8.5, frameon=True, title="watchlist four axes", title_fontsize=9)
fig.tight_layout(rect=[0, 0.08, 1, 1])
fig.savefig(DIR + r"\figure4_volcano.png", bbox_inches="tight")
plt.close(fig)
print("figure4_volcano.png saved")

# ---- watchlist comparison bar chart ----
rows = []
for g, a in g2ax.items():
    v1 = d1[d1["symbol"] == g]
    v2 = d2[d2["symbol"] == g]
    rows.append({"gene": g, "axis": a,
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
b1 = ax.barh(y + 0.21, w["fc1s"], height=0.38, color="#3B6FC4", label="GSE121297 HUVEC×snaclec (human)")
b2 = ax.barh(y - 0.21, w["fc2s"], height=0.38, color="#C46A3B", label="GSE248215 muscle×D. russelii (mouse)")
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
ax.set_xlabel("log2FC (display truncated at ±3/7; * = nominal p<0.05; missing = not measured in that dataset)")
ax.legend(loc="lower right", fontsize=9)
ax.set_title("Figure 10  Expression changes of the prior four-axis watchlist in the two GEO datasets", fontsize=10.5, weight="bold")
fig.tight_layout()
fig.savefig(DIR + r"\figure4c_watchlist.png", bbox_inches="tight")
plt.close(fig)
w.to_csv(DIR + r"\geo_watchlist_combined.csv", index=False, encoding="utf-8-sig")
print("figure4c_watchlist.png saved; geo_watchlist_combined.csv saved")
print()
print(w[w["p1"] < 0.05][["gene", "axis", "fc1", "p1"]].to_string(index=False))
print()
print(w[w["p2"] < 0.05][["gene", "axis", "fc2", "p2"]].to_string(index=False))
