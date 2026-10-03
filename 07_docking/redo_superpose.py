# -*- coding: utf-8 -*-
"""重写 P7 叠合 PDB,保留原始原子行格式"""
from pathlib import Path
import numpy as np

BASE = str(Path(__file__).resolve().parent)

def ca(path, ch):
    m = {}
    for line in open(path, encoding='utf-8', errors='ignore'):
        if line.startswith('ATOM') and line[21] == ch and line[12:16].strip() == 'CA':
            m[int(line[22:26])] = np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])
    return m

mR = ca(BASE + r"\results\hdock\P7\model_1.pdb", 'R')
rR = ca(BASE + r"\prepared\3V2A_full.pdb", 'R')
common = sorted(set(mR) & set(rR))
P = np.array([mR[r] for r in common]); Q = np.array([rR[r] for r in common])
Pc, Qc = P.mean(0), Q.mean(0)
H = (P - Pc).T @ (Q - Qc)
U, S, Vt = np.linalg.svd(H)
D = np.diag([1, 1, np.sign(np.linalg.det(Vt.T @ U.T))])
R = Vt.T @ D @ U.T
t = Qc - R @ Pc

out = open(BASE + r"\results\hdock\P7\model_1_superposed_on_3V2A.pdb", 'w', encoding='utf-8')
n = 0
for line in open(BASE + r"\results\hdock\P7\model_1.pdb", encoding='utf-8', errors='ignore'):
    if line.startswith(('ATOM', 'HETATM')):
        xyz = np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])
        v = R @ xyz + t
        out.write(line[:30] + f"{v[0]:8.3f}{v[1]:8.3f}{v[2]:8.3f}" + line[54:])
        n += 1
    else:
        out.write(line)
out.close()
print("重写完成, 原子数", n)
