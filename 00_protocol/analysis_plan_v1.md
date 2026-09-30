# Analysis Plan v1 (frozen)

**Project**: Network-toxicology mechanism study of snakebite-associated thrombotic microangiopathy (TMA) with molecular-docking validation
**Frozen on**: 2026-09-04 (Phase 0 output, corresponding to protocol v2 revised)
**Change rule**: once frozen, any change requires a version bump (v1.1, v1.2, ...) with an entry appended to the change log at the end; never overwrite older versions.

---

## 1. Species strategy (decided)

**Strategy A (mechanistic depth first)**: restricted to *Daboia russelii* (nominal subspecies / Sri Lankan–South Indian population) + *Daboia siamensis* (Southeast Asian population), including the conserved toxin families shared by both species, emphasising representativeness of Asian snakebite TMA. All conclusions are strictly limited to the studied populations.

## 2. Biological priors: four pathological axes

| Axis | Core events | Key host molecules |
|---|---|---|
| Axis 1: VWF–ADAMTS13 imbalance | Insufficient ULVWF clearance, platelet microthrombi | ADAMTS13, VWF, GP1BA, ITGA2B/ITGB3 |
| Axis 2: Coagulation–fibrinolysis disturbance (VICC) | Factor activation/consumption, thrombin burst | F2, F5, F10, FGA/FGG, PLG, SERPINE1, PROC |
| Axis 3: Alternative complement activation | Endothelial C3 deposition, C5b-9 formation | C3, C5, CFB, CFH, CFI, CD46 |
| Axis 4: Endothelial injury–inflammation–nephrotoxicity | Adhesion-molecule upregulation, oxidative stress, tubular necrosis | VCAM1, ICAM1, SELE, TNF, IL6, NOS3, HMOX1, HAVCR1 |

## 3. Hypotheses (v2 revised, frozen)

- **H1**: SVMP toxins target the VWF–ADAMTS13 axis in a topologically centralised manner, and SVSP toxins target the coagulation cascade (FGA/F2/F10) with high centrality; together they form the "master switch" initiating TMA.
- **H2**: Toxin targets are significantly enriched in the alternative complement and endothelial-activation pathways; complement–coagulation crosstalk amplifies the transition from "coagulopathy" to "microangiopathy". (Non-enrichment of the complement axis is a publishable negative result, with a pre-specified two-way interpretation.)
- **H3**: Core toxin–target complexes (e.g. SVMP–ADAMTS13, SVMP–VWF) have druggable binding interfaces occupiable by batimastat/marimastat-class inhibitors; complement-related candidate pairs such as snaclec–C3 are downgraded to exploratory docking, supplementary material only.

## 4. Key parameter thresholds (frozen; reported as-is in Methods)

| Step | Parameter |
|---|---|
| Toxin de-redundancy | CD-HIT, 90% identity clustering; remove <30 aa fragments |
| GeneCards | main set: relevance score ≥ median or ≥10; ≥5 wide set for sensitivity only |
| DisGeNET | score ≥ 0.1; OMIM fully included; CTD direct evidence only |
| Target evidence tiers | curated (CTD/T3DB/literature) > database-predicted > homology-inferred |
| BLASTp | e-value < 1e-3, all reported as auxiliary evidence; identity > 30% highlighted |
| STRING | main analysis score ≥ 0.7 (hide disconnected nodes); 0.4 for sensitivity |
| Hub genes | cytoHubba MCC/Degree/EPC Top-20 intersection ∩ MCODE modules (K-core 2) |
| Enrichment | GO/KEGG/Reactome, Metascape + clusterProfiler dual platform, BH FDR < 0.05 |
| Protein–protein docking | HDOCK (score ≤ −200) + ClusPro cross-check, HADDOCK prior-restraint refinement; three evidence tiers I/II/III; main text relies on tiers I–II only |
| Docking controls | positive control RVV-X–FX; negative controls 3–5 random unrelated pairs |
| Toxin modelling | ColabFold, active-site pLDDT > 70; short peptides via PEP-FOLD3 |
| Receptor structures | PDB resolution ≤ 3.0 Å; ADAMTS13 locked to PDB 6GHZ (MDTCS domains, backup 3EAS) |
| Small-molecule docking | AutoDock Vina, binding energy ≤ −7 kcal/mol as activity hint |
| Transcriptome validation | limma, \|log2FC\| > 1 and adj.P < 0.05 |

## 5. GEO pre-reconnaissance conclusions (Phase 6 path locked)

**Conclusion: no direct snakebite-patient transcriptome dataset exists in GEO (as anticipated); the fallback strategy was activated and 4 datasets locked (2 primary + 2 backup)** (see `GEO_recon_report.md`):

| Priority | GSE | Design | Role |
|---|---|---|---|
| Primary ① | GSE121297 | HUVEC ± venom snaclec (rhodocetin-αβ), static/shear flow, with controls, n=19 | Expression validation of axis 3/4 (endothelial activation, NF-κB) |
| Primary ② | GSE248215 | Mouse skeletal muscle injected with *D. russelii* / *B. asper* venom, 1/6/24 h, NanoString Fibrosis Panel (~800 genes), n=20 | In-vivo validation in the target species (axis 4/ECM/inflammation) |
| Backup ① | GSE287744 | Human iPSC neural stem cells + Mojave rattlesnake venom 10/30 µg/mL, 4/24 h, RNA-seq, n=24 | Human whole-venom exposure reference |
| Backup ② | GSE262798 | HAP1 cells + cobra venom functional-genomics screen, n=8 | Qualitative reference only |

Phase 6 differential-analysis design: GSE121297 primary contrast "static RCαβ vs static control"; GSE248215 primary contrast "*D. russelii* 24 h vs baseline"; DEG ∩ Hub genes = dual "computational + expression" evidence.

## 6. To-do (this week, non-file items)

- [ ] Register for the HADDOCK web-server guru account (server named HADDOCK2.4, running v2.5 backend; academic e-mail, 1–2 weeks review)
- [ ] Register ClusPro 2.0 account (verified 2026-09-04 as still the latest version)
- [ ] Install/verify: Cytoscape 3.10 + cytoHubba + MCODE, R ≥4.3 + clusterProfiler/limma/GEOquery, PyMOL, CD-HIT, BLAST+

## 7. Change log

- v1 (2026-09-04): first frozen version, based on protocol v2 revised; GEO reconnaissance complete, Phase 6 path fixed.
- v1.1 (2026-09-04): updated docking-platform version info — the HADDOCK web-server backend was upgraded to v2.5 (since December 2024; server still named HADDOCK2.4); ClusPro 2.0 verified as the latest version. Protocol v2 revised and SOP updated in sync.
