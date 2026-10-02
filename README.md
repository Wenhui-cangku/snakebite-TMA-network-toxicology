# Network toxicology of Russell's viper envenomation-associated thrombotic microangiopathy

Analysis code and result tables accompanying the manuscript:

> **Network-based prioritization of venom–host interactions potentially relevant to Russell's viper–associated thrombotic microangiopathy.** Manuscript in preparation; revised following a pre-submission methodological review (2026-10-02).

The study builds a documented-analysis-plan–guided, multi-layer computational pipeline linking *Daboia russelii* / *D. siamensis* venom toxins to host targets, pathways and the TMA phenotype: toxin library curation → six-source disease-gene integration → toxin–target edge mapping → network topology → dual-platform enrichment → structure validation (ClusPro / HADDOCK / HDock / AutoDock Vina) → cross-species transcriptome cross-check → network robustness → AOP framework integration.

---

## Repository layout (mirrors the analysis phases)

| Folder | Phase | Contents |
|---|---|---|
| `00_protocol/` | Phase 0 | Documented analysis plan (SOP), PRISMA counts, change log (`data_management_table_public.xlsx`) |
| `01_toxin_lib/` | Phase 1A | Toxin library: 63 entries / 40 CD-HIT clusters (90%), master table, retrieval SOP |
| `02_disease_genes/` | Phase 1B | Six-source disease-gene integration: 2,190 total / 1,042 core genes, merge summaries |
| `03_target_prediction/` | Phase 2 | Toxin–host target edges with four-tier evidence grading (L1–L4) |
| `04_network/` | Phase 3 | Intersection & topology: strict core 10, Hub 10, PPI tables, robustness analysis |
| `05_enrichment/` | Phase 4 | g:Profiler + Enrichr dual-platform results, prior-pathway tests |
| `06_geo/` | Phase 5 | GEO cross-validation: GSE121297 / GSE248215 DEG tables and watchlist |
| `07_docking/` | Phase 6 | Protein–protein docking inputs/summaries (7 pairs × 3 platforms) |
| `08_md/` | Phase 6 | Orthogonal stability corroboration: iMODS NMA + PRODIGY affinity |
| `08_smallmol/` | Phase 6 | Small-molecule docking summaries (batimastat / marimastat / varespladib) |
| `09_manuscript/fig_en/` | Phase 7 | Figure-generation scripts for all manuscript figures |
| `scripts/` | — | Pipeline scripts in execution order (see below) |

Large raw files (PDB structures, docking outputs, GEO raw matrices) are **not** in this repository; they are archived on Zenodo as a separate dataset: `https://doi.org/10.5281/zenodo.23087108`. This repository itself (code + result tables) is archived on Zenodo under the concept DOI `https://doi.org/10.5281/zenodo.23065792` (always resolves to the latest release; release v1.0.2 = `10.5281/zenodo.23097132`).

## Reproduction order

| # | Script | Produces |
|---|---|---|
| 1 | `scripts/build_phase2_edges.py` | toxin–target edge table (Phase 2) |
| 2 | `scripts/build_phase3.py` | intersection, Venn (Fig. 2), PPI tables, Hub genes (Fig. 3, Table 2) |
| 3 | `scripts/draw_fig2b.py` | PPI three-ring figure (Fig. 3) |
| 4 | `04_network/robustness_analysis.py` | targeted vs random attack curves (pre-v41 version, kept for traceability) |
| 5 | `04_network/robustness_analysis_v41.py` | v41 corrected robustness curves with k = 0 origin (Fig. 11) |
| 6 | `04_network/build_figure4_network.py` | four-layer heterogeneous network (Fig. 5, Cytoscape import) |
| 7 | `scripts/build_phase4.py` | dual-platform enrichment bubble plot (Fig. 4), prior-pathway tests (Table 3) |
| 8 | `scripts/geo_gse121297.py` → `scripts/geo_figures.py` | GEO DEG tables, volcano plots (pre-v41 versions, kept for traceability) |
| 9 | `scripts/geo_v41_reanalysis.py` | canonical v41 GEO re-analysis: fixed-probe 22,453-gene tables (Fig. 9 statistics, Fig. 10) |
| 10 | `scripts/prep_docking.py` → docking platforms → `07_docking/analysis_*.py` | docking summaries (Tables 4–5, Fig. 6) |
| 11 | `07_docking/figure/assemble_fig5_protein.py` | PyMOL panel assembly (Fig. 6) |
| 12 | `09_manuscript/fig_en/*.py` | final manuscript figures (Figs. 2–5, 8–11) |
| 13 | `09_manuscript/make_fig1_fig7.py` | workflow (Fig. 1) and AOP mechanism (Fig. 12) |

Historical one-time merge scripts (`merge_ctd.py`, `merge_omim.py`) document the six-source disease-gene integration; raw CTD/GeneCards exports are re-downloadable per the SOP in `00_protocol/` and are not included.

## Public data sources (access dates)

UniProtKB (2026-09-22) · VenomZone/Tox-Prot · GeneCards (manual export 2026-09-22) · Open Targets Platform · DISEASES · DisGeNET (CURATED) · CTD · OMIM (2026-09-24) · STRING · g:Profiler (2026-09-24) · Enrichr · GEO (GSE121297, GSE248215) · PDB (2E3X, 3S9C, 1KPM, 1WQ9, 2H4C, 7KVE, 2W26, 3GHG, 1M10, 3V2A, 1QRZ, 1PPB) · AlphaFold DB

## Environment

Python 3.12 with pandas / numpy / matplotlib / seaborn / openpyxl / networkx; external web services: ClusPro, HADDOCK 2.4, HDock, iMODS, PRODIGY; AutoDock Vina 1.2; PyMOL (figure rendering); Cytoscape 3.x (final network figure, Fig. 5).

## Change log

See `CHANGELOG.csv` for the full version-by-version change record (v1–v43) of the analysis.

## License

Code is released under the MIT License (`LICENSE`). Result tables and documentation are additionally usable under CC-BY 4.0 when obtained from the Zenodo data snapshot.

## Citation

If you use this code or data, please cite the manuscript ( citation to be updated upon publication ) and the Zenodo archive DOI.
