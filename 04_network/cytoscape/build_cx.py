# -*- coding: utf-8 -*-
"""把 figure4_hetero_network.cyjs 转成 Cytoscape 原生 CX 格式（含坐标）。
CX 是 NDEx 交换格式，Cytoscape 3.x 的 File -> Import -> Network from File 原生支持，
导入后自动恢复 cartesianLayout 坐标，避开 cyjs 识别问题。"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
src = json.load(open(os.path.join(HERE, "figure4_hetero_network.cyjs"), encoding="utf-8"))

nodes_in = src["elements"]["nodes"]
edges_in = src["elements"]["edges"]

id_map = {n["data"]["id"]: i for i, n in enumerate(nodes_in)}

NODE_ATTRS = [("layer", "integer"), ("node_type", "string"), ("family_or_axis", "string"),
              ("hub_status", "string"), ("evidence_note", "string"),
              ("fill_color", "string"), ("shape", "string")]
EDGE_ATTRS = [("evidence_type", "string"), ("line_type", "string"),
              ("width", "double"), ("note", "string")]

nodes, edges, n_attrs, e_attrs, layout = [], [], [], [], []
for n in nodes_in:
    d = n["data"]; nid = id_map[d["id"]]
    label = d.get("label", d["id"]).replace("\n", " ")
    nodes.append({"@id": nid, "n": label})
    for key, dtype in NODE_ATTRS:
        if key in d and d[key] != "":
            n_attrs.append({"po": nid, "n": key, "v": str(d[key]), "d": dtype})
    pos = n.get("position", {"x": 0, "y": 0})
    layout.append({"node": nid, "x": float(pos["x"]), "y": float(pos["y"])})

for j, e in enumerate(edges_in):
    d = e["data"]
    edges.append({"@id": j, "s": id_map[d["source"]], "t": id_map[d["target"]],
                  "i": d.get("interaction", "")})
    for key, dtype in EDGE_ATTRS:
        if key in d and d[key] != "":
            e_attrs.append({"po": j, "n": key, "v": str(d[key]), "d": dtype})

aspects = [
    ("nodes", len(nodes), len(nodes)), ("edges", len(edges), len(edges)),
    ("nodeAttributes", len(n_attrs), None), ("edgeAttributes", len(e_attrs), None),
    ("cartesianLayout", len(layout), None), ("networkAttributes", 1, None),
]
meta = [{"name": a, "version": "1.0", "consistencyGroup": 1, "elementCount": c,
         **({"idCounter": ic} if ic is not None else {})} for a, c, ic in aspects]

cx = [
    {"numberVerification": [{"longNumber": 281474976710655}]},
    {"metaData": meta},
    {"networkAttributes": [{"n": "name", "v": "Figure4_4layer_network", "d": "string"}]},
    {"nodes": nodes},
    {"edges": edges},
    {"nodeAttributes": n_attrs},
    {"edgeAttributes": e_attrs},
    {"cartesianLayout": layout},
    {"status": [{"error": "", "success": True}]},
    {"numberVerification": [{"longNumber": 281474976710655}]},
]

out = os.path.join(HERE, "figure4_hetero_network.cx")
json.dump(cx, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# 自检
chk = json.load(open(out, encoding="utf-8"))
by = {list(f)[0]: f[list(f)[0]] for f in chk}
print("CX written:", out)
print("nodes:", len(by["nodes"]), "edges:", len(by["edges"]),
      "nAttrs:", len(by["nodeAttributes"]), "layout:", len(by["cartesianLayout"]))
