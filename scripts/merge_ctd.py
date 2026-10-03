# -*- coding: utf-8 -*-
"""
Phase 1B - CTD 数据并入疾病基因总表
输入: CTD/*.tsv (6 个 batch query 手工导出)
规则:
  1. 疾病白名单过滤(剔除 CTD 词扩展带入的无关疾病, 如先天性溶血性贫血/地中海贫血/ITP)
  2. DirectEvidence 非空 -> 纳入主集
  3. 仅 InferenceScore: >=50 -> 进宽集; snakebite envenoming 词例外(全量仅57基因且高度切题, 全收进宽集)
  4. CTD inference 列格式: direct:<type> 或 inferred:<maxscore>
  5. 新基因用 mygene.info 映射 UniProt AC
输出: 更新 disease_gene_master.csv + data_management_table.xlsx + 变更记录 v7
"""
from pathlib import Path
import pandas as pd
import glob, os, json, time, urllib.request

ROOT = Path(__file__).resolve().parents[1]  # repo root (snakebite_TMA/)
MASTER = os.path.join(ROOT, r"02_disease_genes\disease_gene_master.csv")
XLSX = os.path.join(ROOT, r"00_protocol\data_management_table.xlsx")
TODAY = "2026-09-22"
INF_THRESHOLD = 50.0

# 疾病白名单: 仅保留与课题病理轴直接对应的 CTD 疾病条目
WHITELIST = {
    "Snake Bites",
    "Atypical Hemolytic Uremic Syndrome",
    "Hemolytic-Uremic Syndrome",
    "Purpura, Thrombotic Thrombocytopenic",
    "Thrombotic thrombocytopenic purpura, acquired",
    "Thrombotic Microangiopathies",
    "Anemia, Hemolytic",
}

TERM_SHORT = {
    "atypical hemolytic uremic syndrome": "aHUS",
    "microangiopathic hemolytic anemia": "MAHA",
    "snakebite envenoming": "snakebite",
    "thrombotic microangiopathy": "TMA",
    "thrombotic thrombocytopenic purpura": "TTP",
    "venom-induced consumption coagulopathy": "VICC",
}

# ---------- 1. 解析 CTD ----------
agg = {}  # symbol_upper -> dict
file_stats = {}
# raw CTD exports live beside the project folder (not in repo)
for f in sorted(glob.glob(os.path.join(ROOT.parent, "CTD", "*.tsv"))):
    term = os.path.basename(f).replace("CTD_disease_genes_", "").replace(".tsv", "").strip()
    short = TERM_SHORT[term]
    df = pd.read_csv(f, sep="\t", dtype=str)
    n_raw = len(df)
    df = df[~df["DiseaseName"].str.contains("Object not found", na=False)]
    n_notfound = n_raw - len(df)
    w = df[df["DiseaseName"].isin(WHITELIST)].copy()
    w["InferenceScore"] = pd.to_numeric(w["InferenceScore"], errors="coerce")
    n_direct = 0
    for _, r in w.iterrows():
        sym = str(r["GeneSymbol"]).strip()
        if not sym or sym == "nan":
            continue
        key = sym.upper()
        a = agg.setdefault(key, {"symbol": sym, "geneid": str(r["GeneID"]).strip(),
                                 "direct": set(), "inf_max": 0.0, "inf_chem": "",
                                 "terms": set(), "diseases": set()})
        a["terms"].add(short)
        a["diseases"].add(str(r["DiseaseName"]))
        de = str(r["DirectEvidence"]).strip() if pd.notna(r["DirectEvidence"]) else ""
        if de:
            a["direct"].add(de)
            n_direct += 1
        else:
            sc = r["InferenceScore"]
            if pd.notna(sc) and sc > a["inf_max"]:
                a["inf_max"] = float(sc)
                a["inf_chem"] = str(r["InferenceChemicalName"]) if pd.notna(r["InferenceChemicalName"]) else ""
    file_stats[term] = {"raw_rows": n_raw, "whitelist_rows": len(w),
                        "notfound": n_notfound,
                        "uniq_genes": w["GeneSymbol"].nunique()}

# CTD annotation 字符串
def ctd_str(a):
    if a["direct"]:
        return "direct:" + "|".join(sorted(a["direct"]))
    if a["inf_max"] > 0:
        return f"inferred:{a['inf_max']:.2f}"
    return ""

# ---------- 2. 决定新基因纳入 ----------
master = pd.read_csv(MASTER, encoding="utf-8-sig")
msym = set(master["基因Symbol"].str.upper())

new_direct, new_inf, new_snakebite = [], [], []
for key, a in agg.items():
    if key in msym:
        continue
    if a["direct"]:
        new_direct.append(key)
    elif a["inf_max"] >= INF_THRESHOLD:
        new_inf.append(key)
    elif a["terms"] == {"snakebite"} or "snakebite" in a["terms"]:
        # snakebite 词例外: 全量收录(最高 8.85, 经 Bungarotoxins/Glutamine 推断)
        new_snakebite.append(key)

new_keys = new_direct + new_inf + new_snakebite
print(f"CTD 聚合唯一基因: {len(agg)}")
print(f"新增: direct {len(new_direct)} | inferred>=50 {len(new_inf)} | snakebite例外 {len(new_snakebite)}")

# ---------- 3. mygene 映射 UniProt ----------
def mygene_map(symbols):
    out = {}
    url = "https://mygene.info/v3/query"
    for i in range(0, len(symbols), 400):
        batch = symbols[i:i+400]
        data = ("q=" + ",".join(batch) +
                "&scopes=symbol&fields=uniprot.Swiss-Prot,entrezgene&species=human").encode()
        req = urllib.request.Request(url, data=data, headers={"User-Agent": "Mozilla/5.0"})
        for attempt in range(3):
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    res = json.loads(resp.read())
                break
            except Exception as e:
                print(f"  mygene retry {attempt+1}: {e}")
                time.sleep(3)
        else:
            continue
        for item in res:
            q = item.get("query", "").upper()
            up = item.get("uniprot", {})
            ac = up.get("Swiss-Prot") if isinstance(up, dict) else None
            if isinstance(ac, list):
                ac = ac[0]
            out[q] = {"uniprot": ac or "", "entrez": str(item.get("entrezgene", ""))}
        time.sleep(0.5)
    return out

new_syms = [agg[k]["symbol"] for k in new_keys]
print(f"mygene 映射 {len(new_syms)} 个新基因 ...")
mg = mygene_map(new_syms)
print(f"  命中 {sum(1 for k in new_keys if mg.get(k,{}).get('uniprot'))}/{len(new_keys)}")

# ---------- 4. 更新总表 ----------
master["基因Symbol"] = master["基因Symbol"].astype(str)
idx = {s.upper(): i for i, s in enumerate(master["基因Symbol"])}
n_annot_exist = 0
for key, a in agg.items():
    if key not in idx:
        continue
    i = idx[key]
    s = ctd_str(a)
    if s:
        cur = master.at[i, "CTD inference"]
        if pd.isna(cur) or "待手工导出" in str(cur):
            master.at[i, "CTD inference"] = s
            n_annot_exist += 1
        src = str(master.at[i, "检索词来源"])
        add = ";".join(f"CTD:{t}" for t in sorted(a["terms"]))
        if "CTD:" not in src:
            master.at[i, "检索词来源"] = src.rstrip("；;") + "；" + add

rows = []
for key in new_keys:
    a = agg[key]
    is_direct = bool(a["direct"])
    uni = mg.get(key, {}).get("uniprot", "")
    entrez = a["geneid"] or mg.get(key, {}).get("entrez", "")
    remark = ""
    if is_direct:
        remark = "CTD direct evidence (" + "|".join(sorted(a["diseases"])) + ")"
    elif key in new_snakebite and a["inf_max"] < INF_THRESHOLD:
        remark = f"CTD inferred via {a['inf_chem']} (snakebite词全量收录例外)"
    else:
        remark = f"CTD inferred score>={INF_THRESHOLD:g} via {a['inf_chem']}"
    if not uni:
        remark += "；mygene未映射UniProt"
    rows.append({
        "基因Symbol": a["symbol"], "UniProt AC": uni, "Entrez ID": entrez,
        "GeneCards score": "", "DisGeNET score": "", "OMIM(有/无)": "",
        "CTD inference": ctd_str(a), "OpenTargets score": "", "OT疾病数": "",
        "DISEASES curated": "",
        "纳入主集(是/否)": "是" if is_direct else "否（宽集）",
        "归属病理轴(1-4)": "",
        "检索词来源": ";".join(f"CTD:{t}" for t in sorted(a["terms"])),
        "下载日期": TODAY, "备注": remark,
    })

master_new = pd.concat([master, pd.DataFrame(rows)], ignore_index=True)
master_new.to_csv(MASTER, index=False, encoding="utf-8-sig")
n_main = (master_new["纳入主集(是/否)"] == "是").sum()
n_broad = len(master_new) - n_main
print(f"\n总表更新: {len(master)} -> {len(master_new)} | 主集 {n_main} | 宽集 {n_broad}")
print(f"已有基因回填 CTD 注释: {n_annot_exist}")

# ---------- 5. 同步 Excel ----------
import openpyxl
wb = openpyxl.load_workbook(XLSX)
ws = wb["疾病基因管理表"]
ws.delete_rows(2, ws.max_row)
cols = list(master_new.columns)
for _, r in master_new.iterrows():
    ws.append(["" if pd.isna(v) else v for v in r[cols]])
log = wb["变更记录"]
log.append([TODAY, "v7",
            f"CTD 手工导出并入（6 词，疾病白名单过滤词扩展；direct 80 基因全在/入主集新增 {len(new_direct)}，"
            f"inferred>=50 新增 {len(new_inf)}，snakebite 词例外全量新增 {len(new_snakebite)}；"
            f"VICC 词 CTD 无收录（Object not found）如实记录；已有基因回填注释 {n_annot_exist} 条；"
            f"总 {len(master_new)}，主集 {n_main}，宽集 {n_broad}）", "用户导出+Kimi并入"])
wb.save(XLSX)
print("Excel 已同步 + 变更记录 v7")

# ---------- 6. 汇总输出 ----------
print("\n=== 文件级统计 ===")
for t, s in file_stats.items():
    print(f"  {t}: 原始行 {s['raw_rows']} | 白名单行 {s['whitelist_rows']} | 唯一基因 {s['uniq_genes']}" +
          (f" | [Object not found]" if s["notfound"] else ""))

print("\n=== 四轴先验分子 CTD 命中 ===")
ax = master_new[master_new["归属病理轴(1-4)"].notna()]
for _, r in ax.iterrows():
    c = r["CTD inference"]
    hit = "" if (pd.isna(c) or "待手工" in str(c)) else str(c)
    print(f"  {r['基因Symbol']:10s} {r['归属病理轴(1-4)']}  {hit}")

# 供报告使用的汇总
summary = {
    "file_stats": file_stats,
    "agg_genes": len(agg),
    "new_direct": sorted(agg[k]["symbol"] for k in new_direct),
    "n_new_inf": len(new_inf), "n_new_snakebite": len(new_snakebite),
    "total": len(master_new), "main": int(n_main), "broad": int(n_broad),
    "annotated_existing": n_annot_exist,
}
with open(os.path.join(ROOT, r"02_disease_genes\ctd_merge_summary.json"), "w", encoding="utf-8") as fo:
    json.dump(summary, fo, ensure_ascii=False, indent=2)
print("\nsummary -> ctd_merge_summary.json")
