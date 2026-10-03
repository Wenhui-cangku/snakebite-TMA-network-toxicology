# -*- coding: utf-8 -*-
"""v51 text revision: hypothesis framing, transcriptomics methods, docking controls,
Data availability de-versioning. Single-run paragraphs verified beforehand."""
import copy, shutil
from pathlib import Path
from docx import Document

MS = Path(r"E:\陈文辉资料夹\论文\蛇伤\snakebite_TMA\09_manuscript")
DOCX = MS / "蛇伤TMA论文_CBI投稿版_EN_v41_revised.docx"
bak = MS / "蛇伤TMA论文_CBI投稿版_EN_v41_revised.docx.bak_v51"
if not bak.exists():
    shutil.copy2(DOCX, bak); print("backup ->", bak.name)

d = Document(DOCX)
ps = d.paragraphs

def replace_in(i, old, new):
    t = ps[i].text
    assert old in t, f"para {i} missing old text: {old[:60]}..."
    assert len(ps[i].runs) >= 1
    ps[i].runs[0].text = t.replace(old, new)
    for r in ps[i].runs[1:]:
        r.text = ""
    print(f"[{i}] replaced ({len(old)} -> {len(new)} chars)")

# --- E1: insert pre-specified hypotheses paragraph after intro para [11] ---
HYP = ("The documented analysis plan (Section 2.1) pre-specified three hypotheses before data "
       "inspection: H1 \u2014 an SVMP\u2013VWF/ADAMTS13 axis was expected to dominate the candidate "
       "mechanism; H2 \u2014 complement- and endothelium-related enrichment was expected to be "
       "prominent; and one further exploratory hypothesis (H3). After the intersection and "
       "enrichment results were inspected, H1 was reformulated toward coagulation/platelet "
       "prominence and H2 toward complement as a secondary host response; whether results had "
       "been seen before each change is reported in the protocol-deviation table (Section 2.1), "
       "and the reformulated hypotheses are revisited in Sections 4.1 and 4.6.")
new_p = copy.deepcopy(ps[11]._p)
ps[11]._p.addnext(new_p)
# re-open paragraph list view via parent
from docx.text.paragraph import Paragraph
newpara = Paragraph(new_p, ps[11]._parent)
newpara.runs[0].text = HYP
for r in newpara.runs[1:]:
    r.text = ""
print("inserted hypotheses paragraph after [11]")

# --- E2: [34] small-molecule methods ---
replace_in(34,
 "metal-coordination parameterization (ligand protonation, Zn charge/atom typing, coordination angles and number) and known-ligand redocking references were not implemented and are acknowledged as a limitation.",
 "metal-coordination parameterization beyond the formal +2 Zn charge (ligand protonation, Zn atom typing, coordination angles and number) was not implemented and is acknowledged as a limitation. "
 "Two control experiments were added to bound this limitation: (i) a known-ligand redocking benchmark \u2014 the co-crystallized peptidomimetic hydroxamate WR2 was re-docked into its receptor, "
 "the P-I SVMP BaP1 (PDB 2W15, 1.05 \u00c5 resolution, catalytic Zn retained at +2 formal charge), using the identical protocol (26 \u00c5 grid box on the catalytic Zn, exhaustiveness = 8, num_modes = 9); "
 "and (ii) two non-chelating negative ligands (caffeine, PubChem CID 2519; D-glucose, CID 5793) docked against the RVV-X pocket under the same settings.")

# --- E3: [37] transcriptomics methods ---
replace_in(37,
 "No gene reached BH-adjusted P < 0.05 in either dataset; all interpretations are based on nominal P < 0.05 and are labeled exploratory.",
 "No gene reached BH-adjusted P < 0.05 in either dataset; all interpretations are based on nominal P < 0.05 and are labeled exploratory. "
 "For both datasets the deposited processed matrices were used as provided (GEO series matrix for GSE121297; the original study's normalized NanoString nCounter matrix for GSE248215); "
 "no additional re-normalization was applied. Because the control arm of GSE248215 contains only two samples, per-gene Welch's tests have minimal power and no empirical-Bayes variance "
 "shrinkage (the limma alternative, not available in the Python-only environment, is recorded in the protocol-deviation table); these comparisons are therefore used strictly as "
 "exploratory trend corroboration rather than inferential evidence.")

# --- E4: [74] results ---
replace_in(74,
 "A single distance does not demonstrate coordination chemistry: hydroxamate protonation state, Zn charge/atom typing, donor angles, and coordination number were not parameterized, and no known-ligand redocking reference was performed; these results are screening-level clues only.",
 "A single distance does not demonstrate coordination chemistry: hydroxamate protonation state, Zn charge/atom typing, donor angles, and coordination number were not parameterized; these results are screening-level clues only. "
 "Two control experiments bound this limitation: re-docking the co-crystallized hydroxamate WR2 into BaP1 (2W15) reproduced the crystal pose (top-pose heavy-atom RMSD 1.45 \u00c5, best score \u22127.97 kcal/mol, "
 "Zn\u2013O 2.22 \u00c5), supporting the pose plausibility of this protocol; and the non-chelating negative ligands caffeine and D-glucose scored \u22125.51 and \u22126.27 kcal/mol against RVV-X \u2014 "
 "1.3\u20132.1 kcal/mol weaker than the hydroxamates \u2014 indicating that pocket scoring separates metal-chelating inhibitors from inert small molecules at the screening level.")

# --- E5: [102] 4.5 clause ---
replace_in(102,
 "with Vina scores (\u22127.64/\u22127.53 kcal/mol) in the range reported for SVMP inhibitors in comparable docking settings; in vitro neutralization experiments",
 "with Vina scores (\u22127.64/\u22127.53 kcal/mol) in the range reported for SVMP inhibitors in comparable docking settings, and with the protocol bounded by a known-ligand redocking benchmark and negative ligands (Section 3.7); in vitro neutralization experiments")

# --- E6: [104] H2 discussion ---
replace_in(104,
 "Our a priori hypothesis H2 (complement participating in TMA amplification as a secondary host response) was not supported by direct evidence in the assembled dataset; we report this as an unresolved question rather than a negative conclusion.",
 "Our pre-specified hypothesis H2 (that complement- and endothelium-related enrichment would be prominent; Section 2.1) was not supported as stated: no direct evidence for complement "
 "involvement was identified in the assembled dataset. Following the documented reformulation (protocol-deviation table, Section 2.1), complement involvement is now treated as a possible "
 "secondary host response, and we report it as an unresolved question rather than a negative conclusion.")

# --- E7: [121] Data availability de-versioning ---
replace_in(121,
 "The v41 revision adds the corrected GEO re-analysis (fixed probe-summarization rule, Welch's t-tests + BH: GSE121297_deg_static_rcab_vs_ctrl_v41reanalysis.csv; GSE248215_deg_DR24h_vs_ctrl_v41reanalysis.csv) and the corrected robustness outputs (robustness_results_v41.json; k = 0 origin, 50% = 27/54 nodes), now included in the archived release.",
 "The release includes the corrected GEO re-analysis (fixed probe-summarization rule, Welch's t-tests + BH correction: GSE121297_deg_static_rcab_vs_ctrl_v41reanalysis.csv; GSE248215_deg_DR24h_vs_ctrl_v41reanalysis.csv) and the corrected robustness outputs (robustness_results_v41.json; k = 0 origin, 50% = 27/54 nodes).")

# --- E8: deviation table "Docking controls" row ---
tb = d.tables[0]
for row in tb.rows:
    if row.cells[0].text.strip() == 'Docking controls':
        assert 'Not performed' in row.cells[2].text
        row.cells[2].paragraphs[0].runs[0].text = ("Performed in the final revision: known-ligand redocking benchmark "
            "(2W15 BaP1\u2013WR2, top-pose RMSD 1.45 \u00c5) + 2 negative ligands (caffeine, D-glucose)")
        row.cells[3].paragraphs[0].runs[0].text = "Added to bound the metal-parameterization limitation"
        row.cells[4].paragraphs[0].runs[0].text = "n/a (methodological control)"
        print("deviation table: Docking controls row updated")

d.save(DOCX)
print("saved:", DOCX.name)
