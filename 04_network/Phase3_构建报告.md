# Phase 3 构建报告 —— 交集、PPI 与拓扑分析

日期：2026-09-24 ｜ 执行：Kimi ｜ 状态：**完成（程序可复跑部分）；Cytoscape GUI 复核可选**

## 1. 韦恩交集（Figure 2a）

- 毒素预测靶点（L1+L2）**15** ∩ 疾病基因主集（六源）**1042** = **候选核心靶点集 n = 10**：
  COL4A1、F10、F11、F5、FGA、GP1BA、KDR、PLG、PROC、PROS1；
- 落选 5 靶点去向：FGB、FN1 在**宽集**（GC 104.7 / 107.2，未达主集阈值，可作敏感性回补）；**F9、PRSS1、CTRB1 六源完全未收录**（F9 与 TMA 病理关联弱属预期；PRSS1/CTRB1 为消化酶，与 TMA 无关，落选出库合理）；
- 图：`04_network/figure2a_venn.png`。

## 2. 扩展层（L4 敏感性层）

按 SOP 设计，主分析用 L1+L2；strict 核心仅 10 节点不足以支撑拓扑统计，故以 L4 STRING 邻居 ∩ 主集（51 节点）构建**扩展层 54 节点**作敏感性/拓扑分析层，全程与 strict 层分开标注。

## 3. STRING PPI（双阈值导出）

| 层 | score≥0.7 | score≥0.4（敏感性） |
|---|---|---|
| strict core10 | 14 边，孤立 2（COL4A1、KDR） | 26 边，孤立 0 |
| extended54 | **321 边，孤立 0** | 615 边，孤立 0 |

导出：`ppi_core10_score{400,700}.tsv`、`ppi_extended61_score{400,700}.tsv`。

## 4. Hub 基因（MCC ∩ Degree ∩ EPC 三榜 Top20，Python 复现 cytoHubba）

扩展层 54 节点 / 321 边上三算法 Top20 取交集，**Hub = 10**：

| 基因 | Degree | 层 | 四轴 |
|---|---|---|---|
| F2（凝血酶） | 25 | 扩展 | 轴2 |
| F3（组织因子） | 22 | 扩展 | — |
| PLG（纤溶酶原） | 21 | strict | 轴2 |
| PROC（蛋白C） | 18 | strict | 轴2 |
| ALB（白蛋白） | 17 | 扩展 | —（STRING 通用枢纽伪迹，如实记录） |
| F8 | 16 | 扩展 | — |
| FGA | 16 | strict | 轴2 |
| F10 | 15 | strict | 轴2 |
| F7 | 14 | 扩展 | — |
| F5 | 14 | strict | 轴2 |

- 技术说明：EPC 在本稠密网络上区分度低（p=0.5 渗透下所有节点同属大连通分量，得分趋同），三榜交集实际由 MCC/Degree 主导——与 cytoHubba 在凝血级联这类稠密子网上的行为一致，Methods 中如实注明；
- 图：`04_network/figure2b_ppi.png`（54 节点，Hub 橙 / strict 核心绿，结构上凝血簇、血小板簇 GP1BA–GP6–GP9–ITGA2B/ITGB3–VWF、VEGF 簇、补体 C4A/C4B/C4BPB 簇清晰可辨）。

## 5. 四轴映射与 QC 核查点（H1/H2 检验）

| 核查分子 | 位置 | 说明 |
|---|---|---|
| **F10** | strict 核心 + Hub | ✅ 直接命中（RVV-X / 抗凝 PLA2 双通路） |
| **F2** | Hub（扩展层） | ✅ 凝血酶，经 STRING 邻居入榜 |
| VWF | 扩展层（未入 Hub） | 血小板簇内，非拓扑中心 |
| GP1BA | strict 核心（未入 Hub） | 轴1 直接靶点 |
| KDR | strict 核心（未入 Hub） | 轴4 直接靶点（VEGF 簇） |
| ADAMTS13 / C3 / VCAM1 | 缺失 | **非毒素直接靶点层**——无任何 L1/L2 边连接，属预期内阴性 |

**如实结论**：SOP 质控点提示"ADAMTS13/VWF/F2/F10/C3/VCAM1 全部缺失 = 交集过窄"——本结果中 F2/F10 命中、VWF 在扩展层、ADAMTS13/C3/VCAM1 缺失。该缺失**不是阈值问题而是分层设计的直接体现**：L2 层仅含 15 个已实验报道的直接靶点，补体（轴3）与 ADAMTS13 的受累按 H2 假说本就是**宿主继发反应**而非毒素直接切割对象，应由 Phase 4 富集层（补体通路显著性）而非直接边层检验。此解读写入 Discussion；同时 FGB/FN1 宽集回补版本可作为敏感性分析。

## 6. 产出文件

- `04_network/figure2a_venn.png`（Figure 2a）、`figure2b_ppi.png`（Figure 2b）
- `04_network/ppi_{core10,extended61}_score{400,700}.tsv`（4 个 PPI 表）
- `04_network/hub_genes.csv`（Hub 10 + 三算法得分 + 四轴）
- `04_network/phase3_topology.json`（三榜完整 Top20）
- 可复跑脚本：`scripts/build_phase3.py`、`redraw_fig2a.py`、`draw_fig2b.py`
- Excel：新增 "Hub基因" sheet + 变更记录 v10

## 7. 遗留

1. Cytoscape 3.10 GUI 复核（cytoHubba/MCODE 官方实现）——手工步骤，随时可做；~~四层异质网络 SVG 主图~~ 素材已备（2026-09-30：`04_network/cytoscape/` 下 cyjs/nodes.csv/edges.csv + 导入样式指南，30 节点 49 边，GUI 打开导出 SVG 即可）；
2. PRISMA 图交集 n 已可回填 10；
3. Phase 4：Hub 10 + strict 核心 10 做 Metascape / clusterProfiler 富集，四轴着色与先验通路检验表。
