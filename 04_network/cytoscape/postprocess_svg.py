# -*- coding: utf-8 -*-
"""Post-process the Cytoscape-exported SVG: add dashes+arrows to mechanism-inference edges (#777777) and dotted+arrows to phenotype-progression edges (#9467bd).
Input Figure4_4layer_network.svg (original untouched), output Figure4_4layer_network_final.svg."""
import math, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "Figure4_4layer_network.svg")
DST = os.path.join(HERE, "Figure4_4layer_network_final.svg")

raw = open(SRC, encoding="utf-8").read()

ARROW_LEN, ARROW_HALF_W = 30.0, 11.0  # in original coordinate units (≈9 px after ~×0.3 scaling)

def arrow_polygon(x1, y1, x2, y2, color):
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    if L == 0: return ""
    ux, uy = dx / L, dy / L
    bx, by = x2 - ux * ARROW_LEN, y2 - uy * ARROW_LEN
    px, py = -uy, ux
    p1 = f"{x2:.2f},{y2:.2f}"
    p2 = f"{bx + px*ARROW_HALF_W:.2f},{by + py*ARROW_HALF_W:.2f}"
    p3 = f"{bx - px*ARROW_HALF_W:.2f},{by - py*ARROW_HALF_W:.2f}"
    return f'<polygon points="{p1} {p2} {p3}" fill="{color}" stroke="none"/>'

def patch(match, color, dash):
    g_open, x1, y1, x2, y2 = match.group(1), *map(float, match.groups()[1:])
    if "stroke-dasharray" not in g_open:
        g_open = g_open[:-1].rstrip() + f' stroke-dasharray="{dash}">'
    arrow = arrow_polygon(x1, y1, x2, y2, color)
    body = f'M {x1} L {y1}'.split()  # unused
    return (g_open + '\n  '
            + f'<path d="M {match.group(2)} {match.group(3)} L {match.group(4)} {match.group(5)}"/>\n'
            + ('  ' + arrow + '\n' if arrow else '')
            + '</g>')

stats = {}
for color, dash in (("#777777", "7 5"), ("#9467bd", "2 3")):
    pat = re.compile(
        r'(<g stroke-opacity="1" stroke-width="[\d.]+" fill="none" stroke="'
        + re.escape(color)
        + r'" stroke-linecap="round">)\s*<path d="M ([-\d.]+) ([-\d.]+) L ([-\d.]+) ([-\d.]+)"/>\s*</g>')
    raw, n = pat.subn(lambda m: patch(m, color, dash), raw)
    stats[color] = n

open(DST, "w", encoding="utf-8").write(raw)

# self-check
import xml.etree.ElementTree as ET
ET.parse(DST)
final = open(DST, encoding="utf-8").read()
print("patched groups:", stats, "(expected #777777=11, #9467bd=4)")
print("polygon arrows:", final.count("<polygon"), "(expected 15)")
print("dasharray 7 5:", final.count('stroke-dasharray="7 5"'), "/ 2 3:", final.count('stroke-dasharray="2 3"'))
print("XML valid ✓ ->", DST)
