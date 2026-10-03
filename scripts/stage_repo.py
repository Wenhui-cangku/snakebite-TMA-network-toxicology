# -*- coding: utf-8 -*-
"""一键组装 GitHub 待上传仓库文件夹（按 GitHub上传文件清单.md 白名单复制）。
输出: E:\\陈文辉资料夹\\论文\\蛇伤\\snakebite-TMA-network-toxicology/
"""
import shutil
from pathlib import Path

SRC = Path(__file__).resolve().parents[1]                # snakebite_TMA
DST = SRC.parent / "snakebite-TMA-network-toxicology"    # 工作区根下并列新文件夹

FILES = [
    # 根
    "README.md", "LICENSE", "CHANGELOG.csv",
    # 00_protocol
    "00_protocol/analysis_plan_v1.md", "00_protocol/GEO_recon_report.md",
    "00_protocol/data_management_table_public.xlsx",
    "00_protocol/PRISMA_flowchart_phase1_filled.png", "00_protocol/PRISMA_flowchart_toxin_filled.png",
    # 01_toxin_lib
    "01_toxin_lib/Phase1A_构建报告.md", "01_toxin_lib/UniProt与VenomZone检索操作步骤.md",
    "01_toxin_lib/toxin_master_table.csv", "01_toxin_lib/toxins_nr90.fasta", "01_toxin_lib/all_toxins_raw.fasta",
    "01_toxin_lib/uniprot_russelii_reviewed1.fasta", "01_toxin_lib/uniprot_russelii_reviewed1.tsv",
    "01_toxin_lib/uniprot_russelii_reviewed2.fasta", "01_toxin_lib/uniprot_russelii_reviewed2.tsv",
    "01_toxin_lib/uniprot_supplement_kunitz_crisp.tsv",
    "01_toxin_lib/supp_crisp.fasta", "01_toxin_lib/supp_kunitz.fasta",
    "01_toxin_lib/supp_svmp_ncbi.fasta", "01_toxin_lib/supp_svmp_ncbi.tsv",
    "01_toxin_lib/supp_venomzone_check.fasta", "01_toxin_lib/supp_venomzone_check.tsv",
    # 02_disease_genes
    "02_disease_genes/Phase1B_构建报告.md", "02_disease_genes/手工导出指南.md",
    "02_disease_genes/disease_gene_master.csv", "02_disease_genes/diseases_knowledge.tsv",
    "02_disease_genes/disgenet_raw.csv", "02_disease_genes/omim_entries_raw.json",
    "02_disease_genes/omim_merge_summary.json", "02_disease_genes/omim_search_mims.json",
    "02_disease_genes/opentargets_raw.csv", "02_disease_genes/ctd_merge_summary.json",
    # 03_target_prediction
    "03_target_prediction/Phase2_构建报告.md", "03_target_prediction/toxin_target_edges.csv",
    "03_target_prediction/literature_evidence_draft.csv", "03_target_prediction/phase2_string_neighbors.json",
    "03_target_prediction/uniprot_fulltext_raw.txt", "03_target_prediction/图2数据源_毒素靶点15_疾病主集1042.xlsx",
    # 04_network
    "04_network/Phase3_构建报告.md", "04_network/build_figure4_network.py", "04_network/robustness_analysis.py",
    "04_network/hub_genes.csv", "04_network/intersection_sets.json", "04_network/phase3_topology.json",
    "04_network/robustness_results.json",
    "04_network/robustness_analysis_v41.py", "04_network/robustness_results_v41.json",
    "04_network/ppi_core10_score400.tsv", "04_network/ppi_core10_score700.tsv",
    "04_network/ppi_extended61_score400.tsv", "04_network/ppi_extended61_score700.tsv",
    "04_network/figure2a_venn.png", "04_network/figure2b_ppi.png", "04_network/figure3c_robustness.png",
    "04_network/cytoscape/edges.csv", "04_network/cytoscape/nodes.csv",
    "04_network/cytoscape/figure4_hetero_network.cyjs", "04_network/cytoscape/figure4_hetero_network_safe.cyjs",
    "04_network/cytoscape/figure4_hetero_network.cx", "04_network/cytoscape/figure4_hetero_network.xgmml",
    "04_network/cytoscape/Figure4_4layer_network_final.svg",
    "04_network/cytoscape/build_cx.py", "04_network/cytoscape/build_xgmml.py", "04_network/cytoscape/postprocess_svg.py",
    "04_network/cytoscape/Cytoscape导入与样式指南.md",
    # 05_enrichment
    "05_enrichment/Phase4_构建报告.md", "05_enrichment/gprofiler_raw.csv", "05_enrichment/enrichr_raw.csv",
    "05_enrichment/enrichment_gprofiler_sig116.csv", "05_enrichment/enrichment_enrichr_sig.csv",
    "05_enrichment/prior_pathway_check.csv", "05_enrichment/figure3_enrichment_bubble.png",
    # 06_geo
    "06_geo/GEO验证报告.md",
    "06_geo/GSE121297_deg_static_rcab_vs_ctrl.csv", "06_geo/GSE121297_watchlist.csv",
    "06_geo/GSE121297_deg_static_rcab_vs_ctrl_v41reanalysis.csv",
    "06_geo/GSE248215_deg_DR24h_vs_ctrl.csv", "06_geo/GSE248215_deg_DR24h_vs_DR1h.csv",
    "06_geo/GSE248215_deg_DR24h_vs_ctrl_v41reanalysis.csv",
    "06_geo/geo_watchlist_combined.csv", "06_geo/gpl570_probe2symbol.csv",
    "06_geo/figure4_volcano.png", "06_geo/figure4c_watchlist.png",
    # 07_docking
    "07_docking/Phase5_报告.md", "07_docking/Phase5A_结构准备报告.md",
    "07_docking/HADDOCK详细教程.md", "07_docking/HDock详细教程.md",
    "07_docking/analysis_haddock_hdock.py", "07_docking/analysis_hdock_p7.py", "07_docking/redo_superpose.py",
    "07_docking/docking_pairs.csv", "07_docking/docking_results.csv",
    # 08_md
    "08_md/MD_SOP.md", "08_md/analyze_imods.py", "08_md/gen_imods_pdb.py",
    "08_md/prep_md_inputs.py", "08_md/prep_prodigy.py", "08_md/imods_prodigy_summary.csv",
    "08_md/mdp/ions.mdp", "08_md/mdp/md.mdp", "08_md/mdp/minim.mdp",
    "08_md/mdp/mmpbsa.in", "08_md/mdp/npt.mdp", "08_md/mdp/nvt.mdp",
    # 08_smallmol
    "08_smallmol/小分子对接报告.md", "08_smallmol/vina_results.csv", "08_smallmol/grid_centers.txt",
    "08_smallmol/ligands/batimastat.sdf", "08_smallmol/ligands/marimastat.sdf", "08_smallmol/ligands/varespladib.sdf",
    "08_smallmol/figure/fig5_smallmol_RVVX_batimastat.pml",
    "08_smallmol/figure/fig5_smallmol_RVVX_marimastat.pml",
    "08_smallmol/figure/fig5_smallmol_PLA2_varespladib.pml",
    # 09_manuscript
    "09_manuscript/make_fig1_fig7.py",
    "09_manuscript/fig_en/fig02_03_11_en.py", "09_manuscript/fig_en/fig04_09_10_en.py",
    "09_manuscript/fig_en/fig05_en.py", "09_manuscript/fig_en/fig08_patch_en.py",
    # scripts
    "scripts/build_phase2_edges.py", "scripts/build_phase3.py", "scripts/build_phase4.py",
    "scripts/merge_ctd.py", "scripts/merge_omim.py",
    "scripts/geo_gse121297.py", "scripts/geo_figures.py", "scripts/geo_v41_reanalysis.py",
    "scripts/draw_fig2b.py", "scripts/redraw_fig2a.py", "scripts/redraw_prisma.py", "scripts/prep_docking.py",
]

# assets_en 12 张正式图（v53：哈希与 docx 内嵌槽位一一对应）
ASSETS = ["figure1_workflow.png", "figure2a_venn.png", "figure2b_ppi.png", "figure3_enrichment_bubble.png",
          "figure5_network.png", "fig6_protein_template.png", "fig6_nma_prodigy_v41.png",
          "fig8_smallmol_template.png",
          "figure4_volcano.png", "figure4c_watchlist.png", "figure3c_robustness.png", "figure7_aop_mechanism.png"]
FILES += [f"09_manuscript/assets_en/{a}" for a in ASSETS]

# v51–v53 修订与重绘脚本（可复现性）
FILES += [
    "04_network/cytoscape/render_fig5_from_cyjs.py",
    "07_docking/figure/_assemble_fig6_template.py",
    "07_docking/figure/ov_P7.pml", "07_docking/figure/ov_P2.pml", "07_docking/figure/ov_P6.pml",
    "08_smallmol/figure/_assemble_fig8_template.py",
    "08_smallmol/figure/ov_RVVX_bat.pml", "08_smallmol/figure/ov_RVVX_mar.pml", "08_smallmol/figure/ov_PLA2_var.pml",
    "08_md/MD在线平台操作清单_P7.md", "08_md/run_md_P7.py", "08_md/input/_fix_p7.py",
    "09_manuscript/_v51_text_edits.py", "09_manuscript/_v52_text_edits.py", "09_manuscript/_v53_refs.py",
    "09_manuscript/_swap_figs_v51.py", "09_manuscript/_swap_fig68_template.py",
    "scripts/stage_repo.py",
]

GITIGNORE = "__pycache__/\n*.pyc\n*.docx\n*.pdf\n*.ps1\n*.log\n"

if DST.exists():
    shutil.rmtree(DST)
DST.mkdir(parents=True)
(DST / ".gitignore").write_text(GITIGNORE, encoding="utf-8")

missing, copied, total = [], 1, 0  # .gitignore 已算 1
for rel in FILES:
    s = SRC / rel
    if not s.exists():
        missing.append(rel)
        continue
    d = DST / rel
    d.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(s, d)
    copied += 1
    total += s.stat().st_size

print(f"copied: {copied} files, {total/1024/1024:.1f} MB -> {DST}")
if missing:
    print("MISSING:")
    for m in missing:
        print("  -", m)
else:
    print("missing: none")
