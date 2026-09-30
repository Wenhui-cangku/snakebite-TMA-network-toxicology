# -*- coding: utf-8 -*-
"""
Phase 1B - merging CTD data into the disease-gene master table
Input: CTD/*.tsv (6 batch-query manual exports)
Rules:
  1. disease-whitelist filtering (removes irrelevant diseases brought in by CTD term expansion, e.g. congenital hemolytic anemia/thalassemia/ITP)
  2. non-empty DirectEvidence -> core set
  3. InferenceScore only: >=50 -> wide set; snakebite envenoming query exception (only 57 genes, all highly relevant — all into the wide set)
  4. CTD inference column format: direct:<type> or inferred:<maxscore>
  5. new genes mapped to UniProt AC via mygene.info
Output: updates disease_gene_master.csv + data_management_table_public.xlsx + change log v7
"""
from pathlib import Path
import pandas as pd
import glob, os, json, time, urllib.request

ROOT = Path(__file__).resolve().parents[1]  # repo root (snakebite_TMA/)
MASTER = os.path.join(ROOT, r"02_disease_genes\disease_gene_master.csv")
XLSX = os.path.join(ROOT, r"00_protocol\data_management_table_public.xlsx")
TODAY = "2026-09-22"
INF_THRESHOLD = 50.0

# disease whitelist: keep only CTD disease entries directly matching the project pathology axes
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

# ---------- 1. parse CTD ----------
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

# CTD annotation string
def ctd_str(a):
    if a["direct"]:
        return "direct:" + "|".join(sorted(a["direct"]))
    if a["inf_max"] > 0:
        return f"inferred:{a['inf_max']:.2f}"
    return ""

# ---------- 2. decide new-gene inclusion ----------
master = pd.read_csv(MASTER, encoding="utf-8-sig")
msym = set(master["gene_symbol"].str.upper())

new_direct, new_inf, new_snakebite = [], [], []
for key, a in agg.items():
    if key in msym:
        continue
    if a["direct"]:
        new_direct.append(key)
    elif a["inf_max"] >= INF_THRESHOLD:
        new_inf.append(key)
    elif a["terms"] == {"snakebite"} or "snakebite" in a["terms"]:
        # snakebite-query exception: full inclusion (max 8.85, inferred via Bungarotoxins/Glutamine)
        new_snakebite.append(key)

new_keys = new_direct + new_inf + new_snakebite
print(f"CTD aggregated unique genes: {len(agg)}")
print(f"new: direct {len(new_direct)} | inferred>=50 {len(new_inf)} | snakebite exception {len(new_snakebite)}")

# ---------- 3. mygene mapping to UniProt ----------
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
print(f"mygene mapping {len(new_syms)} new genes ...")
mg = mygene_map(new_syms)
print(f"  hits {sum(1 for k in new_keys if mg.get(k,{}).get('uniprot'))}/{len(new_keys)}")

# ---------- 4. update master table ----------
master["gene_symbol"] = master["gene_symbol"].astype(str)
idx = {s.upper(): i for i, s in enumerate(master["gene_symbol"])}
n_annot_exist = 0
for key, a in agg.items():
    if key not in idx:
        continue
    i = idx[key]
    s = ctd_str(a)
    if s:
        cur = master.at[i, "CTD inference"]
        if pd.isna(cur) or "pending manual export" in str(cur):
            master.at[i, "CTD inference"] = s
            n_annot_exist += 1
        src = str(master.at[i, "query_source"])
        add = ";".join(f"CTD:{t}" for t in sorted(a["terms"]))
        if "CTD:" not in src:
            master.at[i, "query_source"] = src.rstrip("；;") + ";" + add

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
        remark = f"CTD inferred via {a['inf_chem']} (full-inclusion exception for the snakebite query)"
    else:
        remark = f"CTD inferred score>={INF_THRESHOLD:g} via {a['inf_chem']}"
    if not uni:
        remark += "; mygene did not map to UniProt"
    rows.append({
        "gene_symbol": a["symbol"], "UniProt AC": uni, "Entrez ID": entrez,
        "GeneCards score": "", "DisGeNET score": "", "OMIM(yes/no)": "",
        "CTD inference": ctd_str(a), "OpenTargets score": "", "OT_disease_count": "",
        "DISEASES curated": "",
        "in_core_set(yes/no)": "yes" if is_direct else "no (wide set)",
        "pathology_axis(1-4)": "",
        "query_source": ";".join(f"CTD:{t}" for t in sorted(a["terms"])),
        "download_date": TODAY, "notes": remark,
    })

master_new = pd.concat([master, pd.DataFrame(rows)], ignore_index=True)
master_new.to_csv(MASTER, index=False, encoding="utf-8-sig")
n_main = (master_new["in_core_set(yes/no)"] == "yes").sum()
n_broad = len(master_new) - n_main
print(f"\nmaster table updated: {len(master)} -> {len(master_new)} | core {n_main} | wide {n_broad}")
print(f"existing genes back-filled with CTD annotations: {n_annot_exist}")

# ---------- 5. sync Excel ----------
import openpyxl
wb = openpyxl.load_workbook(XLSX)
ws = wb["disease_genes"]
ws.delete_rows(2, ws.max_row)
cols = list(master_new.columns)
for _, r in master_new.iterrows():
    ws.append(["" if pd.isna(v) else v for v in r[cols]])
log = wb["changelog"]
log.append([TODAY, "v7",
            f"CTD manual export merged (6 queries, disease-whitelist filter terms expanded; direct 80 genes all present / {len(new_direct)} new into core, "
            f"inferred>=50 added {len(new_inf)}, snakebite-query exception added all {len(new_snakebite)}; "
            f"VICC query not catalogued in CTD (Object not found), recorded as-is; annotations back-filled for {n_annot_exist} existing genes; "
            f"total {len(master_new)}, core {n_main}, wide {n_broad})", "user export + Kimi merge"])
wb.save(XLSX)
print("Excel synced + change log v7")

# ---------- 6. summary output ----------
print("\n=== file-level statistics ===")
for t, s in file_stats.items():
    print(f"  {t}: raw rows {s['raw_rows']} | whitelist rows {s['whitelist_rows']} | unique genes {s['uniq_genes']}" +
          (f" | [Object not found]" if s["notfound"] else ""))

print("\n=== CTD hits of four-axis prior molecules ===")
ax = master_new[master_new["pathology_axis(1-4)"].notna()]
for _, r in ax.iterrows():
    c = r["CTD inference"]
    hit = "" if (pd.isna(c) or "pending manual" in str(c)) else str(c)
    print(f"  {r['gene_symbol']:10s} {r['pathology_axis(1-4)']}  {hit}")

# summary for the report
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
