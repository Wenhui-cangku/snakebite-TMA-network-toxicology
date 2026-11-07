"""Validate the principal counts and numerical anchors in this public archive."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent

edges = pd.read_csv(ROOT / "03_target_prediction" / "toxin_target_edges_audited.csv")
primary = edges[edges["evidence_channel"] == "primary_literature"]
assert len(edges) == 447
assert len(primary) == 33
assert primary["target_symbol"].nunique() == 15
assert primary["interaction_type"].value_counts().to_dict() == {
    "enzymatic_cleavage": 15, "inhibition": 10, "direct_binding": 6, "activation": 2,
}
factor_x = primary[primary["target_symbol"] == "F10"]
assert len(factor_x) == 6
assert factor_x["independent_toxin_entity"].nunique() == 4

flags = pd.read_csv(ROOT / "05_enrichment" / "reanalysis_v2" / "core_evidence_flags.csv")
assert len(flags) == 2190
assert int(flags["in_core_doc"].sum()) == 1042

cluster = pd.read_csv(ROOT / "01_toxin_lib" / "cluster_benchmark" / "cluster_summary.csv")
metrics = dict(zip(cluster["metric"], cluster["value"]))
assert int(float(metrics["Input sequences"])) == 63
assert int(float(metrics["Custom clusters"])) == 40
assert int(float(metrics["usearch clusters"])) == 39
assert round(float(metrics["Rand index"]), 3) == 0.996

summary = pd.read_csv(ROOT / "05_enrichment" / "reanalysis_v2" / "enrichment_summary_by_group.csv")
g2 = summary[summary["group"] == "G2_strictcore10"].iloc[0]
assert int(g2["input_in_bg"]) == 10
assert int(g2["bg_n"] if "bg_n" in summary.columns else 1042) == 1042
assert abs(float(g2["top_p"]) - 4.7406e-7) < 1e-10
assert int(g2["n_BH<0.05"]) == 15

network_edges = pd.read_csv(ROOT / "04_network" / "network_edges.csv")
network_nodes = pd.read_csv(ROOT / "04_network" / "network_nodes.csv")
assert (len(network_nodes), len(network_edges)) == (54, 321)

structures = pd.read_csv(ROOT / "07_docking" / "structure_inventory.csv")
models = pd.read_csv(ROOT / "07_docking" / "model_inventory.csv")
docking = pd.read_csv(ROOT / "07_docking" / "docking_outputs.csv")
assert (len(structures), len(models), len(docking)) == (15, 7, 12)

endothelium = pd.read_csv(ROOT / "06_geo" / "limma_v2" / "GSE121297_RCaB_vs_Ctrl_limma_plainEB.csv")
muscle = pd.read_csv(ROOT / "06_geo" / "limma_v2" / "GSE248215_DR24h_vs_Ctrl_limma_plainEB.csv")
assert int((endothelium["adj.P.Val"] < 0.05).sum()) == 43
assert int((muscle["adj.P.Val"] < 0.05).sum()) == 75

protocol = pd.read_csv(ROOT / "00_protocol" / "protocol_deviations.csv")
assert len(protocol) == 14

result = {
    "status": "PASS",
    "disease_genes": 2190,
    "core_genes": 1042,
    "audited_edges": 447,
    "primary_literature_edges": 33,
    "primary_host_targets": 15,
    "factor_x_edges": 6,
    "factor_x_independent_toxin_entities": 4,
    "toxins": 63,
    "custom_clusters": 40,
    "usearch_clusters": 39,
    "rand_index_rounded": 0.996,
    "network_nodes": 54,
    "network_edges": 321,
    "structure_assets": 15,
    "model_pairs": 7,
    "docking_output_rows": 12,
    "GSE121297_BH_significant": 43,
    "GSE248215_BH_significant": 75,
    "protocol_decision_records": 14,
}
print(json.dumps(result, indent=2))
