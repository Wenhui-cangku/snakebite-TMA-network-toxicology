# Phase 1 Operating Manual (I): UniProt & VenomZone Retrieval Steps

> Corresponds to protocol v2 revised Phase 1 (weeks 2–3), 1A toxin-library construction.
> Queries and hit counts were **verified by live runs on 2026-09-22**; output files go to `snakebite_TMA/01_toxin_lib/`.

---

## I. UniProt retrieval (primary source of toxin sequences)

### 1.1 Queries (frozen; identical for web and API)

| Species | Query | Live hits (2026-09-22) |
|---|---|---|
| Russell's viper *Daboia russelii* | `(organism_name:"Daboia russelii") AND (keyword:"Toxin") AND (reviewed:true)` | **52** (reviewed); 89 without the reviewed filter |
| Siamese Russell's viper *Daboia siamensis* | `(organism_name:"Daboia siamensis") AND (keyword:"Toxin") AND (reviewed:true)` | **28** (reviewed); 39 without the reviewed filter |

**Principle**: the main library uses reviewed (Swiss-Prot manually curated) entries; unreviewed (TrEMBL) entries are added only after VenomZone/literature confirmation as genuine venom components (flagged in the source column of the data management table).

> ⚠️ **Live finding (2026-09-22; supplementary searches are mandatory)**: the `keyword:"Toxin"` query **misses the entire Kunitz-inhibitor family** (24 reviewed Kunitz entries across both species lack this keyword), and full-length CRISP sequences exist only as unreviewed. After the main search, always append:
> - `(organism_name:"Daboia russelii") AND (protein_name:"Kunitz") AND (reviewed:true)` → 24 entries
> - `(organism_name:"Daboia russelii") AND (protein_name:"cysteine-rich") AND (length:[200 TO 300])` + accessions A0A223PK22, A0A223PK48 (serotriflin) → 4 full-length CRISPs (unreviewed, flagged pending check)

### 1.2 Click-level web steps (recommended for first execution)

1. Open https://www.uniprot.org/ and click **"Advanced"** left of the search box.
2. Paste the whole query string from 1.1 for the species (including parentheses and quotes), click Search.
3. On the results page confirm the **Reviewed** filter is active (the query already contains `reviewed:true`; it should be auto-selected, showing 52 / 28 entries).
4. Click **"Customize columns"** above the results table; enable and save:
   - Entry, Entry Name, Protein names, Gene Names, Organism, Length
   - under **Structure**: PDB, AlphaFoldDB (for Phase 5 structure-availability assessment)
   - Function [CC], Caution [CC] (annotation text)
5. Click **"Download"** and export twice:
   - format **FASTA (canonical)** → name `01_toxin_lib/uniprot_russelii_reviewed.fasta` (or `..._siamensis_reviewed.fasta`);
   - format **TSV** (download all customised columns) → name `uniprot_russelii_reviewed.tsv`.
6. Record the result total shown at top right into the "download date" and remarks columns of `data_management_table.xlsx`; also fill the first-layer n value of the PRISMA flowchart template.
7. Repeat steps 2–6 with the second species' query.

### 1.3 API script version (for reproducibility archiving; results must match the web version exactly)

```bash
# Russell's viper reviewed toxins → FASTA
curl -s "https://rest.uniprot.org/uniprotkb/stream?query=(organism_name%3A%22Daboia%20russelii%22)%20AND%20(keyword%3A%22Toxin%22)%20AND%20(reviewed%3Atrue)&format=fasta" \
  -o snakebite_TMA/01_toxin_lib/uniprot_russelii_reviewed.fasta

# Siamese Russell's viper reviewed toxins → FASTA
curl -s "https://rest.uniprot.org/uniprotkb/stream?query=(organism_name%3A%22Daboia%20siamensis%22)%20AND%20(keyword%3A%22Toxin%22)%20AND%20(reviewed%3Atrue)&format=fasta" \
  -o snakebite_TMA/01_toxin_lib/uniprot_siamensis_reviewed.fasta

# Annotation table (TSV, incl. PDB/AFDB structure columns)
curl -s "https://rest.uniprot.org/uniprotkb/stream?query=(organism_name%3A%22Daboia%20russelii%22)%20AND%20(keyword%3A%22Toxin%22)%20AND%20(reviewed%3Atrue)&format=tsv&fields=accession,id,protein_name,gene_names,organism_name,length,xref_pdb,xref_alphafolddb,cc_function" \
  -o snakebite_TMA/01_toxin_lib/uniprot_russelii_reviewed.tsv
```

**QC points**: ① FASTA entry count = total shown on the search page (52 / 28); ② web and API executed the same day with identical counts; ③ if they differ, the API result prevails and the difference is logged.

### 1.4 Anticipated entry classification (for family assignment)

Typical Entry Name keywords of the five major Russell's-viper venom families, used for quick grouping during Phase 1 family classification:

| Family | Entry Name / protein-name keywords |
|---|---|
| SVMP (metalloproteinase) | `VMP*`, metalloproteinase, disintegrin (P-II class often separate entries), RVV-X heavy chain |
| SVSP (serine protease) | `VSP*`, thrombin-like enzyme, serine protease |
| PLA2 (phospholipase A2) | `PA2*`, phospholipase A2 |
| snaclec / CTL | `SL*`, snaclec, C-type lectin |
| Kunitz inhibitors | `VK*`, Kunitz-type, textilinin-like |
| Others | LAAO (`OXLA`), 5′-nucleotidase, CRISP (`CRIS*`), VEGF (`VGFF*`), hyaluronidase |

---

## II. VenomZone retrieval (curation cross-check and supplementary source)

> VenomZone (https://venomzone.expasy.org/, maintained by SIB) is the dedicated portal of the UniProtKB/Swiss-Prot **Tox-Prot** knowledgebase; entries are the same records as UniProt. Its role is not bulk download but: ① **checking** by taxonomy/family whether the UniProt search missed entries; ② discovering expert-curated venom components beyond the reviewed set; ③ providing toxin-family assignment and molecular-target annotations (directly usable for the Phase 2 literature-evidence tier).

### 2.1 Click-level steps

1. Open https://venomzone.expasy.org/ and choose **"Snakes"** on the homepage.
2. In the taxonomy tree expand **Viperidae → Daboia**, entering the species pages of *Daboia russelii* and *Daboia siamensis* respectively.
   - Alternative: type `Daboia russelii` or `Daboia siamensis` directly into the homepage search box.
3. Each species page groups all curated toxin entries by **protein family/activity**. Check family by family:
   - whether entry counts match the UniProt reviewed results (52 / 28);
   - when an entry not covered by the UniProt search is found (VenomZone occasionally lists entries lacking the "Toxin" keyword tag), **click into the detail page and record its UniProt accession (AC)** for the supplement list.
4. Read the **"Molecular targets / Function"** annotations entry by entry: extract experimentally reported host targets (e.g. RVV-X→coagulation factor X) directly into the Phase 2 evidence draft (`03_target_prediction/literature_evidence_draft.csv`, columns: toxin_ac / target / evidence / PMID) — this substantially reduces Phase 2 literature-mining effort.
5. VenomZone has no bulk FASTA export — retrieve sequences of supplementary entries via **UniProt ID mapping**:
   - UniProt homepage → **"ID Mapping"** below the search box (https://www.uniprot.org/id-mapping);
   - paste all supplementary ACs → From: `UniProtKB AC/ID`, To: `UniProtKB` → export FASTA + TSV, named `venomzone_supplement.fasta/.tsv`.
6. Fill the cross-check results into the data management table: source column = `UniProt reviewed` or `VenomZone supplement`; check date into the download-date column.

### 2.2 QC points

- VenomZone species-page counts ≥ UniProt reviewed counts is normal; if markedly fewer, check whether VenomZone files some entries under subspecies names (e.g. historical *Daboia russelii russelii* / *D. r. siamensis*) — inspect subspecies levels in the taxonomy tree as well;
- each of the five major families (SVMP/SVSP/PLA2/snaclec/Kunitz) must have representative entries in both databases; any missing family triggers an immediate query review;
- VenomZone molecular-target annotations are the **highest evidence tier (curated)** for Phase 2 — always record them together with the PMID.

---

## III. Completion criteria for this step (executed and verified 2026-09-22, all passed ✓)

| Item | Criterion | Actual status |
|---|---|---|
| FASTA files | main + supplementary FASTAs all generated | ✅ `uniprot_russelii_reviewed1.fasta` (52), `uniprot_russelii_reviewed2.fasta` (28, fully overlapping the former), `supp_kunitz.fasta` (24), `supp_crisp.fasta` (5, incl. 1 duplicate AC), `supp_svmp_ncbi.fasta` (3), `supp_venomzone_check.fasta` (1) |
| Annotation tables | corresponding TSVs complete, with length and PDB/AFDB structure columns | ✅ 5 TSVs complete, structure columns present |
| Merge & deduplication | merged into `all_toxins_raw.fasta`; total = sum of files − duplicates; no duplicate ACs | ✅ 79 unique (52+24+4+3+1, overlap 28 deduplicated) |
| Data management table | source and download date filled per entry; PRISMA template n values filled | ✅ toxin management sheet 63 rows (download date 2026-09-22); `PRISMA_flowchart_toxin_filled.png` filled with measured counts |
| VenomZone cross-check | compared against Tox-Prot curation scope; omissions added | ✅ 71 entries compared; the single full-length omission P86368 added; 20 short-peptide differences are design-level removals |
| Evidence draft | `literature_evidence_draft.csv` contains the molecular-target entries extracted from VenomZone | ✅ 62 entries (43 with target-relevant functional annotations, all with PMIDs) |

> After all self-checks passed on 2026-09-22, de-redundancy was run: 90% identity clustering (CD-HIT-equivalent algorithm) → `toxins_nr90.fasta` (40 cluster representatives); final toxin master table 63 entries (see `Phase1A_report.md` §1/§6/§7).
