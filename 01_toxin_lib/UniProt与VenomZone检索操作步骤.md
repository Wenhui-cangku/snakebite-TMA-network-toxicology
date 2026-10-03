# Phase 1 操作手册（一）：UniProt 与 VenomZone 检索具体步骤

> 对应方案 v2 修正版 Phase 1（第 2–3 周）1A 毒素成分库构建。
> 检索式与命中数已于 **2026-09-22 实测验证**；输出文件统一存入 `snakebite_TMA/01_toxin_lib/`。

---

## 一、UniProt 检索（毒素序列主来源）

### 1.1 检索式（已固化，网页版与 API 通用）

| 蛇种 | 检索式 | 实测命中（2026-09-22） |
|---|---|---|
| 罗素蝰 *Daboia russelii* | `(organism_name:"Daboia russelii") AND (keyword:"Toxin") AND (reviewed:true)` | **52 条**（reviewed）；去掉 reviewed 过滤为 89 条 |
| 暹罗罗素蝰 *Daboia siamensis* | `(organism_name:"Daboia siamensis") AND (keyword:"Toxin") AND (reviewed:true)` | **28 条**（reviewed）；去掉 reviewed 过滤为 39 条 |

**原则**：主库以 reviewed（Swiss-Prot 人工审编）条目为准；unreviewed（TrEMBL）条目仅经 VenomZone/文献核对确证为真实毒液成分后才补充纳入（在数据管理表"来源"列标注）。

> ⚠️ **实测发现（2026-09-22，必须执行补充检索）**：`keyword:"Toxin"` 检索会**漏收整个 Kunitz 抑制剂家族**（两蛇种共 24 条 reviewed Kunitz 条目未挂该关键词），CRISP 全长序列也仅存在于 unreviewed。因此主检索后必须追加执行补充检索式：
> - `(organism_name:"Daboia russelii") AND (protein_name:"Kunitz") AND (reviewed:true)` → 24 条
> - `(organism_name:"Daboia russelii") AND (protein_name:"cysteine-rich") AND (length:[200 TO 300])` + 按登录号取 A0A223PK22、A0A223PK48（serotriflin）→ CRISP 全长 4 条（unreviewed，标注待核对）

### 1.2 网页版点击级步骤（推荐首次执行用）

1. 打开 https://www.uniprot.org/ ，点击检索框左侧 **"Advanced"**（高级检索）。
2. 在高级检索框中**整段粘贴** 1.1 中对应蛇种的检索式（含括号与引号），点击 Search。
3. 结果页左侧确认 **Reviewed** 过滤器已勾选（检索式中已含 `reviewed:true`，此处应自动选中，显示 52 / 28 条）。
4. 点击结果表上方的 **"Customize columns"**，确保勾选以下字段后保存：
   - Entry、Entry Name、Protein names、Gene Names、Organism、Length
   - **Structure** 下的 PDB、AlphaFoldDB（用于 Phase 5 结构可用性判断）
   - Function [CC]、Caution [CC]（注释文本）
5. 点击 **"Download"** 按钮，分两次导出：
   - 格式 **FASTA (canonical)** → 命名 `01_toxin_lib/uniprot_russelii_reviewed.fasta`（或 `..._siamensis_reviewed.fasta`）；
   - 格式 **TSV**（勾选"下载全部自定义列"）→ 命名 `uniprot_russelii_reviewed.tsv`。
6. 在页面记录右上角结果总数，填入数据管理表 `data_management_table.xlsx` 的"下载日期"与备注列；同时填入 PRISMA 流程图模板第一层 n 值。
7. 换第二个蛇种检索式，重复 2–6。

### 1.3 API 脚本版（用于可重复性存档，与网页版结果应完全一致）

```bash
# 罗素蝰 reviewed 毒素 → FASTA
curl -s "https://rest.uniprot.org/uniprotkb/stream?query=(organism_name%3A%22Daboia%20russelii%22)%20AND%20(keyword%3A%22Toxin%22)%20AND%20(reviewed%3Atrue)&format=fasta" \
  -o snakebite_TMA/01_toxin_lib/uniprot_russelii_reviewed.fasta

# 暹罗罗素蝰 reviewed 毒素 → FASTA
curl -s "https://rest.uniprot.org/uniprotkb/stream?query=(organism_name%3A%22Daboia%20siamensis%22)%20AND%20(keyword%3A%22Toxin%22)%20AND%20(reviewed%3Atrue)&format=fasta" \
  -o snakebite_TMA/01_toxin_lib/uniprot_siamensis_reviewed.fasta

# 注释表（TSV，含 PDB/AFDB 结构列）
curl -s "https://rest.uniprot.org/uniprotkb/stream?query=(organism_name%3A%22Daboia%20russelii%22)%20AND%20(keyword%3A%22Toxin%22)%20AND%20(reviewed%3Atrue)&format=tsv&fields=accession,id,protein_name,gene_names,organism_name,length,xref_pdb,xref_alphafolddb,cc_function" \
  -o snakebite_TMA/01_toxin_lib/uniprot_russelii_reviewed.tsv
```

**质控点**：① FASTA 条目数 = 检索页显示总数（52 / 28）；② 网页版与 API 版同日执行、数量一致；③ 若不一致以 API 为准并记录差异。

### 1.4 条目归类预判（供家族分类对照）

罗素蝰毒液五大家族在检索结果中的典型 Entry Name 关键词，Phase 1 家族分类时按此快速归组：

| 家族 | Entry Name / 蛋白名关键词 |
|---|---|
| SVMP（金属蛋白酶） | `VMP*`、metalloproteinase、disintegrin（P-II 类常单独成条）、RVV-X 重链 |
| SVSP（丝氨酸蛋白酶） | `VSP*`、thrombin-like enzyme、serine protease |
| PLA2（磷脂酶 A2） | `PA2*`、phospholipase A2 |
| snaclec / CTL | `SL*`、snaclec、C-type lectin |
| Kunitz 抑制剂 | `VK*`、Kunitz-type、textilinin 类 |
| 其他 | LAAO（`OXLA`）、5′-核苷酸酶、CRISP（`CRIS*`）、VEGF（`VGFF*`）、透明质酸酶 |

---

## 二、VenomZone 检索（审编核对与补充来源）

> VenomZone（https://venomzone.expasy.org/ ，SIB 维护）是 UniProtKB/Swiss-Prot **Tox-Prot** 知识库的专题门户，条目与 UniProt 同源。它的作用不是批量下载，而是：① 按分类/家族**核对** UniProt 检索是否漏条目；② 发现 reviewed 之外但经专家审编的毒液成分；③ 提供毒素家族归类与分子靶点注释（可直接用于 Phase 2 文献证据层）。

### 2.1 点击级步骤

1. 打开 https://venomzone.expasy.org/ ，首页选择 **"Snakes"（蛇类）**入口。
2. 在分类树中逐级展开：**Viperidae（蝰科）→ Daboia（圆斑蝰属）**，分别进入 *Daboia russelii* 与 *Daboia siamensis* 物种页。
   - 替代路径：首页搜索框直接输入 `Daboia russelii` 或 `Daboia siamensis`。
3. 物种页按**蛋白家族/活性**分组展示该蛇种的全部审编毒素条目。逐家族核对：
   - 条目数与 UniProt reviewed 结果（52 / 28）是否一致；
   - 发现 UniProt 检索未覆盖的条目（VenomZone 偶有条目未挂 "Toxin" 关键词标签）时，**点击条目进入详情页，记录其 UniProt 登录号（AC）**，列入补充清单。
4. 逐条阅读详情页的 **"Molecular targets / Function"** 注释：将已实验报道的宿主靶点（如 RVV-X→凝血因子 X）直接摘录到 Phase 2 证据表草稿（`03_target_prediction/literature_evidence_draft.csv`，列：toxin_ac / target / evidence / PMID），此步可显著减少 Phase 2 文献挖掘工作量。
5. VenomZone 无批量 FASTA 导出功能——补充条目的序列通过 **UniProt ID 映射**批量取回：
   - 打开 UniProt 首页 → 检索框下方 **"ID Mapping"**（网址 https://www.uniprot.org/id-mapping ）；
   - 粘贴补充清单的全部 AC → From: `UniProtKB AC/ID`，To: `UniProtKB` → 导出 FASTA + TSV，命名 `venomzone_supplement.fasta/.tsv`。
6. 将核对结果填入数据管理表：每条目"来源"列标注 `UniProt reviewed` 或 `VenomZone 补充`；核对日期记入"下载日期"列。

### 2.2 质控点

- VenomZone 物种页条目数 ≥ UniProt reviewed 数为正常；若显著更少，检查 VenomZone 是否将部分条目归在亚种名（如 *Daboia russelii russelii* / *D. r. siamensis* 历史命名）下——在分类树中同时检查亚种层级；
- 每个五大家族（SVMP/SVSP/PLA2/snaclec/Kunitz）在两库中都必须有代表条目，缺失家族立即回查检索式；
- VenomZone 的分子靶点注释是 Phase 2 **最高证据等级（curated）**来源，摘录时务必连同 PMID 一起记录。

---

## 三、本步骤完成标准（2026-09-22 已执行核对，全部通过 ✓）

| 检查项 | 标准 | 实际状态 |
|---|---|---|
| FASTA 文件 | 主检索 + 补充检索 FASTA 均已生成 | ✅ `uniprot_russelii_reviewed1.fasta`（52）、`uniprot_russelii_reviewed2.fasta`（28，完全重叠于前者）、`supp_kunitz.fasta`（24）、`supp_crisp.fasta`（5，含 1 重复 AC）、`supp_svmp_ncbi.fasta`（3）、`supp_venomzone_check.fasta`（1） |
| 注释表 | 对应 TSV 齐全，含长度与 PDB/AFDB 结构列 | ✅ 5 个 TSV 齐全，结构列均在 |
| 合并去重 | 合并为 `all_toxins_raw.fasta`，总条数 = 各文件之和 − 重复，无重复 AC | ✅ 79 条唯一（52+24+4+3+1，重叠 28 已去重） |
| 数据管理表 | 每条目来源、下载日期已填写；PRISMA 模板 n 值已填 | ✅ 毒素管理表 63 行（下载日期 2026-09-22）；`PRISMA_flowchart_toxin_filled.png` 已填实测计数 |
| VenomZone 交叉核对 | 与 Tox-Prot 审编口径比对，漏收条目补入 | ✅ 71 条比对：唯一全长漏收 P86368 已补；20 条短肽差异属设计性剔除 |
| 证据草稿 | `literature_evidence_draft.csv` 已含 VenomZone 摘录的分子靶点条目 | ✅ 62 条（43 条含靶点相关功能注释，均附 PMID） |

> 以上自查已于 2026-09-22 全部通过后执行去冗余：90% 一致性聚类（CD-HIT 等价算法）→ `toxins_nr90.fasta`（40 簇代表序列），入库毒素总表 63 条（详见 `Phase1A_构建报告.md` §1/§6/§7）。
