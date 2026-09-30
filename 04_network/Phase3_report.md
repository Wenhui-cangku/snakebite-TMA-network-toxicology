# Phase 3 Build Report — Intersection, PPI and Topology Analysis

Date: 2026-09-24 ｜ By: Kimi ｜ Status: **complete (programmatically re-runnable parts); optional Cytoscape GUI review**

## 1. Venn intersection (Figure 2a)

- Predicted toxin targets (L1+L2) **15** ∩ disease-gene core set (six sources) **1,042** = **candidate core target set n = 10**:
  COL4A1, F10, F11, F5, FGA, GP1BA, KDR, PLG, PROC, PROS1;
- Where the 5 excluded targets went: FGB and FN1 are in the **wide set** (GC 104.7 / 107.2, below core thresholds; candidates for sensitivity rescue); **F9, PRSS1, CTRB1 are entirely absent from all six sources** (weak F9–TMA association is expected; PRSS1/CTRB1 are digestive enzymes unrelated to TMA, so exclusion is reasonable);
- Figure: `04_network/figure2a_venn.png`.

## 2. Extended layer (L4 sensitivity layer)

Per SOP design the main analysis uses L1+L2; the strict core of only 10 nodes cannot support topology statistics, so an **extended layer of 54 nodes** was built from L4 STRING neighbours ∩ core set (51 nodes) as the sensitivity/topology layer, labelled separately from the strict layer throughout.

## 3. STRING PPI (dual-threshold exports)

| Layer | score≥0.7 | score≥0.4 (sensitivity) |
|---|---|---|
| strict core10 | 14 edges, 2 isolated (COL4A1, KDR) | 26 edges, 0 isolated |
| extended54 | **321 edges, 0 isolated** | 615 edges, 0 isolated |

Exports: `ppi_core10_score{400,700}.tsv`, `ppi_extended61_score{400,700}.tsv`.

## 4. Hub genes (MCC ∩ Degree ∩ EPC Top-20 three-ranking intersection, Python reproduction of cytoHubba)

Intersecting the three algorithms' Top-20 lists on the extended layer (54 nodes / 321 edges) gives **Hub = 10**:

| Gene | Degree | Layer | Axis |
|---|---|---|---|
| F2 (thrombin) | 25 | extended | axis 2 |
| F3 (tissue factor) | 22 | extended | — |
| PLG (plasminogen) | 21 | strict | axis 2 |
| PROC (protein C) | 18 | strict | axis 2 |
| ALB (albumin) | 17 | extended | — (generic STRING hub artifact, recorded as such) |
| F8 | 16 | extended | — |
| FGA | 16 | strict | axis 2 |
| F10 | 15 | strict | axis 2 |
| F7 | 14 | extended | — |
| F5 | 14 | strict | axis 2 |

- Technical note: EPC has low discrimination on this dense network (at p=0.5 percolation all nodes belong to the same connected component and scores converge), so the three-ranking intersection is effectively driven by MCC/Degree — consistent with cytoHubba behaviour on dense subnetworks such as the coagulation cascade; stated honestly in Methods;
- Figure: `04_network/figure2b_ppi.png` (54 nodes; Hub orange / strict core green; structurally the coagulation cluster, the platelet cluster GP1BA–GP6–GP9–ITGA2B/ITGB3–VWF, the VEGF cluster, and the complement C4A/C4B/C4BPB cluster are clearly distinguishable).

## 5. Four-axis mapping and QC checkpoints (H1/H2 tests)

| Checkpoint molecule | Location | Notes |
|---|---|---|
| **F10** | strict core + Hub | ✅ direct hit (dual RVV-X / anticoagulant-PLA2 pathways) |
| **F2** | Hub (extended layer) | ✅ thrombin, entered via STRING neighbours |
| VWF | extended layer (not Hub) | inside the platelet cluster, not a topological centre |
| GP1BA | strict core (not Hub) | axis-1 direct target |
| KDR | strict core (not Hub) | axis-4 direct target (VEGF cluster) |
| ADAMTS13 / C3 / VCAM1 | absent | **not in the direct toxin-target layer** — no L1/L2 edge connects them; an expected negative |

**Honest conclusion**: the SOP QC point warns that "absence of all of ADAMTS13/VWF/F2/F10/C3/VCAM1 = intersection too narrow" — in this result F2/F10 are hit, VWF is in the extended layer, and ADAMTS13/C3/VCAM1 are absent. This absence is **not a threshold problem but a direct consequence of the layered design**: the L2 layer contains only 15 experimentally reported direct targets; complement (axis 3) and ADAMTS13 involvement are, per hypothesis H2, **host secondary responses** rather than direct toxin substrates, and should be tested at the Phase 4 enrichment layer (complement-pathway significance), not the direct-edge layer. This interpretation is written into the Discussion; a version with FGB/FN1 wide-set rescue can serve as sensitivity analysis.

## 6. Output files

- `04_network/figure2a_venn.png` (Figure 2a), `figure2b_ppi.png` (Figure 2b)
- `04_network/ppi_{core10,extended61}_score{400,700}.tsv` (4 PPI tables)
- `04_network/hub_genes.csv` (Hub 10 + three-algorithm scores + axis)
- `04_network/phase3_topology.json` (complete Top-20 of all three rankings)
- Re-runnable scripts: `scripts/build_phase3.py`, `redraw_fig2a.py`, `draw_fig2b.py`
- Excel: new "Hub genes" sheet + change log v10

## 7. Outstanding

1. Cytoscape 3.10 GUI review (official cytoHubba/MCODE implementations) — manual step, can be done anytime; ~~four-layer heterogeneous-network SVG main figure~~ materials ready (2026-09-30: `04_network/cytoscape/` contains cyjs/nodes.csv/edges.csv + import-and-style guide; 30 nodes, 49 edges; open in the GUI and export SVG);
2. PRISMA intersection n can now be filled with 10;
3. Phase 4: Metascape / clusterProfiler enrichment on Hub 10 + strict core 10, four-axis colouring and prior-pathway test table.
