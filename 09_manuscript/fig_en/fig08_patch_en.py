# -*- coding: utf-8 -*-
"""Fig 8 small-molecule triptych: replace Chinese header line-2 with English (PIL patch)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
import matplotlib  # for bundled DejaVuSans.ttf
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parents[1]
SRC = BASE / "assets" / "fig5_smallmol_3panel.png"
DST = BASE / "assets_en" / "fig5_smallmol_3panel.png"
DST.parent.mkdir(exist_ok=True)

font_path = Path(matplotlib.__file__).parent / "mpl-data" / "fonts" / "ttf" / "DejaVuSans.ttf"
font = ImageFont.truetype(str(font_path), 46)

img = Image.open(SRC).convert("RGB")
dr = ImageDraw.Draw(img)

patches = [
    (283,  "−7.64 kcal/mol, hydroxamate–Zn chelation", 1380, 260),
    (1712, "−7.53 kcal/mol, hydroxamate–Zn chelation", 2820, 1695),
    (3112, "−7.84 kcal/mol, polar contacts His48/Asp49", 4235, 3095),
]
for x0, text, x1, xc in patches:
    dr.rectangle([xc, 84, x1, 172], fill=(255, 255, 255))
    dr.text((x0, 88), text, font=font, fill=(51, 51, 51))

img.save(DST)
print("saved", DST)
