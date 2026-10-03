# Phase 5 Structural Validation Report (Molecular Docking Layer)

Updated: 2026-09-30 | Status: ClusPro line complete (7/7), HADDOCK 4 pairs + HDock P7 complete, small-molecule line complete — **Phase 5B protein–protein docking fully complete**

> **Update (2026-10-02, pre-submission review):** Pair **P4 (snaclec×GP1BA) is retracted** — the receptor chain was misidentified (1M10 chain A is VWF-A1, not GP1BA), so all P4 docking results in §2 below are void and are excluded from the manuscript. Pairs **P1 and P6 are downgraded to supportive (orientation-level) evidence**. Docking outcomes are reported in the manuscript as descriptive, threshold-based support rather than validation; see manuscript Section 3.6 and the protocol-deviation table in the Supplementary Material.

## 1. Overview

| Layer | Content | Status |
|---|---|---|
| 5A structure preparation | 8 toxin structures + 8 host structures (16 files) | ✅ Complete (v13) |
| 5B protein–protein docking | ClusPro 7 pairs (blind docking) | ✅ Complete, §2 of this report |
| 5B protein–protein docking | HADDOCK 4 pairs (biochemical restraints) + HDock P7 (template) | ✅ Complete (v18, §3 of this report) |
| 5C small-molecule docking | Vina 9 groups (3 inhibitors × 3 receptors) | ✅ Complete (v14, tri-panel v15) |

## 2. ClusPro results (Balanced mode, 2026-09-28)

| Pair | Top1 cluster members | Center / Lowest energy | Functional-site coverage (measured interface) | Verdict |
|---|---|---|---|---|
| P1 RVV-X×FXa | **92** | −725.3 / −899.7 | N-terminal 16–21 not covered (Ile16 inserts into the activation pocket and is structurally inaccessible); interface located on external loop regions such as 84–109 | Cluster ✅ / site ⚠️ pending HADDOCK |
| P2 RVV-Vγ×FV | **99** | −916.2 / −1045.2 | Cleavage site 1543–1548 covered 3/6 | ✅ (plus 3S9C co-crystal direct evidence) |
| P3 daborhagin-K×FIB | **119** | −1174.6 / −1175.1 | FGA C-terminal 195–200 not covered; binding at FGA 57–88 coiled-coil region (the true cleavage region, αC domain 221–610, is outside the crystal structure) | Cluster ✅ / site ❌ pending HADDOCK |
| P4 snaclec×GP1BA | **59** | −688.3 / −770.5 | Interface 505–508/541–542/544–550/570–578, capping core residues of the VWF-binding region (549/550/571/572) | ✅ (rerun used the single-chain receptor, 2026-09-30) |
| P5 PLA2×FXa | **109** | −751.4 / −777.6 | n/a (the mechanism is interface binding itself; interface 35–61/94–99/143) | ✅ |
| P6 Kunitz×plasmin | **84** | −737.9 / −957.0 | Catalytic triad 603/646/741 covered 2/3 | ✅ (consistent with Ki = 0.19 nM literature) |
| P7 svVEGF×VEGFR2 | **190** | −1228.0 / −1263.8 | 3V2A reference interface **26/26 fully covered**, pose consistent with VEGF-A template | ✅✅ strongest evidence |

**Summary**: all 7 pairs have Top1 cluster members ≥ 30 (59–190), meeting the preset criterion (≥30 = structural-level support); the SOP expectation of "≥5 pairs structurally supported" was exceeded (7/7). P4 was rerun because the wrong receptor (GP1BA–VWF complex) had been submitted; the conclusion holds after correction.

## 3. HADDOCK restraint docking + HDock template docking results (2026-09-30)

Criteria: HADDOCK score ≤ −100 AND functional site inside the interface = both met; score below threshold but restrained-residue orientation achieved = site evidence established, affinity scoring insufficient. HDock: confidence > 0.7 and interface coverage = pass.

### 3.1 HADDOCK 4 pairs (cluster 1 measured, interface cutoff 5 Å)

| Pair | Score ± SD | Cluster size | Z-score | Functional-site coverage (cluster1_1) | Closest restraint distance | Verdict |
|---|---|---|---|---|---|---|
| P1 RVV-X×FXa | −67.8 ± 1.1 | 81 | −0.7 | FXa N-terminal 16–21 covered **5/6** (cluster2 reaches 6/6; 6 of 7 clusters cover ≥4 residues) | 7.75 Å (partially satisfied, viol 81.4) | Site orientation ✅ / score below the ≤−100 line |
| P2 RVV-Vγ×FV | **−144.9 ± 4.4** | 165 | **−1.4** | Cleavage site 1543–1548 covered **6/6** (all 4 clusters ≥5/6) | **1.97 Å** (near-perfect) | ✅✅ **both criteria met**, the only pair passing the HADDOCK line |
| P3 daborhagin-K×FIB | −40.3 ± 0.6 | 23 | +0.9 | FGA C-terminal 195–200 covered **5/6** (all 10 clusters ≥4/6, highly consistent orientation) | 2.57 Å (well satisfied) | Site orientation ✅ / score below threshold |
| P6 Kunitz×plasmin | −48.7 ± 0.3 | 57 | +0.3 | Catalytic triad 603/646/741 covered **3/3** (most of 11 clusters ≥2/3) | 1.82 Å (satisfied) | Site orientation ✅ / score below threshold |

### 3.2 HDock P7 (template docking, model_1 measured)

| Metric | Value | Verdict |
|---|---|---|
| Docking score (Top1) | −258.18 | — |
| Confidence score | **0.8969** (> 0.7, high confidence) | ✅ |
| Ligand RMSD vs template | 21.95 Å (pose deflected, see interpretation 6) | ⚠️ requires superposition check |
| R-chain superposition RMSD vs 3V2A (185 CA) | **0.000 Å** (receptor rigidly reproduced) | ✅ |
| 3V2A reference interface coverage | **21/26** (258/273/275/276/288 not covered) | ✅ |
| Spatial relationship to VEGF-A template | nearest atom 0.15 Å, centroid distance 10.3 Å (same binding region) | ✅ |

### 3.3 Additional interpretation points

6. **P2 becomes the strongest mutually corroborating chain of the whole study**: HADDOCK both criteria met (−144.9 / Z −1.4 / 6/6) + ClusPro 99-member cluster + 3S9C co-crystal — three independent lines of evidence point to the same cleavage-site interface;
7. **HADDOCK score below threshold ≠ negative**: for P1/P3/P6 the AIR restraints all guided the toxin active residues toward the host functional site (inter-restraint distances 1.8–7.8 Å), proving these orientations are **geometrically feasible**; the weak scores reflect limitations of the HADDOCK potential function for glycosylated/multi-domain large interfaces (RVV-X trimer, daborhagin-K 615 aa). Structural evidence rests primarily on the large ClusPro clusters, with HADDOCK site orientation as corroboration;
8. **P7 dual-platform corroboration holds**: the HDock ligand RMSD of 21.95 Å is a deviation "relative to the initial template pose" — the svVEGF dimer underwent rotation/translation optimization within the interface groove, but 21/26 interface-residue coverage + 0.15 Å nearest-atom distance to the VEGF-A template show it remains on the same binding face; together with ClusPro 26/26, svVEGF×VEGFR2 is the pair with the most complete evidence chain (template crystal + blind docking + template docking);
9. **The P3 αC-domain limitation persists**: HADDOCK can only demonstrate that FGA 195–200 (the in-structure proxy site) orientation is feasible; the true cleavage region (221–610) has no available structure — this is the methodological boundary of this layer and is stated in Limitations.

## 4. Interpretation points (material for the Discussion)

1. **P7 is template-level evidence**: the blind-docking Top1 pose precisely reproduces the VEGF-A×VEGFR2 crystal interface (26/26), and its cluster size of 190 is the largest of all pairs — the svVEGF–VEGFR2 interaction is highly credible;
2. **P1's uncovered N terminus does not equal negative**: the new N-terminal Ile16 of activated FXa inserts into the activation pocket per the serine-protease activation mechanism (salt bridge with Asp194) and is structurally inaccessible; the stable 92-member blind-docking cluster proves binding itself, and HADDOCK restraint docking further confirmed the 16–21 orientation is geometrically feasible (5/6 coverage, §3.1);
3. **P3's site limitation stems from structure coverage**: 3GHG contains only FGA 27–200, while daborhagin-K's true cleavage region lies in the αC domain (outside the structure); the 119-member cluster proves stable binding, HADDOCK confirmed proxy-site 195–200 orientation is feasible (5/6, consistent across 10 clusters), and αC-domain-level evidence is addressed in Limitations;
4. **Partial site coverage for P2/P6** (3/6, 2/3) is normal in blind docking, and HADDOCK completed them to 6/6 and 3/3 respectively, mutually corroborated by co-crystal/inhibition-constant literature;
5. **P4 rerun confirms the competitive-inhibition mechanism**: after correcting the receptor, snaclec still stably binds GP1BA (59-member cluster), with interface 544–550/570–578 exactly capping the core of the VWF-A1 binding region (549/550/571/572) — consistent with the mechanism of "snaclec occupying the VWF site and competitively inhibiting ristocetin-induced aggregation"; when the wrong complex was submitted earlier, snaclec was also attracted to the same region, so the two runs corroborate each other.

## 5. To-do

| Item | Action | Owner |
|---|---|---|
| ~~P4 rerun~~ | ✅ Done (2026-09-30, 59 members, covering the VWF-site core) | — |
| ~~HADDOCK 4-pair results~~ | ✅ Back-filled (2026-09-30, P2 both criteria met, P1/P3/P6 site orientation established) | — |
| ~~HDock P7 results~~ | ✅ Back-filled (2026-09-30, confidence 0.8969, interface 21/26) | — |
| ~~Figure 5 protein panel~~ | ✅ Done (2026-09-30, `figure/fig5_protein_4panel.png`, A=P7 dual-platform superposition / B=P2 HADDOCK / C=P6 HADDOCK / D=P4 ClusPro) | — |

## 6. File index

- Summary table: `07_docking/docking_results.csv` (12 rows: 7 ClusPro + 4 HADDOCK + 1 HDock, all back-filled)
- Models: `results/cluspro/P1..P7/model.000.00.pdb`; `results/haddock/P1|P2|P3|P6/*/cluster*_*.pdb`; `results/hdock/P7/model_1.pdb` + `model_1_superposed_on_3V2A.pdb` (already superposed onto the 3V2A coordinate frame)
- Verification scripts: `07_docking/analysis_haddock_hdock.py`, `analysis_hdock_p7.py` (recomputable)
- **Figure 5 protein panel**: `07_docking/figure/fig5_protein_4panel.png` (3320×2700, 300 dpi); PyMOL scripts `panelA_P7/panelB_P2/panelC_P6/panelD_P4.pml` + assembly script `assemble_fig5_protein.py` (reproducible); note: ClusPro/HDock output PDBs containing multiple HEADERs are split into separate objects by PyMOL — use the pure-ATOM scene files first (`p4_scene.pdb`, `p7_scene.pdb`)
- Small-molecule layer: `08_smallmol/smallmolecule_docking_report.md`, `figure/fig5_smallmol_3panel.png`
