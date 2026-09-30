# -*- coding: utf-8 -*-
"""MD starting-structure preprocessing: extract best poses from docking results, clean into GROMACS-ready pure-ATOM PDBs,
output chain/residue/atom statistics and missing-residue warnings. Output to 08_md/input/"""
import os, re, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
DOCK = os.path.join(BASE, "..", "07_docking")
SMOL = os.path.join(BASE, "..", "08_smallmol")
INP = os.path.join(BASE, "input")
os.makedirs(INP, exist_ok=True)

SOURCES = [
    # (source file, output name, description, whether to relabel chains by TER blocks)
    (os.path.join(DOCK, "figure", "p2_cluster1_1.pdb"), "md_P2_RVVV_FV_haddock.pdb",
     "P2 RVV-Vγ×FV HADDOCK cluster1_1 (both-criteria pose, PyMOL scene version already pure ATOM)", False),
    (os.path.join(DOCK, "results", "hdock", "P7", "model_1.pdb"), "md_P7_svVEGF_VEGFR2_hdock.pdb",
     "P7 svVEGF×VEGFR2 HDock model_1（confidence 0.897）", False),
    (os.path.join(DOCK, "figure", "p4_cluspro.pdb"), "md_P4_snaclec_GP1BA_cluspro.pdb",
     "P4 snaclec×GP1BA ClusPro model.000.00 (pure-ATOM scene version)", True),
]
# small molecule (optional/advanced: requires CGenFF ligand topology)
SMOL_SRC = os.path.join(SMOL, "results", "RVVX_batimastat.pdbqt")

def clean_pdb(src, dst, relabel_blocks=False):
    """keep only ATOM/HETATM/TER/END; count chains, residues, atoms, residue-number gaps.
    with relabel_blocks=True, relabel the chain column by TER blocks as A/B/C… (for ClusPro all-chain-A files)"""
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
                    out.write("TER\n")  # insert TER at chain switches so pdb2gmx splits chains correctly
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
    print(f"  atoms {natoms} (HETATM {het})")
    for ch, reslist in sorted(chains.items()):
        uniq = sorted(set(r for r in reslist if r >= 0))
        gaps = [(a, b) for a, b in zip(uniq, uniq[1:]) if b - a > 1]
        print(f"  chain {ch}: {len(uniq)} residues ({uniq[0]}–{uniq[-1]})", end="")
        if gaps:
            print(f"  ⚠ gaps at {len(gaps)} places: {gaps[:5]}", end="")
        print()

if os.path.exists(SMOL_SRC):
    # pdbqt → pdb (coordinates only, dropping charge/type columns)
    dst = os.path.join(INP, "md_batimastat_RVVX_pose.pdb")
    n = 0
    with open(dst, "w") as out:
        for line in open(SMOL_SRC, errors="ignore"):
            if line.startswith(("ATOM", "HETATM")):
                out.write(line[:66].rstrip() + "\n")
                n += 1
    print(f"\n### md_batimastat_RVVX_pose.pdb  Vina pose {n} atoms (pdbqt→pdb, coordinates only)")
    print("  ⚠ small-molecule MD requires separate CGenFF/ParmEd topology, see SOP §6")

print("\noutput directory:", INP)
print(os.listdir(INP))
