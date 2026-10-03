# GEO 前置侦察报告

**执行日期**：2026-09-04　**执行人**：课题 Phase 0
**检索渠道**：NCBI GEO DataSets（E-utilities: esearch/esummary，db=gds）+ GEO 记录页人工核对
**目的**：为 Phase 6"转录组干法验证"提前锁定可用数据集；若无直接数据集则启用替代策略（对应方案 v2 表 3 难点 9）。

---

## 1. 检索式与命中量

| 编号 | 检索式（db=gds） | 命中 GSE 数 |
|---|---|---|
| Q1 | `(snakebite OR envenoming OR "snake bite") AND "Homo sapiens"[Organism] AND gse[ETYP]` | 3 |
| Q2 | `("snake venom" OR viper OR Daboia OR Bothrops OR Echis OR Crotalus) AND (endothelial OR HUVEC OR kidney OR renal OR fibroblast) AND gse[ETYP]` | 3 |
| Q3 | `("snake venom" OR envenomation) AND (transcriptome OR "expression profiling") AND gse[ETYP]` | 3 |

去重后候选 8 条，逐条人工评估（esummary + 样本级 GSM 标题核对），剔除 4 条无关记录（580 物种甲基化图谱 GSE195869、胶质母细胞瘤药物试验 GSE186332、蛇毒腺类器官 GSE129581、寄生蜂毒腺 GSE76257）。

## 2. 核心结论

> **截至 2026-09-04，GEO 中不存在蛇伤患者外周血/肾脏转录组数据集，亦无蛇毒刺激肾小球内皮细胞数据集。**
> 该阴性结果本身可写入论文 Limitations（呼应方案表 3 难点 9）。按预案启用替代策略，锁定以下 4 个数据集（2 主 2 备）。

## 3. 锁定数据集评估表

### ① GSE121297（主用）——蛇毒 snaclec × 人脐静脉内皮细胞

- 标题：Rigidity and inflammatory responses of interconnected endothelial cells are stimulated by rhodocetin-αβ via the neuropilin-1-MET-axis
- 类型：表达谱芯片；样本 n=19；2019-03 公开
- 分组（GSM 标题核实）：HUVEC 静态对照 ×3 / 静态 + RCαβ ×3 / 剪切流（80 rpm）+ RCαβ ×3；另含未处理 ×4、RCαβ 200 nM 冲击 ×3、HGF 200 ng/mL ×3
- 相关性：RCαβ 为马来蝮（*Calloselasma rhodostoma*）毒液 C 型凝集素样蛋白（snaclec），直接对应本研究 snaclec 家族与轴 3/轴 4 内皮激活；含 NF-κB 通路表型
- 局限：单一纯化组分（非粗毒）、HUVEC 非肾小球内皮；对照设计完整，limma 可直接用
- **主对比设计**：静态 RCαβ vs 静态对照（3 vs 3）；敏感性分析可加剪切流组

### ② GSE248215（主用）——目标蛇种毒液体内暴露时间序列

- 标题：A complex pattern of gene expression in tissue affected by viperid snake envenoming: the emerging role of autophagy-related genes
- 类型：NanoString nCounter Fibrosis V2 Panel（约 800 基因，ECM/免疫/程序性死亡/自噬方向）；小鼠骨骼肌；n=20；2024-03 公开；PMID 38540699
- 设计：*Daboia russelii* 与 *Bothrops asper* 毒液注射后 1 h / 6 h / 24 h 时间序列
- 相关性：**含本研究目标蛇种 *D. russelii***，体内模型，覆盖轴 4（ECM、炎症、细胞死亡）
- 局限：Panel 限定约 800 基因（Hub 交集概率受限）、肌肉组织而非肾脏、小鼠而非人；原始计数与归一化矩阵均有提供
- **主对比设计**：*D. russelii* 24 h vs 1 h/基线；*B. asper* 作跨种参照

### ③ GSE287744（备用）——人源细胞 × 全毒液 RNA-seq

- 标题：Neurocellular stress response to Mojave Type A Rattlesnake venom（人 iPSC 神经干细胞模型）
- 类型：RNA-seq；n=24（4 供体 × 对照/10/30 µg/mL × 4 h/24 h）；2025-04 公开
- 相关性：人源 + 全毒液 + 剂量时间双梯度，设计规范；但细胞类型为神经干细胞，与 TMA 内皮/肾表型距离远
- 用途：主用数据集交集基因的正交印证（应激/炎症共性通路）

### ④ GSE262798（备用）——眼镜蛇毒功能基因组学

- 标题：Molecular dissection of cobra venom highlights heparinoids as an effective snakebite antidote
- 类型：功能基因组学筛选（HAP1 细胞，n=8）；2025-04 公开
- 局限：眼镜蛇（非蝰科）、细胞系非内皮/肾；仅作对翡翠斑/肝素类解毒机制讨论的定性参考，不进 limma 流程

## 4. Phase 6 执行预案（据此写入 analysis_plan_v1.md §5）

1. 下载 GSE121297（系列矩阵）→ limma：静态 RCαβ vs 静态对照，|log2FC|>1 且 adj.P<0.05；
2. 下载 GSE248215（raw counts + normalized）→ NanoString 背景校正后 limma 或 nSolver 流程，*D. russelii* 24 h 主对比；
3. 两数据集 DEG 分别 ∩ Hub 基因 → 双重证据基因清单；
4. 若交集过稀：放宽至 |log2FC|>0.58（敏感性），或用 GSE287744 正交印证；
5. 论文 Limitations 声明：无患者转录组、Panel 基因数受限、组织/物种外推限制。

## 5. 溯源

- 检索与样本结构核实：NCBI E-utilities（esearch/esummary, db=gds），2026-09-04；
- GSE248215 记录页核对（设计、Panel、附件）：https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE248215 ，2026-09-04；
- GSE121297 记录页当时受人机验证限制，分组信息经 E-utilities GSM 标题核实（GSM3430984–GSM3431002）。
