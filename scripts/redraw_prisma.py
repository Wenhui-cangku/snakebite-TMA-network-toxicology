# -*- coding: utf-8 -*-
"""重画 PRISMA Phase1 双线流程图（CTD 并入定稿版）"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot
setup_plot()
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = Path(__file__).resolve().parents[1] / "00_protocol" / "PRISMA_flowchart_phase1_filled.png"

fig, ax = plt.subplots(figsize=(8.6, 10.0), dpi=200)
ax.set_xlim(0, 100); ax.set_ylim(0, 118); ax.axis("off")

def box(x, y, w, h, text, fc, ec, fs=7.8, tc="black"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2",
                                fc=fc, ec=ec, lw=1.2))
    ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=fs, color=tc, linespacing=1.5)

def arrow(x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=13, color="#555555", lw=1.1))

ax.text(50, 116, "图 S0-4   毒素与疾病基因筛选流程（PRISMA 式，Phase 1 双线终版实测，2026-09-22）",
        ha="center", fontsize=10.5, weight="bold")

# ---- A 线：毒素 ----
ax.text(26, 110.5, "A. 毒素成分库线（已完成）", ha="center", fontsize=9.5, weight="bold", color="#8B1A1A")
box(5, 99, 42, 10, "UniProt 主检索 52 + 补充检索 32\n(Kunitz 24 / CRISP 4 / SVMP・Dis 3 / VZ 补漏 1)\n(siamensis 单独导出 28 条完全重叠)", "#FDECEC", "#B22222")
box(5, 86, 42, 9, "合并去重（按登录号）\nn = 79", "#FDECEC", "#B22222")
box(5, 73, 42, 9, "剔除 <30 aa 片段 16 条\n排除 ADAM 样宿主污染 4 条", "#E8F0FE", "#1A56C4")
box(5, 59, 42, 10.5, "入库毒素 n = 63，九大家族齐全\n90% 聚类 → 40 簇代表序列\n丰度权重已回填", "#F3E8FD", "#7B1FA2")
arrow(26, 98.6, 26, 95.4); arrow(26, 85.6, 26, 82.4); arrow(26, 72.6, 26, 69.9)

# ---- B 线：疾病基因 ----
ax.text(74, 110.5, "B. 疾病基因集线（已完成）", ha="center", fontsize=9.5, weight="bold", color="#1A56C4")
box(53, 97.5, 42, 11.5,
    "GeneCards 手工导出（6 词）n = 1356\nOpen Targets（8 个 MONDO 条目）n = 741\nDISEASES curated ∪ DisGeNET（16 CUI，46 基因）\nCTD（6 词白名单）∪ OMIM（14 表型，15 基因）",
    "#E8F0FE", "#1A56C4", fs=7.4)
box(53, 85, 42, 8.5, "mygene 标准化映射（人源）\nsymbol → UniProt AC", "#E8F0FE", "#1A56C4")
box(53, 72, 42, 9.5, "合并去重 n = 2190\n（含四轴先验强制纳入 9 条）", "#E8F0FE", "#1A56C4")
box(53, 57.5, 42, 11, "分层：主集 1042 / 宽集 1148\n(GeneCards ≥逐词中位数 ∪ OT≥0.3 ∪\n≥3疾病 ∪ curated ∪ CTD direct ∪ 先验)\n四轴先验 27/27 在主集 ✓", "#E6F4EA", "#1E7E34", fs=7.4)
arrow(74, 97.1, 74, 93.9); arrow(74, 84.6, 74, 81.9); arrow(74, 71.6, 74, 68.9)

# ---- 汇合 ----
arrow(26, 58.6, 40, 45.5); arrow(74, 57.1, 60, 45.5)
box(28, 38.5, 44, 7.5, "毒素预测靶点（L1+L2，n=15）∩ 疾病基因主集（n=1042）\n韦恩交集 → 候选核心靶点集 n = 10（已定稿）\n扩展层 54 节点（+STRING 邻居∩主集）", "#E6F4EA", "#1E7E34")
box(28, 28.5, 44, 7.5, "STRING PPI（score ≥ 0.7，隐藏孤立节点）\n→ Cytoscape 3.10\ncytoHubba（MCC/Degree/EPC Top 20）∩ MCODE", "#E6F4EA", "#1E7E34")
box(28, 19, 44, 6.5, "Hub 基因 n = 10（F2/F3/F5/F7/F8/F10/FGA/PLG/PROC/ALB）\n→ 富集分析 / 四层异质网络 / 分子对接", "#FFF4D6", "#B8860B")
box(28, 10, 44, 6.5, "三重干法交叉验证\nGEO 转录组（GSE121297 / GSE248215）\n+ 文献共证 + 临床一致性核对", "#FFF4D6", "#B8860B")
arrow(50, 38.1, 50, 36.4); arrow(50, 28.1, 50, 25.9); arrow(50, 18.6, 50, 16.9)

ax.text(50, 6.5, "注：双线计数均为 2026-09-22/24 实测终版；Phase 3 交集与 Hub 已回填，下游 n 值执行时填入。",
        ha="center", fontsize=7.5, color="#555555")

fig.savefig(OUT, bbox_inches="tight")
print("saved:", OUT)
