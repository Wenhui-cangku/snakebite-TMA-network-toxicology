# HDock Detailed Tutorial (Phase 5B · P7 svVEGF → VEGFR2 Template Docking)

Date: 2026-09-28 | Platform: http://hdock.phys.hust.edu.cn/ (Huazhong University of Science and Technology, free for academic use)
Scope: P7 (svVEGF × VEGFR2) — a homologous complex template 3V2A (VEGF-A × VEGFR2) exists, and HDock's **template docking** is exactly suited to this situation.
It can also serve as an optional third-party blind-docking cross-check for P4/P5 (same method, simply without a template).

## 0. Preparation specific to this tutorial (already computed for you)

Interface residues measured from the 3V2A crystal complex (5 Å contact threshold), for the "binding-site residues" field:

- **Receptor VEGFR2 (chain R, 132–329): 26 interface residues** (copy into the receptor binding-site field):
  `133,135,137,195,196,215,216,217,218,219,220,221,253,254,255,256,257,258,273,274,275,276,288,311,312,313`
- Ligand-side svVEGF and VEGF-A are homologous proteins with different numbering — **leave the ligand binding-site field empty** and let template alignment handle it automatically (manual mapping is error-prone; better left to the server);
- Template = **3V2A**, matched **automatically** by the server's hybrid algorithm (there is no template entry field on the page; just make sure "Template-free docking only" is NOT ticked). Our receptor is 3V2A chain R itself and the ligand is homologous to chain A VEGF-A, so a template hit is highly likely;
- The full 3V2A is stored at `prepared/3V2A_full.pdb` (chain R 132–329 = VEGFR2 D2 domain; chain A 13–107 = VEGF-A) for the final PyMOL superposition check.

## 1. Submission steps

1. Open http://hdock.phys.hust.edu.cn/ — account registration is available in the top-right corner (keeps history); **it also works without registration** (just leave an email for notification);
2. Go to the **Docking** page; Docking type = **Protein–protein** (default);
3. **Input Receptor**: choose Upload, upload `07_docking/prepared/H_VEGFR2_3V2A_R.pdb`;
4. **Input Ligand**: choose Upload, upload `07_docking/prepared/T_svVEGF_1WQ9_AB.pdb` (svVEGF homodimer, upload the whole file);
5. Expand **Advanced Options (Optional)** (item by item, per the real interface):
   - **Template-free docking only**: ⚠️ **Do NOT tick!** There is no separate template-PDB field on this page — HDOCK's hybrid algorithm automatically matches homologous templates in its template library (for this system the receptor is 3V2A chain R itself and the ligand is homologous to VEGF-A, so 3V2A will be used as template automatically); ticking this option degrades the run to pure blind docking;
   - Symmetric multimer docking: leave empty;
   - SAXS experimental data file: leave empty;
   - Open **"▸ Specify the residues of the binding site"**: paste the 26 residue numbers from §0 into the **receptor field** (comma-separated); **leave the ligand field empty** (ligand side is handled automatically by template alignment);
6. If an email was entered, double-check it → Jobname: `P7_svVEGF_VEGFR2` → **Submit**; record the returned **Job ID / result-page URL** (archive a screenshot).

## 2. Waiting and retrieval

- A single pair usually takes **1–3 hours** (queue varies); an email arrives on completion;
- The result page gives Top10/Top100 models, each with a **Docking score** (more negative = better) and a **Confidence score**:
  - **> 0.7 = high confidence**; 0.5–0.7 = medium; < 0.5 = low (not usable as supporting evidence);
- If a template was used, a **ligand RMSD** against the template is also given (< 10 Å means the pose matches the VEGF-A template);
- Download **Model 1** (top-ranked) PDB and save to `07_docking/results/hdock/P7/model1.pdb`.

## 3. QC (PyMOL, 3 minutes)

```
load results/hdock/P7/model1.pdb, model
load prepared/3V2A_full.pdb, template
super model and resn+chain *, template and chain R   # or simply align by receptor chain
```
Visual check: does svVEGF in the model sit on the **same binding face** of the VEGFR2 D2 domain (i.e. where VEGF-A sits in 3V2A)? Matching pose + ligand RMSD < 10 Å = template docking credible.

## 4. Verdict and back-fill

- **Verdict (same standard as the docking guide §4)**: Confidence score > 0.7 and pose covering the §0 interface-residue region = structural-level support for P7;
- Back-fill to me: Docking score, Confidence score, ligand RMSD, confirmation of model1.pdb storage;
- I will consolidate into `docking_results.csv`, `Phase5_report.md`, the Excel change log (v16), and produce the P7 complex panel.

## 5. FAQ

| Symptom | Fix |
|---|---|
| Template mapping fails / sequence-alignment error | Tick "Template-free docking only" and rerun as pure blind docking (binding-site residue restraints are retained); use the results as usual, noting this in the interpretation |
| Result page won't open / times out | HDock keeps results for ~2 weeks; visit off-peak; the Job ID can be retrieved from the homepage "Retrieve" |
| Want to validate P4/P5 in passing | Same workflow with the corresponding files, no template (P4 receptor H_GP1BA_1M10_A.pdb / ligand T_snaclecQ38L02_AF.pdb; P5 receptor H_FXa_2W26_AB.pdb / ligand T_PLA2_1KPM_A.pdb) |
| Queue over 24 h | Normal (public server); advance the ClusPro/HADDOCK lines first |

## 6. Citation (for Methods)

Yan Y, Tao H, He J, Huang SY. The HDOCK server for integrated protein–protein docking. *Nat Protoc* 2020;15:1829–1852.
