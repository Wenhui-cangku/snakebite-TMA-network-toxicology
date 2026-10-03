# Phase 5C（可选增强）：分子动力学（MD）模拟 SOP

更新：2026-09-30 ｜ 对应方案：Figure 6（MD 验证对接构象稳定性）
性质：**可选增强项**。无 MD 不影响主结论（论文 Limitations 已如实声明）；加上可显著提升审稿说服力。

---

## 0. 算力现实与路线选择（先选路线再动手）

| 路线 | 硬件 | 100 ns/复合物耗时 | 成本 | 适合 |
|---|---|---|---|---|
| A 云 GPU（AutoDL/恒源云等，RTX 3090/4090） | 租 GPU | P7/P4 约 6–12 h；P2 约 1–2 天 | 约 ¥2/h，全程 < ¥200 | **推荐** |
| B 本机 WSL2 + GROMACS（CPU 20 核） | 自己的电脑 | P7/P4 约 2–4 天；P2 约 1–2 周 | 0 元但占机器 | 不急时 |
| C 轻量替代（浏览器，当天出结果） | 无 | 每个复合物 5–10 分钟 | 0 | **见 §7**：iMODS 正常模式分析 + PRODIGY 亲和力预测，可作 Figure 6 级证据 |

**本机已备好 4 个起始结构**（`08_md/input/`，已纯 ATOM 化、链已规范、统计如下）：

| 文件 | 复合物 | 原子数 | 链 | 备注 |
|---|---|---|---|---|
| `md_P2_RVVV_FV_haddock.pdb` | RVV-Vγ×FV（HADDOCK 双达标） | 15,894 | A=RVV-Vγ(234) B=FV(1374) | B 链 713→1536 断档 = FV B 域缺失构建，晶体结构本身如此，**正常** |
| `md_P7_svVEGF_VEGFR2_hdock.pdb` | svVEGF×VEGFR2（HDock 0.897） | 2,870 | A/B=svVEGF 二聚体 R=VEGFR2(185) | R 链两处小断档=晶体缺失环，可接受 |
| `md_P4_snaclec_GP1BA_cluspro.pdb` | snaclec×GP1BA（ClusPro 59 簇） | 3,475 | A=GP1BA(505–703) B=snaclec(154) | 最小，适合先试跑 |
| `md_batimastat_RVVX_pose.pdb` | batimastat 姿态（仅坐标） | 324 | — | 小分子 MD 见 §6（进阶，可选） |

**建议模拟规模**：3 个蛋白复合物 × 100 ns × 各 1 次（若审稿人要求重复再补 3 次重复）。
优先顺序：**P7 → P4 → P2**（P7 最小、证据链最完整；P2 最大放最后）。

---

## 1. 环境准备（路线 A/B 通用）

```bash
# Ubuntu 22.04（云镜像或 WSL2）
sudo apt update && sudo apt install -y gromacs mpi-default-bin
gmx --version   # 2022+ 均可；GPU 版云镜像自带 CUDA 加速

# 力场：CHARMM36-jul2022（蛋白+离子+TIP3P 水全套）
wget https://charmm-gui.org/archive/charmm36/charmm36-jul2022.ff.tgz
tar xzf charmm36-jul2022.ff.tgz   # 解压到工作目录
```

## 2. 蛋白复合物标准流程（以 P7 为例，P4/P2 换文件名即可）

```bash
MD=~/md/P7; mkdir -p $MD && cd $MD
cp 08_md/input/md_P7_svVEGF_VEGFR2_hdock.pdb complex.pdb

# 1) 拓扑（-ignh 忽略 H 由力场重建；末端默认中性帽不加则去掉 -ter 交互）
gmx pdb2gmx -f complex.pdb -o processed.gro -p topol.top \
    -ff charmm36-jul2022 -water tip3p -ignh

# 2) 盒子与溶剂（复合物距盒壁 1.2 nm）
gmx editconf -f processed.gro -o boxed.gro -c -d 1.2 -bt dodecahedron
gmx solvate -cp boxed.gro -cs spc216.gro -p topol.top -o solvated.gro

# 3) 离子（0.15 M NaCl 生理浓度，自动中和电荷）
gmx grompp -f ions.mdp -c solvated.gro -p topol.top -o ions.tpr
gmx genion -s ions.tpr -p topol.top -pname NA -nname CL \
    -neutral -conc 0.15 -o solv_ions.gro <<< "SOL"

# 4) 能量最小化（50 kJ/mol/nm 收敛）
gmx grompp -f minim.mdp -c solv_ions.gro -p topol.top -o em.tpr
gmx mdrun -deffnm em

# 5) NVT 100 ps → NPT 100 ps（重原子位置限制）
gmx grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr
gmx mdrun -deffnm nvt
gmx grompp -f npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p topol.top -o npt.tpr
gmx mdrun -deffnm npt

# 6) 生产 100 ns（2 fs 步长 = 50,000,000 步；GPU: -nb gpu -pme gpu）
gmx grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top -o md_100ns.tpr
gmx mdrun -deffnm md_100ns -nb gpu -pme gpu -bonded gpu
```

`ions.mdp / minim.mdp / nvt.mdp / npt.mdp / md.mdp` 五个参数文件模板见 `08_md/mdp/`（本目录已附）。

## 3. 分析命令（跑完一个做一个）

```bash
# PBC 校正（先做这个，否则 RMSD 假象）
gmx trjconv -s md_100ns.tpr -f md_100ns.xtc -o md_nojump.xtc -pbc nojump <<< "System"
gmx trjconv -s md_100ns.tpr -f md_nojump.xtc -o md_center.xtc -pbc mol -center -ur compact <<< "Protein / System"

# RMSD（复合物骨架 vs 起始构象）
gmx rms -s md_100ns.tpr -f md_center.xtc -o rmsd.xvg -tu ns <<< "Backbone / Backbone"
# RMSF（每条链分别看界面柔性）
gmx rmsf -s md_100ns.tpr -f md_center.xtc -o rmsf.xvg -res <<< "Backbone"
# 回转半径
gmx gyrate -s md_100ns.tpr -f md_center.xtc -o rg.xvg <<< "Protein"
# 界面氢键数（链 A/B 或 A/R 之间）
gmx hbond -s md_100ns.tpr -f md_center.xtc -num hbond.xvg <<< "chain_A / chain_B"
# 界面关键残基距离（如 P2 切割位点 1543-1548 到 RVV-Vγ 催化区）
gmx distance -s md_100ns.tpr -f md_center.xtc -oav keydist.xvg -select '...'
```

## 4. MM-GBSA 结合自由能（gmx_MMPBSA）

```bash
pip install gmx_MMPBSA  # 需 python3.9-3.11 环境
# mmpbsa.in 模板见 08_md/mdp/mmpbsa.in（GB OBC2, 盐浓度 0.15 M, 取平衡段 50–100 ns 每 10 帧）
mpirun -np 10 gmx_MMPBSA -O -i mmpbsa.in -cs md_100ns.tpr -ct md_center.xtc \
    -ci index.ndx -cg 1 2 -cp topol.top -o FINAL_RESULTS.dat
```
判读：ΔG_bind < −20 kcal/mol 且平衡段稳定 → 强支持；−10~−20 → 中等支持；> −10 或与对接排序矛盾 → 如实写"未获自由能层面支持"。

## 5. Figure 6 建议版式（4 联面板）

| 面板 | 内容 | 数据源 |
|---|---|---|
| A | 3 个复合物 RMSD 曲线（100 ns，平台期判定） | rmsd.xvg |
| B | P7 RMSF 按残基（界面残基区低柔性=稳定） | rmsf.xvg + 界面清单着色 |
| C | 界面氢键数随时间（P2/P4/P7 三线） | hbond.xvg |
| D | MM-GBSA ΔG 柱状图（复合物×能量分解） | FINAL_RESULTS.dat |

绘图脚本可复用 `04_network/robustness_analysis.py` 的 matplotlib 风格（`setup_plot()` + 300 dpi + SVG）。

## 6. 小分子 MD（可选，进阶）

batimastat×RVV-X（晶体含催化 Zn²⁺）：
- 配体拓扑：CGenFF 服务器（https://cgenff.com）上传 `md_batimastat_RVVX_pose.pdb` 得 `.str`，用 `cgenff_charmm2gmx.py` 转 GROMACS 拓扑并入 topol.top；
- **Zn²⁺ 必须用键合模型**（Zn-His/Glu 配位距离约束或 MCPB.py 生成参数），非键合模型 Zn 会漂移——这一层做不好宁可不做，论文里小分子层有对接+螯合几何已够。

## 7. 路线 C：轻量替代（今天就能做，浏览器）

1. **iMODS 正常模式分析**（https://imods.iqf.csic.es）：上传复合物 PDB → 得 deformability/B-factor/特征值/协方差图；本领域论文常用作"复合物稳定性"证据。3 个复合物各 5 分钟，截图存档；
2. **PRODIGY**（https://wenmr.science.uu.nl/prodigy/）：上传复合物 PDB → 预测 ΔG/Kd；为 7 对对接补一层独立亲和力证据（比 MM-GBSA 弱但零成本）。

若时间允许，**推荐组合：路线 C 今天出结果进初稿（标注为 NMA/预测级证据），路线 A 作为返修或后续工作**——避免为了 MD 拖住投稿。

## 8. 质控点

- [ ] EM 收敛（Fmax < 1000 kJ/mol/nm）；NPT 后密度/体积平稳
- [ ] RMSD 在后 50 ns 进入平台（漂移 < 0.05 nm），否则延长或检查构象崩塌
- [ ] 界面氢键数不归零（归零 = 复合物解离，构象不可信，需如实报告）
- [ ] MM-GBSA 取平衡段；能量分解看界面关键残基贡献
- [ ] 所有 .mdp/.tpr/轨迹文件归档，版本记入数据管理表
