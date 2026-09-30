# Phase 1B Build Report: Disease-Gene Set (v1)

**Date**: 2026-09-22　**Protocol**: v2 revised §2.4 + SOP Phase 1B

## 1. Process counts (PRISMA gene line)

| Step | n |
|---|---|
| Open Targets search (8 MONDO disease entries: TMA, TTP×3, aHUS×3, HUS; score≥0.05) | 2,014 records → 741 unique genes |
| DISEASES knowledge (curated channel) supplement | 15 core genes (complement CFH/CFI/CFB/C3/CD46/CFHR1/3/5, THBD, DGKE, ADAMTS13 etc.; all already covered by or merged into OT) |
| mygene normalisation (symbol→UniProt AC, human) | 724/741 mapped |
| Merged and deduplicated | **741** |
| Forced inclusion of four-axis prior molecules (not covered by databases) | +9 (F2, F5, F10, FGG, PROC, VCAM1, ICAM1, SELE, HAVCR1) |
| **Final disease-gene set** | **750 (core 456 / wide 294)** |

Core-set definition (frozen rule replacing the GeneCards threshold): DISEASES curated ∪ OpenTargets score≥0.3 ∪ appearing in ≥3 disease entries ∪ four-axis prior molecules.

## 2. Source availability and handling (written into Methods)

| Planned source | Reality (verified 2026-09-22) | Handling |
|---|---|---|
| GeneCards | anti-scraping 403, no programmatic access | manual-export guide issued (`manual_export_guide.md`); scores backfilled into the master table after export |
| DisGeNET | API 401, requires registered API key | same as above, re-run after user registration |
| OMIM | API requires key | core genetic associations covered via DISEASES curated (UniProtKB-KW/MedlinePlus channels) instead |
| CTD | new site enforces ALTCHA human verification; batch API blocked | manual-export guide issued |
| **Open Targets** (replacement primary source) | ✅ free GraphQL API | primary source, incl. ClinGen/Gene2Phenotype/ClinVar/GWAS evidence |
| **DISEASES knowledge** (JensenLab) | ✅ free download | curated core set |

## 3. QC checks

- Four-axis prior molecules **27/27 in the core set** (axis1 5/5, axis2 8/8, axis3 6/6, axis4 8/8) ✓
- Human-only restriction ✓ (mygene species=human)
- Dual-source cross-check: OT wide set (294, for sensitivity analysis) and core set clearly stratified ✓

## 4. Caveats

1. "snakebite envenoming / VICC" has **no entry in any disease database** (verified 2026-09-22) — snakebite-related genes must be covered by the Phase 2 toxin–target layer; stated honestly in Methods;
2. Before the GeneCards/DisGeNET/OMIM/CTD manual exports were completed, the core-set rule used the replacement thresholds above; after export, scores were backfilled and threshold sensitivity analysis performed;
3. The 456-gene core set is moderately sized; an intersection of tens to ~a hundred with toxin targets was expected (Phase 3).

## 5. Output files

- `02_disease_genes/disease_gene_master.csv` (750 rows, with stratification, four-axis assignment, provenance notes)
- `02_disease_genes/opentargets_raw.csv` (2,014 raw records)
- `02_disease_genes/diseases_knowledge_full.tsv` (full DISEASES archive)
- `02_disease_genes/manual_export_guide.md`

## 6. GeneCards manual-export merge record (2026-09-22 13:52, v2 finalised)

The user completed the six-term GeneCards manual export (browser Export); merged per frozen thresholds:

| Term | Hits n | Per-term median threshold | n ≥10 |
|---|---|---|---|
| thrombotic microangiopathy | 515 | 1.39 | 52 |
| atypical hemolytic uremic syndrome | 960 | 113.85 | 959 |
| thrombotic thrombocytopenic purpura | 637 | 47.79 | 624 |
| microangiopathic hemolytic anemia | 468 | 107.24 | 466 |
| snakebite envenoming | 55 | 20.40 | 37 |
| venom-induced consumption coagulopathy | 39 | 46.30 | 38 |

- GeneCards unique genes 1,356; 698 reached the main threshold (≥ per-term median); 1,075 new rows merged;
- **Final master table: 1,825 genes (core 1,037 / wide 788)**; core = GeneCards ≥ per-term median ∪ OT score≥0.3 ∪ ≥3 diseases ∪ DISEASES curated ∪ four-axis priors;
- Note: the TMA term hits are broad (median only 1.39) while aHUS/TTP hits are concentrated (median >40) — the per-term-median strategy automatically adapts to this inter-term scale difference, superior to a fixed ≥5 threshold (corroborating the necessity of revision point 4);
- snakebite envenoming has 55 hits in GeneCards (none in OT/MedGen) — snakebite-specific genes (e.g. antivenom-resistance, bee/snake-venom reaction genes) thereby entered the wide set;
- Remaining to backfill: DisGeNET (API key), OMIM (API key), CTD (browser manual export); threshold sensitivity analysis after completion (see `manual_export_guide.md`).

**Output updates**: `disease_gene_master.csv` (1,825 rows), Excel management table 1,825 rows + change log v5, `PRISMA_flowchart_phase1_filled.png` (final).

## 7. DisGeNET API merge record (2026-09-22 14:35, user-provided key)

- The academic account is limited to CURATED sources (10 databases incl. CLINGEN/CLINVAR/ORPHANET/UNIPROT) — precisely the highest evidence tier;
- Disease CUIs resolved by reverse lookup from marker genes: main CUIs C2717961 (TMA), C0034155 (TTP), C2931788 (aHUS), C0019061 (HUS) + 12 subtype entries; parameter format `disease=UMLS_<CUI>`;
- 16 disease entries at score≥0.1 yielded **46 unique genes, all already present in the existing master table** (cross-corroboration with GeneCards/OT; no orphan genes); 2 of them (DisGeNET≥0.3) were promoted into the core set;
- Final: **total 1,825 | core 1,039 | wide 786**;
- snakebite/VICC has no DisGeNET entry either (consistent with OT/MedGen); the snakebite layer is covered by Phase 2 toxin–targets;
- Remaining: OMIM (API key), CTD (browser manual export).

## 8. CTD manual-export merge record (2026-09-22 14:51, final)

The user completed the CTD batch-query six-term manual export (site ALTCHA verification blocks programmatic access); merged:

| Term | Raw rows | Whitelist rows | Unique genes | Direct genes | Notes |
|---|---|---|---|---|---|
| atypical hemolytic uremic syndrome | 319 | 319 | 319 | 9 | exact MeSH hit |
| microangiopathic hemolytic anemia | 320,875 | 220,541 | 26,812 | 31 | CTD expanded the term to 54 diseases; whitelist-filtered |
| snakebite envenoming | 64 | 64 | 57 | 0 | hit Snake Bites (MeSH D012909), inferred via Bungarotoxins/Glutamine |
| thrombotic microangiopathy | 120,692 | 91,269 | 20,340 | 20 | expanded to 7 diseases, whitelist-filtered |
| thrombotic thrombocytopenic purpura | 31,829 | 31,829 | 16,708 | 4 | — |
| venom-induced consumption coagulopathy | — | — | 0 | 0 | **No such CTD entry ([Object not found]); recorded honestly** |

**Merge rules (frozen, against term-expansion noise):**

1. **Disease whitelist**: only Snake Bites / aHUS / HUS / TTP (incl. acquired) / Thrombotic Microangiopathies / Anemia, Hemolytic retained — CTD expands MAHA/TMA terms to unrelated diseases (sickle-cell, thalassaemia, congenital haemolytic anaemia, ITP etc.); their direct genes (HBB-class, CDAN1 etc., 22 entries) were removed to prevent false core-set contamination;
2. Non-empty DirectEvidence (marker/mechanism, therapeutic) → **into core set**; 80 unique whitelisted direct genes, of which 77 already present (cross-corroboration), 3 new (EIF2AK1, GCLC, ITPA; all mygene-mapped to UniProt);
3. InferenceScore-only (chemical inference) → threshold **≥50** into the wide set (MAHA term: 631 genes passed; TMA term: 29 passed; 349 new); **the snakebite envenoming term is an exception, fully collected** (only 57 genes, max score 8.85, but the only source hitting the snake-bite MeSH directly; 13 new);
4. `CTD inference` column format: `direct:marker/mechanism` or `inferred:<best score>`; 1,770 existing genes backfilled;
5. The CTD inference layer contains rodent-source genes (e.g. ABCB1A, TRP53, NACHRALPHA series) — 13 entries failed human mygene mapping and were flagged; Phase 2 intersection automatically filters by human UniProt.

**All 27/27 four-axis priors received CTD evidence**: 9 direct (ADAMTS13, C3, CD46, CFB, CFH, CFI, HMOX1, IL6, TNF); the other 18 inferred at 6.2–87.5 (top: ICAM1 87.48, SERPINE1 83.93, VCAM1 82.92).

**Final: total 2,190 genes | core 1,042 | wide 1,148**; PRISMA line B redrawn in sync.

**Output updates**: `disease_gene_master.csv` (2,190 rows), `ctd_merge_summary.json`, Excel management table 2,190 rows + change log v7, `scripts/merge_ctd.py` (re-runnable).

## 9. OMIM API merge record (2026-09-24 12:20, user-provided key)

- 5 disease terms (aHUS / HUS / TTP / TMA / MAHA) via `entry/search` gave 44 unique MIM entries; after batch `entry?include=geneMap` retrieval, 14 entries were kept per the **phenotype whitelist** (AHUS1–8, TTP 274150, CFHD, CFID, CD59-mediated haemolytic anaemia, cblC, cblG); search noise removed (Aicardi-Goutières, macular-degeneration susceptibility, immunodeficiency etc., 12 entries — OMIM has the same term-expansion trap as CTD, handled with the same logic);
- All associations are **mappingKey = 3 (molecular basis known; OMIM's highest evidence tier)**, totalling **15 unique genes**: ADAMTS13, CFH, CFHR1, CFHR3, CD46, CFI, C3, CFB, THBD, DGKE, C1GALT1C1, CD59, MMACHC, PRDX1 (digenic), MTR;
- **15/15 already present in the master table, all in the core set** — six-source cross-corroboration (GeneCards/OT/DISEASES/DisGeNET/CTD/OMIM), no orphan genes, further validating the robustness of the core-set rule; 4 rows previously lacking OMIM annotation were backfilled, bringing OMIM=yes to 16 rows;
- snakebite envenoming / VICC in OMIM: **0 search hits** (consistent with OT/DisGeNET/CTD); the snakebite-specific layer remains covered by Phase 2 toxin–targets;
- Totals unchanged: **total 2,190 | core 1,042 | wide 1,148**.

With this, all six Phase 1B sources are merged (GeneCards / Open Targets / DISEASES / DisGeNET / CTD / OMIM); the disease-gene set is locked.

**Output updates**: `disease_gene_master.csv` (2,190 rows), `omim_search_mims.json`, `omim_entries_raw.json`, `omim_merge_summary.json`, Excel management table + change log v8, `scripts/merge_omim.py` (re-runnable), OMIM added to the PRISMA line-B source box.
