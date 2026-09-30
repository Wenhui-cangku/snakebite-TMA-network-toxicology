# Phase 2 Build Report — Toxin–Human-Target Edge Table (L2 + L4)

Date: 2026-09-24 ｜ By: Kimi ｜ Status: **L2/L4 complete; L1 pending manual export; L3 deferred**

## 1. Overview

| Evidence layer | Edges | Unique targets | Status |
|---|---|---|---|
| L1 curated databases (CTD/T3DB/BindingDB) | 0 | — | ⏳ CTD site enforces ALTCHA anti-bot; to be appended after manual export (same flow as Phase 1B) |
| **L2 literature manual annotation** | **49** | **15** | ✅ complete |
| L3 BLAST homology (auxiliary) | 0 | — | ⏸ no local blastp binary, deferred; SOP already marks it auxiliary-only |
| **L4 STRING neighbour expansion** | **398** | **105** | ✅ complete (15 targets × Top10, score≥0.7) |
| **Total** | **447** | 112 | at the upper end of the SOP-expected 150–400 range (due to full L4 retention) |

Outputs: `03_target_prediction/toxin_target_edges.csv` (447 rows), `phase2_string_neighbors.json` (neighbour archive), re-runnable script `scripts/build_phase2_edges.py`.

## 2. L2 literature layer detail (49 edges / 15 targets)

Source: 43 structured extractions from UniProt/Swiss-Prot curated annotations + 4 PubMed targeted supplementary sets.

### By family

| Family | L2 edges | Direct targets | QC (≥3) |
|---|---|---|---|
| SVMP/disintegrin | 11 | F10, F9, PROS1, FGA, FN1, COL4A1 | ✅ |
| snaclec/CTL | 7 | F10, F9, PROS1, GP1BA | ✅ |
| SVSP | 4 | F5, FGA, FGB | ✅ |
| PLA2 | 4 (incl. 2 family-level) | F10 | ✅ |
| Kunitz | 19 | PLG, F11, F10, PROC, PRSS1, CTRB1 | ✅ |
| VEGF | 2 | KDR | — |
| NGF | 1 (weak 0.5) | GP1BA (indirect protection, By similarity) | — |

### PubMed supplementary-evidence record

- **PMID 27089306**: Daboxin P (major PLA2 of Indian *D. russelii*) targets FX for anticoagulation → family-level edge (could not be assigned to a specific library entry, score 0.6);
- **PMID 21356226**: acidic RVVA-PLA2-I (purified from *D. russelii*) anticoagulant → family-level edge (score 0.6);
- **PMID 18554518 / 28042812**: daborhagin-M/K (= russelysin) hydrolyses fibrinogen Aα chain, fibronectin, type-IV collagen → B8K1W0 (score 1.0) and AAZ39880.1 (same protein, score 0.9);
- **PMID 36423674**: SPAD-1 (RVV-derived HGD-disintegrin) disrupts fibronectin/laminin matrix adhesion → two family-level supporting edges for disintegrins (score 0.6);
- **PMID 37092784 / 28732041 / 21871889**: RVV-X FX-activation reaction mechanism, RVV-V substrate specificity and structural basis → backfilled onto the corresponding edges.

### Handling of entries without targets (recorded honestly)

- **CRISP ×4**: no curated human targets; serotriflin binds the snake's own serum SSP-2 (PMID 18222185), not a human target — no edge;
- **LAAO ×2**: affects platelet aggregation via H₂O₂ generation (PMID 21802487); no single protein target — no edge;
- **P31100 (PLA2)**: functions as chaperone/potentiator of RV-4 (intra-venom interaction), not a human target — no edge;
- **snaclec Q4PRC6–9 / Q4PRD0**: annotation only "interferes with haemostasis (generic)", no specific target — no edge.

## 3. L4 STRING neighbour layer

- For each L2 direct target (15 with score≥0.8), STRING `interaction_partners` was queried (*H. sapiens*, combined score ≥0.7, Top 10), yielding 105 unique neighbour nodes attached to the corresponding toxin edges (`evidence_detail` notes "via ×× target");
- Neighbours include the complete coagulation-cascade extension: F2, F3, F7, F8, F12, F2R, C4A/C4B/C4BPB, SERPINA family, APOA/APOB etc.

## 4. Prospective check against the disease-gene set (Phase 3 rehearsal)

- **10 of 15 L2 direct targets fall in the disease core set**: F10, F5, F11, FGA, PLG, PROC, PROS1, GP1BA, KDR, COL4A1;
- 5 not in the core set: F9, FGB, FN1, PRSS1, CTRB1 (F9/FGB/FN1 are in the wide set or below six-source thresholds — a "wide-set rescue" talking point for Phase 3);
- 51 of 105 STRING neighbours **are in the disease core set** (incl. core coagulation factors F2, F3, F7, F8, F12);
- Four-axis check: axis 1 (GP1BA ✓, VWF via STRING neighbour ✓), axis 2 (F5/F10/PLG/PROC/PROS1 ✓), axis 4 (KDR ✓) already have direct edges; axis 3 (complement) currently only via STRING neighbours (C4A/C4B) — consistent with the H2 expectation, to be interpreted after the Phase 3 intersection.

## 5. Outstanding items

1. **L1**: manual export from CTD/T3DB/BindingDB (following `02_disease_genes/manual_export_guide.md`), then append `evidence_type=ctdb/t3db` edges;
2. **L3**: install BLAST+ or use EBI online BLAST to run `toxins_nr90.fasta` vs the human proteome (e-value<1e-3, auxiliary annotation only);
3. The PRISMA "Venn intersection n=___" placeholder to be filled after Phase 3.
