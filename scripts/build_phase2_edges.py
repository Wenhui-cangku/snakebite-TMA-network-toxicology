# -*- coding: utf-8 -*-
"""
Phase 2 - 毒素-人靶点边表构建（L2 literature curated + L4 STRING 邻居）
L1: CTD/T3DB 需手工导出（ALTCHA 反爬）, 待用户导出后追加
L2: UniProt/Swiss-Prot 审编注释结构化(43条) + PubMed 补证(Daboxin P / RVVA-PLA2-I / daborhagin / SPAD-1)
L3: BLAST 同源辅助 - 本地无 blastp 二进制, 本期暂缓(见报告)
L4: STRING interaction_partners score>=0.7 一层邻居
输出: 03_target_prediction/toxin_target_edges.csv + Phase2_构建报告.md + Excel 靶点边表 sheet + 变更记录 v9
"""
from pathlib import Path
import pandas as pd
import os, json, time, urllib.request, urllib.parse

ROOT = Path(__file__).resolve().parents[1]  # repo root (snakebite_TMA/)
TP = os.path.join(ROOT, r"03_target_prediction")
TODAY = "2026-09-24"

ev = pd.read_csv(os.path.join(TP, "literature_evidence_draft.csv"), encoding="utf-8-sig")
tox = pd.read_csv(os.path.join(ROOT, r"01_toxin_lib\toxin_master_table.csv"), encoding="utf-8-sig")
pmid_map = dict(zip(ev["toxin_ac"], ev["pmids"]))
fam_map = dict(zip(tox["UniProt ID"], tox["毒素家族"]))
tid_map = dict(zip(tox["UniProt ID"], tox["条目ID"]))

# ---------------- L2 结构化 curated 边 ----------------
# (toxin_ac, target, detail, pmids_override or None, score)
L2 = [
    # PLA2
    ("P59071", "F10", "结合 FXa 抑制凝血酶原酶活性 (IC50=130 nM)", "18062812", 1.0),
    ("C0HK16", "F10", "结合 FX/FXa 发挥抗凝活性 (UniProt 审编)", None, 1.0),
    ("PLA2_family", "F10", "家族级文献: Daboxin P（印度 D. russelii 主要 PLA2）靶向 FX 抗凝", "27089306", 0.6),
    ("PLA2_family", "F10", "家族级文献: 酸性 RVVA-PLA2-I 抗凝（纯化自 D. russelii）", "21356226", 0.6),
    # snaclec/CTL (RVV-X)
    ("Q4PRD1", "F10", "RVV-X 轻链1: 识别结合 FX Gla 域 (Ca2+ 依赖)", None, 1.0),
    ("Q4PRD1", "F9", "RVV-X 轻链1: 识别结合 FIX Gla 域", None, 1.0),
    ("Q4PRD2", "F10", "RVV-X 轻链2: 识别结合 FX Gla 域 (Ca2+ 依赖)", None, 1.0),
    ("Q4PRD2", "F9", "RVV-X 轻链2: 识别结合 FIX Gla 域", None, 1.0),
    ("Q7LZ61", "F10", "RVV-X 重链: 切割 Arg-Ile 键激活 FX", "37092784;18616470;1629211;8144654;8639544;18060879;11910189", 1.0),
    ("Q7LZ61", "F9", "RVV-X 重链: 切割 Arg-Ile 键激活 FIX", None, 1.0),
    ("Q7LZ61", "PROS1", "RVV-X 重链: 特异性切割激活 protein S", None, 1.0),
    ("Q4PRD1", "PROS1", "RVV-X 复合体: 切割激活 protein S", None, 0.8),
    ("Q4PRD2", "PROS1", "RVV-X 复合体: 切割激活 protein S", None, 0.8),
    ("Q38L02", "GP1BA", "结合血小板 GPIbα, 抑制瑞斯托霉素诱导聚集", None, 1.0),
    # SVMP
    ("B8K1W0", "FGA", "daborhagin-K (P-III 出血性 SVMP): 水解纤维蛋白原 Aα 链", "18554518;28042812", 1.0),
    ("B8K1W0", "FN1", "daborhagin-M/K: 体外水解纤维连接蛋白", "18554518", 1.0),
    ("B8K1W0", "COL4A1", "daborhagin-M/K: 体外水解 IV 型胶原", "18554518", 1.0),
    ("AAZ39880.1", "FGA", "russelysin = daborhagin-K 同一蛋白 (GenBank 补充条目): 水解纤维蛋白原 Aα 链", "18554518;28042812", 0.9),
    ("AAZ39880.1", "FN1", "russelysin: 水解纤维连接蛋白", "18554518", 0.9),
    ("AAZ39880.1", "COL4A1", "russelysin: 水解 IV 型胶原", "18554518", 0.9),
    ("A0A2H4Z2X6", "FN1", "家族级旁证: RVV 来源 SPAD-1 (HGD-disintegrin) 破坏纤维连接蛋白基质黏附", "36423674", 0.6),
    ("A0A2H4Z2Y1", "FN1", "家族级旁证: RVV 来源 SPAD-1 (HGD-disintegrin) 破坏纤维连接蛋白基质黏附", "36423674", 0.6),
    # SVSP
    ("P18965", "F5", "RVV-V γ: 切割人 FV Arg1545-Ser1546 激活 (Ca2+ 非依赖)", "21640745;3053712;20054136;21871889;28732041", 1.0),
    ("P18964", "F5", "RVV-V: 切割人 FV Arg1545-Ser1546 激活", "21640745;21871889;28732041", 1.0),
    ("E5L0E3", "FGA", "SVSP: 降解纤维蛋白原 α 链, 强酪蛋白水解活性", None, 1.0),
    ("E5L0E4", "FGB", "SVSP: 水解纤维蛋白原 β 链", None, 1.0),
    # Kunitz
    ("H6VC06", "PLG", "抑制纤溶酶 90% (Ki=0.19 nM)", None, 1.0),
    ("H6VC06", "F11", "抑制 FXIa 37% (Ki=6 nM)", None, 1.0),
    ("H6VC06", "F10", "抑制 FXa 20%", None, 1.0),
    ("H6VC06", "PRSS1", "抑制胰蛋白酶 70%", None, 1.0),
    ("H6VC05", "PROC", "抑制活化蛋白 C (APC) IC50=3.5 nM (肝素存在)", None, 1.0),
    ("H6VC05", "F11", "抑制 FXIa 40% (肝素存在)", None, 1.0),
    ("H6VC05", "PLG", "抑制纤溶酶 70% (肝素存在)", None, 1.0),
    ("H6VC05", "PRSS1", "抑制胰蛋白酶 45% (肝素存在)", None, 1.0),
    ("A8Y7P1", "CTRB1", "抑制糜蛋白酶 (Ki=4.77 nM)", None, 1.0),
    ("A8Y7N4", "PRSS1", "抑制胰蛋白酶", None, 1.0),
    ("A8Y7N8", "PRSS1", "抑制胰蛋白酶", None, 1.0),
    ("A8Y7P0", "PRSS1", "抑制胰蛋白酶", None, 1.0),
    ("A8Y7P2", "PRSS1", "抑制胰蛋白酶", None, 1.0),
    ("A8Y7P6", "PRSS1", "抑制胰蛋白酶", None, 1.0),
    ("A8Y7N5", "PLG", "抑制纤溶酶与胰蛋白酶", None, 1.0),
    ("A8Y7N5", "PRSS1", "抑制纤溶酶与胰蛋白酶", None, 1.0),
    ("A8Y7P3", "PLG", "抑制纤溶酶与胰蛋白酶", None, 1.0),
    ("A8Y7P3", "PRSS1", "抑制纤溶酶与胰蛋白酶", None, 1.0),
    ("A8Y7P4", "PLG", "抑制纤溶酶与胰蛋白酶", None, 1.0),
    ("A8Y7P4", "PRSS1", "抑制纤溶酶与胰蛋白酶", None, 1.0),
    # VEGF / NGF
    ("P67861", "KDR", "经 VEGFR-2 (KDR) 信号诱导血管生成; NO 介导低血压", None, 1.0),
    ("P0DL42", "KDR", "经 VEGFR-2 (KDR) 信号诱导血管生成; NO 介导低血压", None, 1.0),
    ("P30894", "GP1BA", "By similarity: 抑制金属蛋白酶对血小板 GPIbα 的蛋白水解 (间接保护)", None, 0.5),
]

rows = []
for ac, tgt, detail, pm, score in L2:
    if ac == "PLA2_family":
        tid, fam = "PLA2_family", "PLA2"
    else:
        tid = tid_map.get(ac, ac)
        fam = fam_map.get(ac, "")
    pmids = pm if pm else str(pmid_map.get(ac, ""))
    rows.append({"toxin_id": tid, "toxin_ac": ac, "family": fam,
                 "target_symbol": tgt, "evidence_type": "literature",
                 "evidence_detail": detail, "pmids": pmids, "score": score,
                 "下载日期": TODAY})

# ---------------- L4 STRING 邻居 ----------------
targets = sorted({r[1] for r in L2})
print("L2 边:", len(rows), "| 唯一靶点:", len(targets), targets)

def string_partners(sym, limit=10, score=700):
    u = ("https://string-db.org/api/tsv/interaction_partners?identifiers=" +
         urllib.parse.quote(sym) + f"&species=9606&limit={limit}&required_score={score}")
    req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
    for att in range(3):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                txt = r.read().decode()
            break
        except Exception as e:
            print("  STRING retry", sym, att + 1, e); time.sleep(3)
    else:
        return []
    out = []
    for i, line in enumerate(txt.strip().split("\n")):
        if i == 0:
            continue
        p = line.split("\t")
        if len(p) >= 6:
            out.append((p[2], p[3], float(p[5])))  # nameA, nameB, score
    return out

print("\n拉取 STRING 一层邻居 (limit=10, score>=0.7) ...")
nb_map = {}
for t in targets:
    nb = string_partners(t)
    nb_map[t] = [(b, s) for a, b, s in nb if a == t or b != t]
    nb_map[t] = [(b if a == t else a, s) for a, b, s in nb]
    print(f"  {t}: {len(nb_map[t])} 邻居")
    time.sleep(0.5)

n_l4 = 0
seen = set()
for ac, tgt, detail, pm, score in L2:
    if score < 0.8:   # 仅对直接 curated 靶点扩展
        continue
    tid = tid_map.get(ac, ac)
    fam = "PLA2" if ac == "PLA2_family" else fam_map.get(ac, "")
    for nb, s in nb_map.get(tgt, []):
        key = (tid, nb)
        if key in seen or nb == tgt:
            continue
        seen.add(key)
        rows.append({"toxin_id": tid, "toxin_ac": ac, "family": fam,
                     "target_symbol": nb, "evidence_type": "string",
                     "evidence_detail": f"STRING 一层邻居, 经 {tgt} (combined score={s:.3f})",
                     "pmids": "", "score": round(s, 3), "下载日期": TODAY})
        n_l4 += 1
print("L4 边:", n_l4)

edges = pd.DataFrame(rows)
edges.to_csv(os.path.join(TP, "toxin_target_edges.csv"), index=False, encoding="utf-8-sig")
print("\n总计:", len(edges), "条边 ->", "toxin_target_edges.csv")
print(edges["evidence_type"].value_counts().to_dict())

# QC: 核心家族 L2 边数
lit = edges[edges["evidence_type"] == "literature"]
for f in ["SVMP/disintegrin", "SVSP", "PLA2", "snaclec/CTL"]:
    print(f"QC {f}: L2 边 {len(lit[lit['family']==f])} (要求>=3)")

# 家族级备注（无边家族）
notes = {
    "CRISP": "4 条 CRISP 无已审编人源靶点; serotriflin 结合蛇自身血清 SSP-2 (PMID 18222185, 非人靶点)",
    "LAAO": "2 条 LAAO 经 H2O2 生成影响血小板聚集 (PMID 21802487), 无单一蛋白靶点",
    "NGF": "P30894 间接保护 GP1BA (By similarity), 已记 0.5 分弱边",
}
json.dump({"nb_map": {k: v for k, v in nb_map.items()}, "family_notes": notes},
          open(os.path.join(TP, "phase2_string_neighbors.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("邻居存档 -> phase2_string_neighbors.json")
