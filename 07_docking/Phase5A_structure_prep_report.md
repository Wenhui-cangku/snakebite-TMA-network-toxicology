# Phase 5A Report — Structure Preparation for Molecular Docking

Date: 2026-09-24 | Executed by: Kimi | Status: **structure preparation complete; web docking to be submitted manually (guide ready)**

## 1. Structure-asset inventory

### Toxins (8)

| Toxin | Source | Resolution / quality | Used for |
|---|---|---|---|
| RVV-X full complex (SVMP heavy chain + snaclec light chain ×2) | PDB **2E3X** | 2.91 Å | P1 |
| RVV-Vγ | PDB **3S9C** (contains FV fragment co-crystal!) | 1.8 Å | P2 |
| PLA2 VRV-PL-VIIIa (P59071) | PDB **1KPM** | 1.8 Å | P5 |
| daboiatoxin heterodimer | PDB 2H4C | 2.6 Å | backup |
| svVEGF (P67861) | PDB **1WQ9** | 2.0 Å | P7 |
| daborhagin-K (B8K1W0) | AlphaFold DB | mean pLDDT **84.0** (>70 for 85% of residues) | P3 |
| snaclec (Q38L02) | AlphaFold DB | mean pLDDT **88.9** | P4 |
| Kunitz (H6VC06) | AlphaFold DB | mean pLDDT **88.6** | P6 |

### Host targets (8, all experimental PDB structures)

FV **7KVE** (3.3 Å cryoEM), FXa **2W26** (2.08 Å), fibrinogen **3GHG** (2.9 Å), GP1BA **1M10** (3.1 Å, with VWF A1 complex template), VEGFR2 **3V2A** (3.2 Å, with VEGF-A pose template), plasminogen **1QRZ** (2.0 Å), thrombin **1PPB** (1.92 Å).

## 2. Docking pairs (7 pairs, all corresponding to L2 literature edges with score=1.0)

| Pair | Proposition |
|---|---|
| P1 | RVV-X → FX activation cleavage |
| P2 | RVV-Vγ → FV (Arg1545 cleavage) |
| P3 | daborhagin-K → fibrinogen Aα |
| P4 | snaclec → GP1BA |
| P5 | PLA2 → FXa (anticoagulant IC50 = 130 nM) |
| P6 | Kunitz → plasmin (Ki = 0.19 nM) |
| P7 | svVEGF → VEGFR2/KDR |

Inventory: `docking_pairs.csv` (with HADDOCK active-residue hints); preprocessed files in `prepared/` (chain-extracted, waters and ligands removed, catalytic Zn retained).

## 3. Two docking-free direct structural evidences (emphasize when writing Results)

1. **3S9C**: RVV-Vγ co-crystallized with an FV substrate fragment (B chain), 1.8 Å — RVV-V→FV is already an experimental structural fact; docking serves only as full-length protein-level validation;
2. **1M10**: GP1BA–VWF A1 complex — provides the binding-site template for P4 (snaclec→GP1BA).

## 4. Local feasibility assessment (stated honestly)

- No protein–protein docking software available locally → HADDOCK 2.4 / ClusPro / HDock web platforms (the docking submission guide includes step-by-step operations and result back-filling workflow);
- Small-molecule layer (batimastat etc. × SVMP): Vina could not be installed locally initially → CB-Dock2/SwissDock web versions (note: Vina was later run locally via standalone exe — see the small-molecule docking report);
- After docking results return, I will assemble the Figure 5 panels and write the Phase 5B report.

## 5. Outputs

`07_docking/structures/` (16 raw structures), `prepared/` (16 docking-ready files), `docking_pairs.csv`, docking submission guide, rerunnable script `scripts/prep_docking.py`; Excel change-log v13.
