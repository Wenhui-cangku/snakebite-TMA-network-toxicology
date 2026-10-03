# Phase 2 构建报告 —— 毒素–人靶点边表（L2 + L4）

日期：2026-09-24 ｜ 执行：Kimi ｜ 状态：**L2/L4 完成，L1 待手工导出，L3 暂缓**

## 1. 总览

| 证据层 | 边数 | 唯一靶点 | 状态 |
|---|---|---|---|
| L1 curated 数据库（CTD/T3DB/BindingDB） | 0 | — | ⏳ CTD 网站 ALTCHA 反爬，需手工导出后追加（同 Phase 1B 流程） |
| **L2 文献人工注释** | **49** | **15** | ✅ 完成 |
| L3 BLAST 同源（辅助） | 0 | — | ⏸ 本机无 blastp 二进制，暂缓；SOP 已注明仅作辅助证据 |
| **L4 STRING 邻居扩展** | **398** | **105** | ✅ 完成（15 靶点 × Top10，score≥0.7） |
| **合计** | **447** | 112 | 落在 SOP 预期 150–400 区间上沿（L4 全量保留所致） |

产出：`03_target_prediction/toxin_target_edges.csv`（447 行）、`phase2_string_neighbors.json`（邻居存档）、可复跑脚本 `scripts/build_phase2_edges.py`。

## 2. L2 文献层明细（49 边 / 15 靶点）

来源：UniProt/Swiss-Prot 审编注释 43 条结构化提取 + PubMed 定向补证 4 组。

### 按家族

| 家族 | L2 边 | 直接靶点 | QC（≥3） |
|---|---|---|---|
| SVMP/disintegrin | 11 | F10、F9、PROS1、FGA、FN1、COL4A1 | ✅ |
| snaclec/CTL | 7 | F10、F9、PROS1、GP1BA | ✅ |
| SVSP | 4 | F5、FGA、FGB | ✅ |
| PLA2 | 4（含 2 家族级） | F10 | ✅ |
| Kunitz | 19 | PLG、F11、F10、PROC、PRSS1、CTRB1 | ✅ |
| VEGF | 2 | KDR | — |
| NGF | 1（弱 0.5） | GP1BA（间接保护，By similarity） | — |

### PubMed 补证记录

- **PMID 27089306**：Daboxin P（印度 *D. russelii* 主要 PLA2）靶向 FX 抗凝 → 家族级边（未能对应到库内具体条目，score 0.6）；
- **PMID 21356226**：酸性 RVVA-PLA2-I（*D. russelii* 纯化）抗凝 → 家族级边（score 0.6）；
- **PMID 18554518 / 28042812**：daborhagin-M/K（= russelysin）水解纤维蛋白原 Aα 链、纤维连接蛋白、IV 型胶原 → B8K1W0（score 1.0）与 AAZ39880.1（同一蛋白，score 0.9）；
- **PMID 36423674**：SPAD-1（RVV 来源 HGD-disintegrin）破坏纤维连接蛋白/层粘连蛋白基质黏附 → 两条 disintegrin 家族级旁证边（score 0.6）；
- **PMID 37092784 / 28732041 / 21871889**：RVV-X 激活 FX 反应机制、RVV-V 底物特异性与结构基础 → 已回填对应边。

### 无靶点条目的处理（如实记录）

- **CRISP ×4**：无已审编人源靶点；serotriflin 结合蛇自身血清 SSP-2（PMID 18222185），非人靶点，不建边；
- **LAAO ×2**：经 H₂O₂ 生成影响血小板聚集（PMID 21802487），无单一蛋白靶点，不建边；
- **P31100（PLA2）**：功能为 RV-4 的伴侣/增效（毒液内互作），非人靶点，不建边；
- **snaclec Q4PRC6–9 / Q4PRD0**：注释仅为"干扰止血（泛述）"，无具体靶点，不建边。

## 3. L4 STRING 邻居层

- 对 L2 直接靶点（score≥0.8 的 15 个）逐一调 STRING `interaction_partners`（*H. sapiens*，combined score ≥0.7，Top 10），得 105 唯一邻居节点，挂到相应毒素边（`evidence_detail` 注明"经 ×× 靶点"）；
- 邻居含完整凝血级联扩展：F2、F3、F7、F8、F12、F2R、C4A/C4B/C4BPB、SERPINA 类、APOA/APOB 等。

## 4. 与疾病基因集的前瞻性核查（Phase 3 预演）

- **L2 直接靶点 15 个中 10 个落在疾病主集**：F10、F5、F11、FGA、PLG、PROC、PROS1、GP1BA、KDR、COL4A1；
- 不在主集 5 个：F9、FGB、FN1、PRSS1、CTRB1（F9/FGB/FN1 在宽集或六源未达阈值——Phase 3 时可作为"宽集回补"讨论点）；
- STRING 邻居 105 个中 **51 个在疾病主集**（含 F2、F3、F7、F8、F12 等核心凝血因子）；
- 四轴对照：轴1（GP1BA ✓、VWF 经 STRING 邻居 ✓）、轴2（F5/F10/PLG/PROC/PROS1 ✓）、轴4（KDR ✓）已有直接边；轴3（补体）目前仅经 STRING 邻居（C4A/C4B）——与 H2 预期一致，Phase 3 交集后重点解读。

## 5. 遗留事项

1. **L1**：CTD/T3DB/BindingDB 手工导出（参照 `02_disease_genes/手工导出指南.md` 流程），导出后追加 `evidence_type=ctdb/t3db` 边；
2. **L3**：BLAST+ 安装或改用 EBI 在线 BLAST 后补跑 `toxins_nr90.fasta` vs 人源蛋白质组（e-value<1e-3，仅辅助标注）；
3. PRISMA 图"韦恩交集 n=___"待 Phase 3 执行后回填。
