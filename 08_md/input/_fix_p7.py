# -*- coding: utf-8 -*-
"""Insert SEQRES for chain R (VEGFR2 132-329, UniProt P35968) and run PDBFixer."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "md_P7_svVEGF_VEGFR2_hdock.pdb")
SEQRES_PDB = os.path.join(HERE, "md_P7_seqres.pdb")
OUT = os.path.join(HERE, "md_P7_fixed.pdb")

AA3 = ["ALA","ARG","ASN","ASP","CYS","GLN","GLU","GLY","HIS","ILE","LEU","LYS","MET",
       "PHE","PRO","SER","THR","TRP","TYR","VAL"]
M3 = dict(zip(AA3, "ARNDCQEGHILKMFPSTWYV"))

# 1. UniProt sequence
seq = "".join(l.strip() for l in open(os.path.join(HERE, "KDR_P35968.fasta")) if not l.startswith(">"))
print("UniProt len", len(seq))
seg = seq[131:329]  # residues 132..329 (1-based)
assert len(seg) == 198, len(seg)

# 2. PDB chain R observed sequence
obs = []
seen = set()
for l in open(SRC):
    if l.startswith("ATOM") and l[21] == "R":
        r = int(l[22:26])
        if r not in seen:
            seen.add(r); obs.append((r, M3[l[17:20].strip()]))
obs.sort()
obs_seq = "".join(a for _, a in obs)
obs_res = [r for r, _ in obs]
print("chain R observed", obs_res[0], "-", obs_res[-1], "n =", len(obs_seq))

# 3. verify: observed == segment minus gaps
seg_map = {132 + i: a for i, a in enumerate(seg)}
pdb_from_uniprot = "".join(seg_map[r] for r in obs_res)
assert pdb_from_uniprot == obs_seq, "MISMATCH: PDB residues do not match UniProt P35968 132-329"
print("sequence identity check PASSED")

# 4. build SEQRES lines (PDB spec: cols 1-6 'SEQRES', 9-10 serNum, 12 chain, 14-17 numRes, 20+ residues)
lines = []
n = len(seg)
res3 = [" ".join([k for k, v in M3.items() if v == a]) for a in seg]
for i, start in enumerate(range(0, n, 13)):
    chunk = res3[start:start+13]
    body = "".join("%-4s" % r for r in chunk)
    lines.append("SEQRES  %2d R %4d  %s" % (i + 1, n, body))
header = "\n".join(lines) + "\n"

# 5. insert before first ATOM
txt = open(SRC).read()
i = txt.find("ATOM")
open(SEQRES_PDB, "w").write(txt[:i] + header + txt[i:])
print("SEQRES inserted ->", SEQRES_PDB)

# 6. PDBFixer
from pdbfixer import PDBFixer
from openmm.app import PDBFile
fixer = PDBFixer(filename=SEQRES_PDB)
fixer.findMissingResidues()
print("missing residues:", fixer.missingResidues)
fixer.findNonstandardResidues(); fixer.replaceNonstandardResidues()
fixer.findMissingAtoms(); fixer.addMissingAtoms()
fixer.addMissingHydrogens(7.4)   # WebGRO/GROMACS can also do this; adding now is harmless
with open(OUT, "w") as f:
    PDBFile.writeFile(fixer.topology, fixer.positions, f)

# 7. verify
chains = {}
for l in open(OUT):
    if l.startswith("ATOM"):
        chains.setdefault(l[21], set()).add(int(l[22:26]))
for c, rs in chains.items():
    sr = sorted(rs); gaps = [(a, b) for a, b in zip(sr, sr[1:]) if b - a > 1]
    print("OUT chain", c, "res", sr[0], "-", sr[-1], "n =", len(sr), "gaps", gaps)
print("atoms:", sum(1 for l in open(OUT) if l.startswith("ATOM")))
print("saved", OUT)
