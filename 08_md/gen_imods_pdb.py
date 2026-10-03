# -*- coding: utf-8 -*-
"""生成 iMODS 专用副本：每条链残基顺序重编号 1..N，去插入码/0 号残基。
输出 prodigy/PX_*_imods.pdb + mapping_PX.csv（原编号→新编号，供回映射）。"""
import os, csv

HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prodigy")
FILES = ["P1_RVVX_FXa", "P2_RVVV_FV", "P3_dabK_FIB", "P4_snaclec_GP1BA",
         "P5_PLA2_FXa", "P6_Kunitz_PLG", "P7_svVEGF_VEGFR2"]

for base in FILES:
    src = os.path.join(HERE, base + ".pdb")
    dst = os.path.join(HERE, base + "_imods.pdb")
    maps = []                       # (chain, orig, new)
    cur_chain, seen, counter = None, {}, 0
    with open(dst, "w") as out:
        for line in open(src, errors="ignore"):
            rec = line[:6].strip()
            if rec in ("ATOM", "HETATM"):
                ch = line[21]
                orig = line[22:27].strip()          # 残基号+插入码
                if ch != cur_chain:
                    cur_chain, seen, counter = ch, {}, 0
                if orig not in seen:
                    counter += 1
                    seen[orig] = counter
                    maps.append((ch, orig, counter))
                new = f"{seen[orig]:>4d} "
                out.write(line[:22] + new + line[27:])
            elif rec in ("TER", "END"):
                out.write(line)
    with open(os.path.join(HERE, f"mapping_{base}.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["chain", "orig_resnum_icode", "new_resnum"])
        w.writerows(maps)
    nch = len({m[0] for m in maps})
    print(f"{base}_imods.pdb  链数={nch}  残基={len(maps)}")

# 自检：重编号后不应再有断档/0号/插入码
import glob
for f in sorted(glob.glob(os.path.join(HERE, "*_imods.pdb"))):
    bad = 0
    for line in open(f):
        if line.startswith(("ATOM", "HETATM")):
            if line[26].strip() or int(line[22:26]) <= 0:
                bad += 1
    print(os.path.basename(f), "残留问题原子:", bad)
