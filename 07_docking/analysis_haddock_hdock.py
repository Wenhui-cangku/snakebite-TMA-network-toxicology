# -*- coding: utf-8 -*-
"""Interface-check script for HADDOCK 4 pairs + HDock P7 results"""
from pathlib import Path
import numpy as np
from collections import defaultdict

BASE = str(Path(__file__).resolve().parent)

def read_pdb(path):
    """returns list of (chain, resnum, resname, atom, xyz)"""
    atoms = []
    for line in open(path, encoding='utf-8', errors='ignore'):
        if line.startswith(('ATOM', 'HETATM')):
            ch = line[21]
            try:
                rn = int(line[22:26])
            except ValueError:
                continue
            resname = line[17:20].strip()
            atom = line[12:16].strip()
            xyz = np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])
            atoms.append((ch, rn, resname, atom, xyz))
    return atoms

def interface_residues(atoms, ch_lig, ch_rec, cutoff=5.0):
    lig = [(rn, xyz) for ch, rn, rs, at, xyz in atoms if ch == ch_lig]
    rec = [(rn, xyz) for ch, rn, rs, at, xyz in atoms if ch == ch_rec]
    lig_coords = np.array([x for _, x in lig])
    rec_coords = np.array([x for _, x in rec])
    # distance matrix (chunked to avoid memory blowup)
    lig_if, rec_if = set(), set()
    for i in range(0, len(lig_coords), 2000):
        block = lig_coords[i:i+2000]
        d = np.sqrt(((block[:, None, :] - rec_coords[None, :, :])**2).sum(-1))
        li, ri = np.where(d <= cutoff)
        for a in li:
            lig_if.add(lig[i+a][0])
        for b in ri:
            rec_if.add(rec[b][0])
    return sorted(lig_if), sorted(rec_if)

def min_dist_between(atoms, chA, resA, chB, resB):
    ca = [xyz for ch, rn, rs, at, xyz in atoms if ch == chA and rn in resA]
    cb = [xyz for ch, rn, rs, at, xyz in atoms if ch == chB and rn in resB]
    if not ca or not cb:
        return None
    ca, cb = np.array(ca), np.array(cb)
    return float(np.sqrt(((ca[:, None] - cb[None])**2).sum(-1)).min())

PAIRS = {
    'P1': dict(file=BASE+r"\results\haddock\P1\773395-P1_RVVX_FXa_summary\cluster1_1.pdb",
               toxin='A', host='B', toxin_name='RVV-X', host_name='FXa',
               host_sites={16,17,18,19,20,21}, site_label='FXa N-terminal 16-21',
               toxin_restr={145,146,149,155}, host_restr={16,17,18,19,20,21}),
    'P2': dict(file=BASE+r"\results\haddock\P2\773398-P22_RVVV_FV_summary\cluster1_1.pdb",
               toxin='A', host='B', toxin_name='RVV-Vγ', host_name='FV',
               host_sites=set(range(1543,1549)), site_label='FV cleavage region 1543-1548',
               toxin_restr={42,193,194,195,196,197}, host_restr=set(range(1543,1549))),
    'P3': dict(file=BASE+r"\results\haddock\P3\773397-P3_daborhaginK_FIB_summary\cluster1_1.pdb",
               toxin='A', host='B', toxin_name='daborhagin-K', host_name='FGA',
               host_sites=set(range(195,201)), site_label='FGA C-terminal 195-200 (proxy)',
               toxin_restr={339,340,343,349}, host_restr=set(range(195,201))),
    'P6': dict(file=BASE+r"\results\haddock\P6\773402-P6_Kunitz_PLG_summary\cluster1_1.pdb",
               toxin='A', host='B', toxin_name='Kunitz', host_name='PLG',
               host_sites={603,646,741}, site_label='PLG catalytic triad 603/646/741',
               toxin_restr=set(range(38,43)), host_restr={603,646,741}),
}

print("="*80)
print("HADDOCK cluster1_1 interface check (cutoff 5 Å)")
print("="*80)
for p, cfg in PAIRS.items():
    atoms = read_pdb(cfg['file'])
    lig_if, rec_if = interface_residues(atoms, cfg['toxin'], cfg['host'])
    rec_if_set, lig_if_set = set(rec_if), set(lig_if)
    site_hit = cfg['host_sites'] & rec_if_set
    trestr_hit = cfg['toxin_restr'] & lig_if_set
    hrestr_hit = cfg['host_restr'] & rec_if_set
    mind = min_dist_between(atoms, cfg['toxin'], cfg['toxin_restr'], cfg['host'], cfg['host_restr'])
    print(f"\n--- {p}: {cfg['toxin_name']} × {cfg['host_name']} ---")
    print(f"interface residues: toxin side {len(lig_if)} | host side {len(rec_if)}")
    print(f"host interface residues: {rec_if}")
    print(f"{cfg['site_label']} coverage: {len(site_hit)}/{len(cfg['host_sites'])} -> {sorted(site_hit)}")
    print(f"toxin restraint residues {sorted(cfg['toxin_restr'])} in interface: {sorted(trestr_hit)} ({len(trestr_hit)}/{len(cfg['toxin_restr'])})")
    print(f"host restraint residues {sorted(cfg['host_restr'])} in interface: {sorted(hrestr_hit)} ({len(hrestr_hit)}/{len(cfg['host_restr'])})")
    print(f"toxin-restraint to host-restraint closest atom distance: {mind:.2f} Å" if mind else "restraint residues missing!")
    # multi-cluster consistency: check whether cluster1_2/2_1/3_1 share the same orientation
print()
print("="*80)
print("multi-cluster orientation consistency (host interface residues of the first 3 clusters per pair)")
print("="*80)
import glob, os
for p, cfg in PAIRS.items():
    folder = os.path.dirname(cfg['file'])
    clus = sorted(glob.glob(folder + r"\cluster*_1.pdb"))
    print(f"\n--- {p} ({len(clus)} clusters) ---")
    for c in clus[:6]:
        atoms = read_pdb(c)
        _, rec_if = interface_residues(atoms, cfg['toxin'], cfg['host'])
        hit = cfg['host_sites'] & set(rec_if)
        name = os.path.basename(c)
        # compact display
        print(f"  {name}: host interface {len(rec_if)} residues, functional-site coverage {sorted(hit) if hit else 'none'}, interface segments {rec_if[:8]}{'...' if len(rec_if)>8 else ''}")
