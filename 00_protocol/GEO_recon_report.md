# GEO Pre-reconnaissance Report

**Date**: 2026-09-04　**By**: project Phase 0
**Channels**: NCBI GEO DataSets (E-utilities: esearch/esummary, db=gds) + manual verification of GEO record pages
**Purpose**: lock usable datasets in advance for Phase 6 "transcriptome dry validation"; if no direct dataset exists, activate the fallback strategy (protocol v2, Table 3, difficulty 9).

---

## 1. Queries and hit counts

| # | Query (db=gds) | GSE hits |
|---|---|---|
| Q1 | `(snakebite OR envenoming OR "snake bite") AND "Homo sapiens"[Organism] AND gse[ETYP]` | 3 |
| Q2 | `("snake venom" OR viper OR Daboia OR Bothrops OR Echis OR Crotalus) AND (endothelial OR HUVEC OR kidney OR renal OR fibroblast) AND gse[ETYP]` | 3 |
| Q3 | `("snake venom" OR envenomation) AND (transcriptome OR "expression profiling") AND gse[ETYP]` | 3 |

8 unique candidates after deduplication; each manually evaluated (esummary + sample-level GSM titles); 4 irrelevant records removed (580-species methylation atlas GSE195869, glioblastoma drug trial GSE186332, snake venom-gland organoids GSE129581, parasitoid-wasp venom gland GSE76257).

## 2. Core conclusion

> **As of 2026-09-04, GEO contains neither snakebite-patient peripheral-blood/kidney transcriptome datasets nor snake-venom-stimulated glomerular-endothelial-cell datasets.**
> This negative result is itself reportable in the manuscript Limitations (echoing protocol Table 3, difficulty 9). The fallback strategy was activated per plan; the following 4 datasets were locked (2 primary + 2 backup).

## 3. Locked-dataset evaluation

### ① GSE121297 (primary) — venom snaclec × HUVEC

- Title: Rigidity and inflammatory responses of interconnected endothelial cells are stimulated by rhodocetin-αβ via the neuropilin-1-MET-axis
- Type: expression microarray; n=19; public since 2019-03
- Groups (verified from GSM titles): HUVEC static control ×3 / static + RCαβ ×3 / shear flow (80 rpm) + RCαβ ×3; plus untreated ×4, RCαβ 200 nM pulse ×3, HGF 200 ng/mL ×3
- Relevance: RCαβ is a C-type lectin-like protein (snaclec) from *Calloselasma rhodostoma* venom, directly matching this study's snaclec family and axis-3/4 endothelial activation; includes NF-κB pathway phenotypes
- Limitations: single purified component (not crude venom); HUVEC, not glomerular endothelium; complete control design, directly usable with limma
- **Primary contrast**: static RCαβ vs static control (3 vs 3); shear-flow group can be added for sensitivity analysis

### ② GSE248215 (primary) — in-vivo time series of target-species venom exposure

- Title: A complex pattern of gene expression in tissue affected by viperid snake envenoming: the emerging role of autophagy-related genes
- Type: NanoString nCounter Fibrosis V2 Panel (~800 genes; ECM/immune/programmed death/autophagy focus); mouse skeletal muscle; n=20; public since 2024-03; PMID 38540699
- Design: *Daboia russelii* and *Bothrops asper* venom injection, 1 h / 6 h / 24 h time series
- Relevance: **includes the target species *D. russelii***, in-vivo model, covers axis 4 (ECM, inflammation, cell death)
- Limitations: panel limited to ~800 genes (restricted Hub-intersection probability); muscle, not kidney; mouse, not human; both raw counts and normalised matrix provided
- **Primary contrast**: *D. russelii* 24 h vs 1 h/baseline; *B. asper* as cross-species reference

### ③ GSE287744 (backup) — human cells × whole venom, RNA-seq

- Title: Neurocellular stress response to Mojave Type A Rattlesnake venom (human iPSC neural-stem-cell model)
- Type: RNA-seq; n=24 (4 donors × control/10/30 µg/mL × 4 h/24 h); public since 2025-04
- Relevance: human + whole venom + dose-and-time gradients, well designed; but neural stem cells are distant from the TMA endothelial/renal phenotype
- Use: orthogonal corroboration of intersection genes from the primary datasets (shared stress/inflammation pathways)

### ④ GSE262798 (backup) — cobra-venom functional genomics

- Title: Molecular dissection of cobra venom highlights heparinoids as an effective snakebite antidote
- Type: functional-genomics screen (HAP1 cells, n=8); public since 2025-04
- Limitations: cobra (non-viperid); cell line neither endothelial nor renal; qualitative reference for the heparinoid-antidote discussion only, not entering the limma pipeline

## 4. Phase 6 execution plan (written into analysis_plan_v1.md §5)

1. Download GSE121297 (series matrix) → limma: static RCαβ vs static control, \|log2FC\|>1 and adj.P<0.05;
2. Download GSE248215 (raw counts + normalised) → NanoString background correction, then limma or nSolver pipeline; *D. russelii* 24 h primary contrast;
3. DEGs of both datasets ∩ Hub genes → dual-evidence gene list;
4. If intersections too sparse: relax to \|log2FC\|>0.58 (sensitivity), or use GSE287744 for orthogonal corroboration;
5. Manuscript Limitations statement: no patient transcriptome; panel gene number restricted; tissue/species extrapolation limits.

## 5. Provenance

- Search and sample-structure verification: NCBI E-utilities (esearch/esummary, db=gds), 2026-09-04;
- GSE248215 record page (design, panel, supplements): https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE248215, 2026-09-04;
- GSE121297 record page was behind a human-verification gate at the time; group information was verified via E-utilities GSM titles (GSM3430984–GSM3431002).
