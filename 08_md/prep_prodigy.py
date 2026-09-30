# -*- coding: utf-8 -*-
"""Route C preparation: 7 pairs of best docking poses → PRODIGY/iMODS normalized PDBs
Chain-block rule: a TER record or a change of original chain ID both count as boundaries; relabeled A/B/C…
Output: 08_md/prodigy/P1..P7_*.pdb + chain_map.txt (reference for web-submission checkboxes)"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
DOCK = os.path.join(BASE, "..", "07_docking")
OUT = os.path.join(BASE, "prodigy")
os.makedirs(OUT, exist_ok=True)

# (id, source file, output name, target chains [relabeled], toxin chains [relabeled])
MODELS = [
    ("P1", os.path.join(DOCK, "results", "cluspro", "P1", "model.000.00.pdb"),
     "P1_RVVX_FXa.pdb", "A B", "C D E"),
    ("P2", os.path.join(DOCK, "figure", "p2_cluster1_1.pdb"),
     "P2_RVVV_FV.pdb", "B", "A"),
    ("P3", os.path.join(DOCK, "results", "cluspro", "P3", "model.000.00.pdb"),
     "P3_dabK_FIB.pdb", "A B C", "D"),
    ("P4", os.path.join(DOCK, "results", "cluspro", "P4", "model.000.00.pdb"),
     "P4_snaclec_GP1BA.pdb", "A", "B"),
    ("P5", os.path.join(DOCK, "results", "cluspro", "P5", "model.000.00.pdb"),
     "P5_PLA2_FXa.pdb", "A B", "C"),
    ("P6", os.path.join(DOCK, "results", "cluspro", "P6", "model.000.00.pdb"),
     "P6_Kunitz_PLG.pdb", "A", "B"),
    ("P7", os.path.join(DOCK, "results", "hdock", "P7", "model_1.pdb"),
     "P7_svVEGF_VEGFR2.pdb", "A", "B C"),
]
NAMES = {
    "P1": ("FXa (coagulation factor Xa)", "RVV-X (SVMP+snaclec complex)"),
    "P2": ("FV (coagulation factor V)", "RVV-Vγ (SVSP)"),
    "P3": ("fibrinogen FGA (3GHG)", "daborhagin-K (SVMP P-III)"),
    "P4": ("GP1BA (VWF receptor)", "snaclec Q38L02"),
    "P5": ("FXa (coagulation factor Xa)", "PLA2 VRV-PL-VIIIa"),
    "P6": ("plasmin (PLG)", "Kunitz H6VC06"),
    "P7": ("VEGFR2 (KDR)", "svVEGF P67861 dimer"),
}
LETTERS = "ABCDEFGHIJ"

def process(src, dst):
    blocks, cur_res, cur_orig = [], [], None
    natom = 0
    def flush(out):
        if cur_res:
            blocks.append((min(cur_res), max(cur_res), len(cur_res)))
    with open(dst, "w", encoding="ascii", errors="ignore") as out:
        for line in open(src, encoding="utf-8", errors="ignore"):
            rec = line[:6].strip()
            if rec in ("ATOM", "HETATM"):
                orig_ch = line[21]
                if cur_orig is not None and orig_ch != cur_orig:
                    # original chain-ID change = new block
                    blocks.append((min(cur_res), max(cur_res), len(cur_res)))
                    cur_res = []
                    out.write("TER\n")
                cur_orig = orig_ch
                out.write(line[:21] + LETTERS[len(blocks)] + line[22:] if line.endswith("\n")
                          else line[:21] + LETTERS[len(blocks)] + line[22:] + "\n")
                rs = line[22:26].strip()
                if rs.isdigit():
                    cur_res.append(int(rs))
                natom += 1
            elif rec == "TER":
                if cur_res:
                    blocks.append((min(cur_res), max(cur_res), len(cur_res)))
                    cur_res = []
                    cur_orig = None
                    out.write("TER\n")
            elif rec == "END":
                out.write("END\n")
        if cur_res:
            blocks.append((min(cur_res), max(cur_res), len(cur_res)))
    return blocks, natom

print(f"{'pair':<6}{'file':<26}{'atoms':>6}  chain blocks (letter: residue range [atom count])")
report = []
for pid, src, name, tgt, tox in MODELS:
    dst = os.path.join(OUT, name)
    blocks, natom = process(src, dst)
    desc = "  ".join(f"{LETTERS[i]}: {a}-{b}[{c}]" for i, (a, b, c) in enumerate(blocks))
    print(f"{pid:<4}{name:<26}{natom:>6}  {desc}")
    report.append((pid, name, tgt, tox, desc))

with open(os.path.join(OUT, "chain_map.txt"), "w", encoding="utf-8") as f:
    f.write("PRODIGY / iMODS chain-ownership reference (relabeled letters govern)\n")
    f.write("When submitting to PRODIGY: Partner 1 = target chains, Partner 2 = toxin chains (swapping order does not change ΔG)\n")
    f.write("=" * 76 + "\n")
    for pid, name, tgt, tox, desc in report:
        t, x = NAMES[pid]
        f.write(f"\n{pid}  {name}\n  chain blocks: {desc}\n  target chains {tgt} = {t}\n  toxin chains {tox} = {x}\n")
print("\nchain_map.txt written")
