# Phase 4 构建报告 —— 富集分析与四轴解读

日期：2026-09-24 ｜ 执行：Kimi ｜ 状态：**完成**

## 1. 方法

- 基因集 = Hub 10 ∪ strict 核心 10 = **15 唯一基因**（F2, F3, F5, F7, F8, F10, FGA, PLG, PROC, ALB, COL4A1, F11, GP1BA, KDR, PROS1）；
- 平台 1：**g:Profiler g:GOSt**（GO:BP/CC/MF + KEGG + Reactome，g:SCS 严格校正，替代 SOP 中 Metascape 手工上传）；
- 平台 2：**Enrichr**（KEGG_2021_Human / Reactome_2022 / GO_Biological_Process_2023，BH 校正，替代 clusterProfiler R 步骤）；
- 双平台取交集显著（FDR<0.05 均满足）为准，单平台条目单独标注。

## 2. 结果总览

- g:Profiler 显著 **116** 条（GO:BP 54 / GO:CC 26 / GO:MF 8 / KEGG 1 / REAC 27）；
- Enrichr 显著 **202** 条（GO:BP 124 / KEGG 6 / Reactome 72）；
- **双平台共同显著 9 主题**：Complement and coagulation cascades、Platelet activation、Fibrin Clot Formation（Common/Intrinsic/Extrinsic Pathway）、Hemostasis、Platelet degranulation、Gamma-carboxylation。

最强信号：REAC:R-HSA-140877 Formation of Fibrin Clot（p=9.7e-23，11/15 基因）；KEGG:04610（p=3.9e-18 / Enrichr adj=1.6e-22，双平台第一）。

## 3. 先验通路检验表（写入 Results）

| 先验通路 | g:Profiler | Enrichr | 结论 |
|---|---|---|---|
| **hsa04610 补体与凝血级联** | p=3.90e-18 ✓ | adj=1.63e-22 ✓ | **双平台显著 ✓✓** |
| **hsa04611 血小板激活** | REAC 等效 p=1.47e-07 ✓ | adj=1.45e-03 ✓ | **双平台显著 ✓✓** |
| ECM–receptor interaction | 未达 g:SCS | adj=1.81e-02 ✓ | 单平台 |
| Focal adhesion | 未达 g:SCS | adj=4.68e-02 ✓ | 单平台（边缘） |
| PI3K–Akt | 未显著 | adj=9.08e-02 | 不显著 |
| NF-κB | 未显著 | 无此条目 | **不显著** |
| Fluid shear stress & atherosclerosis | 未显著 | adj=1.52e-01 | 不显著 |

机器可读版：`prior_pathway_check.csv`。

## 4. H2 关键点（必须写进 Discussion 的如实发现）

**KEGG:04610 "Complement and coagulation cascades" 的 11 个驱动基因为 F2、F3、F5、F7、F8、F10、FGA、PLG、PROC、F11、PROS1——全部是凝血/纤溶臂，补体臂贡献为 0。** 也就是说：

1. 毒素**直接靶点层**（L1+L2，15 基因）完全是一个凝血/纤溶故事（Figure 3 全轴2 着色即直观证据）；
2. 补体（轴3）在直接层没有任何富集支撑——与 Phase 3 中 C3/ADAMTS13 不在直接靶点层一致；
3. H2（补体参与蛇伤 TMA）若成立，其作用层级是**宿主继发反应**，需靠 GEO 转录组验证层（GSE121297/GSE248215 中补体基因差异表达）而非毒素-靶点直接边来证明——这正好构成三重验证设计的逻辑闭环；
4. NF-κB / PI3K–Akt / 流体剪切（轴4 炎症-内皮维度）在 15 基因核心集上不显著，如实记录；这些维度同样留给转录组与临床一致性层检验。

## 5. 产出文件

- `05_enrichment/figure3_enrichment_bubble.png`（Figure 3，按驱动基因四轴着色 + KEGG:04610 注释）
- `05_enrichment/gprofiler_raw.csv`（116 条）、`enrichr_raw.csv`（全量）、`enrichment_gprofiler_sig116.csv`、`enrichment_enrichr_sig.csv`（202 条）
- `05_enrichment/prior_pathway_check.csv`（先验通路检验表）
- 可复跑脚本：`scripts/build_phase4.py`
- Excel：新增 "Phase4富集" sheet + 变更记录 v11
