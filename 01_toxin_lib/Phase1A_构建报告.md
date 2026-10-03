# Phase 1A 构建报告：毒素成分库（v1）

**执行日期**：2026-09-22　**对应方案**：v2 修正版 Phase 1 + 操作手册（一）
**脚本**：`snakebite_TMA/scripts/build_toxin_lib.py`（可重复执行）

## 1. 流程计数（PRISMA 毒素线，可直接填入流程图）

| 步骤 | n |
|---|---|
| UniProt 主检索（keyword:"Toxin"，reviewed；两蛇种） | 52（含 *D. siamensis* 28 + *D. russelii* 24；检索词通过同义词自动覆盖两蛇种） |
| 用户第二次导出（*D. siamensis* 单独） | 28（与主检索完全重叠） |
| **补充检索 1**（见 §2 重要发现）：Kunitz reviewed + CRISP 全长 | 24 + 4 |
| **补充检索 2**（SVMP 回补）：russelysin（GenBank AAZ39880）+ disintegrin ×2 | 3 |
| 合并去重（按 UniProt AC / GenBank 登录号） | **78** |
| 剔除 <30 aa 片段化序列 | −16（多为 Kunitz/CRISP 的短片段条目，如 P85039/40/41、P86537） |
| 排除 ADAM 样宿主蛋白（A0A223PK09/14/28/29 等，转录组注释的宿主 ADAM，非毒液 SVMP） | 已排除（未入库） |
| 片段剔除后入库 | **62** |
| 90% 一致性聚类（CD-HIT 等价贪心算法） | **40 个簇**（代表序列 40 条，`toxins_nr90.fasta`） |

## 2. 重要方法学发现（写入论文 Methods/手册更新）

> **UniProt `keyword:"Toxin"` 检索会漏收 Kunitz 抑制剂家族**——两个蛇种的 24 条 reviewed Kunitz 型丝氨酸蛋白酶抑制剂（BPTI/DrKIn/RVV-II 系列）均未挂 "Toxin" 关键词标签；CRISP 家族亦仅有短碎片。已按手册质控规则（五大家族必须齐全）执行补充检索式：
> `(organism_name:"Daboia russelii") AND (protein_name:"Kunitz") AND (reviewed:true)` 及 CRISP 全长条目（F2Q6F2/F2Q6F3/A0A223PK22/A0A223PK48，其中 CRISP 全长为 unreviewed，已在总表"来源"列标注"待 VenomZone/文献核对"）。
> 该发现同时验证了 VenomZone 交叉核对步骤的必要性。

## 3. 最终毒素库构成（62 条，40 簇）

| 毒素家族 | 条数 | 说明 |
|---|---|---|
| Kunitz 抑制剂 | 21 | DrKIn-I/II、BPTI 系列、RVV-II 等 |
| PLA2 | 15 | 酸性/碱性 svPLA2（Drk-a1、DsM 系列） |
| snaclec/CTL | 8 | 含 RVV-X 轻链 1/2（Q4PRD1/Q4PRD2）、dabocetin 等 |
| SVMP/disintegrin | 5 | **RVV-X 重链（Q7LZ61）、daborhagin-K（B8K1W0）、russelysin（AAZ39880）、disintegrin ×2** |
| SVSP | 4 | 凝血酶样酶、因子 V 激活剂 RVV-Vα 等 |
| CRISP | 4 | 含 serotriflin（unreviewed，待核对） |
| LAAO / VEGF / NGF | 2 / 2 / 1 | |

物种分布：*D. siamensis* 38 条、*D. russelii* 24 条。
结构可用性：PDB 有 11 条、AlphaFold 模型 48 条、无结构 3 条（Phase 5 按 pLDDT>70 规则处理）。
**丰度权重已回填**（家族级，Tan et al. 功能毒液蛋白质组，斯里兰卡 *D. russelii*：PLA2 35.0%、snaclec 22.4%、SVSP 16.0%、SVMP 6.9%、LAAO 5.2%、Kunitz 4.6%、NGF 3.5%、CRISP 2.0%）[Source: Monash/Tan et al. functional venomics, 经 WebSearch 核实，2026-09-22]。

## 4. SVMP 回补结论（原阻塞项已解除）

- UniProt reviewed 的罗素蝰 SVMP 仅 2 条全长（RVV-X 重链、daborhagin-K）——经 NCBI Protein 回补 russelysin（615 aa 出血性 P-III SVMP）与 2 条 disintegrin（110 aa），SVMP/disintegrin 达 5 条，足以支撑对接矩阵的 SVMP×{ADAMTS13, VWF-A1, FGA} 与阳性对照 RVV-X–FX；
- 文献佐证：亚洲 *Daboia* 毒液 SVMP 丰度 2.5–22%（地理变异），其中绝大部分为 RVV-X 类 P-III SVMP——本库构成与该文献图景一致；ADAM 样宿主蛋白（转录组注释污染）已排除并记录排除理由；
- RVV-X 轻链（snaclec）2 条已在库内（Q4PRD1/Q4PRD2），RVV-X 异源三聚体三条链均已覆盖。

## 5. 产出文件清单

| 文件 | 内容 |
|---|---|
| `01_toxin_lib/toxin_master_table.csv` | 毒素总表 v2（62 行 × 14 列，含家族/聚类/结构状态/丰度权重） |
| `01_toxin_lib/all_toxins_raw.fasta` | 合并去重原始序列（78 条） |
| `01_toxin_lib/toxins_nr90.fasta` | 90% 聚类代表序列（40 条，后续对接用） |
| `01_toxin_lib/uniprot_supplement_kunitz_crisp.tsv` 等 | 补充条目注释表 |
| `00_protocol/data_management_table.xlsx` | 毒素管理表已填实 59 行，变更记录已追加 |
| `scripts/build_toxin_lib.py` | 全流程可重复脚本 |

## 6. 收尾核对记录（2026-09-22，对照操作手册 §1.2–1.4）

| 核对项 | 结果 |
|---|---|
| ① FASTA 条目数 vs 检索页总数 | 文件1 = 52 ✓；文件2 = 28 ✓；文件2 完全重叠于文件1（28/28）✓；`all_toxins_raw.fasta` = 78 条唯一 ✓；`toxins_nr90.fasta` = 40 条 = 簇数 ✓ |
| ② 网页版 vs API 一致性 | 用户网页下载（52/28）与 API 实测（52/28）同日一致 ✓ |
| ③ FASTA vs TSV 元数据 | 唯一无 TSV 元数据条目为 AAZ39880.1（GenBank russelysin，预期内，来源已标注）✓ |
| ④ 家族归类 vs §1.4 关键词表 | Entry 前缀与预判模式全部吻合：Kunitz→`VKT*`、PLA2→`PA2*`、SVSP→`VSP*`、snaclec→`SL*`、SVMP→`VM3DK`+russelysin、LAAO→`OXLA`、VEGF→`TXVE`、NGF→`NGFV`、CRISP→登录号补充 ✓ |
| 数据管理表 | 毒素管理表 62 行已填实（含下载日期 2026-09-22、来源、备注）；变更记录 v1/v2 已追加 ✓ |
| PRISMA 流程图 | 实测计数版已生成：`00_protocol/PRISMA_flowchart_toxin_filled.png`（图 S0-2）✓ |

## 7. VenomZone 交叉核对记录（2026-09-22，操作手册 §2）

**方法**：VenomZone 物种页为 JS 动态渲染无法直接抓取，改用其首页公开的等效权威检索式（Tox-Prot 审编口径）：`taxonomy_id:{8707/343250} AND (cc_tissue_specificity:venom) AND reviewed:true`，与本库逐 AC 比对。

| 核对项 | 结果 |
|---|---|
| VenomZone 口径 reviewed 毒液条目 | 71 条（D. russelii 33 + D. siamensis 38） |
| 本库缺失 | 21 条 → 其中 **20 条为 10–25 aa 短肽测序证据条目**（P86529–P86537、P85039–42 等，属 <30 aa 设计性剔除，不算漏收）；**唯一全长漏收 P86368（碱性 PLA2-3，121 aa）已补入** |
| 本库多出（reviewed） | 7 条：snaclec 3–7（Q4PRC6–9、Q4PRD0，挂 Toxin 关键词但无 venom 组织注释）——保留，属合理扩收 |
| 五大家族两库覆盖 | 齐全 ✓ |
| 亚种层级核查 | D. siamensis 历史上为 D. russelii siamensis，UniProt organism_name 检索已通过同义词自动覆盖 ✓ |
| 靶点注释摘录（步骤③） | 已从 UniProt 全文解析 62 条目的 FUNCTION 注释与 PMID：43 条含靶点相关功能描述 → `03_target_prediction/literature_evidence_draft.csv`（Phase 2 curated 证据起点） |

**结论**：本库与 VenomZone/Tox-Prot 审编口径一致性通过核对；最终总库 **63 条 / 40 簇**。
