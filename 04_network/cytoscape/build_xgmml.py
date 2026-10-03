# -*- coding: utf-8 -*-
"""把 figure4_hetero_network.cyjs 转成 XGMML（Cytoscape 各版本均可直接导入）。
内嵌节点坐标/颜色/形状与边颜色/宽度；y 轴翻转以匹配 matplotlib 预览的视觉方向。"""
import json, os
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
src = json.load(open(os.path.join(HERE, "figure4_hetero_network.cyjs"), encoding="utf-8"))

# 每层节点尺寸（与指南 §3 一致）
SIZE = {1: (60, 60), 2: (45, 45), 3: (70, 40), 4: (65, 65)}
EDGE_COLOR = {"direct": "#333333", "membership": "#AAAAAA",
              "mechanism": "#777777", "progression": "#9467BD"}

L = []
L.append('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')
L.append('<graph label="Figure4_4layer_network" xmlns="http://www.cs.rpi.edu/XGMML" directed="1">')

for n in src["elements"]["nodes"]:
    d = n["data"]; nid = d["id"]
    label = d.get("label", nid).replace("\n", " ")
    layer = int(d.get("layer", 2))
    w, h = SIZE.get(layer, (50, 50))
    x = float(n["position"]["x"]); y = -float(n["position"]["y"])  # y 翻转
    shape = d.get("shape", "ELLIPSE")
    fill = d.get("fill_color", "#999999")
    bw = 4.0 if d.get("hub_status") else 1.5
    L.append(f'  <node id="{escape(nid)}" label="{escape(label)}">')
    L.append(f'    <att name="layer" type="integer" value="{layer}"/>')
    L.append(f'    <att name="node_type" type="string" value="{escape(str(d.get("node_type","")))}"/>')
    L.append(f'    <att name="family_or_axis" type="string" value="{escape(str(d.get("family_or_axis","")))}"/>')
    L.append(f'    <att name="hub_status" type="string" value="{escape(str(d.get("hub_status","")))}"/>')
    L.append(f'    <att name="evidence_note" type="string" value="{escape(str(d.get("evidence_note","")))}"/>')
    L.append(f'    <graphics type="{shape}" fill="{fill}" x="{x}" y="{y}" w="{w}" h="{h}" outline="#000000" width="{bw}"/>')
    L.append('  </node>')

for e in src["elements"]["edges"]:
    d = e["data"]
    inter = d.get("interaction", "")
    color = EDGE_COLOR.get(inter, "#666666")
    width = float(d.get("width", 1.5))
    L.append(f'  <edge id="{escape(d["id"])}" label="{inter}" source="{escape(d["source"])}" target="{escape(d["target"])}">')
    L.append(f'    <att name="interaction" type="string" value="{escape(inter)}"/>')
    L.append(f'    <att name="evidence_type" type="string" value="{escape(str(d.get("evidence_type","")))}"/>')
    L.append(f'    <att name="line_type" type="string" value="{escape(str(d.get("line_type","")))}"/>')
    L.append(f'    <att name="note" type="string" value="{escape(str(d.get("note","")))}"/>')
    L.append(f'    <graphics width="{width}" fill="{color}"/>')
    L.append('  </edge>')

L.append('</graph>')
out = os.path.join(HERE, "figure4_hetero_network.xgmml")
open(out, "w", encoding="utf-8").write("\n".join(L))

# 自检
import xml.etree.ElementTree as ET
t = ET.parse(out)
ns = "{http://www.cs.rpi.edu/XGMML}"
g = t.getroot()
print("XGMML written:", out)
print("nodes:", len(g.findall(f"{ns}node")), "edges:", len(g.findall(f"{ns}edge")))
