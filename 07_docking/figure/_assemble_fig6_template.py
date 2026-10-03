# -*- coding: utf-8 -*-
"""Figure 6 template-style rebuild: per-complex row = overview (dashed pocket box)
-> dashed zoom lines -> close-up render. A=P7, B=P2(+callouts), C=P6(+callouts)."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

FIG = Path(r"E:\陈文辉资料夹\论文\蛇伤\snakebite_TMA\07_docking\figure")
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

OV = 900          # overview tile size (from 1200^2)
CU_W, CU_H = 1200, 900   # close-up tile (from 1600x1200)
GAP = 170         # zoom-connector zone width
TITLE = 96        # title strip height
MX, MY = 40, 36   # outer margins
ROW_H = TITLE + CU_H
W = MX * 2 + OV + GAP + CU_W           # 2250
H = MY * 2 + ROW_H * 3                 # 3030

S_OV = OV / 1200.0        # overview scale
S_CU = CU_W / 1600.0      # close-up scale

rows = [
    dict(ov="ov_P7.png", cu="panelA_P7.png", letter="A",
         title="P7  svVEGF × VEGFR2-D2", sub="HDOCK pose vs VEGF-A template 3V2A",
         box_rel=(0.50, 0.25, 0.92, 0.60), labels=[]),
    dict(ov="ov_P2.png", cu="panelB_P2.png", letter="B",
         title="P2  RVV-Vγ × coagulation factor V", sub="HADDOCK cluster 1, score −144.9",
         box_rel=(0.45, 0.09, 0.81, 0.47),
         labels=[("ARG1545", (808, 648)), ("HIS42", (768, 696)), ("SER195", (872, 688))]),
    dict(ov="ov_P6.png", cu="panelC_P6_nolabel.png", letter="C",
         title="P6  Kunitz × plasmin", sub="HADDOCK cluster 1 (exploratory pose)",
         box_rel=(0.40, 0.33, 0.74, 0.67),
         labels=[("HIS603", (793, 519)), ("ASP646", (663, 514)), ("SER741", (890, 575))]),
]

canvas = Image.new("RGB", (W, H), "white")
dr = ImageDraw.Draw(canvas)
f_letter, f_title, f_sub, f_lab = font(64, True), font(52, True), font(40), font(38, True)

for i, r in enumerate(rows):
    y0 = MY + i * ROW_H
    x_ov, x_cu = MX, MX + OV + GAP
    y_img = y0 + TITLE
    # title strip: letter + name (left), sub (right)
    dr.text((MX + 4, y0 + 14), r["letter"], font=f_letter, fill="black")
    lx = MX + 90
    dr.text((lx, y0 + 22), r["title"], font=f_title, fill="black")
    bb = dr.textbbox((0, 0), r["sub"], font=f_sub)
    dr.text((W - MX - (bb[2] - bb[0]) - 10, y0 + 32), r["sub"], font=f_sub, fill=(60, 60, 60))
    # images
    ov = Image.open(FIG / r["ov"]).convert("RGB").resize((OV, OV), Image.LANCZOS)
    cu = Image.open(FIG / r["cu"]).convert("RGB").resize((CU_W, CU_H), Image.LANCZOS)
    canvas.paste(ov, (x_ov, y_img))
    canvas.paste(cu, (x_cu, y_img + (CU_H - CU_H) // 2))
    # dashed box on overview + zoom connectors
    bx = [x_ov + v * OV for v in (r["box_rel"][0], r["box_rel"][1], r["box_rel"][2], r["box_rel"][3])]
    # box_rel is relative to overview tile: (x1,y1,x2,y2)
    x1, y1 = x_ov + r["box_rel"][0] * OV, y_img + r["box_rel"][1] * OV
    x2, y2 = x_ov + r["box_rel"][2] * OV, y_img + r["box_rel"][3] * OV
    dashed_rect(dr, (x1, y1, x2, y2))
    dashed_line(dr, (x2, y1), (x_cu, y_img), width=3)
    dashed_line(dr, (x2, y2), (x_cu, y_img + CU_H), width=3)
    # close-up residue callouts (anchor coords in original 1600x1200 -> scaled)
    for j, (txt, (ax, ay)) in enumerate(r["labels"]):
        tx, ty = x_cu + 24, y_img + 210 + j * 92
        px, py = x_cu + ax * S_CU, y_img + ay * S_CU
        dr.text((tx, ty), txt, font=f_lab, fill="black", stroke_width=6, stroke_fill="white")
        bb = dr.textbbox((tx, ty), txt, font=f_lab, stroke_width=6)
        dr.line([bb[2] + 8, (bb[1] + bb[3]) / 2, px, py], fill="black", width=4)
        dr.ellipse([px - 8, py - 8, px + 8, py + 8], fill="black", outline="white", width=3)

out = ASSETS / "fig6_protein_template.png"
canvas.save(out, dpi=(300, 300))
print("saved:", out, canvas.size)
