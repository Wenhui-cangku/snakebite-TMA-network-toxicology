# P7 svVEGF×VEGFR2 All-Atom MD Operations Checklist (Online Platforms)

> Purpose: add a real MD layer to the manuscript (pre-submission review item 13). Run all-atom MD
> on the most critical complex (P7) to produce RMSD/RMSF/Rg trajectories for a supplementary figure
> plus one corroborating sentence in the main text.
> Input file ready: `08_md/input/md_P7_fixed_noh.pdb` (376 residues, 3063 heavy atoms, loops rebuilt).
> Chain IDs: chain A = VEGFR2 (198 consecutive residues), chains B/C = svVEGF dimer.

## Platform choice (WebGRO registration unavailable; alternatives tested)

| Platform | URL | Cost | Length cap | Status (tested 2026-10-03) | Recommendation |
|---|---|---|---|---|---|
| **VisualDynamics 3.0** | https://visualdynamics.fiocruz.br | **Free** | 5 ns/run | Online 200, operated by Fiocruz | ★★★ first choice |
| Neurosnap GROMACS | https://neurosnap.ai | Paid | Custom | Online 200 | ★★ backup (when 20 ns+ needed) |
| Tamarind Bio GROMACS | https://www.tamarind.bio | Paid | Microsecond-scale | Online 200 | ★ backup |
| MDWeb | mdweb.irbbarcelona.org | — | — | Unreachable | Unavailable |

**VisualDynamics preferred**: formally published in BMC Bioinformatics 2023 (DOI 10.1186/s12859-023-05234-y, 130+ citations),
GROMACS backend, supports apoprotein mode (a protein–protein complex can be uploaded as an apoprotein),
produces RMSD/RMSF/Rg plots in the browser plus downloadable .xtc/.gro trajectories. 5 ns is short, but the
primary dynamics evidence in this study comes from iMODS edNMA; MD serves only as a stability spot-check,
sufficient to answer "does the pose fall apart instantly".
For 20 ns scale, use Neurosnap (paid) or continue from the last frame after a VisualDynamics 5 ns run.

---

## 1. VisualDynamics registration

1. Open https://visualdynamics.fiocruz.br → "Launch App" → request an account (Request access)
2. Use an institutional email (glmu.edu.cn) and state academic research use
3. Wait for the approval email (manual review by Fiocruz, typically 1–3 days)

## 2. Submission form (Apoprotein mode, field by field)

| Field | Entry |
|---|---|
| PDB file | Upload `md_P7_fixed_noh.pdb` |
| Force field | **AMBER94 / AMBER99SB** (whichever is listed; avoid GROMOS+PRODRG combinations) |
| Water model | **TIP3P** |
| Box type | **Cubic / Triclinic** (default is fine) |
| Distance to box edge | 1.0 nm |
| Neutralize | Checked (automatic Na⁺/Cl⁻) |
| Ignore hydrogens | Checked (input has no hydrogens) |
| Simulation length | **5 ns** (maximum) |
| Temperature | 300 K |

## 3. Run and retrieval

- One job at a time; email notification on completion
- Download: RMSD / RMSF / Rg / SASA plots (export PNG directly from the webpage) + trajectory files
- Place the result zip in `08_md/results_visualdynamics/`

## 4. Interpretation criteria (self-check before writing into the manuscript)

| Metric | Passing behaviour | Meaning |
|---|---|---|
| RMSD | Plateaus within 5 ns (±0.1 nm fluctuation) | Complex overall stable |
| RMSF | Interface residues below the molecular average | Interface rigidity, cross-confirms iMODS edNMA |
| Rg | Flat, no sustained rise | No unfolding/dissociation |

If RMSD keeps climbing → write honestly "the pose was not stable over the 5 ns window" and downgrade the pair's conclusion (same honesty standard as the P4 retraction).

## 5. Manuscript integration points (to be written once results arrive)

- **Methods 2.8** addition: "The P7 complex was subjected to a 5 ns all-atom MD spot-check (VisualDynamics, GROMACS backend, AMBER force field, TIP3P, 300 K)."
- **Results 3.6** one additional sentence + **SM** new Figure S_MD (RMSD/RMSF/Rg triptych)
- **Limitations**: 5 ns is only a stability spot-check and does not replace long MD or free-energy calculations
- References to add: Zanchi et al., BMC Bioinformatics 24 (2023) 133, doi:10.1186/s12859-023-05234-y + GROMACS (doi:10.1016/j.softx.2015.06.001)

## 6. Local fallback route (if all platforms unavailable / queues too long)

`08_md/run_md_P7.py` (OpenMM script) is ready, but the local 20-core CPU only reaches ~2–5 ns/day for the
179k-atom system — a 20 ns run takes about a week with the machine running continuously; only reconsider after
installing an NVIDIA GPU (OpenCL/CUDA gives a 50–100× speedup).
Then: `python run_md_P7.py smoke` self-check → `python run_md_P7.py` long run (checkpoint-restart enabled).


---

## Appendix A. Input-file preprocessing record (✅ completed 2026-10-03)

Original chain composition of `md_P7_svVEGF_VEGFR2_hdock.pdb`: chain R = VEGFR2 (132–329, missing loops 264–271 and 278–282), chains A/B = complete svVEGF dimer.

**Loops rebuilt with PDBFixer** (SEQRES constructed from UniProt P35968; 185/185 residue identity check passed):
- **`md_P7_fixed_noh.pdb` (3063 heavy atoms, no hydrogens — the file to upload to VisualDynamics)**
- `md_P7_fixed.pdb` (hydrogenated version, 6103 atoms, backup)
- Chain IDs reordered: chain A = VEGFR2 (198 consecutive residues), chains B/C = svVEGF dimer
- PyMOL visual check passed: rebuilt loops lie on the VEGFR2 surface, far from the svVEGF binding interface
- Preprocessing script: `input/_fix_p7.py` (reproducible)

---

## Appendix B. VisualDynamics submission record (✅ submitted 2026-10-03 20:15 UTC)

- Platform version: VisualDynamics **v5.0.9** (note: different interface from v3.0; no temperature/neutralisation options; MDP generated automatically from platform templates)
- Job page: https://visualdynamics.fiocruz.br/simulations/657c3177-06f6-4687-834a-dcd4dac7c453
- **Job ID: 525**, Macromolecule name: mdp7fixednoh, Status: QUEUED → waiting to run
- Actual form parameters:
  | Item | Value |
  |---|---|
  | Simulation Type | **Free Protein** (pure protein complex) |
  | PDB | md_P7_fixed_noh.pdb (3063 heavy atoms) |
  | Force Field | **amber99sb-ildn** (AMBER99SB-ILDN, side-chain-corrected; cite this in the manuscript) |
  | Water Model | tip3p |
  | Box Type | cubic |
  | Box Distance | **1.0 nm** (changed from the 0.1 default) |
  | Length | fixed 5 ns (platform hard cap) |
- Note: the Commands / MDP Files preview buttons are disabled before submission — normal behaviour, does not affect submission
- **Retrieving results**: once Status becomes FINISHED → Downloads tab on the job page → download zip → extract to `08_md\results_visualdynamics\`
- The force-field description in the manuscript methods sentence should read "AMBER99SB-ILDN force field, TIP3P water, cubic box with 1.0 nm solute–box distance"
