# Phase 1A Build Report: Toxin Library (v1)

**Date**: 2026-09-22　**Protocol**: v2 revised Phase 1 + operating manual (I)
**Script**: `snakebite_TMA/scripts/build_toxin_lib.py` (re-runnable)

## 1. Process counts (PRISMA toxin line; can be entered directly into the flowchart)

| Step | n |
|---|---|
| UniProt main search (keyword:"Toxin", reviewed; both species) | 52 (*D. siamensis* 28 + *D. russelii* 24; organism synonyms automatically cover both species) |
| User's second export (*D. siamensis* alone) | 28 (fully overlapping the main search) |
| **Supplementary search 1** (see §2 key finding): Kunitz reviewed + CRISP full-length | 24 + 4 |
| **Supplementary search 2** (SVMP replenishment): russelysin (GenBank AAZ39880) + disintegrin ×2 | 3 |
| Merged and deduplicated (by UniProt AC / GenBank accession) | **78** |
| <30 aa fragment sequences removed | −16 (mostly short Kunitz/CRISP fragments, e.g. P85039/40/41, P86537) |
| ADAM-like host proteins excluded (A0A223PK09/14/28/29 etc.; host ADAMs from transcriptome annotation, not venom SVMPs) | excluded (never entered the library) |
| Library after fragment removal | **62** |
| 90% identity clustering (CD-HIT-equivalent greedy algorithm) | **40 clusters** (40 representative sequences, `toxins_nr90.fasta`) |

## 2. Key methodological finding (written into Methods / manual update)

> **The UniProt `keyword:"Toxin"` search misses the Kunitz-inhibitor family** — all 24 reviewed Kunitz-type serine-protease inhibitors (BPTI/DrKIn/RVV-II series) of the two species lack the "Toxin" keyword tag; the CRISP family also had only short fragments. Per the manual's QC rule (all five major families must be present), supplementary queries were executed:
> `(organism_name:"Daboia russelii") AND (protein_name:"Kunitz") AND (reviewed:true)` and CRISP full-length entries (F2Q6F2/F2Q6F3/A0A223PK22/A0A223PK48; the full-length CRISPs are unreviewed and are flagged "pending VenomZone/literature check" in the master table's source column).
> This finding also validates the necessity of the VenomZone cross-check step.

## 3. Final library composition (62 entries, 40 clusters)

| Toxin family | Entries | Notes |
|---|---|---|
| Kunitz inhibitors | 21 | DrKIn-I/II, BPTI series, RVV-II etc. |
| PLA2 | 15 | acidic/basic svPLA2 (Drk-a1, DsM series) |
| snaclec/CTL | 8 | incl. RVV-X light chains 1/2 (Q4PRD1/Q4PRD2), dabocetin |
| SVMP/disintegrin | 5 | **RVV-X heavy chain (Q7LZ61), daborhagin-K (B8K1W0), russelysin (AAZ39880), disintegrin ×2** |
| SVSP | 4 | thrombin-like enzyme, factor V activator RVV-Vα etc. |
| CRISP | 4 | incl. serotriflin (unreviewed, pending check) |
| LAAO / VEGF / NGF | 2 / 2 / 1 | |

Species distribution: *D. siamensis* 38, *D. russelii* 24.
Structural availability: 11 PDB entries, 48 AlphaFold models, 3 without structures (handled by the pLDDT>70 rule in Phase 5).
**Abundance weights backfilled** (family level; Tan et al. functional venomics of Sri Lankan *D. russelii*: PLA2 35.0%, snaclec 22.4%, SVSP 16.0%, SVMP 6.9%, LAAO 5.2%, Kunitz 4.6%, NGF 3.5%, CRISP 2.0%) [Source: Tan et al. functional venomics, verified via WebSearch, 2026-09-22].

## 4. SVMP replenishment conclusion (former blocker resolved)

- UniProt reviewed Russell's-viper SVMPs comprised only 2 full-length entries (RVV-X heavy chain, daborhagin-K) — russelysin (615-aa haemorrhagic P-III SVMP) and 2 disintegrins (110 aa) were replenished from NCBI Protein, bringing SVMP/disintegrin to 5 entries, sufficient for the SVMP×{ADAMTS13, VWF-A1, FGA} docking matrix plus the RVV-X–FX positive control;
- Literature support: SVMP abundance in Asian *Daboia* venoms is 2.5–22% (geographic variation), mostly RVV-X-like P-III SVMPs — the library composition matches this picture; ADAM-like host proteins (transcriptome-annotation contamination) were excluded with documented reasons;
- Both RVV-X light chains (snaclec; Q4PRD1/Q4PRD2) were already in the library — all three chains of the RVV-X heterotrimer are covered.

## 5. Output files

| File | Content |
|---|---|
| `01_toxin_lib/toxin_master_table.csv` | toxin master table v2 (62 rows × 14 columns; family/cluster/structure status/abundance weight) |
| `01_toxin_lib/all_toxins_raw.fasta` | merged deduplicated raw sequences (78) |
| `01_toxin_lib/toxins_nr90.fasta` | 90% cluster representatives (40, for docking) |
| `01_toxin_lib/uniprot_supplement_kunitz_crisp.tsv` etc. | supplementary-entry annotation tables |
| `00_protocol/data_management_table.xlsx` | toxin management sheet filled (59 rows); change log appended |
| `scripts/build_toxin_lib.py` | fully re-runnable pipeline script |

## 6. Closing QC record (2026-09-22, against manual §1.2–1.4)

| Check | Result |
|---|---|
| ① FASTA counts vs search-page totals | file 1 = 52 ✓; file 2 = 28 ✓; file 2 fully overlaps file 1 (28/28) ✓; `all_toxins_raw.fasta` = 78 unique ✓; `toxins_nr90.fasta` = 40 = cluster count ✓ |
| ② Web vs API consistency | user's web downloads (52/28) and API run (52/28) same-day identical ✓ |
| ③ FASTA vs TSV metadata | the only entry without TSV metadata is AAZ39880.1 (GenBank russelysin, expected, source flagged) ✓ |
| ④ Family assignment vs §1.4 keyword table | Entry prefixes all match expectations: Kunitz→`VKT*`, PLA2→`PA2*`, SVSP→`VSP*`, snaclec→`SL*`, SVMP→`VM3DK`+russelysin, LAAO→`OXLA`, VEGF→`TXVE`, NGF→`NGFV`, CRISP→by accession ✓ |
| Data management table | 62 rows filled (download date 2026-09-22, source, notes); change log v1/v2 appended ✓ |
| PRISMA flowchart | measured-count version generated: `00_protocol/PRISMA_flowchart_toxin_filled.png` (Fig. S0-2) ✓ |

## 7. VenomZone cross-check record (2026-09-22, manual §2)

**Method**: VenomZone species pages are JS-rendered and cannot be scraped directly; the equivalent authoritative query published on its homepage (Tox-Prot curation scope) was used instead: `taxonomy_id:{8707/343250} AND (cc_tissue_specificity:venom) AND reviewed:true`, compared AC-by-AC against this library.

| Check | Result |
|---|---|
| VenomZone-scope reviewed venom entries | 71 (D. russelii 33 + D. siamensis 38) |
| Missing from this library | 21 → of which **20 are 10–25 aa short-peptide sequencing-evidence entries** (P86529–P86537, P85039–42 etc.; <30 aa design-level removals, not true omissions); **the single full-length omission P86368 (basic PLA2-3, 121 aa) was added** |
| Extra in this library (reviewed) | 7: snaclec 3–7 (Q4PRC6–9, Q4PRD0; carry the Toxin keyword but lack venom-tissue annotation) — retained as justified expansion |
| Five major families in both databases | complete ✓ |
| Subspecies-level check | D. siamensis was historically D. russelii siamensis; the UniProt organism_name search covers it automatically via synonyms ✓ |
| Target-annotation extraction (step ③) | FUNCTION annotations and PMIDs parsed from UniProt full text for 62 entries: 43 contain target-relevant functional descriptions → `03_target_prediction/literature_evidence_draft.csv` (Phase 2 curated-evidence starting point) |

**Conclusion**: consistency with the VenomZone/Tox-Prot curation scope verified; final library **63 entries / 40 clusters**.
