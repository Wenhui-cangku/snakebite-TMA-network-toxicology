# -*- coding: utf-8 -*-
"""
Phase 1B - OMIM API 并入疾病基因总表
输入: omim_entries_raw.json (44 条目已抓取) + omim_search_mims.json
规则:
  1. 表型白名单(仅 aHUS/HUS/TTP/补体缺陷/钴胺素代谢障碍相关 TMA, 剔除 AGS/黄斑变性/免疫缺陷等检索噪声)
  2. 全部 mappingKey=3(分子基础已知) -> 纳入主集
  3. OMIM(有/无) 列写 "有"; 新基因 mygene 映射 UniProt
输出: 更新 disease_gene_master.csv + Excel + 变更记录 v8
"""
from pathlib import Path
import pandas as pd
import json, os, time, urllib.request

ROOT = Path(__file__).resolve().parents[1]  # repo root (snakebite_TMA/)
MASTER = os.path.join(ROOT, r"02_disease_genes\disease_gene_master.csv")
XLSX = os.path.join(ROOT, r"00_protocol\data_management_table.xlsx")
TODAY = "2026-09-24"

# 表型白名单 MIM -> 简称
WL = {
    "235400": "AHUS1", "612922": "AHUS2", "612923": "AHUS3", "612924": "AHUS4",
    "612925": "AHUS5", "612926": "AHUS6", "615008": "AHUS7/NPHS7", "301110": "AHUS8",
    "274150": "TTP", "609814": "CFHD", "610984": "CFID",
    "612300": "CD59-HAA", "277400": "cblC", "250940": "cblG",
}

entries = json.load(open(os.path.join(ROOT, r"02_disease_genes\omim_entries_raw.json")))

gene2mims = {}
for mim in WL:
    e = entries.get(mim)
    if not e:
        print("!! 缺失条目", mim)
        continue
    for g in e.get("phenotypeMapList", []):
        pm = g["phenotypeMap"]
        if int(pm.get("phenotypeMappingKey", 0)) != 3:
            continue
        sym = pm.get("approvedGeneSymbols", "").split(",")[0].strip()
        if not sym:
            continue
        gene2mims.setdefault(sym.upper(), {"symbol": sym, "mims": set(), "entrez": pm.get("geneIDs", "")})
        gene2mims[sym.upper()]["mims"].add(WL[mim])

print(f"OMIM 白名单基因: {len(gene2mims)}")
for k, v in sorted(gene2mims.items()):
    print(f"  {v['symbol']:12s} <- {sorted(v['mims'])}")

master = pd.read_csv(MASTER, encoding="utf-8-sig")
idx = {s.upper(): i for i, s in enumerate(master["基因Symbol"].astype(str))}

new_keys = [k for k in gene2mims if k not in idx]
print(f"\n已在库: {len(gene2mims)-len(new_keys)} | 新增: {len(new_keys)}")

# mygene 映射新基因
def mygene_map(symbols):
    out = {}
    data = ("q=" + ",".join(symbols) +
            "&scopes=symbol&fields=uniprot.Swiss-Prot,entrezgene&species=human").encode()
    req = urllib.request.Request("https://mygene.info/v3/query", data=data,
                                 headers={"User-Agent": "Mozilla/5.0"})
    for att in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                res = json.loads(resp.read())
            break
        except Exception as e:
            print("  mygene retry", att+1, e); time.sleep(3)
    else:
        return out
    for item in res:
        up = item.get("uniprot", {})
        ac = up.get("Swiss-Prot") if isinstance(up, dict) else None
        if isinstance(ac, list):
            ac = ac[0]
        out[item.get("query", "").upper()] = {"uniprot": ac or "", "entrez": str(item.get("entrezgene", ""))}
    return out

mg = mygene_map([gene2mims[k]["symbol"] for k in new_keys]) if new_keys else {}

# 更新已有行
n_fill = 0
for k, v in gene2mims.items():
    if k not in idx:
        continue
    i = idx[k]
    cur = str(master.at[i, "OMIM(有/无)"]) if pd.notna(master.at[i, "OMIM(有/无)"]) else ""
    if cur != "有":
        master.at[i, "OMIM(有/无)"] = "有"
        n_fill += 1
    if master.at[i, "纳入主集(是/否)"] != "是":
        master.at[i, "纳入主集(是/否)"] = "是"
        print(f"  提主集: {v['symbol']}")
    src = str(master.at[i, "检索词来源"])
    if "OMIM" not in src:
        master.at[i, "检索词来源"] = src.rstrip("；;") + "；OMIM"

# 新行
rows = []
for k in new_keys:
    v = gene2mims[k]
    uni = mg.get(k, {}).get("uniprot", "")
    rows.append({
        "基因Symbol": v["symbol"], "UniProt AC": uni,
        "Entrez ID": v["entrez"] or mg.get(k, {}).get("entrez", ""),
        "GeneCards score": "", "DisGeNET score": "", "OMIM(有/无)": "有",
        "CTD inference": "", "OpenTargets score": "", "OT疾病数": "",
        "DISEASES curated": "", "纳入主集(是/否)": "是", "归属病理轴(1-4)": "",
        "检索词来源": "OMIM", "下载日期": TODAY,
        "备注": f"OMIM curated mappingKey3 ({'|'.join(sorted(v['mims']))})" + ("" if uni else "；mygene未映射UniProt"),
    })

master_new = pd.concat([master, pd.DataFrame(rows)], ignore_index=True)
master_new.to_csv(MASTER, index=False, encoding="utf-8-sig")
n_main = (master_new["纳入主集(是/否)"] == "是").sum()
print(f"\n总表: {len(master)} -> {len(master_new)} | 主集 {n_main} | 宽集 {len(master_new)-n_main}")
print(f"已有基因 OMIM 列回填: {n_fill}")

# Excel 同步
import openpyxl
wb = openpyxl.load_workbook(XLSX)
ws = wb["疾病基因管理表"]
ws.delete_rows(2, ws.max_row)
cols = list(master_new.columns)
for _, r in master_new.iterrows():
    ws.append(["" if pd.isna(v) else v for v in r[cols]])
wb["变更记录"].append([TODAY, "v8",
    f"OMIM API 并入（用户提供 Key；5 病词检索 44 条目，表型白名单 14 个 MIM 条目，"
    f"mappingKey=3 共 {len(gene2mims)} 唯一基因；{len(gene2mims)-len(new_keys)} 已在库交叉印证、新增 {len(new_keys)} 条全部入主集；"
    f"snakebite/VICC 在 OMIM 无条目如实记录；总 {len(master_new)}，主集 {n_main}，宽集 {len(master_new)-n_main}）",
    "Kimi"])
wb.save(XLSX)
print("Excel 已同步 + 变更记录 v8")

json.dump({k: {"symbol": v["symbol"], "mims": sorted(v["mims"])} for k, v in gene2mims.items()},
          open(os.path.join(ROOT, r"02_disease_genes\omim_merge_summary.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print("summary -> omim_merge_summary.json")
