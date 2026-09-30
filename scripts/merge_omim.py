# -*- coding: utf-8 -*-
"""
Phase 1B - merging the OMIM API into the disease-gene master table
Input: omim_entries_raw.json (44 entries fetched) + omim_search_mims.json
Rules:
  1. phenotype whitelist (only aHUS/HUS/TTP/complement-deficiency/cobalamin-metabolism-related TMA; removes retrieval noise such as AGS/macular degeneration/immunodeficiency)
  2. all mappingKey=3 (molecular basis known) -> core set
  3. OMIM(yes/no) column set to "yes"; new genes mapped to UniProt via mygene
Output: updates disease_gene_master.csv + Excel + change log v8
"""
from pathlib import Path
import pandas as pd
import json, os, time, urllib.request

ROOT = Path(__file__).resolve().parents[1]  # repo root (snakebite_TMA/)
MASTER = os.path.join(ROOT, r"02_disease_genes\disease_gene_master.csv")
XLSX = os.path.join(ROOT, r"00_protocol\data_management_table_public.xlsx")
TODAY = "2026-09-24"

# phenotype whitelist MIM -> short name
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
        print("!! missing entry", mim)
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

print(f"OMIM whitelist genes: {len(gene2mims)}")
for k, v in sorted(gene2mims.items()):
    print(f"  {v['symbol']:12s} <- {sorted(v['mims'])}")

master = pd.read_csv(MASTER, encoding="utf-8-sig")
idx = {s.upper(): i for i, s in enumerate(master["gene_symbol"].astype(str))}

new_keys = [k for k in gene2mims if k not in idx]
print(f"\nalready in library: {len(gene2mims)-len(new_keys)} | new: {len(new_keys)}")

# mygene mapping of new genes
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

# update existing rows
n_fill = 0
for k, v in gene2mims.items():
    if k not in idx:
        continue
    i = idx[k]
    cur = str(master.at[i, "OMIM(yes/no)"]) if pd.notna(master.at[i, "OMIM(yes/no)"]) else ""
    if cur != "yes":
        master.at[i, "OMIM(yes/no)"] = "yes"
        n_fill += 1
    if master.at[i, "in_core_set(yes/no)"] != "yes":
        master.at[i, "in_core_set(yes/no)"] = "yes"
        print(f"  promoted to core: {v['symbol']}")
    src = str(master.at[i, "query_source"])
    if "OMIM" not in src:
        master.at[i, "query_source"] = src.rstrip("；;") + ";OMIM"

# new rows
rows = []
for k in new_keys:
    v = gene2mims[k]
    uni = mg.get(k, {}).get("uniprot", "")
    rows.append({
        "gene_symbol": v["symbol"], "UniProt AC": uni,
        "Entrez ID": v["entrez"] or mg.get(k, {}).get("entrez", ""),
        "GeneCards score": "", "DisGeNET score": "", "OMIM(yes/no)": "yes",
        "CTD inference": "", "OpenTargets score": "", "OT_disease_count": "",
        "DISEASES curated": "", "in_core_set(yes/no)": "yes", "pathology_axis(1-4)": "",
        "query_source": "OMIM", "download_date": TODAY,
        "notes": f"OMIM curated mappingKey3 ({'|'.join(sorted(v['mims']))})" + ("" if uni else "; mygene did not map to UniProt"),
    })

master_new = pd.concat([master, pd.DataFrame(rows)], ignore_index=True)
master_new.to_csv(MASTER, index=False, encoding="utf-8-sig")
n_main = (master_new["in_core_set(yes/no)"] == "yes").sum()
print(f"\nmaster table: {len(master)} -> {len(master_new)} | core {n_main} | wide {len(master_new)-n_main}")
print(f"existing genes back-filled in the OMIM column: {n_fill}")

# Excel sync
import openpyxl
wb = openpyxl.load_workbook(XLSX)
ws = wb["disease_genes"]
ws.delete_rows(2, ws.max_row)
cols = list(master_new.columns)
for _, r in master_new.iterrows():
    ws.append(["" if pd.isna(v) else v for v in r[cols]])
wb["changelog"].append([TODAY, "v8",
    f"OMIM API merged (user-provided key; 5 disease queries, 44 entries, phenotype whitelist 14 MIM entries, "
    f"mappingKey=3 giving {len(gene2mims)} unique genes; {len(gene2mims)-len(new_keys)} already in library as cross-confirmation, {len(new_keys)} new all into core; "
    f"snakebite/VICC have no OMIM entries, recorded as-is; total {len(master_new)}, core {n_main}, wide {len(master_new)-n_main})",
    "Kimi"])
wb.save(XLSX)
print("Excel synced + change log v8")

json.dump({k: {"symbol": v["symbol"], "mims": sorted(v["mims"])} for k, v in gene2mims.items()},
          open(os.path.join(ROOT, r"02_disease_genes\omim_merge_summary.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print("summary -> omim_merge_summary.json")
