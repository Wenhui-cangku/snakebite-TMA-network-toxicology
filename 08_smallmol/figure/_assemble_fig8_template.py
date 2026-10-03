# -*- coding: utf-8 -*-
"""Figure 8 template-style rebuild: per-ligand row = overview (dashed pocket box)
-> dashed zoom lines -> close-up render with callouts. a=batimastat, b=marimastat, c=varespladib."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

FIG = Path(r"E:\陈文辉资料夹\论文\蛇伤\snakebite_TMA\08_smallmol\figure")
ASSETS = Path(r"E:\陈文辉资料夹\论文\蛇伤\snakebite_TMA\09_manuscript\assets_en")

def font(sz, bold=False):
    f = "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"
    try:
        return ImageFont.truetype(f, sz)
    except Exception:
        return ImageFont.truetype("C:/Windows/Fonts/arial.ttf", sz)

def dashed_line(dr, p1, p2, fill=(60, 60, 60), width=3, dash=14, gap=10):
    import math
    x1, y1 = p1; x2, y2 = p2
    L = math.hypot(x2 - x1, y2 - y1)
    if L == 0:
        return
    dx, dy = (x2 - x1) / L, (y2 - y1) / L
    t = 0.0
    while t < L:
        t2 = min(t + dash, L)
        dr.line([x1 + dx * t, y1 + dy * t, x1 + dx * t2, y1 + dy * t2], fill=fill, width=width)
        t += dash + gap

def dashed_rect(dr, box, fill=(60, 60, 60), width=3):
    x1, y1, x2, y2 = box
    dashed_line(dr, (x1, y1), (x2, y1), fill, width)
    dashed_line(dr, (x2, y1), (x2, y2), fill, width)
    dashed_line(dr, (x2, y2), (x1, y2), fill, width)
    dashed_line(dr, (x1, y2), (x1, y1), fill, width)

OV = 900
CU_W, CU_H = 1200, 900
GAP = 170
TITLE = 96
MX, MY = 40, 36
ROW_H = TITLE + CU_H
W = MX * 2 + OV + GAP + CU_W
H = MY * 2 + ROW_H * 3
S_CU = CU_W / 1600.0

rows = [
    dict(ov="ov_RVVX_bat.png", cu="fig5_smallmol_RVVX_batimastat_nolabel.png", letter="a",
         title="batimastat × RVV-X (SVMP)", sub="Binding energy: −7.64 kcal/mol",
         box_rel=(0.35, 0.47, 0.65, 0.83),
         labels=[("HIS155", (1027, 721)), ("HIS145", (1128, 747)), ("Zn2+", (973, 818)), ("HIS149", (1106, 1068))]),
    dict(ov="ov_RVVX_mar.png", cu="fig5_smallmol_RVVX_marimastat_nolabel.png", letter="b",
         title="marimastat × RVV-X (SVMP)", sub="Binding energy: −7.53 kcal/mol",
         box_rel=(0.38, 0.15, 0.67, 0.50),
         labels=[("HIS155", (1060, 749)), ("HIS145", (1124, 823)), ("Zn2+", (978, 861)), ("HIS149", (1105, 1146))]),
    dict(ov="ov_PLA2_var.png", cu="fig5_smallmol_PLA2_varespladib_nolabel.png", letter="c",
         title="varespladib × PLA2 (1KPM)", sub="Binding energy: −7.84 kcal/mol",
         box_rel=(0.35, 0.35, 0.68, 0.73),
         labels=[("ASP49", (1158, 633)), ("HIS48", (910, 740))]),
]

canvas = Image.new("RGB", (W, H), "white")
dr = ImageDraw.Draw(canvas)
f_letter, f_title, f_sub, f_lab = font(64, True), font(52, True), font(44), font(38, True)

for i, r in enumerate(rows):
    y0 = MY + i * ROW_H
    x_ov, x_cu = MX, MX + OV + GAP
    y_img = y0 + TITLE
    dr.text((MX + 4, y0 + 14), r["letter"], font=f_letter, fill="black")
    lx = MX + 90
    dr.text((lx, y0 + 22), r["title"], font=f_title, fill="black")
    bb = dr.textbbox((0, 0), r["sub"], font=f_sub)
    dr.text((W - MX - (bb[2] - bb[0]) - 10, y0 + 30), r["sub"], font=f_sub, fill=(60, 60, 60))
    ov = Image.open(FIG / r["ov"]).convert("RGB").resize((OV, OV), Image.LANCZOS)
    cu = Image.open(FIG / r["cu"]).convert("RGB").resize((CU_W, CU_H), Image.LANCZOS)
    canvas.paste(ov, (x_ov, y_img))
    canvas.paste(cu, (x_cu, y_img))
    x1, y1 = x_ov + r["box_rel"][0] * OV, y_img + r["box_rel"][1] * OV
    x2, y2 = x_ov + r["box_rel"][2] * OV, y_img + r["box_rel"][3] * OV
    dashed_rect(dr, (x1, y1, x2, y2))
    dashed_line(dr, (x2, y1), (x_cu, y_img), width=3)
    dashed_line(dr, (x2, y2), (x_cu, y_img + CU_H), width=3)
    for j, (txt, (ax, ay)) in enumerate(r["labels"]):
        tx, ty = x_cu + 24, y_img + 210 + j * 92
        px, py = x_cu + ax * S_CU, y_img + ay * S_CU
        dr.text((tx, ty), txt, font=f_lab, fill="black", stroke_width=6, stroke_fill="white")
        bb = dr.textbbox((tx, ty), txt, font=f_lab, stroke_width=6)
        dr.line([bb[2] + 8, (bb[1] + bb[3]) / 2, px, py], fill="black", width=4)
        dr.ellipse([px - 8, py - 8, px + 8, py + 8], fill="black", outline="white", width=3)

out = ASSETS / "fig8_smallmol_template.png"
canvas.save(out, dpi=(300, 300))
print("saved:", out, canvas.size)
