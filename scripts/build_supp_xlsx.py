# Repo-portable copy of the workspace builder (paths resolved from this file location).
# -*- coding: utf-8 -*-
"""Build Supplementary_Tables_S1-S10.xlsx (v44, 2026-10-02).
Sources: English staging-repo CSVs + generated S4/S6/S10 tables."""
import json
from pathlib import Path
import pandas as pd

WS = Path(__file__).resolve().parents[1]  # repo root
REPO = Path(__file__).resolve().parents[1]  # repo root (English CSVs)
SUPP = WS / '09_manuscript/supplementary'
DATA = SUPP / 'data'
OUT = SUPP / 'Supplementary_Tables_S1-S10.xlsx'

def rd(p, **kw):
    return pd.read_csv(p, encoding='utf-8-sig', **kw)

sheets = {}

# README
readme = pd.DataFrame({'Supplementary Tables S1–S10 — index': [
 'Network-based prioritization of venom–host interactions potentially relevant to Russell\u2019s viper–associated thrombotic microangiopathy',
 '',
 'Companion workbook to the Supplementary Material document (Supplementary_Material.docx).',
 'One sheet per table; large tables (S2, S3, S9) are provided here in machine-readable form.',
 '',
 'S1_Toxin_master        63 curated venom-toxin entries, 40 clusters (90% identity), families/species/structure status/abundance weights',
 'S2_Disease_genes       2,190 integrated disease-gene records from six sources with per-source evidence and core/broad flags',
 'S3_Toxin_target_edges  447 toxin–host edges, four-tier evidence (L2 literature-curated, L4 STRING neighbours)',
 'S4_Hub_full_ranking    Degree/MCC/EPC scores and ranks for all 54 extended-layer nodes (cytoHubba-equivalent, Python)',
 'S5a_gProfiler          116 significant terms (g:SCS<0.05), 15-gene input',
 'S5b_Enrichr            424 Enrichr rows (202 significant at BH q<0.05), three libraries',
 'S5c_Prior_pathways     Seven a priori pathway tests on both platforms',
 'S6_Sensitivity         Forced-inclusion sensitivity: input sets, set-size/topology effects, g:Profiler 11-gene rerun, verdict',
 'S6_gProfiler_11genes   Full 93-term g:Profiler result for the 11-gene (no forced inclusion) input',
 'S7_Docking             7 pairs × ClusPro/HADDOCK/HDock metrics + iMODS/PRODIGY summary; P4 retraction note',
 'S8_Small_molecule      AutoDock Vina 1.2.7: 9 receptor×ligand results, grid centres, Zn-chelation check',
 'S9a_GEO_samples        Sample tables and contrast design for GSE121297 / GSE248215',
 'S9b_GSE121297_DEG      22,453-gene fixed-probe Welch+BH table (v41 canonical)',
 'S9c_GSE248215_DEG      760-gene Welch+BH table (v41 canonical)',
 'S9d_GEO_watchlist      35 a priori molecules × two datasets (log2FC, P, significance flags)',
 'S10_Robustness         k=0..54 targeted curve, 100 per-run random curves (seed 1234), mean±SD; removal order',
 '',
 'Data archived on Zenodo: code+results concept DOI 10.5281/zenodo.23065792 (release v1.0.2 = 10.5281/zenodo.23097132);',
 'large raw files (FASTA, PDB inputs/outputs, GEO raw matrices) dataset DOI 10.5281/zenodo.23087108.',
 'Generated 2026-10-02 (change log v44).']})
sheets['README'] = readme

# S1–S3 straight from English repo copies
sheets['S1_Toxin_master'] = rd(REPO / '01_toxin_lib/toxin_master_table.csv')
sheets['S2_Disease_genes'] = rd(REPO / '02_disease_genes/disease_gene_master.csv')
sheets['S3_Toxin_target_edges'] = rd(REPO / '03_target_prediction/toxin_target_edges.csv')

# S4 generated ranking
sheets['S4_Hub_full_ranking'] = rd(DATA / 'S4_full_three_algorithm_ranking.csv')

# S5 enrichment
sheets['S5a_gProfiler'] = rd(REPO / '05_enrichment/gprofiler_raw.csv')
sheets['S5b_Enrichr'] = rd(REPO / '05_enrichment/enrichr_raw.csv')
sheets['S5c_Prior_pathways'] = rd(REPO / '05_enrichment/prior_pathway_check.csv')

# S6 sensitivity summary
GENES15 = ['F2','F3','F5','F7','F8','F10','FGA','PLG','PROC','ALB','COL4A1','F11','GP1BA','KDR','PROS1']
FORCED = ['F2','F5','F10','FGG','PROC','VCAM1','ICAM1','SELE','HAVCR1']
GENES11 = [g for g in GENES15 if g not in FORCED]
ext = set(json.load(open(WS / '04_network/intersection_sets.json', encoding='utf-8'))['extended'])
forced_in_ext = sorted(set(FORCED) & ext)
d11 = rd(DATA / 'S6_gprofiler_input11_no_forced.csv')
def term(d, key):
    h = d[d.native.str.contains(key, regex=False, na=False)]
    if len(h):
        r = h.iloc[0]
        return f'P = {r.p_value:.1e}, {r.intersection_size}/{r.query_size} genes'
    return 'not significant (g:SCS ≥ 0.05)'
d15 = rd(DATA / 'S6_gprofiler_input15_verify.csv')
s6 = pd.DataFrame({'S6 — Sensitivity to forced inclusion of nine a priori genes': [
 'Forced-inclusion genes (not covered by any of the six disease-gene sources; added per documented analysis plan):',
 ', '.join(FORCED), '',
 'Block 1 — enrichment input sets',
 f'Main input (Hub 10 ∪ strict core 10), n = 15: {", ".join(GENES15)}',
 f'Sensitivity input (forced genes removed), n = 11: {", ".join(GENES11)}', '',
 'Block 2 — disease-gene set sizes',
 'Core (main) set: 1,042 → 1,033 genes; total library: 2,190 → 2,181 genes',
 'A priori four-axis watchlist coverage by the six sources: 27/27 → 18/27 (the nine forced genes are uncovered by definition)', '',
 'Block 3 — intersection and topology (extended layer, 54 nodes / 321 edges)',
 'Strict core: 10 → 9 nodes (loses F10)',
 f'Forced genes present in the extended layer: {", ".join(forced_in_ext) if forced_in_ext else "none"}',
 'Hub 10 loses F2, F5, F10, PROC (4/10); the six retained hubs (F3, F7, F8, FGA, PLG, ALB) keep their relative degree order among the remaining nodes', '',
 'Block 4 — enrichment stability (g:Profiler g:GOSt, g:SCS, hsapiens, GO+KEGG+REAC; rerun 2026-10-02)',
 f'15-gene verification rerun: 116 terms — identical term set to the archived analysis (reproducibility check passed)',
 f'11-gene sensitivity run: 93 terms (full table in sheet S6_gProfiler_11genes)',
 f'  REAC:R-HSA-140877 Formation of Fibrin Clot:  15-gene {term(d15,"R-HSA-140877")}  →  11-gene {term(d11,"R-HSA-140877")}',
 f'  KEGG:04610 Complement and coagulation cascades:  15-gene {term(d15,"KEGG:04610")}  →  11-gene {term(d11,"KEGG:04610")}',
 f'  REAC:R-HSA-76002 Platelet activation:  15-gene {term(d15,"R-HSA-76002")}  →  11-gene {term(d11,"R-HSA-76002")}',
 f'  REAC:R-HSA-114608 Platelet degranulation:  15-gene {term(d15,"R-HSA-114608")}  →  11-gene {term(d11,"R-HSA-114608")}',
 f'  REAC:R-HSA-159854 gamma-carboxylation:  15-gene {term(d15,"R-HSA-159854")}  →  11-gene {term(d11,"R-HSA-159854")}',
 '  KEGG:04610 drivers in the 11-gene run: F3, F7, F8, FGA, PLG, F11, PROS1 (all coagulation/fibrinolysis arm; complement arm = 0, as in the main analysis)', '',
 'Verdict: the dominant axis-2 coagulation/platelet theme is qualitatively stable without forced inclusion;',
 'effect sizes and ranks are reduced (e.g., fibrin clot 11/15 → 7/11); gamma-carboxylation becomes marginal;',
 'PI3K–Akt / NF-κB / fluid shear stress remain non-significant in both runs.']})
sheets['S6_Sensitivity'] = s6
sheets['S6_gProfiler_11genes'] = d11

# S7 docking: manual parse of the raw CSV (unquoted commas inside the coverage field)
def parse_docking(p):
    rows = []
    lines = open(p, encoding='utf-8-sig').read().splitlines()
    header = lines[0].split(',')
    for ln in lines[1:]:
        if not ln.strip():
            continue
        remark = ''
        if ',"' in ln:
            ln, r = ln.split(',"', 1)
            remark = r.rstrip('"')
        f = ln.split(',')
        fixed8, verdict = f[:8], f[-1]
        coverage = ','.join(f[8:-1])
        rows.append(fixed8 + [coverage, verdict, remark])
    cols = ['pair','toxin','host','platform','top1_cluster_members','center_energy','lowest_energy',
            'interface_residue_count','functional_site_coverage','verdict','notes']
    df = pd.DataFrame(rows, columns=cols)
    return df
dock = parse_docking(REPO / '07_docking/docking_results.csv')
assert len(dock) == 12, f'docking rows {len(dock)}'
dock.loc[len(dock)] = ['P4 (note)','snaclec (AlphaFold)','GP1BA','ALL','—','—','—','—',
 'RETRACTED 2026-10-02: receptor chain misidentified (1M10 chain A = VWF-A1 domain, not GP1BA); pair withdrawn from the evidence chain',
 'retracted','see manuscript §2.1 deviation table; Fig. 6 panel D blanked']
imods = rd(REPO / '08_md/imods_prodigy_summary.csv')
# simpler: two sheets — docking metrics and orthogonal stability
sheets['S7_Docking'] = dock
imods2 = imods.copy()
sheets['S7_iMODS_PRODIGY'] = imods2

# S8 small molecule
vina = rd(REPO / '08_smallmol/vina_results.csv')
grid = pd.DataFrame([l.split() for l in open(WS / '08_smallmol/grid_centers.txt').read().splitlines() if l.strip()],
                    columns=['receptor','grid_center_x','grid_center_y','grid_center_z'])
zn = pd.DataFrame([
 ['batimastat × RVV-X (2E3X)','2.29','2.22','1.40','correct chelation'],
 ['marimastat × RVV-X (2E3X)','2.24','2.22','2.34','correct chelation'],
 ['batimastat × daborhagin-K (AF + modelled Zn)','7.97','8.91','10.34','no chelation — arm not trusted'],
], columns=['pair','pose1_Zn_dist_Å','pose2_Zn_dist_Å','pose3_Zn_dist_Å','verdict'])
s8 = pd.concat([vina, pd.DataFrame([{}]),
    pd.DataFrame([{'docking_pair':'Grid centres (Å), 26×26×26 Å box, exhaustiveness=8, num_modes=9, Vina 1.2.7, Meeko 0.8.0'}]),
    grid, pd.DataFrame([{}]),
    pd.DataFrame([{'docking_pair':'Zn-chelation geometry check (shortest ligand-atom→Zn distance)'}]), zn],
    ignore_index=True)
sheets['S8_Small_molecule'] = s8

# S9 GEO
import gzip, re
def samples(f, used_map, platform):
    txt = gzip.open(f, 'rt', errors='ignore').read()
    gsms = re.findall(r'"(GSM\d+)"', txt.split('!Sample_geo_accession')[1].split('\n')[0])
    titles = [t.strip() for t in re.findall(r'"([^"]+)"', txt.split('!Sample_title')[1].split('\n')[0])]
    return pd.DataFrame({'GSM': gsms, 'title': titles, 'platform': platform,
                         'group_in_this_study': [used_map.get(t.split(': ')[-1] if ': ' in t else t, 'not used') for t in titles]})
s121 = samples(WS / '06_geo/GSE121297-GPL570_series_matrix.txt.gz',
    {'HUVEC-1 Static ctrl':'control (static)','HUVEC-2 Static ctrl':'control (static)','HUVEC-3 Static ctrl':'control (static)',
     'HUVEC-1 Static Rcab':'RCab-treated (static)','HUVEC-2 Static Rcab':'RCab-treated (static)','HUVEC-3 Static Rcab':'RCab-treated (static)'},
    'GPL570 (HG-U133 Plus 2.0)')
s248 = samples(WS / '06_geo/GSE248215_series_matrix.txt.gz',
    {'Control-1':'control (PBS)','Control-2':'control (PBS)','DR-A-24h':'D. russelii venom 24 h','DR-B-24h':'D. russelii venom 24 h','DR-C-24h':'D. russelii venom 24 h'},
    'NanoString Fibrosis V2 (760 genes)')
s9a = pd.concat([s121, pd.DataFrame([{}]), s248], ignore_index=True)
sheets['S9a_GEO_samples'] = s9a
sheets['S9b_GSE121297_DEG'] = rd(REPO / '06_geo/GSE121297_deg_static_rcab_vs_ctrl.csv')
sheets['S9c_GSE248215_DEG'] = rd(REPO / '06_geo/GSE248215_deg_DR24h_vs_ctrl.csv')
sheets['S9d_GEO_watchlist'] = rd(REPO / '06_geo/geo_watchlist_combined.csv')

# S10 robustness
sheets['S10_Robustness'] = rd(DATA / 'S10_robustness_per_run_curves.csv')
sheets['S10_Removal_order'] = rd(DATA / 'S10_targeted_removal_order.csv')

with pd.ExcelWriter(OUT, engine='openpyxl') as w:
    for name, df in sheets.items():
        df.to_excel(w, sheet_name=name[:31], index=False)
print('sheets:', list(sheets))
for n, d in sheets.items():
    print(f'  {n}: {d.shape}')
print('saved:', OUT)
