# Small-Molecule Docking Report (Phase 5C · Local AutoDock Vina Layer)

Date: 2026-09-28 | Tools: AutoDock Vina 1.2.7 (Windows standalone exe, `vina_bin/`) + Meeko 0.8.0 (PDBQT preparation)

## 1. Background

This layer tests "whether known antidote/antitoxin small molecules can bind toxin catalytic pockets", providing structure-level clues for the drug-repurposing discussion:
- **batimastat / marimastat** (hydroxamate broad-spectrum metalloprotease inhibitors; reported in the literature to inhibit snake-venom SVMPs) → docked into the SVMP catalytic pocket;
- **varespladib** (PLA2 inhibitor, in clinical trials for snakebite envenoming) → docked into the PLA2 active pocket.

## 2. Methods

- Ligands: PubChem 3D SDF (batimastat CID 5362422, marimastat CID 119031, varespladib CID 155815), converted to PDBQT with `mk_prepare_ligand`;
- Receptors (`receptors/`):
  - **RVVX_A** = 2E3X chain A (SVMP catalytic domain, experimental crystal structure, **with catalytic Zn**; Zn +2 formal charge correctly written by meeko);
  - **daborhaginK** = AlphaFold model + Zn **modelled** at the NE2 centroid of the three catalytic His residues (339/343/349) (no crystal; pocket accuracy limited);
  - **PLA2_1KPM** = 1KPM chain A (experimental crystal structure; grid centred on the His48/Asp49 catalytic dyad);
- Grid box: centred on the catalytic Zn / catalytic dyad, 26×26×26 Å; exhaustiveness=8, num_modes=9, Vina scoring function;
- Result files: `results/<receptor>_<ligand>.pdbqt` (poses) and `.log` (scores), summarised in `vina_results.csv`.

## 3. Results (best affinities, kcal/mol)

| Receptor \ Ligand | batimastat | marimastat | varespladib |
|---|---|---|---|
| **RVV-X (SVMP, crystal + Zn)** | **−7.64** ✅ | **−7.53** ✅ | −7.88 |
| **daborhagin-K (SVMP, AF model)** | −5.52 | −5.12 | −5.80 |
| **PLA2 (1KPM, crystal)** | −7.28 | −7.13 | **−7.84** ✅ |

(✅ = the ligand's expected target class)

## 4. Mechanistic check (Zn chelation)

The pharmacophore of hydroxamate inhibitors must directly chelate the catalytic Zn (~2 Å). Shortest ligand-atom–to–Zn distances of the top poses:

| Docking pair | pose1 | pose2 | pose3 | Verdict |
|---|---|---|---|---|
| batimastat × RVV-X | 2.29 Å | 2.22 Å | 1.40 Å | ✅ correct chelation |
| marimastat × RVV-X | 2.24 Å | 2.22 Å | 2.34 Å | ✅ correct chelation |
| batimastat × daborhagin-K | 7.97 Å | 8.91 Å | 10.34 Å | ❌ not chelated |

The best-scoring poses simultaneously satisfy correct Zn-chelation geometry → the crystal-structure arm (2E3X) results are credible.

## 5. Conclusions and limitations (stated honestly)

1. **batimastat / marimastat × SVMP: supported** — scores ≤ −7.5 on the experimental crystal structure with correct chelation geometry, consistent with the literature on hydroxamate inhibition of venom metalloproteases;
2. **varespladib × PLA2: supported** — top-tier score on its expected target class (−7.84); note, however, that it also scores −7.88 against the RVV-X pocket, i.e. **no in silico selectivity** — used in the manuscript only as a mechanism-level clue, with selectivity conclusions left to the literature;
3. **daborhagin-K arm not adopted** — the AF model + modelled Zn combination scores weakly overall (−5.1 to −5.8) and shows no chelation; judged a model-accuracy limitation rather than a true negative; SVMP-inhibition evidence rests on the 2E3X crystal arm;
4. Vina affinity ≠ experimental Ki; used only for relative comparison and mechanistic-plausibility checking.

## 6. References

Eberhardt J, et al. J. Chem. Inf. Model. 2021 (Vina 1.2); Trott O, Olson AJ. J. Comput. Chem. 2010 (Vina).

---

## Addendum: docking control experiments (2026-10-03, pre-submission revision)

To address the methodological risks "Zn coordination not parameterised, no redocking benchmark, no negative controls", two low-cost control sets were added (all files in `controls/`, summary in `controls/docking_controls_summary.csv`):

1. **Redocking benchmark (pose plausibility)**: PDB 2W15 (P-I SVMP BaP1 co-crystallised with the peptidomimetic hydroxamate WR2, 1.05 Å, catalytic Zn retained with +2 formal charge). Redocking WR2 with the same Vina protocol (26 Å box on the catalytic Zn, exhaustiveness 8, num_modes 9): **top-pose heavy-atom RMSD = 1.45 Å (passes the ≤2.0 Å criterion), best score −7.97 kcal/mol, Zn–O 2.22 Å**. The ligand PDBQT was prepared from SMILES via RDKit/Meeko; RMSD was computed with element-grouped Hungarian matching (symmetry-corrected approximation).
2. **Negative-ligand controls**: caffeine (CID 2519) / D-glucose (CID 5793) docked against RVV-X (2E3X chain A) under identical conditions: best scores **−5.51 / −6.27 kcal/mol**, i.e. 1.3–2.1 kcal/mol weaker than the hydroxamates (−7.64/−7.53), showing that pocket scoring discriminates metal-chelating inhibitors from inert small molecules at screening level. Note: because the grid box is Zn-centred, the Zn–O distances of the negative-ligand top poses (2.38/2.21 Å) are not discriminative — the discriminative metric is the score difference, and this is stated honestly in the manuscript.

Limitations remain: metal coordination is not parameterised beyond the +2 formal charge (protonation/coordination geometry); the above controls only bound screening-level credibility and do not constitute affinity validation.
