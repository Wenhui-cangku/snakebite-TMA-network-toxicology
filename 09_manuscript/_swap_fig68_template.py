# -*- coding: utf-8 -*-
"""Swap Fig.6 + Fig.8 media with template-style versions; fix wp:extent/a:ext cy
for new aspect ratio (2350x3060 portrait); sync to both upload packages."""
import shutil, zipfile, re, io
from pathlib import Path
from PIL import Image

MS = Path(r"E:\陈文辉资料夹\论文\蛇伤\snakebite_TMA\09_manuscript")
DOCX = MS / "蛇伤TMA论文_CBI投稿版_EN_v41_revised.docx"
SWAPS = [
    ("word/media/ec4aa1910b67d638b28f347c2fc3b7fcf531091e.png",
     MS / "assets_en" / "fig6_protein_template.png"),
    ("word/media/add15508dce48e6168be0547a697691417b79c19.png",
     MS / "assets_en" / "fig8_smallmol_template.png"),
]

bak = MS / "蛇伤TMA论文_CBI投稿版_EN_v41_revised.docx.bak_v53_figstyle"
if not bak.exists():
    shutil.copy2(DOCX, bak)
    print("backup ->", bak.name)

with zipfile.ZipFile(DOCX) as z:
    doc = z.read("word/document.xml").decode("utf-8")
    rels = z.read("word/_rels/document.xml.rels").decode("utf-8")

new_w, new_h = Image.open(SWAPS[0][1]).size
print("new image size:", new_w, new_h)

for media, newpng in SWAPS:
    m = re.search(r'Id="(rId\d+)"[^>]*Target="media/' + re.escape(media.split("/")[-1]) + r'"', rels)
    assert m, f"rel not found for {media}"
    rid = m.group(1)
    # locate the drawing containing this embed
    idx = doc.find(f'r:embed="{rid}"')
    assert idx > 0, f"embed {rid} not in document.xml"
    # nearest wp:extent BEFORE idx
    ext_m = None
    for mm in re.finditer(r'<wp:extent cx="(\d+)" cy="(\d+)"/>', doc):
        if mm.start() < idx:
            ext_m = mm
        else:
            break
    assert ext_m, "wp:extent not found"
    cx = int(ext_m.group(1)); cy = int(ext_m.group(2))
    new_cy = round(cx * new_h / new_w)
    doc = doc[:ext_m.start()] + f'<wp:extent cx="{cx}" cy="{new_cy}"/>' + doc[ext_m.end():]
    # nearest a:ext AFTER (new) idx
    idx2 = doc.find(f'r:embed="{rid}"')
    aext_m = re.search(r'<a:ext cx="(\d+)" cy="(\d+)"/>', doc[idx2:])
    assert aext_m, "a:ext not found"
    s = idx2 + aext_m.start(); e = idx2 + aext_m.end()
    doc = doc[:s] + f'<a:ext cx="{cx}" cy="{new_cy}"/>' + doc[e:]
    print(f"{media.split('/')[-1][:12]}… {rid}: extent {cx}x{cy} -> {cx}x{new_cy}")

new_bytes = {media: Path(newpng).read_bytes() for media, newpng in SWAPS}
tmp = DOCX.with_suffix(".tmp.docx")
with zipfile.ZipFile(DOCX) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
    for item in zin.namelist():
        if item == "word/document.xml":
            zout.writestr(zin.getinfo(item), doc.encode("utf-8"))
        elif item in new_bytes:
            zout.writestr(zin.getinfo(item), new_bytes[item])
        else:
            zout.writestr(zin.getinfo(item), zin.read(item))
tmp.replace(DOCX)
print("docx updated:", DOCX.name)

# sync upload packages
for pkg in [MS / "submission" / "CBI_upload_package", MS / "submission" / "CBI_投稿上传文件"]:
    dst = pkg / DOCX.name
    if dst.exists():
        shutil.copy2(DOCX, dst)
        print("synced ->", dst)
