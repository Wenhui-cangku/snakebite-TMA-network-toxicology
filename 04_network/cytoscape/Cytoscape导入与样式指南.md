# Figure 4 四层异质网络 — Cytoscape 导入与样式指南

更新：2026-09-30 ｜ 对应 SOP：Phase 2 第 214 行"四层异质网络（核心主图）"
设计依据：毒素→核心靶点→富集通路→TMA 表型；节点按类别着色，边按证据等级分线型。

## 0. 文件清单（均在 `04_network/cytoscape/`）

| 文件 | 用途 |
|---|---|
| `figure4_hetero_network.xgmml` | **首选**：所有 Cytoscape 3.x 必认的经典格式，坐标/颜色/形状/边框全内嵌（2026-09-30 新增） |
| `figure4_hetero_network.cx` | CX 交换格式（坐标内置）；新版 Cytoscape 可用 |
| `figure4_hetero_network.cyjs` | Cytoscape.js JSON，分层布局坐标内置；部分环境不识别则用 XGMML/CX |
| `figure4_hetero_network_safe.cyjs` | cyjs 安全版（emoji→[PASS]），emoji 解析报错时用 |
| `nodes.csv` | 节点表（30 节点：7 毒素 + 12 靶点 + 6 通路 + 5 表型），含颜色/形状/坐标列 |
| `edges.csv` | 边表（49 条：14 直接互作 + 20 通路成员 + 11 机制推断 + 4 表型进展） |
| `figure4_preview.png` | matplotlib 预览（供快速核对拓扑，非最终发表图） |
| `../build_figure4_network.py` | 生成脚本，改节点/边后重跑即可再出 cyjs/csv/png |
| `build_cx.py` / `build_xgmml.py` | 由 cyjs 生成 CX / XGMML 的转换脚本 |

## 1. 方法一（推荐）：导入 XGMML

**首选 XGMML**：Cytoscape → `File → Import → Network from File…` → 选 `figure4_hetero_network.xgmml` → 直接载入：四层横向布局、节点颜色/形状/Hub 加粗边框、边颜色全部自动就位。

XGMML 是 Cytoscape 从 2.x 到 3.10 都内置支持的经典格式，不会落入"表格导入"对话框。若误动布局：`Edit → Undo`，或重新导入。

### 1.1 导入报错排查（2026-09-30 补充）

cyjs 文件本身已通过完整性校验（30 节点/49 边、JSON 合法、无悬空引用、无重复 id）。

**典型报错**：弹窗 "The network cannot be created without selecting the source and target columns"，或预览窗口显示 JSON 原文 —— 说明当前 Cytoscape 没认出 cyjs/cx 格式、把文件当成普通表格了。按以下顺序解决：

1. **首选：改用 XGMML 文件** `figure4_hetero_network.xgmml`（所有 3.x 版本必认，样式坐标全内嵌）；
2. 若坚持用 cyjs/cx：确认入口是 `File → Import → Network from File…`（不是 File → Open，也不能双击）；emoji 兼容性存疑时用 `figure4_hetero_network_safe.cyjs`；
3. **备选：CSV 导入**（方法二）。注意：导入 `edges.csv` 时必须在对话框里把 **source 列设为 Source（绿点）、target 列设为 Target（红点）、interaction 列设为 Interaction Type（蓝点）**，否则就会弹"未选 source/target 列"的报错；
4. 导入后核对 §5 质控点（30 节点 / 49 边）。

## 2. 方法二：CSV 导入（需要完全自定义时）

1. `File → Import → Network from File…` → 选 `edges.csv`：
   - Source Column = `source`，Target Column = `target`，Interaction Type = `interaction`；
2. `File → Import → Table from File…` → 选 `nodes.csv`：
   - Import Data As = `Node Table Columns`，Key Column = `id`；
3. 布局：`Layout → yFiles Layouts → Hierarchic`（orientation 从左到右），
   或按 `layer` 列手工分行（Layout → Grid Layout → by attribute）。

## 3. 样式（Style 面板设置）

### 节点（Node 页）
| 属性 | 映射 | 值 |
|---|---|---|
| Fill Color | Column=`fill_color`，Mapping Type=**Passthrough** | 毒素红 #D62728 / 靶点蓝 #1F77B4 / 通路绿 #2CA02C / 表型紫 #9467BD |
| Shape | Column=`shape`，Passthrough | 毒素 HEXAGON / 靶点 ELLIPSE / 通路 ROUND_RECTANGLE / 表型 DIAMOND |
| Label | Column=`label`，Passthrough | — |
| Size | layer=1:60，layer=2:45，layer=3:70×40（用 `Custom graphics` 或 Size Lock 关闭后高宽分设），layer=4:65 | 可 Discrete Mapping by `layer` |
| Border Width | Column=`hub_status`，Discrete | "Hub+strict" = 4（加粗黑框标 Hub），其余 = 1.5 |
| Label Font Size | 12–14 | 通路节点可调 10（名字长） |

### 边（Edge 页）
| 属性 | 映射 | 值 |
|---|---|---|
| Line Type | Column=`line_type`，Passthrough（或 Discrete by `interaction`） | 直接互作 solid / 成员 solid / 机制推断 dashed / 进展 dotted |
| Width | Column=`width`，Passthrough | 3.0 / 1.2 / 2.0 / 2.0 |
| Stroke Color | Discrete by `interaction` | direct #333333 / membership #AAAAAA / mechanism #777777 / progression #9467BD |
| Target Arrow Shape | Discrete：mechanism 与 progression = ARROW（有向），direct/membership = NONE | — |

## 4. 导出发表图

- `File → Export → Network to Image…` → 格式 **SVG**（矢量，投稿用）+ PNG（600 dpi，预览）；
- 导出前：View → Show Graphics Details 打开；确认标签无遮挡（通路名长的可略移）；
- 图例（4 色节点 + 4 线型）单独用文字说明或 AI/PS 合成，Cytoscape 不自动生成图例。

## 5. 质控点（导入后逐项核对）

- [ ] 节点数 = **30**（7+12+6+5），边数 = **49**
- [ ] RVV-X 应连出 3 条实线（F10/F9/PROS1）；F10 有 3 条入边（RVV-X/PLA2/Kunitz）——凝血轴枢纽
- [ ] KDR 仅连 svVEGF（入）与 Focal Adhesion + VEGFR2 Signaling（出）——轴4 独立簇
- [ ] 表型层 5 节点间有 4 条紫色点线（VICC→三联 + 渗漏→AKI）
- [ ] 虚线边（机制推断）共 11 条，全部落在 L3→L4

## 6. 设计说明（写入 Methods/图注的素材）

- **L1→L2 仅收 score=1.0 的文献直接互作**（STRING 扩展邻域不进主图，保证证据等级）；RVV-X 三亚基合并为单一节点；
- **L2→L3 成员边**取 g:Profiler/Enrichr 交集基因与 12 直接靶点的交；
- **L3→L4 为机制推断边**（虚线标示），证据等级低于实线，图注中须声明；
- ECM–receptor interaction 与 Focal adhesion 为单平台（Enrichr）显著，节点备注已注明，图注建议同注；
- Hub 节点（F10/F5/FGA/PLG）以加粗黑框标示，对应 Phase 3 cytoHubba 三榜交集结果。
