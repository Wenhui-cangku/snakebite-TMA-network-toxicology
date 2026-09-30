# -*- coding: utf-8 -*-
"""
Phase 2 - toxin–human-target edge table construction (L2 literature curated + L4 STRING neighbors)
L1: CTD/T3DB require manual export (ALTCHA anti-scraping); to be appended after user export
L2: structured UniProt/Swiss-Prot curated annotations (43 entries) + PubMed corroboration (Daboxin P / RVVA-PLA2-I / daborhagin / SPAD-1)
L3: BLAST homology support — no local blastp binary; postponed this round (see report)
L4: STRING interaction_partners score>=0.7 first-shell neighbors
Output: 03_target_prediction/toxin_target_edges.csv + Phase2_report.md + Excel target_edges sheet + change log v9
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
fam_map = dict(zip(tox["UniProt ID"], tox["toxin_family"]))
tid_map = dict(zip(tox["UniProt ID"], tox["entry_id"]))

# ---------------- L2 structured curated edges ----------------
# (toxin_ac, target, detail, pmids_override or None, score)
L2 = [
    # PLA2
    ("P59071", "F10", "binds FXa and inhibits prothrombinase activity (IC50=130 nM)", "18062812", 1.0),
    ("C0HK16", "F10", "binds FX/FXa for anticoagulant activity (UniProt curated)", None, 1.0),
    ("PLA2_family", "F10", "Family-level literature: Daboxin P (major PLA2 of Indian D. russelii) targets FX for anticoagulation", "27089306", 0.6),
    ("PLA2_family", "F10", "Family-level literature: acidic RVVA-PLA2-I anticoagulant (purified from D. russelii)", "21356226", 0.6),
    # snaclec/CTL (RVV-X)
    ("Q4PRD1", "F10", "RVV-X light chain 1: recognizes and binds the FX Gla domain (Ca2+-dependent)", None, 1.0),
    ("Q4PRD1", "F9", "RVV-X light chain 1: recognizes and binds the FIX Gla domain", None, 1.0),
    ("Q4PRD2", "F10", "RVV-X light chain 2: recognizes and binds the FX Gla domain (Ca2+-dependent)", None, 1.0),
    ("Q4PRD2", "F9", "RVV-X light chain 2: recognizes and binds the FIX Gla domain", None, 1.0),
    ("Q7LZ61", "F10", "RVV-X heavy chain: cleaves the Arg-Ile bond to activate FX", "37092784;18616470;1629211;8144654;8639544;18060879;11910189", 1.0),
    ("Q7LZ61", "F9", "RVV-X heavy chain: cleaves the Arg-Ile bond to activate FIX", None, 1.0),
    ("Q7LZ61", "PROS1", "RVV-X heavy chain: specifically cleaves and activates protein S", None, 1.0),
    ("Q4PRD1", "PROS1", "RVV-X complex: cleaves and activates protein S", None, 0.8),
    ("Q4PRD2", "PROS1", "RVV-X complex: cleaves and activates protein S", None, 0.8),
    ("Q38L02", "GP1BA", "binds platelet GPIbalpha and inhibits ristocetin-induced aggregation", None, 1.0),
    # SVMP
    ("B8K1W0", "FGA", "daborhagin-K (P-III hemorrhagic SVMP): hydrolyzes the fibrinogen Aalpha chain", "18554518;28042812", 1.0),
    ("B8K1W0", "FN1", "daborhagin-M/K: hydrolyzes fibronectin in vitro", "18554518", 1.0),
    ("B8K1W0", "COL4A1", "daborhagin-M/K: hydrolyzes type IV collagen in vitro", "18554518", 1.0),
    ("AAZ39880.1", "FGA", "russelysin = same protein as daborhagin-K (GenBank supplementary entry): hydrolyzes the fibrinogen Aalpha chain", "18554518;28042812", 0.9),
    ("AAZ39880.1", "FN1", "russelysin: hydrolyzes fibronectin", "18554518", 0.9),
    ("AAZ39880.1", "COL4A1", "russelysin: hydrolyzes type IV collagen", "18554518", 0.9),
    ("A0A2H4Z2X6", "FN1", "Family-level corroboration: RVV-derived SPAD-1 (HGD-disintegrin) disrupts fibronectin-matrix adhesion", "36423674", 0.6),
    ("A0A2H4Z2Y1", "FN1", "Family-level corroboration: RVV-derived SPAD-1 (HGD-disintegrin) disrupts fibronectin-matrix adhesion", "36423674", 0.6),
    # SVSP
    ("P18965", "F5", "RVV-V gamma: cleaves human FV Arg1545-Ser1546 for activation (Ca2+-independent)", "21640745;3053712;20054136;21871889;28732041", 1.0),
    ("P18964", "F5", "RVV-V: cleaves human FV Arg1545-Ser1546 for activation", "21640745;21871889;28732041", 1.0),
    ("E5L0E3", "FGA", "SVSP: degrades the fibrinogen alpha chain; strong caseinolytic activity", None, 1.0),
    ("E5L0E4", "FGB", "SVSP: hydrolyzes the fibrinogen beta chain", None, 1.0),
    # Kunitz
    ("H6VC06", "PLG", "inhibits plasmin 90% (Ki=0.19 nM)", None, 1.0),
    ("H6VC06", "F11", "inhibits FXIa 37% (Ki=6 nM)", None, 1.0),
    ("H6VC06", "F10", "inhibits FXa 20%", None, 1.0),
    ("H6VC06", "PRSS1", "inhibits trypsin 70%", None, 1.0),
    ("H6VC05", "PROC", "inhibits activated protein C (APC) IC50=3.5 nM (in presence of heparin)", None, 1.0),
    ("H6VC05", "F11", "inhibits FXIa 40% (in presence of heparin)", None, 1.0),
    ("H6VC05", "PLG", "inhibits plasmin 70% (in presence of heparin)", None, 1.0),
    ("H6VC05", "PRSS1", "inhibits trypsin 45% (in presence of heparin)", None, 1.0),
    ("A8Y7P1", "CTRB1", "inhibits chymotrypsin (Ki=4.77 nM)", None, 1.0),
    ("A8Y7N4", "PRSS1", "inhibits trypsin", None, 1.0),
    ("A8Y7N8", "PRSS1", "inhibits trypsin", None, 1.0),
    ("A8Y7P0", "PRSS1", "inhibits trypsin", None, 1.0),
    ("A8Y7P2", "PRSS1", "inhibits trypsin", None, 1.0),
    ("A8Y7P6", "PRSS1", "inhibits trypsin", None, 1.0),
    ("A8Y7N5", "PLG", "inhibits plasmin and trypsin", None, 1.0),
    ("A8Y7N5", "PRSS1", "inhibits plasmin and trypsin", None, 1.0),
    ("A8Y7P3", "PLG", "inhibits plasmin and trypsin", None, 1.0),
    ("A8Y7P3", "PRSS1", "inhibits plasmin and trypsin", None, 1.0),
    ("A8Y7P4", "PLG", "inhibits plasmin and trypsin", None, 1.0),
    ("A8Y7P4", "PRSS1", "inhibits plasmin and trypsin", None, 1.0),
    # VEGF / NGF
    ("P67861", "KDR", "induces angiogenesis via VEGFR-2 (KDR) signaling; NO-mediated hypotension", None, 1.0),
    ("P0DL42", "KDR", "induces angiogenesis via VEGFR-2 (KDR) signaling; NO-mediated hypotension", None, 1.0),
    ("P30894", "GP1BA", "By similarity: inhibits metalloprotease proteolysis of platelet GPIbalpha (indirect protection)", None, 0.5),
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
                 "download_date": TODAY})

# ---------------- L4 STRING neighbors ----------------
targets = sorted({r[1] for r in L2})
print("L2 edges:", len(rows), "| unique targets:", len(targets), targets)

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

print("\nfetching STRING first-shell neighbors (limit=10, score>=0.7) ...")
nb_map = {}
for t in targets:
    nb = string_partners(t)
    nb_map[t] = [(b, s) for a, b, s in nb if a == t or b != t]
    nb_map[t] = [(b if a == t else a, s) for a, b, s in nb]
    print(f"  {t}: {len(nb_map[t])} neighbors")
    time.sleep(0.5)

n_l4 = 0
seen = set()
for ac, tgt, detail, pm, score in L2:
    if score < 0.8:   # expand only for direct curated targets
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
                     "evidence_detail": f"STRING first-shell neighbor, via {tgt} (combined score={s:.3f})",
                     "pmids": "", "score": round(s, 3), "download_date": TODAY})
        n_l4 += 1
print("L4 edges:", n_l4)

edges = pd.DataFrame(rows)
edges.to_csv(os.path.join(TP, "toxin_target_edges.csv"), index=False, encoding="utf-8-sig")
print("\ntotal:", len(edges), "edges ->", "toxin_target_edges.csv")
print(edges["evidence_type"].value_counts().to_dict())

# QC: L2 edge counts of core families
lit = edges[edges["evidence_type"] == "literature"]
for f in ["SVMP/disintegrin", "SVSP", "PLA2", "snaclec/CTL"]:
    print(f"QC {f}: L2 edges {len(lit[lit['family']==f])} (require >=3)")

# family-level notes (families without edges)
notes = {
    "CRISP": "No curated human targets for the 4 CRISPs; serotriflin binds the snake's own serum SSP-2 (PMID 18222185, non-human target)",
    "LAAO": "The 2 LAAOs affect platelet aggregation via H2O2 generation (PMID 21802487); no single protein target",
    "NGF": "P30894 indirectly protects GP1BA (By similarity); recorded as a 0.5-score weak edge",
}
json.dump({"nb_map": {k: v for k, v in nb_map.items()}, "family_notes": notes},
          open(os.path.join(TP, "phase2_string_neighbors.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("neighbor archive -> phase2_string_neighbors.json")
