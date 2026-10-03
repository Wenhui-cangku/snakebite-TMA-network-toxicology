# -*- coding: utf-8 -*-
"""MD 起始结构预处理：从对接结果提取最优构象，清理为 GROMACS 可吃的纯 ATOM PDB，
输出链/残基/原子统计与缺残基警示。输出到 08_md/input/"""
import os, re, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
DOCK = os.path.join(BASE, "..", "07_docking")
SMOL = os.path.join(BASE, "..", "08_smallmol")
INP = os.path.join(BASE, "input")
os.makedirs(INP, exist_ok=True)

SOURCES = [
    # (源文件, 输出名, 说明, 是否按TER分块重标链)
    (os.path.join(DOCK, "figure", "p2_cluster1_1.pdb"), "md_P2_RVVV_FV_haddock.pdb",
     "P2 RVV-Vγ×FV HADDOCK cluster1_1（双达标构象，PyMOL 场景版已纯 ATOM）", False),
    (os.path.join(DOCK, "results", "hdock", "P7", "model_1.pdb"), "md_P7_svVEGF_VEGFR2_hdock.pdb",
     "P7 svVEGF×VEGFR2 HDock model_1（confidence 0.897）", False),
    (os.path.join(DOCK, "figure", "p4_cluspro.pdb"), "md_P4_snaclec_GP1BA_cluspro.pdb",
     "P4 snaclec×GP1BA ClusPro model.000.00（纯 ATOM 场景版）", True),
]
# 小分子（可选/进阶：需 CGenFF 配体拓扑）
SMOL_SRC = os.path.join(SMOL, "results", "RVVX_batimastat.pdbqt")

def clean_pdb(src, dst, relabel_blocks=False):
    """只保留 ATOM/HETATM/TER/END；统计链、残基、原子数、残基号断档。
    relabel_blocks=True 时按 TER 分块把链列重标为 A/B/C…（用于 ClusPro 全 A 链文件）"""
    chains = {}
    het = 0
    block = 0
    letters = "ABCDEFGH"
    prev_chain = None
    wrote_ter = False
    with open(dst, "w", encoding="ascii", errors="ignore") as out:
        for line in open(src, encoding="utf-8", errors="ignore"):
            rec = line[:6].strip()
            if rec in ("ATOM", "HETATM"):
                if relabel_blocks:
                    line = line[:21] + letters[block] + line[22:]
                cur = line[21]
                if prev_chain is not None and cur != prev_chain and not wrote_ter:
                    out.write("TER\n")  # 链切换处补 TER，保证 pdb2gmx 正确拆链
                prev_chain = cur
                wrote_ter = False
                if rec == "HETATM":
                    het += 1
                out.write(line if line.endswith("\n") else line + "\n")
                ch = line[21].strip() or "?"
                res = line[22:26].strip()
                chains.setdefault(ch, []).append(int(res) if res.isdigit() else -1)
            elif rec == "TER":
                block += 1
                wrote_ter = True
                out.write(line.rstrip("\n") + "\n")
            elif rec == "END":
                out.write(line.rstrip("\n") + "\n")
    return chains, het

print("=" * 70)
for src, name, note, relabel in SOURCES:
    dst = os.path.join(INP, name)
    chains, het = clean_pdb(src, dst, relabel_blocks=relabel)
    natoms = sum(len(v) for v in chains.values())
    print(f"\n### {name}")
    print(f"  {note}")
    print(f"  原子 {natoms}（HETATM {het}）")
    for ch, reslist in sorted(chains.items()):
        uniq = sorted(set(r for r in reslist if r >= 0))
        gaps = [(a, b) for a, b in zip(uniq, uniq[1:]) if b - a > 1]
        print(f"  链 {ch}: {len(uniq)} 残基 ({uniq[0]}–{uniq[-1]})", end="")
        if gaps:
            print(f"  ⚠ 断档 {len(gaps)} 处: {gaps[:5]}", end="")
        print()

if os.path.exists(SMOL_SRC):
    # pdbqt → pdb（仅坐标，去 charge/类型列）
    dst = os.path.join(INP, "md_batimastat_RVVX_pose.pdb")
    n = 0
    with open(dst, "w") as out:
        for line in open(SMOL_SRC, errors="ignore"):
            if line.startswith(("ATOM", "HETATM")):
                out.write(line[:66].rstrip() + "\n")
                n += 1
    print(f"\n### md_batimastat_RVVX_pose.pdb  Vina 姿态 {n} 原子（pdbqt→pdb，仅坐标）")
    print("  ⚠ 小分子 MD 需另配 CGenFF/ParmEd 拓扑，见 SOP §6")

print("\n输出目录:", INP)
print(os.listdir(INP))
