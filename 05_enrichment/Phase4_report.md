# Phase 4 Build Report — Enrichment Analysis and Four-Axis Interpretation

Date: 2026-09-24 ｜ By: Kimi ｜ Status: **complete**

## 1. Methods

- Gene set = Hub 10 ∪ strict core 10 = **15 unique genes** (F2, F3, F5, F7, F8, F10, FGA, PLG, PROC, ALB, COL4A1, F11, GP1BA, KDR, PROS1);
- Platform 1: **g:Profiler g:GOSt** (GO:BP/CC/MF + KEGG + Reactome, strict g:SCS correction; replaces the SOP's manual Metascape upload);
- Platform 2: **Enrichr** (KEGG_2021_Human / Reactome_2022 / GO_Biological_Process_2023, BH correction; replaces the clusterProfiler R step);
- Significance on both platforms (FDR<0.05 on each) is the criterion; single-platform terms are flagged separately.

## 2. Results overview

- g:Profiler: **116** significant terms (GO:BP 54 / GO:CC 26 / GO:MF 8 / KEGG 1 / REAC 27);
- Enrichr: **202** significant terms (GO:BP 124 / KEGG 6 / Reactome 72);
- **9 themes significant on both platforms**: Complement and coagulation cascades, Platelet activation, Fibrin Clot Formation (Common/Intrinsic/Extrinsic Pathway), Hemostasis, Platelet degranulation, Gamma-carboxylation.

Strongest signal: REAC:R-HSA-140877 Formation of Fibrin Clot (p=9.7e-23, 11/15 genes); KEGG:04610 (p=3.9e-18 / Enrichr adj=1.6e-22, top on both platforms).

## 3. Prior-pathway test table (written into Results)

| Prior pathway | g:Profiler | Enrichr | Conclusion |
|---|---|---|---|
| **hsa04610 Complement and coagulation cascades** | p=3.90e-18 ✓ | adj=1.63e-22 ✓ | **both platforms ✓✓** |
| **hsa04611 Platelet activation** | REAC equivalent p=1.47e-07 ✓ | adj=1.45e-03 ✓ | **both platforms ✓✓** |
| ECM–receptor interaction | below g:SCS | adj=1.81e-02 ✓ | single platform |
| Focal adhesion | below g:SCS | adj=4.68e-02 ✓ | single platform (marginal) |
| PI3K–Akt | not significant | adj=9.08e-02 | not significant |
| NF-κB | not significant | no such term | **not significant** |
| Fluid shear stress & atherosclerosis | not significant | adj=1.52e-01 | not significant |

Machine-readable version: `prior_pathway_check.csv`.

## 4. H2 key point (an honest finding that must go into the Discussion)

**The 11 driver genes of KEGG:04610 "Complement and coagulation cascades" are F2, F3, F5, F7, F8, F10, FGA, PLG, PROC, F11, PROS1 — all in the coagulation/fibrinolysis arm; the complement arm contributes 0.** In other words:

1. The toxin **direct-target layer** (L1+L2, 15 genes) is entirely a coagulation/fibrinolysis story (the all-axis-2 colouring of Figure 3 is the intuitive evidence);
2. Complement (axis 3) has no enrichment support at the direct layer — consistent with C3/ADAMTS13 being absent from the direct-target layer in Phase 3;
3. If H2 (complement participation in snakebite TMA) holds, its level of action is the **host secondary response**, to be evidenced by the GEO transcriptome layer (differential expression of complement genes in GSE121297/GSE248215) rather than by direct toxin–target edges — this completes the logical loop of the triple-validation design;
4. NF-κB / PI3K–Akt / fluid shear stress (the axis-4 inflammation–endothelium dimension) are not significant on the 15-gene core set — recorded honestly; these dimensions are likewise left to the transcriptome and clinical-consistency layers.

## 5. Output files

- `05_enrichment/figure3_enrichment_bubble.png` (Figure 3, driver genes coloured by four-axis assignment + KEGG:04610 annotation)
- `05_enrichment/gprofiler_raw.csv` (116 terms), `enrichr_raw.csv` (full), `enrichment_gprofiler_sig116.csv`, `enrichment_enrichr_sig.csv` (202 terms)
- `05_enrichment/prior_pathway_check.csv` (prior-pathway test table)
- Re-runnable script: `scripts/build_phase4.py`
- Excel: new "Phase4 enrichment" sheet + change log v11
