# GEO Transcriptome Validation Report (layer 1 of the triple dry validation)

Date: 2026-09-24 ｜ By: Kimi ｜ Status: **complete**

## 1. Datasets and contrast design

| Dataset | Model | Primary contrast | Platform / genes |
|---|---|---|---|
| GSE121297 | human HUVEC × snaclec (rhodocetin-αβ) | static RCαβ vs static control (3v3) | Affymetrix HG-U133 Plus 2.0 / 22,453 genes |
| GSE248215 | mouse skeletal muscle × *D. russelii* venom (30 µg in-vivo injection) | 24 h vs PBS control (3v2) | NanoString Fibrosis V2 Panel / 760 genes |

Method note: differential expression was explored using Welch's t-tests in Python with Benjamini-Hochberg correction; one fixed probe per gene (highest mean across the six contrast samples, chosen before testing); probes annotated via the g:Profiler convert API; NanoString used the author-provided normalised log2 matrix. **Both datasets have small sample sizes (3v3 / 3v2), and no DEG reaches adj<0.05 after BH correction** — per the reconnaissance plan, interpretation uses "nominal p<0.05 + \|log2FC\|" as exploratory judgement, labelled throughout; this limitation is written into Limitations.

v41 standardisation note (2026-10-02): the pipeline was finalised as the fully reproducible fixed-probe rule implemented in `scripts/geo_v41_reanalysis.py` (22,453 genes in GSE121297). An earlier archived run (kept locally as `..._archived21183.csv`, not uploaded) additionally resolved multi-symbol probe conflicts and yielded 21,183 genes; log2FC and raw P values of all shared genes are identical, BH values shift only through the changed denominator (e.g. VCAM1 0.75→0.76, ICAM1 0.67→0.68), and the conclusion (0 genes at BH-adjusted P<0.05) is unchanged.

## 2. Core findings (watchlist of 35 prior molecules)

### GSE121297 (human endothelium × snaclec)

- **Strong axis-4 endothelial/inflammatory activation** (nominally significant): SELE +6.24 (p=2.3e-5), VCAM1 +4.63, ICAM1 +3.01, NOS3 −0.43; at the whole-transcriptome level CXCL5 +5.68, CXCL3 +3.82, LTB +2.94, EBI3 +2.60 are likewise top signals — reproducing the original study's conclusion of snaclec→endothelial inflammatory activation; **dataset quality self-check passed**;
- Axis-3 complement: only CFB +1.69 (p=0.096 trend); C3/C5/CFH/CFI/CD46 unchanged;
- Axis 1/2: VWF, ADAMTS13, F2/F5/F10 and other coagulation factors show no transcriptional change (expected: coagulation factors are liver-synthesised and not locally regulated by endothelium).

### GSE248215 (mouse in vivo × *D. russelii* venom 24 h)

- **HMOX1 +3.05 (p=0.0013)** — strongest axis-4 oxidative-stress hit; IL6 +2.10, SERPINE1 +2.07, HAVCR1 +0.99 (kidney-injury marker), positive trends for TNF/VCAM1/ICAM1;
- KDR −0.81 (p=0.0017, among the most significant) — downregulation of endothelial repair/angiogenesis;
- Axis-3 complement: CFH +1.08 (p=0.095 trend); C3 −0.59, CFI unchanged;
- Axis 2: SERPINE1 up (fibrinolysis-inhibition direction, consistent with VICC); FGA/FGG transcription down (consumption or negative-phase direction, ns).

## 3. Verdicts on the three hypothesis axes (honest)

| Axis | Direct-target layer (Phase 3/4) | GEO transcriptome layer | Overall verdict |
|---|---|---|---|
| Axis 1 platelet/VWF | direct edge (GP1BA, VWF neighbour) | no transcriptional change | supported at the direct-action layer; neutral at the secondary transcriptional layer |
| **Axis 2 coagulation/fibrinolysis** | **strong support (Hub + dual-platform enrichment)** | SERPINE1 ↑ (fibrinolysis inhibition) | **strongest across the whole chain** |
| **Axis 3 complement** | 0 genes at the direct layer | **CFB (human endothelium, trend) + CFH (mouse in vivo, trend)** | **weak positive**: complement is neither a direct toxin target nor more than a bystander-factor trend at the transcription layer — H2 must be downgraded to "alternative complement may participate" and cannot serve as a main mechanism; written honestly into the Discussion |
| **Axis 4 endothelium/inflammation/kidney** | KDR direct edge | **strong support (SELE/VCAM1/ICAM1/HMOX1/IL6 consistent across human/mouse)** | **tied strongest with axis 2** |

## 4. Conclusions

1. Toxin→coagulation/fibrinolysis (axis 2) is the dominant mechanism; the transcriptome layer shows no contradiction;
2. Endothelial inflammatory activation (axis 4) replicates across species in **human endothelial cells** and the **target-species in-vivo model**, forming the second pillar;
3. Complement (axis 3) lacks direct support in all three evidence layers: no L1/L2 edge, 0 enrichment-driver genes, only CFB/CFH trends at the transcription layer — per the SOP's pre-specified strategy this is reported as a **negative result** in the Discussion (H2 downgraded);
4. The in-vivo upregulation trend of HAVCR1 (KIM-1, kidney-injury marker) provides a preliminary transcriptional clue for the AKI phenotype.

## 5. Output files

- `06_geo/GSE121297_deg_static_rcab_vs_ctrl.csv` (22,453-gene full table), `GSE121297_deg_static_rcab_vs_ctrl_v41reanalysis.csv` (canonical v41 output), `GSE121297_watchlist.csv`
- `06_geo/GSE248215_deg_DR24h_vs_ctrl.csv`, `GSE248215_deg_DR24h_vs_ctrl_v41reanalysis.csv`, `GSE248215_deg_DR24h_vs_DR1h.csv`
- `06_geo/geo_watchlist_combined.csv` (35 molecules × two datasets)
- `06_geo/figure4_volcano.png` (Figure 4a/4b), `figure4c_watchlist.png` (Figure 4c)
- Raw archive: series matrices ×3, `gpl570_probe2symbol.csv` (61,013 probe mappings)
- Re-runnable scripts: `scripts/geo_v41_reanalysis.py` (canonical v41 pipeline), `scripts/geo_gse121297.py`, `geo_figures.py`
- Excel: change log v12

## 6. Limitations (written into the manuscript)

Small sample sizes (3v3, 3v2 controls); no snakebite-patient transcriptome (GEO negative result); NanoString panel limited to 760 genes; tissue-extrapolation distance from mouse muscle/human umbilical-vein endothelium to glomerular endothelium; no DEG reaches adj<0.05 under BH correction, so all interpretation is based on nominal p values and labelled exploratory.
