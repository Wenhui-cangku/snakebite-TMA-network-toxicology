# -*- coding: utf-8 -*-
"""Figure 4 four-layer heterogeneous network: generate Cytoscape import files (nodes/edges/cyjs) + matplotlib preview"""
import json, csv, sys
from pathlib import Path

OUT = Path(__file__).resolve().parent / "cytoscape"
OUT.mkdir(exist_ok=True)

# ---------- nodes ----------
# (id, label, layer, type, family/axis, hub, docking/notes, color, shape)
NODES = [
    # L1 toxins
    ("RVVX",  "RVV-X",        1, "toxin", "SVMP+snaclec complex", "", "ClusPro✅ HADDOCK-site✅", "#D62728", "HEXAGON"),
    ("RVVV",  "RVV-Vγ",       1, "toxin", "SVSP",                "", "ClusPro✅ HADDOCK✅✅ co-crystal✅", "#D62728", "HEXAGON"),
    ("DABK",  "daborhagin-K", 1, "toxin", "SVMP (P-III)",        "", "ClusPro✅ HADDOCK-site✅", "#D62728", "HEXAGON"),
    ("SNAC",  "snaclec Q38L02",1,"toxin", "snaclec/CTL",         "", "ClusPro✅", "#D62728", "HEXAGON"),
    ("PLA2",  "PLA2 VRV-PL-VIIIa",1,"toxin","PLA2",              "", "ClusPro✅", "#D62728", "HEXAGON"),
    ("KUN",   "Kunitz H6VC06", 1, "toxin","Kunitz inhibitor",       "", "ClusPro✅ HADDOCK-site✅", "#D62728", "HEXAGON"),
    ("SVVEGF","svVEGF",       1, "toxin", "VEGF",                "", "ClusPro✅✅ HDock✅", "#D62728", "HEXAGON"),
    # L2 host direct targets
    ("F10",   "F10",    2, "target", "Axis2 coagulation/fibrinolysis", "Hub+strict", "RVV-X activation / PLA2 binding / weak Kunitz inhibition", "#1F77B4", "ELLIPSE"),
    ("F9",    "F9",     2, "target", "Axis2 coagulation/fibrinolysis", "",          "RVV-X activation", "#1F77B4", "ELLIPSE"),
    ("PROS1", "PROS1",  2, "target", "Axis2 coagulation/fibrinolysis", "strict",    "RVV-X activation", "#1F77B4", "ELLIPSE"),
    ("F5",    "F5",     2, "target", "Axis2 coagulation/fibrinolysis", "Hub+strict","RVV-Vγ activation", "#1F77B4", "ELLIPSE"),
    ("FGA",   "FGA",    2, "target", "Axis2 coagulation/fibrinolysis", "Hub+strict","daborhagin-K hydrolysis", "#1F77B4", "ELLIPSE"),
    ("FN1",   "FN1",    2, "target", "ECM",           "",          "daborhagin-K hydrolysis", "#1F77B4", "ELLIPSE"),
    ("COL4A1","COL4A1", 2, "target", "ECM",           "strict",    "daborhagin-K hydrolysis", "#1F77B4", "ELLIPSE"),
    ("GP1BA", "GP1BA",  2, "target", "Axis1 VWF/platelet","strict",    "snaclec binding (competitive inhibition)", "#1F77B4", "ELLIPSE"),
    ("PLG",   "PLG",    2, "target", "Axis2 coagulation/fibrinolysis", "Hub+strict","Kunitz inhibition Ki=0.19nM", "#1F77B4", "ELLIPSE"),
    ("F11",   "F11",    2, "target", "Axis2 coagulation/fibrinolysis", "strict",    "Kunitz inhibition Ki=6nM", "#1F77B4", "ELLIPSE"),
    ("PRSS1", "PRSS1",  2, "target", "other (digestive enzyme)",  "",          "Kunitz inhibition 70%", "#1F77B4", "ELLIPSE"),
    ("KDR",   "KDR",    2, "target", "Axis4 endothelium/inflammation/kidney","strict",  "svVEGF activation", "#1F77B4", "ELLIPSE"),
    # L3 pathways
    ("PW_FIB",  "Formation of Fibrin Clot\n(REAC 140877, p=9.7e-23)", 3, "pathway", "coagulation", "", "", "#2CA02C", "ROUND_RECTANGLE"),
    ("PW_COAG", "Complement & Coagulation\n(KEGG 04610, p=3.9e-18)",  3, "pathway", "coagulation+complement", "", "", "#2CA02C", "ROUND_RECTANGLE"),
    ("PW_PLT",  "Platelet Activation\n(REAC 76002, p=1.5e-07)",       3, "pathway", "Axis1 platelet", "", "", "#2CA02C", "ROUND_RECTANGLE"),
    ("PW_ECM",  "ECM-Receptor Interaction\n(KEGG 04512, adj=0.018)",  3, "pathway", "ECM", "", "single platform (Enrichr)", "#2CA02C", "ROUND_RECTANGLE"),
    ("PW_FA",   "Focal Adhesion\n(KEGG 04510, adj=0.047)",            3, "pathway", "ECM", "", "single platform (Enrichr, borderline)", "#2CA02C", "ROUND_RECTANGLE"),
    ("PW_VEGF", "VEGFR2 Signaling\n(REAC 195399, adj=0.023)",         3, "pathway", "Axis4 endothelium", "", "", "#2CA02C", "ROUND_RECTANGLE"),
    # L4 phenotypes
    ("PH_VICC", "VICC\nconsumptive coagulopathy",        4, "phenotype", "", "", "", "#9467BD", "DIAMOND"),
    ("PH_THR",  "Thrombocytopenia\nthrombocytopenia", 4, "phenotype", "", "", "", "#9467BD", "DIAMOND"),
    ("PH_MAHA", "MAHA\nmicroangiopathic hemolytic anemia",  4, "phenotype", "", "", "", "#9467BD", "DIAMOND"),
    ("PH_AKI",  "AKI\nacute kidney injury",           4, "phenotype", "", "", "", "#9467BD", "DIAMOND"),
    ("PH_LEAK", "Capillary Leak\ncapillary leak / hypotension", 4, "phenotype", "", "", "", "#9467BD", "DIAMOND"),
]

# ---------- edges ----------
# (source, target, interaction, evidence, note)
EDGES = [
    # L1→L2 literature direct interactions (score=1)
    ("RVVX","F10","direct","literature","RVV-X heavy chain cleaves and activates FX (PMID 37092784 et al.)"),
    ("RVVX","F9","direct","literature","RVV-X heavy chain cleaves and activates FIX"),
    ("RVVX","PROS1","direct","literature","RVV-X cleaves and activates protein S"),
    ("RVVV","F5","direct","literature","RVV-Vγ cleaves FV Arg1545-Ser1546"),
    ("DABK","FGA","direct","literature","hydrolyzes fibrinogen Aα (PMID 18554518)"),
    ("DABK","FN1","direct","literature","hydrolyzes fibronectin in vitro"),
    ("DABK","COL4A1","direct","literature","hydrolyzes type IV collagen in vitro"),
    ("SNAC","GP1BA","direct","literature","binds GPIbα and inhibits ristocetin-induced aggregation"),
    ("PLA2","F10","direct","literature","binds FXa IC50=130nM (PMID 18062812)"),
    ("KUN","PLG","direct","literature","inhibits plasmin 90% Ki=0.19nM"),
    ("KUN","F11","direct","literature","inhibits FXIa 37% Ki=6nM"),
    ("KUN","F10","direct","literature","inhibits FXa 20%"),
    ("KUN","PRSS1","direct","literature","inhibits trypsin 70%"),
    ("SVVEGF","KDR","direct","literature","induces angiogenesis via VEGFR2 / NO hypotension"),
    # L2→L3 pathway membership
    ("F10","PW_FIB","membership","enrichment",""),("F5","PW_FIB","membership","enrichment",""),
    ("FGA","PW_FIB","membership","enrichment",""),("F11","PW_FIB","membership","enrichment",""),
    ("GP1BA","PW_FIB","membership","enrichment",""),("PROS1","PW_FIB","membership","enrichment",""),
    ("F10","PW_COAG","membership","enrichment",""),("FGA","PW_COAG","membership","enrichment",""),
    ("PLG","PW_COAG","membership","enrichment",""),("F11","PW_COAG","membership","enrichment",""),
    ("PROS1","PW_COAG","membership","enrichment",""),
    ("FGA","PW_PLT","membership","enrichment",""),("PLG","PW_PLT","membership","enrichment",""),
    ("GP1BA","PW_PLT","membership","enrichment",""),("PROS1","PW_PLT","membership","enrichment",""),
    ("COL4A1","PW_ECM","membership","enrichment",""),("GP1BA","PW_ECM","membership","enrichment",""),
    ("COL4A1","PW_FA","membership","enrichment",""),("KDR","PW_FA","membership","enrichment",""),
    ("KDR","PW_VEGF","membership","enrichment",""),
    # L3→L4 mechanism inference
    ("PW_FIB","PH_VICC","mechanism","inference","massive fibrin formation→consumptive coagulopathy"),
    ("PW_FIB","PH_MAHA","mechanism","inference","microthrombi→mechanical hemolysis"),
    ("PW_FIB","PH_THR","mechanism","inference","platelet consumption"),
    ("PW_COAG","PH_VICC","mechanism","inference","full activation of the coagulation cascade"),
    ("PW_COAG","PH_MAHA","mechanism","inference","microthrombi+complement"),
    ("PW_COAG","PH_AKI","mechanism","inference","renal microthrombi / complement-mediated renal injury"),
    ("PW_PLT","PH_THR","mechanism","inference","aggregation+consumption"),
    ("PW_PLT","PH_MAHA","mechanism","inference","microvascular platelet thrombi"),
    ("PW_ECM","PH_AKI","mechanism","inference","glomerular basement membrane type IV collagen injury"),
    ("PW_VEGF","PH_LEAK","mechanism","inference","vascular permeability↑→capillary leak"),
    ("PW_VEGF","PH_AKI","mechanism","inference","hypotension→renal hypoperfusion"),
    # L4 internal progression
    ("PH_VICC","PH_THR","progression","inference","one of the clinical manifestations of VICC"),
    ("PH_VICC","PH_MAHA","progression","inference","VICC→TMA progression"),
    ("PH_VICC","PH_AKI","progression","inference","VICC→TMA progression"),
    ("PH_LEAK","PH_AKI","progression","inference","hypoperfusion aggravates renal injury"),
]

# ---------- layered coordinates ----------
# column x: L1=-620, L2=-210, L3=210, L4=620; vertically even spacing within each layer
LAYERS_X = {1: -640, 2: -215, 3: 230, 4: 700}
# manual ordering to reduce edge crossings
ORDER = {
    1: ["RVVV","RVVX","PLA2","KUN","DABK","SNAC","SVVEGF"],
    2: ["F5","F10","F9","F11","PROS1","PLG","PRSS1","FGA","FN1","COL4A1","GP1BA","KDR"],
    3: ["PW_FIB","PW_COAG","PW_PLT","PW_ECM","PW_FA","PW_VEGF"],
    4: ["PH_VICC","PH_THR","PH_MAHA","PH_AKI","PH_LEAK"],
}
GAP = {1: 150, 2: 105, 3: 170, 4: 175}
pos = {}
for layer, ids in ORDER.items():
    n = len(ids)
    y0 = (n - 1) * GAP[layer] / 2
    for i, nid in enumerate(ids):
        pos[nid] = (LAYERS_X[layer], y0 - i * GAP[layer])

# ---------- nodes.csv / edges.csv ----------
with open(OUT/"nodes.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id","label","layer","node_type","family_or_axis","hub_status","evidence_note","fill_color","shape","x","y"])
    for nid,label,layer,nt,fam,hub,note,color,shape in NODES:
        w.writerow([nid,label,layer,nt,fam,hub,note,color,shape,*pos[nid]])

with open(OUT/"edges.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["source","target","interaction","evidence_type","note","line_type","width"])
    lt = {"direct":("solid",3.0),"membership":("solid",1.2),"mechanism":("dashed",2.0),"progression":("dotted",2.0)}
    for s,t,inter,ev,note in EDGES:
        w.writerow([s,t,inter,ev,note,*lt[inter]])

# ---------- .cyjs (with coordinates; layered layout on direct open in Cytoscape) ----------
cy = {
  "format_version": "1.0",
  "generated_by": "snakebite_TMA phase3-4 script",
  "target_cytoscapejs_version": "~2.1",
  "data": {"name": "Figure4_4layer_network"},
  "elements": {
    "nodes": [{"data": {"id": nid, "label": label, "layer": layer, "node_type": nt,
                        "family_or_axis": fam, "hub_status": hub, "evidence_note": note,
                        "fill_color": color, "shape": shape},
               "position": {"x": pos[nid][0], "y": -pos[nid][1]}}   # cyjs y-axis points down
              for nid,label,layer,nt,fam,hub,note,color,shape in NODES],
    "edges": [{"data": {"id": f"e{i}", "source": s, "target": t,
                        "interaction": inter, "evidence_type": ev, "note": note}}
              for i,(s,t,inter,ev,note) in enumerate(EDGES)],
  },
}
with open(OUT/"figure4_hetero_network.cyjs", "w", encoding="utf-8") as f:
    json.dump(cy, f, ensure_ascii=False, indent=1)

print(f"nodes={len(NODES)} edges={len(EDGES)} -> {OUT}")
print("files: nodes.csv / edges.csv / figure4_hetero_network.cyjs")

# ---------- matplotlib preview ----------
sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot
setup_plot()
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

fig, ax = plt.subplots(figsize=(16, 12), dpi=200)
edge_style = {"direct": dict(color="#333", lw=2.2, ls="-"),
              "membership": dict(color="#AAAAAA", lw=1.0, ls="-"),
              "mechanism": dict(color="#777", lw=1.6, ls="--"),
              "progression": dict(color="#9467BD", lw=1.6, ls=":")}
for s,t,inter,ev,note in EDGES:
    x1,y1 = pos[s]; x2,y2 = pos[t]
    ax.plot([x1,x2],[y1,y2], zorder=1, **edge_style[inter])
marker = {"toxin":"h","target":"o","pathway":"s","phenotype":"D"}
size   = {"toxin":1500,"target":900,"pathway":2200,"phenotype":1800}
for nid,label,layer,nt,fam,hub,note,color,shape in NODES:
    x,y = pos[nid]
    ax.scatter(x,y,s=size[nt],c=color,marker=marker[nt],zorder=3,
               edgecolors="black" if "Hub" in hub else "#333",
               linewidths=2.2 if "Hub" in hub else 0.8)
    parts = label.split("\n")
    if layer == 1:      # toxins: label to the right of the node
        ax.annotate(parts[0],(x+70,y),ha="left",va="center",zorder=4,fontsize=9.5,weight="bold",color="#7F1919")
    elif layer == 2:    # genes: label inside the node
        ax.annotate(parts[0],(x,y),ha="center",va="center",zorder=4,fontsize=8.5,color="white",weight="bold")
    elif layer == 3:    # pathways: label to the right, two lines
        ax.annotate(parts[0],(x+120,y+18),ha="left",va="center",zorder=4,fontsize=8.5,weight="bold",color="#1E5A1E")
        if len(parts)>1:
            ax.annotate(parts[1],(x+120,y-20),ha="left",va="center",zorder=4,fontsize=7.5,color="#555")
    else:               # phenotypes: label to the right, two lines
        ax.annotate(parts[0],(x+95,y+18),ha="left",va="center",zorder=4,fontsize=9.5,weight="bold",color="#4B2A6B")
        if len(parts)>1:
            ax.annotate(parts[1],(x+95,y-22),ha="left",va="center",zorder=4,fontsize=8,color="#555")
# layer titles
for layer,name in [(1,"Layer 1  Toxins"),(2,"Layer 2  Host Direct Targets"),
                   (3,"Layer 3  Enriched Pathways"),(4,"Layer 4  TMA Phenotypes")]:
    ax.text(LAYERS_X[layer], 640, name, ha="center", fontsize=13, weight="bold")
handles = [Line2D([0],[0],color="#333",lw=2.2,label="direct interaction (literature)"),
           Line2D([0],[0],color="#AAAAAA",lw=1.0,label="pathway membership"),
           Line2D([0],[0],color="#777",lw=1.6,ls="--",label="mechanism inference"),
           Line2D([0],[0],color="#9467BD",lw=1.6,ls=":",label="phenotype progression")]
ax.legend(handles=handles, loc="lower left", fontsize=10, framealpha=0.9)
ax.set_xlim(-800, 1250); ax.set_ylim(-700, 720); ax.axis("off")
fig.tight_layout()
fig.savefig(OUT/"figure4_preview.png", bbox_inches="tight")
print("preview:", OUT/"figure4_preview.png")
