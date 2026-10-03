# Phase 1B 构建报告：疾病基因集（v1）

**执行日期**：2026-09-22　**对应方案**：v2 修正版 §2.4 + SOP Phase 1B

## 1. 流程计数（PRISMA 基因线）

| 步骤 | n |
|---|---|
| Open Targets 检索（8 个 MONDO 疾病条目：TMA、TTP×3、aHUS×3、HUS；score≥0.05） | 2014 条记录 → 741 唯一基因 |
| DISEASES knowledge（curated 渠道）补充 | 15 个核心基因（补体 CFH/CFI/CFB/C3/CD46/CFHR1/3/5、THBD、DGKE、ADAMTS13 等，全部已被 OT 覆盖或并入） |
| mygene 标准化映射（symbol→UniProt AC，人源） | 724/741 映射成功 |
| 合并去重 | **741** |
| 四轴先验分子强制纳入（数据库未收录） | +9（F2、F5、F10、FGG、PROC、VCAM1、ICAM1、SELE、HAVCR1） |
| **最终疾病基因集** | **750（主集 456 / 宽集 294）** |

主集定义（替代 GeneCards 阈值的固化规则）：DISEASES curated ∪ OpenTargets score≥0.3 ∪ 出现于≥3个疾病条目 ∪ 四轴先验分子。

## 2. 来源可用性实况与处理（写入 Methods）

| 计划来源 | 实况（2026-09-22 实测） | 处理 |
|---|---|---|
| GeneCards | 反爬 403，无法程序化抓取 | 手工导出指南已出（见 `手工导出指南.md`），导出后分数补填进总表 |
| DisGeNET | API 401，需注册 API Key | 同上，待用户注册后补跑 |
| OMIM | API 需 Key | 以 DISEASES curated（UniProtKB-KW/MedlinePlus 渠道）替代覆盖核心遗传关联 |
| CTD | 新站启用 ALTCHA 人机验证，批量接口被封 | 手工导出指南已出 |
| **Open Targets**（替代主来源） | ✅ 免费 GraphQL API | 主来源，含 ClinGen/Gene2Phenotype/ClinVar/GWAS 等证据 |
| **DISEASES knowledge**（JensenLab） | ✅ 免费下载 | curated 核心集 |

## 3. 质控核查

- 四轴先验分子 **27/27 在主集**（轴1 5/5、轴2 8/8、轴3 6/6、轴4 8/8）✓
- 人源限定 ✓（mygene species=human）
- 双来源交叉：OT 宽集（敏感性分析用 294）与主集分层明确 ✓

## 4. 注意点

1. "snakebite envenoming / VICC" 在所有疾病库中**均无条目**（2026-09-22 实测）——蛇伤相关基因需靠 Phase 2 毒素–靶点层覆盖，论文 Methods 中如实说明；
2. GeneCards/DisGeNET/OMIM/CTD 的手工导出完成前，主集规则以上述替代阈值为准；导出完成后将分数补填并做阈值敏感性分析；
3. 主集 456 个基因规模适中，预期与毒素靶点交集数十至百余个（Phase 3）。

## 5. 产出文件

- `02_disease_genes/disease_gene_master.csv`（750 行，含分层、四轴归属、溯源备注）
- `02_disease_genes/opentargets_raw.csv`（2014 条原始记录）
- `02_disease_genes/diseases_knowledge_full.tsv`（DISEASES 全量存档）
- `02_disease_genes/手工导出指南.md`

## 6. GeneCards 手工导出并入记录（2026-09-22 13:52，v2 定稿）

用户完成 GeneCards 六词手工导出（浏览器 Export），已按固化阈值并入：

| 检索词 | 命中 n | 逐词中位数阈值 | ≥10 条数 |
|---|---|---|---|
| thrombotic microangiopathy | 515 | 1.39 | 52 |
| atypical hemolytic uremic syndrome | 960 | 113.85 | 959 |
| thrombotic thrombocytopenic purpura | 637 | 47.79 | 624 |
| microangiopathic hemolytic anemia | 468 | 107.24 | 466 |
| snakebite envenoming | 55 | 20.40 | 37 |
| venom-induced consumption coagulopathy | 39 | 46.30 | 38 |

- GeneCards 唯一基因 1356，达主阈值（≥逐词中位数）698；新增并入 1075 条；
- **终版总表：1825 基因（主集 1037 / 宽集 788）**，主集 = GeneCards≥逐词中位数 ∪ OT score≥0.3 ∪ ≥3 疾病 ∪ DISEASES curated ∪ 四轴先验；
- 注意：TMA 词条命中宽泛（中位数仅 1.39），而 aHUS/TTP 词条命中集中（中位数 >40）——逐词中位数策略自动适配了这种词间尺度差异，优于固定 ≥5 阈值（佐证修正点 4 的必要性）；
- snakebite envenoming 在 GeneCards 有 55 条命中（OT/MedGen 均无）——蛇伤特异基因（如蛇毒血清耐药、蜂/蛇毒反应相关基因）由此进入宽集；
- 剩余待补：DisGeNET（API Key）、OMIM（API Key）、CTD（浏览器手工导出），补全后做阈值敏感性分析（见 `手工导出指南.md`）。

**产出文件更新**：`disease_gene_master.csv`（1825 行）、Excel 管理表 1825 行 + 变更记录 v5、`PRISMA_flowchart_phase1_filled.png`（终版）。

## 7. DisGeNET API 并入记录（2026-09-22 14:35，用户提供 Key）

- 学术账号限 CURATED 来源（CLINGEN/CLINVAR/ORPHANET/UNIPROT 等 10 库）——恰为最高证据等级；
- 疾病 CUI 经标志基因反查解析：主条目 C2717961（TMA）、C0034155（TTP）、C2931788（aHUS）、C0019061（HUS）+ 12 个亚型条目；参数格式 `disease=UMLS_<CUI>`；
- 16 个疾病条目 score≥0.1 共得 **46 唯一基因，全部已在现有总表内**（与 GeneCards/OT 交叉印证，无新增孤儿基因），其中 2 条（DisGeNET≥0.3）提升入主集；
- 定稿：**总 1825 | 主集 1039 | 宽集 786**；
- snakebite/VICC 在 DisGeNET 亦无条目（与 OT/MedGen 一致），蛇伤层由 Phase 2 毒素–靶点覆盖；
- 剩余待补：OMIM（API Key）、CTD（浏览器手工导出）。

## 8. CTD 手工导出并入记录（2026-09-22 14:51，终版定稿）

用户完成 CTD batch query 六词手工导出（网站 ALTCHA 人机验证无法程序化），已并入：

| 检索词 | 原始行 | 白名单行 | 唯一基因 | direct 基因 | 备注 |
|---|---|---|---|---|---|
| atypical hemolytic uremic syndrome | 319 | 319 | 319 | 9 | 精确命中 MeSH 条目 |
| microangiopathic hemolytic anemia | 320,875 | 220,541 | 26,812 | 31 | CTD 词扩展至 54 个疾病，已按白名单过滤 |
| snakebite envenoming | 64 | 64 | 57 | 0 | 命中 Snake Bites (MeSH D012909)，经 Bungarotoxins/Glutamine 推断 |
| thrombotic microangiopathy | 120,692 | 91,269 | 20,340 | 20 | 扩展 7 疾病，白名单过滤 |
| thrombotic thrombocytopenic purpura | 31,829 | 31,829 | 16,708 | 4 | — |
| venom-induced consumption coagulopathy | — | — | 0 | 0 | **CTD 无此条目（[Object not found]），如实记录** |

**并入规则（固化，防词扩展噪声）：**

1. **疾病白名单**：仅保留 Snake Bites / aHUS / HUS / TTP(含 acquired) / Thrombotic Microangiopathies / Anemia, Hemolytic——CTD 会把 MAHA/TMA 词扩展到镰贫、地贫、先天性溶贫、ITP 等无关疾病（其 direct 基因如 HBB 类、CDAN1 等 22 条已剔除，防止假性主集污染）；
2. DirectEvidence 非空（marker/mechanism、therapeutic）→ **纳入主集**；白名单内 direct 共 80 唯一基因，其中 77 已在库（交叉印证），新增 3 条（EIF2AK1、GCLC、ITPA，均经 mygene 映射 UniProt）；
3. 仅 InferenceScore（化学品推断）→ 阈值 **≥50** 进宽集（MAHA 词 631 基因达线、TMA 词 29 达线，新增 349）；**snakebite envenoming 词例外全量收录**（仅 57 基因、最高 8.85 分，但为唯一直接命中蛇咬 MeSH 的来源，新增 13）；
4. `CTD inference` 列格式：`direct:marker/mechanism` 或 `inferred:<最高分>`；已有基因回填注释 1,770 条；
5. CTD 推断层含啮齿动物源基因（如 ABCB1A、TRP53、NACHRALPHA 系列）——13 条 mygene 人源映射失败已注记，Phase 2 交集时自动以人源 UniProt 为准过滤。

**四轴先验 27/27 全部获 CTD 证据**：direct 9 条（ADAMTS13、C3、CD46、CFB、CFH、CFI、HMOX1、IL6、TNF），其余 18 条 inferred 6.2–87.5 分（最高 ICAM1 87.48、SERPINE1 83.93、VCAM1 82.92）。

**定稿：总 2,190 基因 | 主集 1,042 | 宽集 1,148**；PRISMA B 线已同步重画。

**产出文件更新**：`disease_gene_master.csv`（2,190 行）、`ctd_merge_summary.json`、Excel 管理表 2,190 行 + 变更记录 v7、`scripts/merge_ctd.py`（可复跑）。

## 9. OMIM API 并入记录（2026-09-24 12:20，用户提供 Key）

- 5 个疾病词（aHUS / HUS / TTP / TMA / MAHA）`entry/search` 得 44 个唯一 MIM 条目，批量 `entry?include=geneMap` 抓取后按**表型白名单**保留 14 个条目（AHUS1–8、TTP 274150、CFHD、CFID、CD59 介导溶贫、cblC、cblG），剔除检索噪声（Aicardi-Goutières、黄斑变性易感、免疫缺陷等 12 条——OMIM 同样存在词扩展陷阱，与 CTD 处理逻辑一致）；
- 全部关联为 **mappingKey = 3（分子基础已知，OMIM 最高证据等级）**，共 **15 唯一基因**：ADAMTS13、CFH、CFHR1、CFHR3、CD46、CFI、C3、CFB、THBD、DGKE、C1GALT1C1、CD59、MMACHC、PRDX1（双基因遗传）、MTR；
- **15/15 全部已在现有总表且全在主集**——与 GeneCards/OT/DISEASES/DisGeNET/CTD 六源交叉印证，无孤儿基因，主集规则稳健性再获验证；4 条此前缺 OMIM 标注的行已回填，全表 OMIM=有 共 16 条；
- snakebite envenoming / VICC 在 OMIM **检索 0 命中**（与 OT/DisGeNET/CTD 一致），蛇伤特异层继续由 Phase 2 毒素–靶点覆盖；
- 总数不变：**总 2,190 | 主集 1,042 | 宽集 1,148**。

至此 Phase 1B 六源全部并入完毕（GeneCards / Open Targets / DISEASES / DisGeNET / CTD / OMIM），疾病基因集终版锁定。

**产出文件更新**：`disease_gene_master.csv`（2,190 行）、`omim_search_mims.json`、`omim_entries_raw.json`、`omim_merge_summary.json`、Excel 管理表 + 变更记录 v8、`scripts/merge_omim.py`（可复跑）、PRISMA B 线源框已补 OMIM。
