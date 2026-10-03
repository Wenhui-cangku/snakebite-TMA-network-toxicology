# -*- coding: utf-8 -*-
"""HADDOCK 4对 + HDock P7 结果界面核对脚本"""
from pathlib import Path
import numpy as np
from collections import defaultdict

BASE = str(Path(__file__).resolve().parent)

def read_pdb(path):
    """返回 list of (chain, resnum, resname, atom, xyz)"""
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
    # 距离矩阵(分块防爆内存)
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
               host_sites={16,17,18,19,20,21}, site_label='FXa N端16-21',
               toxin_restr={145,146,149,155}, host_restr={16,17,18,19,20,21}),
    'P2': dict(file=BASE+r"\results\haddock\P2\773398-P22_RVVV_FV_summary\cluster1_1.pdb",
               toxin='A', host='B', toxin_name='RVV-Vγ', host_name='FV',
               host_sites=set(range(1543,1549)), site_label='FV切割区1543-1548',
               toxin_restr={42,193,194,195,196,197}, host_restr=set(range(1543,1549))),
    'P3': dict(file=BASE+r"\results\haddock\P3\773397-P3_daborhaginK_FIB_summary\cluster1_1.pdb",
               toxin='A', host='B', toxin_name='daborhagin-K', host_name='FGA',
               host_sites=set(range(195,201)), site_label='FGA C端195-200(代理)',
               toxin_restr={339,340,343,349}, host_restr=set(range(195,201))),
    'P6': dict(file=BASE+r"\results\haddock\P6\773402-P6_Kunitz_PLG_summary\cluster1_1.pdb",
               toxin='A', host='B', toxin_name='Kunitz', host_name='PLG',
               host_sites={603,646,741}, site_label='PLG催化三联体603/646/741',
               toxin_restr=set(range(38,43)), host_restr={603,646,741}),
}

print("="*80)
print("HADDOCK cluster1_1 界面核对 (cutoff 5 Å)")
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
    print(f"界面残基数: 毒素侧 {len(lig_if)} | 宿主侧 {len(rec_if)}")
    print(f"宿主界面残基: {rec_if}")
    print(f"{cfg['site_label']} 覆盖: {len(site_hit)}/{len(cfg['host_sites'])} -> {sorted(site_hit)}")
    print(f"毒素约束残基 {sorted(cfg['toxin_restr'])} 进入界面: {sorted(trestr_hit)} ({len(trestr_hit)}/{len(cfg['toxin_restr'])})")
    print(f"宿主约束残基 {sorted(cfg['host_restr'])} 进入界面: {sorted(hrestr_hit)} ({len(hrestr_hit)}/{len(cfg['host_restr'])})")
    print(f"毒素约束-宿主约束 最近原子距离: {mind:.2f} Å" if mind else "约束残基缺失!")
    # 多簇一致性: 看 cluster1_2/2_1/3_1 是否一致取向
print()
print("="*80)
print("多簇取向一致性 (各对前3个簇的宿主界面残基)")
print("="*80)
import glob, os
for p, cfg in PAIRS.items():
    folder = os.path.dirname(cfg['file'])
    clus = sorted(glob.glob(folder + r"\cluster*_1.pdb"))
    print(f"\n--- {p} ({len(clus)} 簇) ---")
    for c in clus[:6]:
        atoms = read_pdb(c)
        _, rec_if = interface_residues(atoms, cfg['toxin'], cfg['host'])
        hit = cfg['host_sites'] & set(rec_if)
        name = os.path.basename(c)
        # 压缩显示
        print(f"  {name}: 宿主界面{len(rec_if)}残基, 功能位点覆盖 {sorted(hit) if hit else '无'}, 界面区段 {rec_if[:8]}{'...' if len(rec_if)>8 else ''}")
