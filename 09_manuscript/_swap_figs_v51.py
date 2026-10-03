# -*- coding: utf-8 -*-
"""v51: swap 4 figure media slots (Fig1/Fig2/Fig6/Fig12) in the CBI docx.
Slot identity verified by current pixel size before writing."""
import shutil, zipfile, io
from pathlib import Path
from PIL import Image

MS = Path(r"E:\陈文辉资料夹\论文\蛇伤\snakebite_TMA\09_manuscript")
DOCX = MS / "蛇伤TMA论文_CBI投稿版_EN_v41_revised.docx"
ASSETS = MS / "assets_en"

SWAPS = [
    # (media prefix, expected current size, new png)
    ("word/media/96a862870a9f073c0728", (2310, 2502), "figure1_workflow.png"),          # Fig 1
    ("word/media/64f472abfdec2fa08ea6", (1289, 902),  "figure2a_venn.png"),             # Fig 2
    ("word/media/ec4aa1910b67d638b28f", (3320, 2700), "fig5_protein_3panel_v51.png"),   # Fig 6
    ("word/media/a6a694527717fe201155", (3065, 1851), "figure7_aop_mechanism.png"),     # Fig 12
]

zin = zipfile.ZipFile(DOCX)
names = zin.namelist()
plan = {}
for prefix, exp, newpng in SWAPS:
    hit = [n for n in names if n.startswith(prefix)]
    assert len(hit) == 1, f"slot not unique: {prefix} -> {hit}"
    name = hit[0]
    cur = Image.open(io.BytesIO(zin.read(name))).size
    assert cur == exp, f"slot check failed {name}: {cur} != {exp}"
    data = (ASSETS / newpng).read_bytes()
    plan[name] = data
    print(f"verified {name} {cur} <- {newpng} {Image.open(io.BytesIO(data)).size}")
zin.close()

tmp = DOCX.with_suffix(".tmp.docx")
with zipfile.ZipFile(DOCX) as zi, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zo:
    for item in zi.namelist():
        zo.writestr(zi.getinfo(item), plan.get(item, zi.read(item)))
tmp.replace(DOCX)
print("4 figure slots swapped")

z = zipfile.ZipFile(DOCX)
for name in plan:
    ok = z.read(name) == plan[name]
    print("verify:", name.split('/')[-1][:24], ok)
