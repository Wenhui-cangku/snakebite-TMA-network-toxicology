# -*- coding: utf-8 -*-
"""Generate iMODS-specific copies: sequentially renumber residues of each chain to 1..N, removing insertion codes / residue 0.
Output prodigy/PX_*_imods.pdb + mapping_PX.csv (original numbering → new numbering, for back-mapping)."""
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
                orig = line[22:27].strip()          # residue number + insertion code
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
    print(f"{base}_imods.pdb  chains={nch}  residues={len(maps)}")

# self-check: after renumbering there should be no gaps / residue 0 / insertion codes
import glob
for f in sorted(glob.glob(os.path.join(HERE, "*_imods.pdb"))):
    bad = 0
    for line in open(f):
        if line.startswith(("ATOM", "HETATM")):
            if line[26].strip() or int(line[22:26]) <= 0:
                bad += 1
    print(os.path.basename(f), "remaining problem atoms:", bad)
