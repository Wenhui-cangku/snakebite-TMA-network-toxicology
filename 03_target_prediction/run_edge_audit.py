# -*- coding: utf-8 -*-
"""
Edge-level evidence audit for the public analysis archive.
Every one of the 49 literature-annotated rows was read individually and assigned:
interaction_type (direct_binding / enzymatic_cleavage / inhibition / activation /
family_extrapolation / annotation_inference), evidence_channel, protein_state,
independent toxin entity (RVV-X chains merged; russelysin = daborhagin-K deduped),
and flags. STRING rows are labelled annotation_inference and excluded from curated counts.
Row-index mapping below is the audit trail (row id = index in toxin_target_edges.csv).
"""
import os
from pathlib import Path

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
BASE = SCRIPT_DIR.parent
e = pd.read_csv(SCRIPT_DIR / "toxin_target_edges.csv")
mt = pd.read_csv(BASE / "01_toxin_lib" / "toxin_library.csv")
name_of = dict(zip(mt["toxin_id"], mt["toxin_name"]))
sp_of = dict(zip(mt["toxin_id"], mt["species"]))

# row: (interaction_type, channel, protein_state, flags)
A = {
 0:  ("inhibition", "primary_literature", "FXa (active enzyme)", "IC50=130 nM; binding to FXa documented"),
 1:  ("direct_binding", "primary_literature", "FX and FXa", "UniProt-curated binding"),
 2:  ("family_extrapolation", "family_level", "FX", "family-level literature"),
 3:  ("family_extrapolation", "family_level", "FX", "family-level literature"),
 4:  ("direct_binding", "primary_literature", "FX zymogen (Gla domain)", "RVV-X light chain 1; Ca2+-dependent"),
 5:  ("direct_binding", "primary_literature", "FIX zymogen (Gla domain)", "RVV-X light chain 1"),
 6:  ("direct_binding", "primary_literature", "FX zymogen (Gla domain)", "RVV-X light chain 2; Ca2+-dependent"),
 7:  ("direct_binding", "primary_literature", "FIX zymogen (Gla domain)", "RVV-X light chain 2"),
 8:  ("enzymatic_cleavage", "primary_literature", "FX zymogen -> FXa (activation)", "RVV-X heavy chain; Arg-Ile cleavage"),
 9:  ("enzymatic_cleavage", "primary_literature", "FIX zymogen -> FIXa (activation)", "RVV-X heavy chain"),
 10: ("enzymatic_cleavage", "primary_literature", "protein S (cleavage/activation)", "RVV-X heavy chain"),
 11: ("enzymatic_cleavage", "primary_literature", "protein S", "complex-level evidence attributed to light chain; attribution uncertain"),
 12: ("enzymatic_cleavage", "primary_literature", "protein S", "complex-level evidence attributed to light chain; attribution uncertain"),
 13: ("direct_binding", "primary_literature", "platelet GPIb alpha", "dabocetin; inhibits ristocetin-induced aggregation (functional readout)"),
 14: ("enzymatic_cleavage", "primary_literature", "fibrinogen A-alpha chain (degradation)", "daborhagin-K"),
 15: ("enzymatic_cleavage", "primary_literature", "fibronectin (degradation)", "daborhagin-M/K"),
 16: ("enzymatic_cleavage", "primary_literature", "collagen IV (degradation)", "daborhagin-M/K"),
 17: ("enzymatic_cleavage", "primary_literature", "fibrinogen A-alpha chain (degradation)", "DUPLICATE: russelysin = daborhagin-K (same protein)"),
 18: ("enzymatic_cleavage", "primary_literature", "fibronectin (degradation)", "DUPLICATE: russelysin = daborhagin-K"),
 19: ("enzymatic_cleavage", "primary_literature", "collagen IV (degradation)", "DUPLICATE: russelysin = daborhagin-K"),
 20: ("family_extrapolation", "family_level", "fibronectin matrix", "SPAD-1 family-level supporting evidence"),
 21: ("family_extrapolation", "family_level", "fibronectin matrix", "SPAD-1 family-level supporting evidence"),
 22: ("enzymatic_cleavage", "primary_literature", "FV zymogen -> FVa (Arg1545-Ser1546)", "RVV-V gamma"),
 23: ("enzymatic_cleavage", "primary_literature", "FV zymogen -> FVa", "RVV-V"),
 24: ("enzymatic_cleavage", "primary_literature", "fibrinogen alpha chain (degradation)", "SVSP"),
 25: ("enzymatic_cleavage", "primary_literature", "fibrinogen beta chain (degradation)", "SVSP"),
 26: ("inhibition", "primary_literature", "plasmin (ACTIVE enzyme, not plasminogen)", "Ki=0.19 nM; 90% inhibition"),
 27: ("inhibition", "primary_literature", "FXIa (active enzyme)", "Ki=6 nM; 37% inhibition"),
 28: ("inhibition", "primary_literature", "FXa (active enzyme)", "20% inhibition"),
 29: ("inhibition", "primary_literature", "trypsin (active enzyme)", "70% inhibition"),
 30: ("inhibition", "primary_literature", "activated protein C (APC)", "IC50=3.5 nM, heparin-dependent"),
 31: ("inhibition", "primary_literature", "FXIa (active enzyme)", "40%, heparin-dependent"),
 32: ("inhibition", "primary_literature", "plasmin (ACTIVE enzyme)", "70%, heparin-dependent"),
 33: ("inhibition", "primary_literature", "trypsin (active enzyme)", "45%, heparin-dependent"),
 34: ("inhibition", "primary_literature", "chymotrypsin (active enzyme)", "Ki=4.77 nM"),
 46: ("activation", "primary_literature", "VEGFR-2 (cell-surface receptor)", "ligand-receptor signalling; angiogenesis; NO-mediated hypotension"),
 47: ("activation", "primary_literature", "VEGFR-2 (cell-surface receptor)", "ligand-receptor signalling"),
 48: ("annotation_inference", "by_similarity", "platelet GPIb alpha (indirect protection)", "By similarity; indirect anti-proteolysis, NOT a direct target"),
}
for i in range(35, 46):
    A[i] = ("annotation_inference", "uniprot_annotation_no_pmid",
            "trypsin / plasmin (active enzymes)" if i != 40 and i != 42 and i != 44 else "plasmin (ACTIVE enzyme) / trypsin",
            "NO PMID on record: UniProt annotation only; must not count as literature-curated evidence")

# independent toxin entity: RVV-X chains are one complex; russelysin = daborhagin-K
entity = {"T059": "RVV-X complex", "T060": "RVV-X complex", "T061": "RVV-X complex",
          "T025": "daborhagin-K", "T026": "daborhagin-K"}

rows = []
for i, r in e.iterrows():
    d = r.to_dict()
    d["edge_id"] = i
    d["toxin_name"] = name_of.get(r["toxin_id"], r["toxin_id"])
    d["species"] = sp_of.get(r["toxin_id"], "")
    d["independent_toxin_entity"] = entity.get(r["toxin_id"], r["toxin_id"])
    if r["evidence_type"] == "string":
        d.update(interaction_type="annotation_inference", evidence_channel="STRING_neighborhood",
                 protein_state="", audit_flags="STRING expansion; excluded from curated evidence counts",
                 has_pmid=False)
    else:
        t, ch, st, fl = A[i]
        d.update(interaction_type=t, evidence_channel=ch, protein_state=st, audit_flags=fl,
                 has_pmid=pd.notna(r["pmids"]))
    rows.append(d)

out = pd.DataFrame(rows)
cols = ["edge_id","toxin_id","toxin_name","independent_toxin_entity","family","species","target_symbol",
        "interaction_type","evidence_channel","protein_state","pmids","has_pmid","score","audit_flags","evidence_detail"]
out = out[cols + [c for c in out.columns if c not in cols]]
output_path = Path(os.environ.get("EDGE_OUT", SCRIPT_DIR / "toxin_target_edges_audited.csv")).resolve()
output_path.parent.mkdir(parents=True, exist_ok=True)
out.to_csv(output_path, index=False, encoding="utf-8-sig")

lit = out[out['evidence_type'] == 'literature'] if 'evidence_type' in out else out[out['evidence_channel'] != 'STRING_neighborhood']
lit = out[out['evidence_channel'] != 'STRING_neighborhood']
print("=== channel counts (49 literature-annotated rows) ===")
print(lit['evidence_channel'].value_counts().to_string())
print("\n=== interaction_type among primary_literature edges ===")
prim = lit[lit['evidence_channel'] == 'primary_literature']
print(prim['interaction_type'].value_counts().to_string())
print("primary edges:", len(prim))
print("\n=== targets retaining >=1 primary-literature edge ===")
print(sorted(prim['target_symbol'].unique()), "n =", prim['target_symbol'].nunique())

print("\n=== F10 convergence reassessment ===")
f10 = lit[lit['target_symbol'] == 'F10']
for ch in ['primary_literature','family_level','uniprot_annotation_no_pmid','by_similarity']:
    sub = f10[f10['evidence_channel'] == ch]
    if len(sub):
        print("%s: %d edges | types=%s | independent entities=%s" %
              (ch, len(sub), dict(sub['interaction_type'].value_counts()),
               sorted(set(sub['independent_toxin_entity']))))
f10p = f10[f10['evidence_channel'] == 'primary_literature']
print("F10 primary edges:", len(f10p), "| independent toxin entities:", sorted(set(f10p['independent_toxin_entity'])))
print("F10 by type:", dict(f10p['interaction_type'].value_counts()))
print("\nPLG primary edges protein_state check:")
print(lit[(lit['target_symbol']=='PLG') & (lit['evidence_channel']=='primary_literature')][['toxin_id','protein_state']].to_string(index=False))
