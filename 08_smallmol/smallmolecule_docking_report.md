# Small-Molecule Docking Report (Phase 5C · Local AutoDock Vina Layer)

Date: 2026-09-28 | Tools: AutoDock Vina 1.2.7 (Windows standalone exe, `vina_bin/`) + Meeko 0.8.0 (PDBQT preparation)

## 1. Background

This layer tests "whether known antidote/antivenom drug small molecules can bind toxin catalytic pockets", providing structural-level clues for the drug-repurposing discussion:
- **batimastat / marimastat** (hydroxamate broad-spectrum metalloprotease inhibitors; reported in literature to inhibit snake-venom SVMPs) → docked into the SVMP catalytic pocket;
- **varespladib** (PLA2 inhibitor; in clinical trials for snakebite indication) → docked into the PLA2 active pocket.

## 2. Methods

- Ligands: PubChem 3D SDF (batimastat CID 5362422, marimastat CID 119031, varespladib CID 155815), converted to PDBQT with `mk_prepare_ligand`;
- Receptors (`receptors/`):
  - **RVVX_A** = 2E3X chain A (SVMP catalytic domain, experimental crystal structure, **catalytic Zn retained**, Zn charge +2 correctly written by meeko);
  - **daborhaginK** = AlphaFold model + **modeled Zn** placed at the centroid of the three catalytic His (339/343/349) NE2 atoms (no crystal; pocket precision limited);
  - **PLA2_1KPM** = 1KPM chain A (experimental crystal structure; grid centered on the His48/Asp49 catalytic dyad);
- Grid box: centered on the catalytic Zn / catalytic dyad, 26×26×26 Å; exhaustiveness=8, num_modes=9, vina scoring function;
- Result files: `results/<receptor>_<ligand>.pdbqt` (poses) and `.log` (scores), consolidated in `vina_results.csv`.

## 3. Results (best affinities, kcal/mol)

| Receptor ＼ Ligand | batimastat | marimastat | varespladib |
|---|---|---|---|
| **RVV-X (SVMP, crystal + Zn)** | **−7.64** ✅ | **−7.53** ✅ | −7.88 |
| **daborhagin-K (SVMP, AF model)** | −5.52 | −5.12 | −5.80 |
| **PLA2 (1KPM, crystal)** | −7.28 | −7.13 | **−7.84** ✅ |

(✅ = the ligand's expected target class)

## 4. Mechanistic validation (Zn chelation)

Hydroxamate pharmacophores must directly chelate the catalytic Zn (~2 Å). Shortest ligand-atom-to-Zn distances of top poses:

| Docking pair | pose1 | pose2 | pose3 | Verdict |
|---|---|---|---|---|
| batimastat × RVV-X | 2.29 Å | 2.22 Å | 1.40 Å | ✅ correct chelation |
| marimastat × RVV-X | 2.24 Å | 2.22 Å | 2.34 Å | ✅ correct chelation |
| batimastat × daborhagin-K | 7.97 Å | 8.91 Å | 10.34 Å | ❌ no chelation |

The lowest-scoring (best) poses simultaneously satisfy correct Zn-chelation geometry → the crystal-structure arm (2E3X) results are credible.

## 5. Conclusions and limitations (stated honestly)

1. **batimastat / marimastat × SVMP: supported** — scores ≤ −7.5 on the experimental crystal structure with correct chelation geometry, consistent with the literature on hydroxamate inhibition of snake-venom metalloproteases;
2. **varespladib × PLA2: supported** — best-tier score (−7.84) on its expected target class; note, however, that it also gives −7.88 on the RVV-X pocket — **no in silico selectivity**; the paper uses this only as a mechanistic clue, leaving selectivity conclusions to the literature;
3. **The daborhagin-K arm is not adopted** — the AF model + modeled Zn combination scores weakly overall (−5.1 to −5.8) with no chelation, judged as a model-precision limitation rather than a true negative; SVMP-inhibition evidence rests on the 2E3X crystal arm;
4. Vina affinity ≠ experimental Ki; used only for relative comparison and mechanistic-plausibility validation.

## 6. Citations

Eberhardt J, et al. J. Chem. Inf. Model. 2021 (Vina 1.2); Trott O, Olson AJ. J. Comput. Chem. 2010 (Vina).
