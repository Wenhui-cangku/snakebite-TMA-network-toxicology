# Supplementary Material

**Manuscript:** An evidence-calibrated venom–host interaction map of Russell's viper envenoming: coagulation architecture and hypotheses for thrombotic microangiopathy

**Article type:** Research

**Contents:** Supplementary Methods SM.1–SM.10 and Supplementary Tables S1–S10. Large datasets are supplied in the accompanying workbook, `05_Supplementary_Tables_S1-S10_JVAT.xlsx`.

## Supplementary table index

| Table | Contents | Workbook organization |
|---|---|---|
| S1 | Protocol deviations and post hoc analysis decisions | One worksheet with the original plan, implemented analysis, timing/trigger, inferential consequence and source file for each decision |
| S2 | Source-resolved disease-gene evidence flags | Core evidence flags for 2,190 genes and a field dictionary |
| S3 | Toxin sequence library and clustering benchmark | Sixty-three toxin records, cluster summary, complete memberships and discrepant pairs |
| S4 | Edge-level toxin–host evidence audit | All 447 audited rows, channel and mechanism summaries, and the six factor X interactions |
| S5 | Background-matched enrichment | G1–G7 definitions, summary statistics and complete tested-term outputs for every group |
| S6 | Permutation and sensitivity analyses | Ten-thousand-permutation results, leave-one-source-out reconstruction, no-GeneCards analyses and g:Profiler comparisons |
| S7 | Descriptive STRING-expanded network | All 321 edges, 54 nodes, hub metrics and complete Degree/MCC/EPC Top-20 rankings |
| S8 | Structural identity and model disposition | Fifteen structure assets, seven model pairs and twelve archived docking-output rows with manuscript disposition |
| S9 | Expression-context analysis | Sample metadata, limma summary and five complete primary/sensitivity result tables |
| S10 | Targeted vascular literature search | Eighteen queries, 146 focused PubMed records and 45 mechanism-anchor records |

## SM.1. Analysis plan and post hoc decisions

The analysis plan was timestamped on 4 September 2026 and retained in the project repository; it was not prospectively registered. The prespecified interpretive framework comprised four axes: VWF–platelet interactions, coagulation–fibrinolysis, complement, and endothelial/inflammatory/renal responses. The initial hypotheses were preferential involvement of the VWF–ADAMTS13 and coagulation axes (H1), enrichment of complement and endothelial programs (H2), and tractable small-molecule interfaces at selected toxin–target complexes (H3).

H1 and H2 were reformulated after data inspection around the observed coagulation architecture and layered host-response branches. H3 was restricted to exploratory structural context after review of receptor identity, ligand activation state, structural coverage and control discrimination. These revisions are identified as post hoc rather than relabelled as prospective predictions. The resulting study output is an evidence-calibrated mechanism map and an experimental agenda, not a confirmatory causal model or a validated classifier of thrombotic microangiopathy.

Supplementary Table S1 records the original plan, implemented analysis, timing or trigger, inferential consequence and source file for each decision. In addition to hypothesis reformulation, the table covers the clustering implementation, evidence-channel reclassification, independent toxin-entity definitions, descriptive network topology, ascertainment-matched enrichment backgrounds, permutation and sensitivity analyses, limma reanalysis, removal of HAVCR1-centered renal interpretation, structural eligibility thresholds, withdrawal of P4, the plasminogen/plasmin state mismatch in P6, and the restricted interpretation of P1, P3 and P7.

**Supplementary Table S1. Protocol deviations and post hoc decisions.** Fourteen decision records are provided in the `S1_Protocol_deviations` worksheet.

## SM.2. Source-resolved disease-gene evidence resource

The disease vocabulary covered thrombotic microangiopathy, thrombotic thrombocytopenic purpura, atypical hemolytic uremic syndrome, hemolytic uremic syndrome, microangiopathic hemolytic anemia, snakebite envenoming and venom-induced consumption coagulopathy. Six database channels were integrated with a prespecified four-axis prior channel: GeneCards, Open Targets, DISEASES curated knowledge, DisGeNET CURATED records, the Comparative Toxicogenomics Database and OMIM. Human gene symbols were harmonized through UniProt/MyGene.info identifier mappings.

GeneCards records were manually exported on 22 September 2026 and thresholded at the median relevance score for each disease term. Open Targets records were retrieved through the GraphQL API, using score ≥0.05 for the broad collection and score ≥0.3 or association with at least three disease entries for core eligibility. DisGeNET records were retrieved at score ≥0.1, with score ≥0.3 used for core eligibility. CTD records were restricted to a prespecified disease whitelist; non-empty direct evidence qualified for the core, whereas InferenceScore ≥50 qualified for the broad collection. OMIM entries were restricted to phenotype-whitelisted records with mappingKey = 3. DISEASES curated associations and the prespecified four-axis molecules completed the core-eligibility channels.

The resulting resource contained 2,190 genes, including a core of 1,042 genes. Independent reconstruction from the source flags reproduced all 1,042 core memberships without omissions or additions. Sixty-five core genes carried a snakebite-specific source annotation and 31 carried a VICC-specific annotation. These provenance labels distinguish direct snakebite/VICC retrieval from associations derived from related TMA phenotypes.

The workbook retains the gene-level flags rather than unresolved placeholders or unavailable API fields. Leave-one-source-out reconstruction and analyses after removal of GeneCards are reported separately in Supplementary Table S6.

**Supplementary Table S2. Disease-gene evidence flags and field dictionary.** `S2_Core_evidence_flags` contains 2,190 gene records; `S2_Field_dictionary` defines every evidence column and the core-membership field.

## SM.3. Toxin sequence library and clustering benchmark

UniProtKB was queried on 22 September 2026 for reviewed toxin entries from *Daboia russelii* and *Daboia siamensis*. The primary query returned 52 entries and an independent *D. siamensis* export returned 28 entries, all overlapping the primary set. VenomZone/Tox-Prot curation cross-checked species coverage and venom annotation. Quality control required representation of SVMP, SVSP, PLA2, snaclec and Kunitz families and prompted family-specific recovery of Kunitz, CRISP and SVMP/disintegrin sequences.

Records were deduplicated by UniProt or GenBank accession. Transcriptome-derived host ADAM-like proteins were excluded and sequences shorter than 30 amino acids were removed after comparison with curated short-peptide entries. The merged library contained 78 unique records. Removal of 16 short fragments left 62 sequences, and VenomZone cross-checking restored the full-length PLA2 entry P86368, yielding 63 sequences. External venom-abundance annotations are family-level estimates for Sri Lankan *D. russelii* and are not entry-specific quantitative weights.

Redundancy was reduced using a custom length-seeded greedy 90%-identity procedure. Global-alignment identity was normalized to the shorter sequence and a 5-mer coverage prefilter was applied. This implementation is not CD-HIT and is not described as CD-HIT-equivalent. The same 63 sequences were clustered using usearch v11.0.667 `cluster_fast` at 90% identity.

Cluster assignments were compared over all 1,953 sequence pairs, calculated as 63 choose 2. The custom procedure produced 40 clusters and 35 within-cluster pairs; usearch produced 39 clusters and 41 within-cluster pairs. Thirty-four within-cluster pairs were shared. One pair was custom-only and seven were usearch-only, giving 1,945 concordant same/different-cluster assignments. The Rand index was therefore 1,945/1,953 = 0.995903738, reported to three decimal places as 0.996. The custom-only pair was G8XQX1–Q4F867. The seven usearch-only pairs comprised A0A223PK22–A0A223PK48 and six pairwise merges among A8CG84, C0HK16, P59071, P84674 and P86368 that are explicitly listed in the workbook.

These differences are consistent with marginal merge decisions near the identity threshold and with different identity denominators and heuristic merge behavior. Downstream evidence curation and structural analyses use specific accessions rather than cluster boundaries.

**Supplementary Table S3. Toxin library and complete clustering benchmark.** `S3_Toxin_library` contains 63 records; `S3_Cluster_summary`, `S3_Cluster_membership` and `S3_Discrepant_pairs` preserve the full comparison and its arithmetic.

## SM.4. Mechanism-typed toxin–host evidence audit

Every row of the original toxin–host table was audited for toxin identity, independent toxin entity, host target, interaction mechanism, protein state, PMID support and evidence channel. The 447 rows comprised 398 STRING-neighborhood rows, 33 primary-literature rows, 11 UniProt-annotation rows without a row-specific PMID, four family-level rows and one similarity-inference row. Of 49 rows initially labelled as literature evidence, 33 had primary-literature support and formed the main curated interaction set.

Interaction mechanisms were preserved as enzymatic cleavage, inhibition, direct binding or activation rather than collapsed into a single numerical evidence score. The 33 primary rows comprised 15 enzymatic-cleavage, ten inhibition, six direct-binding and two activation interactions across 15 host targets. Ten targets mapped to the strict disease-gene core: COL4A1, F10, F11, F5, FGA, GP1BA, KDR, PLG, PROC and PROS1. FGB and FN1 were present in the broad disease collection but did not meet core thresholds; CTRB1, F9 and PRSS1 were absent from the broad collection. These classifications describe disease-gene filtering and do not remove the underlying experimental evidence.

The two RVV-X light chains and heavy chain were treated as components of one toxin complex rather than independent corroborating toxins. Duplicate russelysin/daborhagin-K naming was flagged, and plasmin was distinguished from plasminogen throughout. STRING neighbors were retained as annotation-based functional-association expansion and were not interpreted as curated direct toxin–host binding.

Factor X accounted for six primary-literature edges from four independent toxin entities: the RVV-X complex, Daboxin P, basic PLA2 VRV-PL-VIIIa and DrKIn-II. These interactions resolve into zymogen recognition, zymogen activation and activated factor X inhibition. This factor X sheet makes the protein-state transitions explicit and prevents RVV-X subunit pseudoreplication.

**Supplementary Table S4. Complete edge-level evidence audit.** `S4_Edge_audit` contains all 447 rows with English evidence descriptions. Additional worksheets summarize evidence channels, mechanism classes and the six factor X interactions.

## SM.5. Background-matched enrichment analyses

Enrichment analyses used GO Biological Process 2023, KEGG 2021 Human and Reactome 2022. Exact hypergeometric tests were implemented using log-gamma calculations, and Benjamini–Hochberg adjustment was performed within each gene-set library. Every input was tested against a background matched to its ascertainment rather than against a common unrelated background.

G1 was a supporting analysis of all 15 literature-selected host targets against 16,662 annotated genes. G2, the primary analysis, evaluated ten strict-core targets against the 1,042-gene core from which they were ascertained. G3 evaluated five STRING-specific hub genes against the same core background. G4 evaluated the 15-gene union of strict-core and STRING-specific hub genes. G5 repeated G4 after removal of ALB. G6 removed nine prior-labelled axis genes from both the input and background, leaving seven input genes and 1,033 background genes. G7 removed all 27 four-axis genes, leaving four input genes and 1,015 background genes.

In G2, Formation of Fibrin Clot was the leading term (P = 4.7406 × 10⁻⁷), with 15 terms at BH < 0.05. G3 returned Extrinsic Pathway of Fibrin Clot Formation as its leading term (P = 5.5207 × 10⁻⁵; three BH-significant terms). G4 returned Formation of Fibrin Clot (P = 3.6068 × 10⁻¹¹; 24 terms), and G5 retained 21 BH-significant terms after ALB removal. G6 returned two BH-significant terms, led by Negative Regulation of Blood Coagulation (P = 2.7765 × 10⁻⁶). G7 yielded no BH-significant terms. G1 returned Complement and coagulation cascades as its leading term against the annotated-genome background (P = 7.3867 × 10⁻¹⁸; 69 BH-significant terms); this supporting analysis is not substituted for the primary G2 result.

**Supplementary Table S5. Group definitions and complete enrichment outputs.** The workbook contains group definitions, the prespecified G2/G3/G4/G5/G6/G7/G1 reporting order, and all tested terms with overlap, background size, raw P, BH-adjusted P and overlapping genes.

## SM.6. Permutation, source and axis sensitivity analyses

For G2–G4, 10,000 equally sized random gene sets were sampled from the 1,042-gene core background using seed 20261106. The observed minimum P value and the minimum P value among 43 coagulation-related terms were compared with their respective permutation distributions. Empirical P values used the plus-one correction for the observed statistic and the 10,000 permutations.

For G2, the global empirical P value was 2.0 × 10⁻⁴ and the coagulation-specific empirical P value was 1.0 × 10⁻⁴. For G3, the corresponding values were 0.039796 and 2.0 × 10⁻⁴. For G4, both were 1.0 × 10⁻⁴. These tests evaluate random sampling within the disease-focused background and are distinct from BH adjustment across gene-set terms.

Leave-one-source-out reconstruction removed one evidence channel at a time. Removing GeneCards produced a 482-gene core with seven strict-core targets; removing Open Targets produced 709 core genes with all ten strict-core targets retained. Removing DISEASES, DisGeNET, CTD direct evidence or the prior-axis channel produced 1,042, 1,041, 1,039 and 1,042 core genes, respectively, with all ten strict-core targets retained. The full-core reconstruction contained 1,042 genes and ten strict-core targets.

Against the 482-gene no-GeneCards background, the remaining seven strict-core targets retained Formation of Fibrin Clot as the leading pathway (P = 1.9361 × 10⁻⁶; ten BH-significant terms). The ten-gene union input returned P = 1.44 × 10⁻⁷ with 12 BH-significant terms. g:Profiler custom-background analyses with g:SCS correction were archived on 6 November 2026; the leading G2 result was P = 1.1283 × 10⁻⁵. These analyses provide cross-platform analytical consistency, not independent biological confirmation. Local BH and g:SCS procedures are reported separately.

**Supplementary Table S6. Permutation and sensitivity outputs.** Worksheets preserve the permutation summary, leave-one-source-out reconstruction, no-GeneCards strict-core and union analyses, and g:Profiler G2/G4 custom-background outputs.

## SM.7. Descriptive STRING-expanded network

The STRING-expanded layer comprised 54 nodes and 321 human functional-association edges at combined score ≥0.7. STRING associations can reflect several evidence types, including text mining and co-expression; they were therefore not interpreted as physical toxin–host interactions. The expanded layer provides descriptive context for the ten strict-core targets rather than an independent validation layer.

Degree, MCC and EPC rankings were reimplemented in NetworkX. The three Top-20 rankings intersected in ten descriptive hub candidates: F2, F3, ALB, F8, F7, PLG, PROC, FGA, F10 and F5. EPC values were tied across this dense network and were retained without forcing a rank order. No robustness-based ranking, module-derived causal claim or pathway-dominance claim was introduced. ALB was retained as a generic-network hub in the descriptive layer and was explicitly tested by removal in enrichment group G5.

The workbook provides all edges and nodes, the hub metrics and the complete core10/extended-network rankings. Node degree was recomputed from the 321 archived edges and is supplied to facilitate independent inspection.

**Supplementary Table S7. Descriptive STRING-expanded network.** Four worksheets contain 321 edges, 54 nodes, ten hub-metric records and the complete Degree/MCC/EPC Top-20 rankings.

## SM.8. Supplementary Structural Methods

### Structure inventory and identity audit

Fifteen raw structure assets were audited directly from PDB-format HEADER, TITLE, COMPND, DBREF and resolution records: twelve experimental PDB entries and three AlphaFold DB monomer v2.0 predictions. Structure preparation used chain-extracted files with waters and non-relevant ligands removed; catalytic zinc was retained where required. AlphaFold predictions were identified as predictions rather than experimental structures. The workbook records identity, chain assignment, accession, resolution or prediction quality, intended role and manuscript disposition for every asset.

The RVV-X asset 2E3X contains the heavy chain Q7LZ61 and light chains Q4PRD2 and Q4PRD1; these chains represent one toxin complex. The host asset 2W26 represents activated factor Xa, with chains covering residues 235–468 and 129–177. The host asset 7KVE is human coagulation factor V chain B at 3.3 Å cryo-EM resolution. The 3S9C co-complex contains RVV-V gamma chain A and a factor V fragment chain B at 1.8 Å. Its TITLE records residues 1533–1546, whereas COMPND/DBREF maps UNP residues 1561–1574; these numbering systems are retained separately rather than mixed. The 3S9C co-complex is the experimental structural anchor for P2, and any additional docking is descriptive.

The 3GHG fibrinogen structure contains alpha, beta and gamma chains but does not cover the fibrinogen alpha-C cleavage region. P3 is therefore restricted to a proxy-site structural context and cannot establish the geometry of the missing alpha-C region. The 3V2A complex contains VEGFR2/KDR chain R and VEGF-A chain A. VEGF-A is a template ligand rather than the venom ligand, so P7 remains template-dependent. The HDock ligand RMSD of 21.95 Å precludes a claim of exact template-pose reproduction.

The 1M10 complex contains VWF A1 chain A and GP1BA chain B at 3.1 Å. An earlier file label treated chain A as GP1BA; the raw PDB annotation shows that this assignment was incorrect. P4 was withdrawn and is excluded from structural support and figures. Its archived output appears in the workbook only to document withdrawal.

The 1QRZ structure is the plasminogen catalytic domain, not activated plasmin. Because the curated biochemical interaction concerns plasmin, P6 was restricted to orientation-level context and cannot upgrade the literature edge. P1 was likewise restricted to orientation-level context after review of factor X zymogen versus activated factor Xa state. P5 remains a descriptive interface pose without an independent site-specific validation control.

The initial structure-eligibility preference was resolution ≤3.0 Å. Contextual use of 7KVE (3.3 Å), 1M10 (3.1 Å) and 3V2A (3.2 Å) was documented explicitly, with identity, activation state, coverage and template dependence taking precedence over a resolution-only interpretation. This threshold deviation does not rescue the withdrawn P4 model.

### Docking outputs and permitted interpretation

ClusPro blind docking was run for seven pairs, HADDOCK restraint docking for P1/P2/P3/P6, and HDock template docking for P7. The workbook retains twelve output rows, including cluster size or model rank, center energy or docking score, secondary energy/Z-score/confidence fields where applicable, interface counts and functional-site or template coverage. Mixed source columns are explicitly labelled so that a Z-score or confidence value is not misread as an energy.

Scores, cluster sizes and interface descriptors are properties of the generated poses. They are not independent demonstrations of binding, affinity, selectivity, efficacy or physiological stability and do not increase the evidence grade of a literature-curated interaction. P4 is withdrawn; P1 and P6 provide orientation-level context only; P3 is limited by structural coverage; P7 is template-dependent. These dispositions supersede any earlier threshold-based support labels in internal analysis reports.

**Supplementary Table S8. Structure inventory, model inventory and docking-output disposition.** Three worksheets contain 15 structure assets, seven model pairs and twelve docking-output records with pair-specific interpretation limits.

## SM.9. Expression-context analysis

GSE121297 compares human umbilical vein endothelial cells exposed to rhodocetin-αβ, a snaclec from *Calloselasma rhodostoma*, with static controls (3 vs 3; Affymetrix HG-U133 Plus 2.0, GPL570). The six analysed samples were GSM3430994–GSM3430996 (static controls) and GSM3430997–GSM3430999 (static rhodocetin-αβ). The submitted RMA-normalized log2 series matrix was used. Probes were annotated through g:Profiler, and one probe per gene was selected by the fixed rule of highest mean expression across all six samples, yielding 22,453 genes.

GSE248215 compares mouse skeletal muscle collected 24 h after *D. russelii* venom exposure with controls (3 vs 2; NanoString Fibrosis V2, 760 genes). The analysed samples were Control-1/Control-2 and DR-A-24h/DR-B-24h/DR-C-24h. The deposited log2-transformed normalized NanoString matrix was used. Quality control for both datasets included intensity distributions, multidimensional scaling and raw-P histograms.

Differential expression was analysed with limma v3.68.5 in R 4.6.2 using classical empirical-Bayes moderation as the primary method. Benjamini–Hochberg adjustment was performed across all tested genes. Sensitivity analyses used `eBayes(trend = TRUE, robust = TRUE)` for both datasets and quantile normalization for GSE121297.

Classical limma identified 43 BH-significant genes in GSE121297 and 75 in GSE248215. The trend-plus-robust variants identified 54 and 131 genes, respectively, including 40 of the 43 and 72 of the 75 primary significant genes. The GSE121297 quantile-normalization sensitivity analysis identified 53 significant genes. Complete result tables, rather than only significant subsets, are supplied for all five analyses.

In GSE121297, SELE was the leading primary-analysis change (log2FC = 6.25; BH = 1.89 × 10⁻⁴). ICAM1 was significant (BH = 7.40 × 10⁻³), while VCAM1 showed a large positive effect (log2FC = 4.63) but did not meet BH < 0.05 (BH = 0.064) and is therefore treated as an effect-size observation. In GSE248215, CCL2 was the leading change (BH = 4.37 × 10⁻³). SERPINE1 was upregulated (log2FC = 2.07; BH = 0.022 in the primary analysis and 3.73 × 10⁻⁴ in the trend-plus-robust analysis). HAVCR1 remained non-significant under both variants (BH approximately 0.20–0.27) and was removed from renal and translational interpretations.

These datasets provide endothelial-activation and inflammatory-myotoxic context in their respective experimental models. They are not a patient TMA cohort, do not share a tissue or exposure design and were not combined in a cross-tissue meta-analysis.

**Supplementary Table S9. Sample metadata and complete limma outputs.** Two metadata/summary worksheets and five full result worksheets preserve sample roles, software, normalization, gene-level statistics and BH-significance flags.

## SM.10. Targeted vascular literature search

Eighteen PubMed Title/Abstract queries were executed through NCBI E-utilities on 6 November 2026 without date or language restrictions. A1–A4 addressed VWF/ADAMTS13, TMA and platelet adhesion; B1–B4 addressed complement; and C1–C10 refined species, mechanism and clinical-context searches. Complete field-tagged queries, execution dates and hit counts are provided in the workbook.

The initial eight queries returned 1,019 query–hit instances and the ten supplementary queries returned 417, giving 1,436 cross-query instances. This total counts the same article repeatedly when it was retrieved by multiple queries and is not a unique-article count. The focused archive contained 146 unique PMIDs, all with PubMed XML; 143 records included abstracts and three did not.

Forty-five mechanism-anchor articles underwent detailed review. Forty-two had abstracts or open full text available for mechanism assessment. PMID 20085531, PMID 24682198 and PMID 4071062 were retained as bibliographic leads only and were not used for specific mechanistic numerical inference without accessible full text. The workbook identifies these records explicitly.

Evidence was stratified into *Daboia*-specific observations, other-viperid mechanisms, elapid/cobra venom factor mechanisms and host downstream processes. Broad discovery queries A4, B3 and C7 were used for candidate discovery and vocabulary checking; they were not represented as fully screened systematic-review sets. The archive therefore supports a targeted scoping search and does not provide a PRISMA exhaustive-screening claim.

**Supplementary Table S10. Search queries, focused archive and mechanism anchors.** Three worksheets contain 18 queries, 146 unique PubMed records with available abstracts and provenance, and 45 mechanism-anchor records with review-basis labels.
