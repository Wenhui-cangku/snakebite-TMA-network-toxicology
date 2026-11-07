# JVAT reanalysis archive: Russell's viper venom–host interaction map

## Associated manuscript

**An evidence-calibrated venom–host interaction map of Russell's viper envenoming: coagulation architecture and hypotheses for thrombotic microangiopathy**

Archive version: `v2026.11.07-JVAT`  
Prepared: 7 November 2026  
Repository: https://github.com/Wenhui-cangku/snakebite-TMA-network-toxicology

This archive contains the English analysis inputs, result tables, public-path scripts, supplementary material and figure sources for the JVAT manuscript. It supersedes earlier CBI-oriented supplementary files and review archives. Raw third-party database records remain subject to their original licenses and access conditions.

## Principal verified anchors

- 63 toxin sequences; 40 custom clusters and 39 usearch clusters.
- Pairwise clustering agreement: **Rand index = 0.996**, calculated as 1,945/1,953 = 0.9959037378392217.
- 2,190 disease-associated genes and a reproducible 1,042-gene core.
- 447 audited toxin–host rows, including 33 primary-literature interactions across 15 host targets.
- Ten strict-core host targets; factor X has six primary-literature edges from four independent toxin entities.
- G2 leading result: Formation of Fibrin Clot, P = 4.7406 × 10⁻⁷; 15 BH-significant terms.
- Ten-thousand permutations for G2–G4 with seed 20261106.
- STRING-expanded context: 54 nodes and 321 functional-association edges.
- Classical limma: 43 BH-significant genes in GSE121297 and 75 in GSE248215.
- Fifteen structure assets, seven model pairs and twelve archived docking-output rows.
- Fourteen protocol-deviation and post hoc decision records.

Run `python validate_archive.py` from the archive root to check these anchors.

## Directory guide

| Path | Contents |
|---|---|
| `00_protocol/` | Fourteen decision records and analysis notes |
| `01_toxin_lib/` | English toxin library, raw FASTA, cluster benchmark and portable benchmark script |
| `02_disease_genes/` | Source-resolved evidence flags, field dictionary and provenance summaries |
| `03_target_prediction/` | Base and audited edge tables, mechanism summaries, literature-search tables and edge-audit script |
| `04_network/` | Strict-core definitions, STRING associations, node/edge tables and descriptive rankings |
| `05_enrichment/reanalysis_v2/` | G1–G7 outputs, matched backgrounds, permutations, LOSO/no-GeneCards/g:Profiler results, GMT libraries and analysis scripts |
| `06_geo/` | Analysis-ready expression matrices, five limma result tables, QC outputs, R scripts and session information |
| `07_docking/` | Structure identity, model disposition and docking-output summaries |
| `09_manuscript/` | Blinded manuscript source, supplementary files, figure scripts and validated figure outputs |
| `MANIFEST.csv` | Relative path, size and SHA256 for every archived payload file |
| `CHANGELOG.csv` | Version-specific changes |
| `CITATION.cff` | Citation metadata |

## Reproduction notes

### Software

- Python 3.12 with pandas, NumPy, SciPy, Matplotlib, NetworkX and openpyxl.
- R 4.6.2 with limma 3.68.5 for the archived expression analysis.
- Optional: usearch v11.0.667 to rerun the external clustering benchmark. The executable is not bundled.
- The figure script can use `daimon_runtime` when available but falls back to standard Matplotlib settings.

### 1. Validate archived results

```bash
python validate_archive.py
```

### 2. Rerun the edge audit

```bash
python 03_target_prediction/run_edge_audit.py
```

Set the `EDGE_OUT` environment variable to write to a separate output file. The public base edge table and toxin library use English fields; no private paths are required.

### 3. Rerun the clustering benchmark

Install usearch v11.0.667 separately and set `USEARCH_BIN` to its executable path. Then run:

```bash
python 01_toxin_lib/run_cluster_benchmark.py
```

Set `CLUSTER_OUT` to a separate directory if desired. The custom procedure is a length-seeded greedy 90%-identity method; it is not CD-HIT. The archived comparison exposes all marginal pair differences and the corrected Rand arithmetic.

### 4. Reconstruct the core and run source-sensitivity checks

```bash
python 05_enrichment/reanalysis_v2/run_loso.py
```

Set `LOSO_OUT` to a separate directory if desired. The explicit `analysis_inputs.json` preserves the core and axis definitions without private source paths.

### 5. Rerun matched-background enrichment and permutations

The three Enrichr GMT snapshots are included. To refresh them, run `download_gmt.py`; refreshed libraries may differ from the archived analysis.

```bash
python 05_enrichment/reanalysis_v2/run_reanalysis.py
```

Defaults: 10,000 permutations and seed 20261106. For a small technical smoke test only, set `N_PERM=100`; do not use a reduced run for manuscript inference. Set `REANALYSIS_OUT` to a separate directory to preserve archived outputs.

The no-GeneCards and g:Profiler follow-up is:

```bash
python 05_enrichment/reanalysis_v2/run_nogc_and_gprofiler.py
```

This script contacts the public g:Profiler API unless `SKIP_GPROFILER=1` is set. Local no-GeneCards analyses run without that service.

### 6. Rerun limma

Run from the `06_geo` directory:

```bash
Rscript run_limma_plain_sens.R
Rscript run_limma.R
```

`run_limma_plain_sens.R` is the classical empirical-Bayes primary analysis. `run_limma.R` performs trend-plus-robust and quantile-normalization sensitivity analyses. Set `LIMMA_OUT` to a separate directory to avoid overwriting archived outputs. The analysis-ready matrices are included; large original GEO downloads and intermediate raw matrices are not duplicated here.

### 7. Rebuild figures

```bash
python 09_manuscript/resubmission_JVAT/source/generate_jvat_figures.py
```

The script reads relative archive inputs and writes six PNG/SVG pairs under `09_manuscript/resubmission_JVAT/figures/`. The cached permutation nulls are included solely to preserve the archived figure-generation path; `generate_v3_figures.py` also checks their archived summary values.

## Structural interpretation rules

P4 was withdrawn because the receptor chain had been misidentified. P1 and P6 provide orientation-level context only. P3 is restricted by missing fibrinogen alpha-C coverage. P7 is template-dependent and has ligand RMSD = 21.95 Å. Docking scores, cluster sizes and interface counts are pose descriptors, not independent demonstrations of binding, affinity, efficacy or physiological stability. The 1QRZ model represents the plasminogen catalytic domain, not activated plasmin.

## Third-party data and related archives

Public sources comprised UniProtKB, VenomZone/Tox-Prot, GeneCards, Open Targets, DISEASES, DisGeNET CURATED, CTD, OMIM, STRING, g:Profiler, Enrichr, GEO (GSE121297 and GSE248215), PDB and AlphaFold DB. Access dates and query-level details are preserved in the supplementary tables.

Large structural and expression-related source files from the earlier project snapshot are separately archived at https://doi.org/10.5281/zenodo.23087108. Earlier project releases are linked to the Zenodo concept DOI https://doi.org/10.5281/zenodo.23065792. After this version is released, cite its **version-specific Zenodo URL and DOI**; the concept DOI alone does not prove that this version is archived.

## Privacy and exclusions

This archive excludes API credentials, private absolute paths, `node_modules`, internal review correspondence, Chinese internal reports, rejected CBI manuscripts, obsolete supplementary files and unrelated local documents. The public copies use relative paths and English file names and text.

## License and citation

Code is provided under the MIT License; see `LICENSE`. Result tables and documentation may be shared under CC BY 4.0 with appropriate citation and preservation of third-party source terms. See `CITATION.cff` and cite both the associated manuscript and the version-specific archive record when available.
