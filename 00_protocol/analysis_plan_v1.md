# 分析计划 v1（固化版）

**项目**：蛇伤相关血栓性微血管病（TMA）的网络毒理学机制研究与分子对接验证
**固化日期**：2026-09-04（Phase 0 输出，对应研究方案 v2 修正版）
**变更规则**：本文件固化后任何变更须升级版本号（v1.1、v1.2…），在文末"变更记录"追加说明，不得覆盖旧版。

---

## 1. 蛇种策略（已定）

采用**策略 A（机制深度优先）**：限定 *Daboia russelii*（罗素蝰指名亚种/斯里兰卡-南印度种群）+ *Daboia siamensis*（暹罗罗素蝰/东南亚种群），纳入两蛇种共有的保守毒素家族，强调亚洲蛇伤 TMA 代表性。结论表述严格限定于所研究种群。

## 2. 生物学先验：四条病理轴

| 轴 | 核心事件 | 关键宿主分子 |
|---|---|---|
| 轴 1 vWF–ADAMTS13 失衡 | ULVWF 清除不足、血小板微血栓 | ADAMTS13、VWF、GP1BA、ITGA2B/ITGB3 |
| 轴 2 凝血–纤溶紊乱（VICC） | 凝血因子激活/消耗、凝血酶爆发 | F2、F5、F10、FGA/FGG、PLG、SERPINE1、PROC |
| 轴 3 补体旁路激活 | 内皮 C3 沉积、C5b-9 形成 | C3、C5、CFB、CFH、CFI、CD46 |
| 轴 4 内皮损伤–炎症–肾毒性 | 黏附分子上调、氧化应激、肾小管坏死 | VCAM1、ICAM1、SELE、TNF、IL6、NOS3、HMOX1、HAVCR1 |

## 3. 研究假设（v2 修正版，已固化）

- **H1**：SVMP 类毒素以网络拓扑上高度中心化的方式靶向 vWF–ADAMTS13 轴，SVSP 类毒素以高中心度靶向凝血级联（FGA/F2/F10），二者共同构成 TMA 启动的"主开关"。
- **H2**：毒素靶点在补体旁路与内皮激活通路上显著富集，补体–凝血交叉对话是 TMA 由"凝血病"向"微血管病"转化的放大器。（补体轴不富集为可发表的阴性结果，预设双向解释。）
- **H3**：核心"毒素–靶点"复合物（如 SVMP–ADAMTS13、SVMP–VWF）具有可成药结合界面，可被 batimastat / marimastat 类抑制剂占据；snaclec–C3 等补体相关候选对降级为探索性对接，仅入补充材料。

## 4. 关键参数阈值（固化，论文 Methods 照此报告）

| 环节 | 参数 |
|---|---|
| 毒素去冗余 | CD-HIT，序列一致性 90% 聚类，去 <30 aa 片段 |
| GeneCards | 主分析集 relevance score ≥ 中位数或 ≥10；≥5 宽集仅敏感性分析 |
| DisGeNET | score ≥ 0.1；OMIM 全纳入；CTD 取 direct evidence |
| 靶点证据等级 | curated（CTD/T3DB/文献）> database-predicted > homology-inferred |
| BLASTp | e-value < 1e-3 全部报告并标注辅助证据；identity > 30% 重点标注 |
| STRING | 主分析 score ≥ 0.7（隐藏孤立节点）；0.4 作敏感性分析 |
| Hub 基因 | cytoHubba MCC/Degree/EPC Top 20 三者交集 ∩ MCODE 模块（K-core 2） |
| 富集 | GO/KEGG/Reactome，Metascape + clusterProfiler 双平台，BH 校正 FDR < 0.05 |
| 蛋白–蛋白对接 | HDOCK（score ≤ −200）+ ClusPro 交叉，HADDOCK 先验约束精修；Ⅰ/Ⅱ/Ⅲ 三级证据，正文仅依据 Ⅰ–Ⅱ 级 |
| 对接对照 | 阳性对照 RVV-X–FX；阴性对照 3–5 对随机无关联对 |
| 毒素建模 | ColabFold，活性位点区 pLDDT > 70；短肽用 PEP-FOLD3 |
| 受体结构 | PDB 分辨率 ≤ 3.0 Å；ADAMTS13 锁定 PDB 6GHZ（MDTCS 域段，备选 3EAS） |
| 小分子对接 | AutoDock Vina，结合能 ≤ −7 kcal/mol 为活性提示 |
| 转录组验证 | limma，|log2FC| > 1 且 adj.P < 0.05 |

## 5. GEO 前置侦察结论（Phase 6 路径锁定）

**结论：GEO 中不存在蛇伤患者转录组直接数据集（与预判一致），启用替代策略，已锁定 2 主 2 备共 4 个数据集**（详见 `GEO_recon_report.md`）：

| 优先级 | GSE | 设计 | 用途定位 |
|---|---|---|---|
| 主用 ① | GSE121297 | HUVEC ± 蛇毒 snaclec（rhodocetin-αβ），静态/剪切流，含对照，n=19 | 轴 3/轴 4（内皮激活、NF-κB）表达验证 |
| 主用 ② | GSE248215 | 小鼠骨骼肌注射 *D. russelii* / *B. asper* 毒液 1/6/24 h，NanoString 纤维化 Panel（约 800 基因），n=20 | 目标蛇种体内验证（轴 4/ECM/炎症） |
| 备用 ① | GSE287744 | 人 iPSC 神经干细胞 + 莫哈维响尾蛇毒 10/30 µg/mL，4/24 h，RNA-seq，n=24 | 人源全毒液暴露参考 |
| 备用 ② | GSE262798 | HAP1 细胞 + 眼镜蛇毒功能基因组学筛选，n=8 | 仅作定性参考 |

Phase 6 差异分析设计：GSE121297 按"静态 RCαβ vs 静态对照"为主对比；GSE248215 按"*D. russelii* 24 h vs 基线"为主对比；DEG ∩ Hub 基因交集即"计算+表达"双重证据。

## 6. 待办（本周内完成，非文件类）

- [ ] 注册 HADDOCK 网页服务器 guru 账号（服务器名 HADDOCK2.4，后台运行 2.5 版；学术邮箱申请，审核 1–2 周）
- [ ] 注册 ClusPro 2.0 账号（经 2026-09-04 核实仍为最新版本）
- [ ] 安装/确认：Cytoscape 3.10 + cytoHubba + MCODE、R ≥4.3 + clusterProfiler/limma/GEOquery、PyMOL、CD-HIT、BLAST+

## 7. 变更记录

- v1（2026-09-04）：首版固化，依据研究方案 v2 修正版；GEO 侦察完成，Phase 6 路径确定。
- v1.1（2026-09-04）：更新对接平台版本信息——HADDOCK 网页服务器后台已升级为 2.5 版（2024 年 12 月起，服务器仍名 HADDOCK2.4）；ClusPro 2.0 经核实仍为最新版本。同步更新研究方案 v2 修正版与 SOP。
