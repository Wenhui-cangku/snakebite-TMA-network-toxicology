# -*- coding: utf-8 -*-
"""iMODS 原始数据深度分析 + Figure 6 拼版
从 job 目录的 imode_cart.evec / imode.eval / input.pdb：
1) 逐残基迁移率 m_i = Σ_k |v_ik|²/λ_k（前 20 模式）
2) 残基相关矩阵 c_ij = Σ_k (v_i·v_j)/λ_k，归一化为相关系数
3) 界面残基（毒素链 vs 靶点链全原子 ≤5Å）柔性统计
4) Figure 6：A=PRODIGY ΔG；B=界面/其余迁移率比；C=代表迁移率曲线；D=代表相关矩阵
输出：figure6_nma_prodigy.png/.svg + imods_prodigy_summary.csv"""
import sys, os, math, glob, csv
from pathlib import Path
sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot
setup_plot()
import numpy as np
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "prodigy", "results_iMODS")

PAIRS = {  # 对: (job目录名片段, 靶点链, 毒素链, 标签)
    "P1": ("P1", "AB", "CDE", "RVV-X×FXa"),
    "P2": ("P2", "B", "A", "RVV-Vγ×FV"),
    "P3": ("P3", "ABC", "D", "dabK×FIB"),
    "P4": ("P4", "A", "B", "snaclec×GP1BA"),
    "P5": ("P5 ", "AB", "C", "PLA2×FXa"),   # 目录名为 "P5 job"
    "P6": ("P6", "A", "B", "Kunitz×plasmin"),
    "P7": ("P7", "A", "BC", "svVEGF×VEGFR2"),
}
PRODIGY = {  # 对: (ΔG, Kd)
    "P1": (-13.8, "8e-11"), "P2": (-11.7, "2.8e-09"), "P3": (-15.2, "7e-12"),
    "P4": (-9.2, "1.9e-07"), "P5": (-13.7, "8.5e-11"), "P6": (-10.7, "1.5e-08"),
    "P7": (-12.1, "1.3e-09"),
}
P6_EXP_DG = -13.25  # Ki=0.19 nM → ΔG=RT·lnK (298K)

def find_job(tag):
    cands = glob.glob(os.path.join(RES, tag.strip(), f"{tag.strip()}job*")) or \
            glob.glob(os.path.join(RES, tag.strip(), f"{tag.strip()} job*"))
    if not cands:
        cands = glob.glob(os.path.join(RES, tag.strip(), "*job*"))
    return cands[0]

def parse_evec(path):
    txt = open(path, errors="ignore").read().split("\n")
    n = None; modes = []
    i = 0
    for i, ln in enumerate(txt[:5]):
        if "Contains" in ln:
            n = int(ln.split()[0]); break
    while i < len(txt):
        ln = txt[i].strip()
        toks = ln.split()
        if len(toks) == 2 and toks[0].isdigit():
            try:
                lam = float(toks[1])
            except ValueError:
                i += 1; continue
            vals = []
            i += 1
            while len(vals) < n and i < len(txt):
                if txt[i].strip() == "****":
                    i += 1; continue
                vals += [float(x) for x in txt[i].split()]
                i += 1
            modes.append((lam, np.array(vals[:n])))
        else:
            i += 1
    return n, modes

def parse_nodes(path):
    """imode_model.pdb 全原子节点顺序（含段端 N/C 帽），返回 [(链, 残基号, 原子名)]"""
    res = []
    for line in open(path, errors="ignore"):
        if line.startswith(("ATOM", "HETATM")):
            res.append((line[21].strip(), int(line[22:26]), line[12:16].strip()))
    return res

def interface_residues(path, tgt, tox):
    """两链组间全原子 ≤5Å 界面残基，返回 {(链,残基号)} 并集。向量化实现。"""
    tgt_list, tox_list = [], []
    for line in open(path, errors="ignore"):
        if not line.startswith("ATOM"):
            continue
        ch = line[21].strip()
        xyz = (float(line[30:38]), float(line[38:46]), float(line[46:54]))
        rn = int(line[22:26])
        if ch in tgt:
            tgt_list.append((xyz, (ch, rn)))
        elif ch in tox:
            tox_list.append((xyz, (ch, rn)))
    T = np.array([t[0] for t in tgt_list]); X = np.array([t[0] for t in tox_list])
    iface = set()
    for i in range(0, len(X), 200):
        d = np.sqrt(((T[None, :, :] - X[i:i+200][:, None, :]) ** 2).sum(-1))  # (200, nT)
        hit_x, hit_t = np.where(d <= 5.0)
        for hx in set(hit_x.tolist()):
            iface.add(tox_list[i + hx][1])
        for ht in set(hit_t.tolist()):
            iface.add(tgt_list[ht][1])
    return iface

rows = []
profiles = {}
cormats = {}
for pid, (tag, tgt, tox, label) in PAIRS.items():
    job = find_job(tag)
    evec = os.path.join(job, "imode_cart.evec")
    inp = os.path.join(job, "input.pdb")
    n, modes = parse_evec(evec)
    model_pdb = os.path.join(job, "imode_model.pdb")
    ca = parse_nodes(model_pdb)          # 节点顺序与 3N 向量一致
    nres = n // 3
    assert len(ca) == nres, f"{pid}: 节点数{len(ca)} != 向量{nres}"
    lam = np.array([m[0] for m in modes])
    V = np.stack([m[1] for m in modes])          # (20, 3N)
    mob = ((V ** 2).reshape(len(modes), nres, 3).sum(axis=2) / lam[:, None]).sum(axis=0)
    mob_rel = mob / mob.mean()
    iface = interface_residues(inp, tgt, tox)
    iface_set = {(ch, rn) for ch, rn in iface}
    idx_iface = [i for i, (ch, rn, _) in enumerate(ca) if (ch, rn) in iface_set]
    idx_rest = [i for i in range(nres) if i not in idx_iface]
    ratio = np.median(mob[idx_iface]) / np.median(mob[idx_rest])
    # 相关矩阵
    C = np.zeros((nres, nres))
    for k in range(len(modes)):
        v = V[k].reshape(nres, 3)
        C += (v @ v.T) / lam[k]
    d = np.sqrt(np.diag(C))
    corr = C / np.outer(d, d)
    profiles[pid] = (ca, mob_rel, idx_iface)
    cormats[pid] = (corr, ca)
    dg, kd = PRODIGY[pid]
    rows.append([pid, label, dg, kd, f"{lam[0]:.3e}", len(idx_iface), f"{ratio:.2f}"])
    print(f"{pid} {label}: λ1={lam[0]:.3e} 界面残基={len(idx_iface)} 迁移率比={ratio:.2f} PRODIGY ΔG={dg}")

# 汇总 CSV
with open(os.path.join(HERE, "imods_prodigy_summary.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["配对", "复合物", "PRODIGY ΔG (kcal/mol)", "Kd (M)", "iMODS λ1", "界面残基数(5Å)", "界面/其余迁移率比"])
    w.writerows(rows)

# ---------- Figure 6 ----------
fig, axes = plt.subplots(2, 2, figsize=(11.5, 9))

# A: PRODIGY ΔG
ax = axes[0][0]
pids = list(PAIRS)
dgs = [PRODIGY[p][0] for p in pids]
labels = [PAIRS[p][3] for p in pids]
bars = ax.bar(range(7), dgs, color="#C62828", alpha=0.85, width=0.62)
ax.axhline(P6_EXP_DG, color="#1565C0", ls="--", lw=1.4)
ax.text(3.0, P6_EXP_DG - 0.95, "P6 exp. ΔG = −13.3 (Ki 0.19 nM)", ha="left",
        fontsize=8, color="#1565C0")
for i, v in enumerate(dgs):
    ax.text(i, v - 0.9, f"{v:.1f}", ha="center", fontsize=8.5, color="#37474F", fontweight="bold")
ax.set_xticks(range(7)); ax.set_xticklabels(labels, rotation=28, ha="right", fontsize=8)
ax.set_ylabel("PRODIGY predicted ΔG (kcal/mol)")
ax.set_ylim(min(dgs) - 2.8, 1.2)
ax.set_title("A  Predicted binding affinity (PRODIGY)", fontsize=10, fontweight="bold")

# B: 界面迁移率比
ax = axes[0][1]
ratios = [float(r[6]) for r in rows]
ax.bar(range(7), ratios, color="#2E7D32", alpha=0.85, width=0.62)
ax.axhline(1.0, color="#555", ls="--", lw=1.2)
ax.text(6.4, 1.02, "ratio = 1 (no difference)", ha="right", fontsize=8, color="#555")
for i, v in enumerate(ratios):
    ax.text(i, v + 0.02, f"{v:.2f}", ha="center", fontsize=8)
ax.set_xticks(range(7)); ax.set_xticklabels(labels, rotation=28, ha="right", fontsize=8)
ax.set_ylabel("median mobility, interface / rest")
ax.set_title("B  Interface rigidity (NMA, <1 = stiffer interface)", fontsize=10, fontweight="bold")

# C: P7 迁移率曲线（代表）
ax = axes[1][0]
ca, mob_rel, idx_iface = profiles["P7"]
xs = range(len(ca))
ax.plot(xs, mob_rel, color="#37474F", lw=1.2)
ax.scatter(idx_iface, [mob_rel[i] for i in idx_iface], s=18, color="#C62828",
           zorder=5, label="interface residues (≤5 Å)")
# 链边界
bounds, prev = [], None
for i, (ch, rn, _) in enumerate(ca):
    if ch != prev:
        bounds.append((i, ch)); prev = ch
for i, ch in bounds[1:]:
    ax.axvline(i, color="#90A4AE", lw=0.8, ls=":")
for k, (i, ch) in enumerate(bounds):
    ax.text(i + 8, max(mob_rel) * (0.95 - 0.10 * (k % 2)), f"chain {ch}", fontsize=8, color="#546E7A")
ax.set_xlabel("residue index (sequential)"); ax.set_ylabel("relative mobility")
ax.legend(fontsize=8, loc="center right")
ax.set_title("C  NMA mobility profile — P7 svVEGF×VEGFR2", fontsize=10, fontweight="bold")

# D: P7 相关矩阵
ax = axes[1][1]
corr, ca7 = cormats["P7"]
im = ax.imshow(corr, cmap="bwr", vmin=-1, vmax=1, origin="lower")
for i, ch in bounds[1:]:
    ax.axvline(i, color="k", lw=0.6); ax.axhline(i, color="k", lw=0.6)
ax.set_title("D  Residue cross-correlation — P7", fontsize=10, fontweight="bold")
ax.set_xlabel("residue index"); ax.set_ylabel("residue index")
fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

fig.tight_layout()
out = os.path.join(HERE, "..", "09_manuscript", "assets")
fig.savefig(os.path.join(out, "fig6_nma_prodigy.png"), dpi=300, bbox_inches="tight")
fig.savefig(os.path.join(out, "fig6_nma_prodigy.svg"), bbox_inches="tight")
print("\nfig6 saved to assets")
