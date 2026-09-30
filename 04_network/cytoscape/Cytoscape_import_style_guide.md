# Figure 4 Four-Layer Heterogeneous Network — Cytoscape Import & Style Guide

Updated: 2026-09-30 | Corresponding SOP: Phase 2, line 214 "four-layer heterogeneous network (core main figure)"
Design basis: toxin → core target → enriched pathway → TMA phenotype; nodes colored by category, edges styled by evidence level.

## 0. File inventory (all under `04_network/cytoscape/`)

| File | Purpose |
|---|---|
| `figure4_hetero_network.xgmml` | **Preferred**: classic format recognized by all Cytoscape 3.x versions; coordinates/colors/shapes/borders fully embedded (added 2026-09-30) |
| `figure4_hetero_network.cx` | CX exchange format (coordinates embedded); usable in newer Cytoscape |
| `figure4_hetero_network.cyjs` | Cytoscape.js JSON with layered-layout coordinates embedded; if your environment does not recognize it, use XGMML/CX |
| `figure4_hetero_network_safe.cyjs` | Safe cyjs version (emoji → [PASS]); use when emoji parsing errors occur |
| `nodes.csv` | Node table (30 nodes: 7 toxins + 12 targets + 6 pathways + 5 phenotypes), with color/shape/coordinate columns |
| `edges.csv` | Edge table (49 edges: 14 direct interactions + 20 pathway memberships + 11 mechanism inferences + 4 phenotype progressions) |
| `figure4_preview.png` | matplotlib preview (for quick topology checking, not the final publication figure) |
| `../build_figure4_network.py` | Generator script; re-run after editing nodes/edges to regenerate cyjs/csv/png |
| `build_cx.py` / `build_xgmml.py` | Conversion scripts from cyjs to CX / XGMML |

## 1. Method 1 (recommended): import XGMML

**XGMML first**: Cytoscape → `File → Import → Network from File…` → select `figure4_hetero_network.xgmml` → loads directly: four-layer horizontal layout, node colors/shapes/Hub bold borders, edge colors all applied automatically.

XGMML is a classic format with built-in support from Cytoscape 2.x through 3.10, and will not fall into the "table import" dialog. If you accidentally disturb the layout: `Edit → Undo`, or re-import.

### 1.1 Troubleshooting import errors (added 2026-09-30)

The cyjs file itself has passed integrity validation (30 nodes / 49 edges, valid JSON, no dangling references, no duplicate ids).

**Typical error**: a popup saying "The network cannot be created without selecting the source and target columns", or a preview window showing raw JSON text — this means Cytoscape did not recognize the cyjs/cx format and treated the file as a plain table. Resolve in this order:

1. **Preferred: use the XGMML file** `figure4_hetero_network.xgmml` (recognized by all 3.x versions, styles and coordinates fully embedded);
2. If you insist on cyjs/cx: make sure the entry point is `File → Import → Network from File…` (not File → Open, and never double-click); if emoji compatibility is in doubt, use `figure4_hetero_network_safe.cyjs`;
3. **Fallback: CSV import** (Method 2). Note: when importing `edges.csv` you must set the **source column as Source (green dot), target column as Target (red dot), and interaction column as Interaction Type (blue dot)** in the dialog, otherwise you will get the "source/target columns not selected" error;
4. After import, verify the QC points in §5 (30 nodes / 49 edges).

## 2. Method 2: CSV import (when full customization is needed)

1. `File → Import → Network from File…` → select `edges.csv`:
   - Source Column = `source`, Target Column = `target`, Interaction Type = `interaction`;
2. `File → Import → Table from File…` → select `nodes.csv`:
   - Import Data As = `Node Table Columns`, Key Column = `id`;
3. Layout: `Layout → yFiles Layouts → Hierarchic` (orientation left to right),
   or manually arrange rows by the `layer` column (Layout → Grid Layout → by attribute).

## 3. Styles (Style panel settings)

### Nodes (Node tab)
| Property | Mapping | Value |
|---|---|---|
| Fill Color | Column=`fill_color`, Mapping Type=**Passthrough** | toxin red #D62728 / target blue #1F77B4 / pathway green #2CA02C / phenotype purple #9467BD |
| Shape | Column=`shape`, Passthrough | toxin HEXAGON / target ELLIPSE / pathway ROUND_RECTANGLE / phenotype DIAMOND |
| Label | Column=`label`, Passthrough | — |
| Size | layer=1: 60, layer=2: 45, layer=3: 70×40 (use `Custom graphics` or disable Size Lock to set height/width separately), layer=4: 65 | Discrete Mapping by `layer` is also fine |
| Border Width | Column=`hub_status`, Discrete | "Hub+strict" = 4 (bold black frame marks Hub), others = 1.5 |
| Label Font Size | 12–14 | pathway nodes may be reduced to 10 (long names) |

### Edges (Edge tab)
| Property | Mapping | Value |
|---|---|---|
| Line Type | Column=`line_type`, Passthrough (or Discrete by `interaction`) | direct interaction solid / membership solid / mechanism inference dashed / progression dotted |
| Width | Column=`width`, Passthrough | 3.0 / 1.2 / 2.0 / 2.0 |
| Stroke Color | Discrete by `interaction` | direct #333333 / membership #AAAAAA / mechanism #777777 / progression #9467BD |
| Target Arrow Shape | Discrete: mechanism and progression = ARROW (directed); direct/membership = NONE | — |

## 4. Exporting the publication figure

- `File → Export → Network to Image…` → format **SVG** (vector, for submission) + PNG (600 dpi, preview);
- Before export: View → Show Graphics Details ON; confirm no label occlusion (long pathway names may be nudged slightly);
- The legend (4 node colors + 4 line types) should be added separately as text or composed in AI/PS — Cytoscape does not auto-generate legends.

## 5. QC checklist (verify item by item after import)

- [ ] Node count = **30** (7+12+6+5), edge count = **49**
- [ ] RVV-X should have 3 outgoing solid lines (F10/F9/PROS1); F10 has 3 incoming edges (RVV-X/PLA2/Kunitz) — coagulation-axis hub
- [ ] KDR connects only svVEGF (in) and Focal Adhesion + VEGFR2 Signaling (out) — Axis 4 independent cluster
- [ ] Among the 5 phenotype-layer nodes there are 4 purple dotted lines (VICC → triad + leakage → AKI)
- [ ] Dashed edges (mechanism inference) total 11, all falling on L3→L4

## 6. Design notes (material for Methods/figure legend)

- **L1→L2 includes only literature direct interactions with score=1.0** (STRING-expanded neighbors are excluded from the main figure to guarantee evidence level); the three RVV-X subunits are merged into a single node;
- **L2→L3 membership edges** are the intersection of g:Profiler/Enrichr consensus genes with the 12 direct targets;
- **L3→L4 are mechanism-inference edges** (drawn dashed), a lower evidence level than solid lines, and must be declared in the figure legend;
- ECM–receptor interaction and Focal adhesion are significant on a single platform (Enrichr) only; this is noted in node remarks and should also be noted in the legend;
- Hub nodes (F10/F5/FGA/PLG) are marked with bold black frames, corresponding to the Phase 3 cytoHubba three-list intersection result.
