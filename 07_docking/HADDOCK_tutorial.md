# HADDOCK 2.4 Web Server Detailed Tutorial (Phase 5B · Restraint-Guided Docking)

Date: 2026-09-28 | Scope: the four pairs P1 / P2 / P3 / P6 (with well-defined catalytic/cleavage-site restraints)
P4 / P5 / P7 have no clear catalytic-residue restraints and rely primarily on ClusPro blind docking (see the docking submission guide §1, §3); not covered by this tutorial.

**All upload files are ready**: 8 files under `07_docking/prepared/haddock/`, named by pair — upload directly, do not modify.
All active-residue numbers have been verified by script against the PDB files (not UniProt numbering) and can be copied as-is.

---

## 1. Register an account (do it today — review takes 1–2 days)

1. Open https://wenmr.science.uu.nl/haddock2.4/
2. Click **Register**: fill in name, affiliation, email; linking an ORCID is recommended (if you have none, register free at https://orcid.org in 5 minutes);
3. In the purpose field, state academic use (e.g. "protein-protein docking for snake venom toxin–host target interaction study");
4. Submit and wait for the manual-review email (usually 1–2 business days); jobs can only be submitted after approval.

> ⏰ **Time note**: registration review is the only "everything stops if blocked" step of this phase — do it first. While waiting, run ClusPro in parallel (no review needed).

## 2. Overall workflow

```
Log in → Submit a new job → interface level = guru
→ Molecule 1 = toxin (ligand) → fill active residues
→ Molecule 2 = host (receptor) → fill active residues
→ passive residues auto → keep default sampling → submit
→ email notification (hours–1 day) → download cluster1 top1 from result page
```

## 3. Step-by-step

### Step 1 Enter the submission page
After login, top menu **Submit** → "HADDOCK2.4 submission". Set Interface level to **guru** (only guru/expert allow manually entering active residues; the easy interface does not).

> Selecting guru for the first time jumps to a **permission-request page** ("restricted to users with certain attributes"): choose Guru in the dropdown, paste the following text into the Description field (416/550 characters, 59 words), Submit, then wait for the review email (1–2 business days):
> ```
> We study interactions between Russell's viper (Daboia russelii) venom toxins and human coagulation proteins (factor Xa, factor V, fibrinogen, plasminogen). Known catalytic residues (SVMP zinc motif, SVSP catalytic triad, Kunitz reactive loop) and cleavage sites will be used as active/passive residue restraints to guide docking. Guru access is needed to define these residues manually. Academic use only. Thank you.
> ```

### Step 2 Fill in Molecule 1 (toxin)
- ⚠️ **The page is a three-page wizard** (Input data → Input parameters → Docking parameters); **you must complete each page and click Next at the bottom to unlock the next** — clicking the top tabs directly raises "No data have been found from previous step(s)";
- **Which chain of the structure must be used?**: choose **All** (the P1 trimer is submitted as the whole file; residues 145–155 exist only on chain A — verified unambiguous);
- **Molecule 1 PDB file**: upload `prepared/haddock/PX_T_*.pdb`; Kind = "Protein or Protein-Ligand"; keep coarse-grain / cyclic / Fix at it0 / charged termini **all OFF**; keep default Segment ID;
- **Active residues** (page 2 "Input parameters", collapsible section "Active/Passive residues – Selection #1"): copy from the §4 quick-reference table, comma-separated, e.g. `145,146,149,155`;
- **Passive residues**: leave empty, and tick ☑ **"Define passive residues automatically around the active residues"** (the server takes surface neighbors of the active residues automatically);
- Keep defaults for everything else (Histidine protonation, Semi-flexible, Fully-flexible, EM restraints) — the server handles them.

### Step 3 Fill in Molecule 2 (host)
Same as Step 2 (Selection #2 collapsible section); upload the host file such as `P1_H_FXa_A.pdb` and enter the host-side active residues.

### Step 4 Run parameters (keep all defaults)
- Sampling: it0 (rigid docking) = 1000, it1 (semi-flexible refinement) = 200, water (solvent refinement) = 200 — **defaults are fine, do not change**;
- Disulfide bonds: auto-detected by the server;
- Advanced restraints (ambig restraints / tbl files): leave empty — not needed.

### Step 5 Submit and wait
- After submission, record the **Job ID and result-page URL** (screenshots into `results/haddock/` are fine too);
- All 4 pairs can be **submitted in parallel** without queue conflicts (shared account queue, but each pair returns independently);
- Each pair typically takes hours to 1 day; an email arrives upon completion.

### Step 6 Download results
The result page ranks by cluster (cluster 1 = best). Download:
- the **top1 structure of cluster1** (filename like `cluster1_1.pdb`);
- the on-page statistics: cluster1 **HADDOCK score**, **cluster size**, **Z-score**.

Store under `07_docking/results/haddock/P1/` (same for P2, P3, P6; create the folder if missing).

## 4. Quick-reference table for the 4 pairs (copy directly)

### P1　RVV-X → FXa (activation-cleavage proposition)
| Item | File | Active residues (copy) | Basis |
|---|---|---|---|
| Molecule 1 toxin | `P1_T_RVVX_noZn.pdb` (trimer, Zn removed) | `145,146,149,155` | Zn catalytic motif HELSHNLGMYH (145–155): catalytic His145/Glu146/His149 + coordinating His155, verified |
| Molecule 2 host | `P1_H_FXa_A.pdb` (chain A only) | `16,17,18,19,20,21` | Heavy-chain N terminus IVGGQE…, i.e. the **new N terminus produced by activation cleavage** |

> ⚠️ **Numbering trap (already hit for you)**: 2W26 uses **chymotrypsin numbering**, not UniProt numbering. After cleavage at the FX activation site Arg194–Ile195 (mature-FX numbering), the new N terminus is Ile16 in this file; the 194/195 in the file are catalytic-region Asp194/Ser195 — **do NOT enter them**.

### P2　RVV-Vγ → FV (cleavage at Arg1545–Ser1546)
| Item | File | Active residues (copy) | Basis |
|---|---|---|---|
| Molecule 1 toxin | `P2_T_RVVV.pdb` | `42,193,194,195,196,197` | Catalytic His (originally 41, renumbered to **42** on 2026-09-28) + GDSGG motif (193–197, containing Ser195), verified |
| Molecule 2 host | `P2_H_FV_B.pdb` | `1543,1544,1545,1546,1547,1548` | Cleavage site Arg1545–Ser1546 (verified 1545=ARG, 1546=SER) ±2 |

> Note: the 3S9C B chain is itself an FV-fragment co-crystal (direct structural evidence); this docking is a validation complement on full-length FV — state this when interpreting results.

### P3　daborhagin-K → fibrinogen Aα (α-fibrinogenolysis proposition)
| Item | File | Active residues (copy) | Basis |
|---|---|---|---|
| Molecule 1 toxin | `P3_T_daborhaginK.pdb` (AF model) | `339,340,343,349` | Zn catalytic motif HEIGHNLGLTH (339–349) catalytic residues, verified |
| Molecule 2 host | `P3_H_FIB_A.pdb` (FGA chain only) | `195,196,197,198,199,200` | C-terminal surface of the Aα chain within the structure (…PSDRQ) |

> ⚠️ **Limitation (write into the paper)**: the 3GHG crystal contains only FGA 27–200; the true cleavage region lies in the αC domain (~221–610, outside the structure). The restraint here uses the best in-structure proxy position; interpret results as "binding feasibility" rather than "precise cleavage site". Using only chain A avoids restraint ambiguity from overlapping numbering with chains B/C; note the missing β/γ-chain context when interpreting.

### P6　Kunitz → plasmin (Ki = 0.19 nM inhibition proposition)
| Item | File | Active residues (copy) | Basis |
|---|---|---|---|
| Molecule 1 toxin | `P6_T_Kunitz.pdb` (AF model) | `38,39,40,41,42` | Reactive loop 31–46 (CNLAPESGRCRAHLRR, verified) loop-tip region; candidate P1 = Arg39/Arg41 |
| Molecule 2 host | `P6_H_PLG_A.pdb` | `603,646,741` | Catalytic triad His603/Asp646/Ser741, verified |

> Optional QC: open `P6_T_Kunitz.pdb` in PyMOL, run `select loop, resi 31-46` → `show surface, loop`, and visually confirm 38–42 sit at the most exposed loop tip; if a more tip-ward residue is found, take a screenshot and fine-tune the active-residue list accordingly.

## 5. Result interpretation (standard to copy into Methods)

| Metric | Meaning | Pass line |
|---|---|---|
| HADDOCK score | Weighted energy terms (lower is better) | **≤ −100** |
| Cluster size | Members of the best cluster | larger = more stable; < 4 suggests unreliability |
| Z-score | Significance vs random poses | ≤ −2.0 preferred |

**Verdict (consistent with the docking submission guide §4)**: HADDOCK score ≤ −100 **AND** the Top1 interface covers the functional site in the table above (open cluster1_1.pdb in PyMOL for a visual check) = structural-level support for the interaction.

## 6. FAQ

| Symptom | Fix |
|---|---|
| **"multiple chains with overlapping numbering: A7 - B7"** | Fixed (2026-09-28): chain B of `P1_T_RVVX_noZn.pdb` was shifted +1000, chain C +2000; re-upload the same-named file |
| **"multiple residues with number 61 in chain A / duplicated atom names"** | Fixed (2026-09-28): insertion residues (61A, 36A etc.) in `P1_H_FXa_A.pdb` and `P2_T_RVVV.pdb` were sequentially renumbered; P2 toxin active residues now use the new numbers `42,193,194,195,196,197` (tutorial §4 updated); everything else unchanged |
| Zn/ligand-related error at submission | P1 already uses the Zn-removed version (`P1_T_RVVX_noZn.pdb`) and should not trigger it again; if it still does, send me a screenshot of the error |
| "Residue number does not exist / ambiguous" | Check for a wrong file (the host must be the single-chain version under haddock/, not the multi-chain version in prepared/ root) |
| Very small cluster size, high score | Do not force a negative verdict; record the actual values and judge jointly with ClusPro results (guide §4) |
| No queue movement for over 2 days | Normal (public-server queue); run other pairs first; resubmit if over 5 days |
| Want to increase sampling for precision | Not recommended. Defaults it0=1000/it1=200/water=200 are officially validated; changing them makes comparison with literature harder |

## 7. Back-fill to me after completion

For each pair, give me 4 things (a message listing them is fine):
1. cluster1 HADDOCK score, cluster size, Z-score;
2. confirmation that `cluster1_1.pdb` has been saved to `results/haddock/PX/`;
3. PyMOL visual-check conclusion: does the interface cover the functional site (yes/no + screenshot preferred);
4. any errors or anomalies.

I will then: consolidate `docking_results.csv`, make cross-platform verdicts, build Figure 5 panels in PyMOL, write up `Phase5_report.md`, and sync the Excel change log (v14).
