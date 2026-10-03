# Phase 5A 报告 —— 分子对接结构准备

日期：2026-09-24 ｜ 执行：Kimi ｜ 状态：**结构准备完成；网页对接待手工提交（指南已备）**

## 1. 结构资产盘点

### 毒素（8 个）

| 毒素 | 来源 | 分辨率/质量 | 用途 |
|---|---|---|---|
| RVV-X 全复合体（SVMP 重链 + snaclec 轻链 ×2） | PDB **2E3X** | 2.91 Å | P1 |
| RVV-Vγ | PDB **3S9C**（含 FV 片段共结晶！） | 1.8 Å | P2 |
| PLA2 VRV-PL-VIIIa（P59071） | PDB **1KPM** | 1.8 Å | P5 |
| daboiatoxin 异二聚体 | PDB 2H4C | 2.6 Å | 备用 |
| svVEGF（P67861） | PDB **1WQ9** | 2.0 Å | P7 |
| daborhagin-K（B8K1W0） | AlphaFold DB | 平均 pLDDT **84.0**（>70 占 85%） | P3 |
| snaclec（Q38L02） | AlphaFold DB | 平均 pLDDT **88.9** | P4 |
| Kunitz（H6VC06） | AlphaFold DB | 平均 pLDDT **88.6** | P6 |

### 宿主靶点（8 个，全部 PDB 实验结构）

FV **7KVE**（3.3 Å cryoEM）、FXa **2W26**（2.08 Å）、纤维蛋白原 **3GHG**（2.9 Å）、GP1BA **1M10**（3.1 Å，含 VWF A1 复合体模板）、VEGFR2 **3V2A**（3.2 Å，含 VEGF-A 姿态模板）、纤溶酶原 **1QRZ**（2.0 Å）、凝血酶 **1PPB**（1.92 Å）。

## 2. 对接配对（7 对，全部对应 L2 文献边 score=1.0）

| 配对 | 命题 |
|---|---|
| P1 | RVV-X → FX 激活切割 |
| P2 | RVV-Vγ → FV（Arg1545 切割） |
| P3 | daborhagin-K → 纤维蛋白原 Aα |
| P4 | snaclec → GP1BA |
| P5 | PLA2 → FXa（抗凝 IC50=130 nM） |
| P6 | Kunitz → 纤溶酶（Ki=0.19 nM） |
| P7 | svVEGF → VEGFR2/KDR |

清单：`docking_pairs.csv`（含 HADDOCK 活性残基提示）；预处理文件 `prepared/`（按链提取、去水去配体、保留催化 Zn）。

## 3. 两条免对接直接结构证据（写 Results 时强调）

1. **3S9C**：RVV-Vγ 与 FV 底物片段（B 链）共结晶，1.8 Å——RVV-V→FV 已是实验结构事实，对接仅作全长蛋白层验证；
2. **1M10**：GP1BA–VWF A1 复合体——为 P4（snaclec→GP1BA）提供结合位点模板。

## 4. 本机可行性评估（如实）

- 蛋白–蛋白对接本机无软件 → HADDOCK 2.4 / ClusPro / HDock 网页平台（《对接提交指南.md》已含逐步操作与结果回填流程）；
- 小分子层（batimastat 等 × SVMP）：Vina 无法本机安装 → CB-Dock2/SwissDock 网页版；
- 对接结果返回后由我汇总出 Figure 5 面板并写 Phase 5B 报告。

## 5. 产出

`07_docking/structures/`（16 个原始结构）、`prepared/`（16 个对接就绪文件）、`docking_pairs.csv`、`对接提交指南.md`、可复跑脚本 `scripts/prep_docking.py`；Excel 变更记录 v13。
