# GEO 转录组验证报告（三重干法验证第 1 层）

日期：2026-09-24 ｜ 执行：Kimi ｜ 状态：**完成**

## 1. 数据集与对比设计

| 数据集 | 模型 | 主对比 | 平台/基因数 |
|---|---|---|---|
| GSE121297 | 人 HUVEC × snaclec（rhodocetin-αβ） | 静态 RCαβ vs 静态对照（3v3） | Affymetrix HG-U133 Plus 2.0 / 22,454 基因 |
| GSE248215 | 小鼠骨骼肌 × *D. russelii* 毒液（30 µg 体内注射） | 24 h vs PBS 对照（3v2） | NanoString Fibrosis V2 Panel / 760 基因 |

方法说明：limma 流程以 Python 复现（Welch t + BH FDR；探针经 g:Profiler convert API 注释，基因级取最高表达探针）；NanoString 用作者提供的归一化 log2 矩阵。**两数据集样本量小（3v3 / 3v2），BH 校正后均无 DEG 达 adj<0.05**——按侦察预案以"名义 p<0.05 + |log2FC|"作探索性判读并全程标注，此限制写入 Limitations。

## 2. 核心发现（watchlist 35 先验分子）

### GSE121297（人内皮 × snaclec）

- **轴4 内皮/炎症强烈激活**（名义显著）：SELE +6.24（p=2.3e-5）、VCAM1 +4.63、ICAM1 +3.01、NOS3 −0.43；全转录组层面 CXCL5 +5.68、CXCL3 +3.82、LTB +2.94、EBI3 +2.60 同为顶部信号——重现原研究的 snaclec→内皮炎症激活结论，**数据集质量自证通过**；
- 轴3 补体：仅 CFB +1.69（p=0.096 趋势），C3/C5/CFH/CFI/CD46 均无变化；
- 轴1/轴2：VWF、ADAMTS13、F2/F5/F10 等凝血因子无转录变化（预期内：凝血因子肝源合成，局部内皮不调控）。

### GSE248215（小鼠体内 × *D. russelii* 毒液 24h）

- **HMOX1 +3.05（p=0.0013）**——轴4 氧化应激最强命中；IL6 +2.10、SERPINE1 +2.07、HAVCR1 +0.99（肾损伤标志）、TNF/VCAM1/ICAM1 正向趋势；
- KDR −0.81（p=0.0017，最显著之一）——内皮修复/血管生成下调；
- 轴3 补体：CFH +1.08（p=0.095 趋势），C3 −0.59、CFI 无变化；
- 轴2：SERPINE1 上调（纤溶抑制方向，与 VICC 一致），FGA/FGG 转录下降（消耗或负相反应方向，ns）。

## 3. 对三条假说轴的判定（如实）

| 轴 | 直接靶点层（Phase 3/4） | GEO 转录组层 | 综合判定 |
|---|---|---|---|
| 轴1 血小板/vWF | 直接边（GP1BA、VWF 邻居） | 无转录变化 | 毒素直接作用层支持，继发转录层中性 |
| **轴2 凝血/纤溶** | **强支持（Hub+富集双平台）** | SERPINE1 ↑（纤溶抑制） | **全链条支持最强** |
| **轴3 补体** | 直接层 0 基因 | **CFB（人内皮，趋势）+ CFH（小鼠体内，趋势）** | **弱阳性**：补体既非毒素直接靶点，转录层亦仅旁路因子趋势——H2 需降格表述为"旁路补体可能参与"，不能作为主机制；如实写入 Discussion |
| **轴4 内皮/炎症/肾** | KDR 直接边 | **强支持（SELE/VCAM1/ICAM1/HMOX1/IL6 跨人/小鼠一致）** | **与轴2 并列最强** |

## 4. 结论

1. 毒素→凝血/纤溶（轴2）是主导机制，转录组层无矛盾；
2. 内皮炎症激活（轴4）在**人源内皮细胞**与**目标蛇种体内模型**中跨物种重复，成为第二支柱；
3. 补体（轴3）在三层证据中均缺直接支撑：无 L1/L2 边、富集驱动 0 基因、转录层仅 CFB/CFH 趋势——按 SOP 预定策略作为**阴性结果如实写入 Discussion**（H2 降格）；
4. HAVCR1（KIM-1，肾损伤标志）体内上调趋势为 AKI 表型提供了初步转录线索。

## 5. 产出文件

- `06_geo/GSE121297_deg_static_rcab_vs_ctrl.csv`（22,454 基因全表）、`GSE121297_watchlist.csv`
- `06_geo/GSE248215_deg_DR24h_vs_ctrl.csv`、`GSE248215_deg_DR24h_vs_DR1h.csv`
- `06_geo/geo_watchlist_combined.csv`（35 分子双数据集汇总）
- `06_geo/figure4_volcano.png`（Figure 4a/4b）、`figure4c_watchlist.png`（Figure 4c）
- 原始存档：系列矩阵 ×3、`gpl570_probe2symbol.csv`（61,013 探针映射）
- 可复跑脚本：`scripts/geo_gse121297.py`、`geo_figures.py`
- Excel：变更记录 v12

## 6. Limitations（写入论文）

样本量小（3v3、3v2 对照）、无蛇伤患者转录组（GEO 阴性结果）、NanoString Panel 仅 760 基因、小鼠肌肉/人脐静脉内皮与肾小球内皮存在组织外推距离、BH 校正下无 DEG 达 adj<0.05 故全部判读基于名义 p 值并标注探索性。
