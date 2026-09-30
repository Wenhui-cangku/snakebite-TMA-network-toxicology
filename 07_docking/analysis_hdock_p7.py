# -*- coding: utf-8 -*-
"""Superposition validation of HDock P7 model_1 against the 3V2A template"""
from pathlib import Path
import numpy as np

BASE = str(Path(__file__).resolve().parent)
IF26 = [133,135,137,195,196,215,216,217,218,219,220,221,253,254,255,256,257,258,273,274,275,276,288,311,312,313]

def read_pdb(path):
    atoms = []
    for line in open(path, encoding='utf-8', errors='ignore'):
        if line.startswith(('ATOM','HETATM')):
            atoms.append(dict(ch=line[21], rn=int(line[22:26]), atom=line[12:16].strip(),
                              xyz=np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])))
    return atoms

def kabsch(P, Q):
    """P, Q: Nx3 corresponding points; returns rotation matrix and translation superposing P onto Q"""
    Pc, Qc = P.mean(0), Q.mean(0)
    H = (P - Pc).T @ (Q - Qc)
    U, S, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    D = np.diag([1, 1, d])
    R = Vt.T @ D @ U.T
    return R, Qc - R @ Pc

model = read_pdb(BASE + r"\results\hdock\P7\model_1.pdb")
ref   = read_pdb(BASE + r"\prepared\3V2A_full.pdb")

# common CAs of chain R
def ca_map(atoms, ch):
    return {a['rn']: a['xyz'] for a in atoms if a['ch'] == ch and a['atom'] == 'CA'}

mR, rR = ca_map(model, 'R'), ca_map(ref, 'R')
common = sorted(set(mR) & set(rR))
P = np.array([mR[r] for r in common]); Q = np.array([rR[r] for r in common])
R, t = kabsch(P, Q)
rmsd_R = float(np.sqrt(((P @ R.T + t - Q)**2).sum(-1).mean()))
print(f"chain R (VEGFR2 D2) superposition: {len(common)} CAs, RMSD = {rmsd_R:.3f} Å")

# transform the whole model
for a in model:
    a['xyz'] = R @ a['xyz'] + t

# 26 interface-residue coverage: whether any svVEGF (chain A/B) atom lies within 5 Å of chain-R residue atoms
veg = np.array([a['xyz'] for a in model if a['ch'] in ('A','B')])
cov = []
for rn in IF26:
    rec = np.array([a['xyz'] for a in model if a['ch'] == 'R' and a['rn'] == rn])
    if len(rec) == 0:
        cov.append((rn, None)); continue
    d = np.sqrt(((veg[:,None]-rec[None])**2).sum(-1)).min()
    cov.append((rn, d <= 5.0))
hit = [rn for rn,ok in cov if ok]
print(f"26-interface-residue coverage: {len(hit)}/26 -> {hit}")
print(f"not covered: {[rn for rn,ok in cov if ok is False]}")

# spatial relationship to the template VEGF-A (3V2A chain A): compare centroids and closest distance
refA = np.array([a['xyz'] for a in ref if a['ch'] == 'A'])
com_model = veg.mean(0); com_ref = refA.mean(0)
print(f"svVEGF centroid vs VEGF-A template centroid distance: {float(np.linalg.norm(com_model-com_ref)):.2f} Å")
dmin = float(np.sqrt(((veg[:,None]-refA[None])**2).sum(-1)).min())
print(f"svVEGF to VEGF-A template closest atom distance: {dmin:.2f} Å")

# write out the superposed complex for PyMOL plotting
out = BASE + r"\results\hdock\P7\model_1_superposed_on_3V2A.pdb"
with open(out, 'w', encoding='utf-8') as f:
    i = 1
    for a in model:
        f.write(f"ATOM  {i:>5}  {a['atom']:<4} ALA {a['ch']}{a['rn']:>4}    "
                f"{a['xyz'][0]:8.3f}{a['xyz'][1]:8.3f}{a['xyz'][2]:8.3f}  1.00  0.00\n")
        i += 1
print(f"superposed complex written: {out}")
