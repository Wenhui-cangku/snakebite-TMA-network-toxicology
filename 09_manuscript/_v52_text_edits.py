# -*- coding: utf-8 -*-
"""v52 text edits: items 7/8/9/10 of pre-submission review."""
import shutil, sys
from docx import Document

SRC = '蛇伤TMA论文_CBI投稿版_EN_v41_revised.docx'
shutil.copy(SRC, SRC + '.bak_v52')
d = Document(SRC)
ps = d.paragraphs

def set_text(p, new):
    # keep first run's formatting, drop others
    runs = p.runs
    assert runs, 'no runs'
    runs[0].text = new
    for r in runs[1:]:
        r.text = ''

def replace_in(idx, old, new, count=1):
    t = ps[idx].text
    assert old in t, 'NOT FOUND in [%d]: %s' % (idx, old[:60])
    set_text(ps[idx], t.replace(old, new, count))

# --- 10a. Title shorten ---
assert 'Network-based prioritization' in ps[0].text
set_text(ps[0], "Network toxicology of venom\u2013host interactions in Russell's viper\u2013associated thrombotic microangiopathy")

# --- 10b. Keywords: +AOP, drop D. siamensis ---
assert ps[6].text.startswith('Keywords:')
set_text(ps[6], "Keywords: Snakebite envenoming; Thrombotic microangiopathy; Daboia russelii; Network toxicology; Adverse outcome pathway; Venom\u2013host interactions")

# --- 10c. Abstract: pre-specified hypotheses statement ---
replace_in(5,
    "We conducted an exploratory network toxicology study integrating curated venom proteins",
    "Hypotheses were pre-specified before data inspection and reformulated as documented. We conducted an exploratory network toxicology study integrating curated venom proteins")

# --- 8a. STRING version ---
replace_in(29,
    "The PPI was exported from STRING [22] at combined score \u2265 0.7",
    "The PPI was exported from STRING v12.5 [22] (functional associations; accessed 2026-09-22) at combined score \u2265 0.7")

# --- 8b. g:Profiler release + Enrichr access date ---
replace_in(31,
    "g:Profiler g:GOSt [25] (three GO ontologies [28] + KEGG [29] + Reactome [30], g:SCS correction with the default annotated-gene background, accessed 2026-09-24)",
    "g:Profiler g:GOSt [25] (release e114_eg62; three GO ontologies [28] + KEGG [29] + Reactome [30], g:SCS correction with the default annotated-gene background, accessed 2026-09-24)")
replace_in(31,
    "Enrichr [26,27] (KEGG_2021_Human / Reactome_2022 / GO_Biological_Process_2023, Benjamini\u2013Hochberg FDR [31])",
    "Enrichr [26,27] (accessed 2026-09-24; gene-set libraries KEGG_2021_Human / Reactome_2022 / GO_Biological_Process_2023, Benjamini\u2013Hochberg FDR [31])")

# --- 7. GSE248215 downgraded to descriptive ---
replace_in(38,
    "Differential expression was explored using Welch's t-tests in Python, with Benjamini\u2013Hochberg correction across tested genes [31];",
    "For GSE121297 (3 vs 3), differential expression was explored using Welch's t-tests in Python, with Benjamini\u2013Hochberg correction across tested genes [31];")
replace_in(38,
    "No gene reached BH-adjusted P < 0.05 in either dataset; all interpretations are based on nominal P < 0.05 and are labeled exploratory.",
    "No gene reached BH-adjusted P < 0.05 in GSE121297; all interpretations are based on nominal P < 0.05 and are labeled exploratory.")
replace_in(38,
    "Because the control arm of GSE248215 contains only two samples, per-gene Welch's tests have minimal power and no empirical-Bayes variance shrinkage (the limma alternative, not available in the Python-only environment, is recorded in the protocol-deviation table); these comparisons are therefore used strictly as exploratory trend corroboration rather than inferential evidence.",
    "For GSE248215 (3 vs 2), no statistical testing was performed: with two samples in the control arm, per-gene variance estimates are unreliable, and neither Welch's tests nor empirical-Bayes shrinkage (limma; not available in the Python-only environment, recorded in the protocol-deviation table) can yield meaningful inference \u2014 only descriptive log2 fold-changes are reported for this dataset.")
replace_in(38,
    "with log2FC, nominal P, and BH-adjusted P reported per gene and per tissue",
    "with log2FC reported per gene and per tissue (nominal P and BH-adjusted P for GSE121297 only)")

# --- 7b. Results paragraph: GSE248215 descriptive ---
replace_in(80,
    "No gene reached BH-adjusted P < 0.05 in either dataset (22,453 genes tested in GSE121297; 760 in GSE248215); the following are nominal, exploratory observations.",
    "No gene reached BH-adjusted P < 0.05 in GSE121297 (22,453 genes tested); for GSE248215 (760 panel genes, 3 vs 2) only descriptive fold-changes are reported, without statistical testing. The following are nominal, exploratory observations.")
replace_in(80,
    "GSE248215 (mouse skeletal muscle 24 h after D. russelii venom [45]): HMOX1 +3.05 (P = 0.0013, BH P = 0.095), KDR \u22120.81 (P = 0.0017, BH P = 0.095), IL6 +2.10 (P = 0.092, BH P = 0.33), SERPINE1 +2.07 (P = 0.122, BH P = 0.36), HAVCR1 +0.99 (P = 0.144, BH P = 0.38); complement components CFB/CFH showed non-significant trends, and murine Sele was not measured by the panel.",
    "GSE248215 (mouse skeletal muscle 24 h after D. russelii venom [45]; descriptive log2FC only, no testing): HMOX1 +3.05, KDR \u22120.81, IL6 +2.10, SERPINE1 +2.07, HAVCR1 +0.99; complement components CFB/CFH showed small-magnitude changes, and murine Sele was not measured by the panel.")

# --- 7c. Fig. 9 caption: panel B becomes descriptive ---
assert ps[82].text.startswith('Fig. 9.')
set_text(ps[82], "Fig. 9. Expression comparison of the two surrogate datasets. A = GSE121297 volcano plot (Welch's t-tests; nominal P; red points mark nominal P < 0.05 only; 0 of 22,453 genes reached BH-adjusted P < 0.05). B = GSE248215 descriptive log2 fold-changes of watchlist genes (3 vs 2; no statistical testing performed).")

# --- 9. Move Ki calibration to Limitations ---
replace_in(70,
    " The attempted calibration against the experimental Ki = 0.19 nM of the P6 Kunitz\u2013plasmin interaction [9] is not valid: the modeled complex used plasminogen rather than the inhibited active enzyme, and the 2.6 kcal/mol deviation between the predicted \u0394G (\u221210.7) and the Ki-derived value (\u2248 \u221213.3) corresponds to roughly an 80-fold difference in Kd at 25 \u00b0C; no external error model or additional anchors are available. These values are therefore reported as descriptive model properties (Fig. 7A), without a calibration claim.",
    " These values are therefore reported as descriptive model properties (Fig. 7A), without a calibration claim; the attempted calibration against the experimental Ki of the P6 Kunitz\u2013plasmin interaction is discussed in Section 4.7.")
replace_in(107,
    "PRODIGY and NMA descriptors depend on the input poses and are not independent validations;",
    "PRODIGY and NMA descriptors depend on the input poses and are not independent validations; an attempted calibration of PRODIGY \u0394G against the experimental Ki = 0.19 nM of the P6 Kunitz\u2013plasmin interaction [9] was not valid, because the modeled complex used plasminogen rather than the inhibited active enzyme, and the resulting 2.6 kcal/mol deviation (\u2248 80-fold in Kd at 25 \u00b0C) has no external error model or additional anchors;")

d.save(SRC)
print('v52 text edits saved OK')
