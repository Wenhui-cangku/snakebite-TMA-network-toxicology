# An evidence-calibrated venom–host interaction map of Russell's viper envenoming: coagulation architecture and hypotheses for thrombotic microangiopathy

**Running head:** Venom–host architecture and microangiopathy hypotheses

## Abstract

**Background:** Russell's viper envenoming causes venom-induced consumption coagulopathy, and a subset of patients develops thrombotic microangiopathy. The shared molecular architecture and the mechanisms distinguishing microangiopathy from uncomplicated coagulopathy remain insufficiently resolved. We developed an evidence-calibrated venom–host interaction map to resolve the best-supported coagulopathy architecture and prioritize testable microangiopathy mechanisms.

**Methods:** We integrated 63 venom-protein sequences grouped into 40 clusters, 2,190 source-resolved disease-associated genes with a reproducible 1,042-gene core, and 33 primary-literature-supported interactions spanning 15 host targets. Interactions were mechanism-typed and analyzed using matched backgrounds, 10,000 permutations and source- and axis-sensitivity analyses. Two public expression datasets were analyzed with limma, and targeted vascular literature was stratified by species and evidence function.

**Results:** Ten curated targets mapped to the strict core. Factor X formed a multi-mechanism convergence node, with four independent toxin entities mediating zymogen recognition, zymogen activation and activated factor X inhibition. Against the 1,042-gene core background, the strict-core targets showed coagulation enrichment (leading P = 4.74 × 10⁻⁷; coagulation-specific empirical P = 1.0 × 10⁻⁴). Sensitivity analyses delineated the signal's dependence on curated knowledge. limma identified 43 and 75 Benjamini–Hochberg-significant genes, providing endothelial-activation and inflammatory-myotoxic context. The map did not establish a validated discriminator of thrombotic microangiopathy; instead, it prioritized von Willebrand factor multimer processing, ADAMTS13 activity, shear-dependent platelet adhesion and complement activation for microangiopathy-stratified studies.

**Conclusion:** This resource resolves complementary factor X perturbation as the best-supported coagulopathy module and converts heterogeneous evidence into an auditable experimental agenda. The prioritized vascular measurements provide decisive tests of candidate microangiopathy mechanisms without presuming patient-level causality.

**Keywords:** Snakebite envenoming; *Daboia russelii*; Venom-induced consumption coagulopathy; Thrombotic microangiopathy; Venom–host interactions; Factor X; Evidence calibration

## Background

Snakebite envenoming is a neglected tropical disease that causes substantial mortality and long-term disability, particularly in agricultural communities across South and Southeast Asia [1]. Russell's viper (*Daboia russelii* and *D. siamensis*) is a leading cause of clinically important envenoming in this region. Its systemic manifestations include venom-induced consumption coagulopathy (VICC), local tissue injury, shock and organ dysfunction. VICC reflects venom-driven activation and consumption of coagulation factors and is not interchangeable with classical disseminated intravascular coagulation. A subset of patients develops thrombotic microangiopathy (TMA), characterized by thrombocytopenia, microangiopathic hemolytic anemia and microvascular organ injury, frequently involving the kidney. Clinical series distinguish snakebite-associated TMA from uncomplicated VICC and from the severe ADAMTS13 deficiency that defines thrombotic thrombocytopenic purpura [2,3]. The molecular events that accompany this clinical transition remain insufficiently resolved.

Russell's viper venom contains a biochemically diverse mixture of phospholipases A2 (PLA2), snake venom metalloproteinases (SVMP), serine proteinases (SVSP), C-type lectin-like proteins (snaclecs), Kunitz-type inhibitors and other protein families [4]. Several components have well-defined hemostatic activities. RVV-X recognizes and activates coagulation factor X, whereas RVV-V activates factor V [5–8]. Kunitz-type inhibitors modulate activated protein C, plasmin and other serine proteinases [9,10]. Dabocetin interacts with platelet GPIbα, and venom PLA2 can bind coagulation factor X or inhibit activated factor X [11–13]. These studies provide a strong mechanistic foundation, but their individual experimental designs, toxin entities and host protein states are heterogeneous. A molecule-specific account of how these interactions converge is therefore more informative than an undifferentiated list of predicted targets.

The central analytical challenge is to integrate this dispersed knowledge without allowing the structure of a database or an arbitrary statistical background to determine the biological conclusion. Literature-derived interactions answer a different question from STRING neighborhood associations, and a gene set drawn from a disease-focused resource should not automatically be tested against an unrelated genome-wide background. An evidence-calibrated map must therefore preserve the provenance, interaction type and protein state of every toxin–host edge while matching each enrichment analysis to the sampling frame from which its input was drawn. Expression datasets can add biological context, but their tissue, species and exposure models must remain explicit.

Here, we developed an evidence-calibrated map of venom–host interactions in Russell's viper envenoming. The analysis plan initially prioritized the VWF–ADAMTS13 axis, complement–coagulation crosstalk and structurally tractable toxin interfaces. We evaluated these axes through source-resolved curation, mechanism-typed interactions, background-matched enrichment, permutation testing and expression-context analysis. Our objective was to resolve the best-supported molecular architecture of VICC and to define the vascular measurements required to explain progression to TMA. The resulting resource links a multi-mechanism factor X core to a focused set of experiments on VWF multimer processing, shear-dependent platelet adhesion and complement–endothelium interactions.

## Methods

### 2.1. Study design and analysis plan

The study used a four-axis interpretive framework defined before network analysis: VWF–platelet interactions; coagulation–fibrinolysis; complement; and endothelial, inflammatory and renal responses. The timestamped analysis plan specified three initial hypotheses: preferential involvement of the VWF–ADAMTS13 and coagulation axes (H1), enrichment of complement and endothelial programs (H2), and tractable small-molecule interfaces at selected toxin–target complexes (H3). The plan was recorded in the project repository but was not prospectively registered. After data inspection, H1 and H2 were reformulated around the observed coagulation architecture and host-response branches, and H3 was restricted to exploratory structural context. Structural hypotheses were revised after verification of receptor identity, ligand activation state and control discrimination. The timing and rationale of every post hoc decision are reported in Supplementary Table S1. All analyses were treated as exploratory, with the primary output defined as an auditable mechanism map rather than a confirmatory causal model.

### 2.2. Toxin sequence library and clustering benchmark

UniProtKB [14] was queried on 22 September 2026 for reviewed toxin entries from *D. russelii* and *D. siamensis*. The primary query returned 52 entries; an independent *D. siamensis* export returned 28 entries, all of which overlapped the primary set. VenomZone/Tox-Prot curation [15] was used to cross-check species coverage and venom annotation. Quality control required representation of SVMP, SVSP, PLA2, snaclec and Kunitz families. This rule identified Kunitz entries missed by the toxin-keyword query and prompted family-specific searches, together with targeted recovery of CRISP and SVMP/disintegrin sequences. Records were deduplicated by UniProt or GenBank accession, transcriptome-derived host ADAM-like proteins were excluded, and sequences shorter than 30 amino acids were removed after comparison with curated short-peptide entries.

The merged library contained 78 unique records. Removal of 16 short fragments left 62 sequences, and VenomZone cross-checking restored one full-length PLA2 entry (P86368), yielding 63 sequences. Redundancy was reduced using a custom greedy 90%-identity clustering procedure seeded by sequence length. The algorithm uses global alignment identity normalized to the shorter sequence and a 5-mer coverage prefilter; it is not CD-HIT. To benchmark its behavior, the same 63 sequences were clustered with usearch v11.0.667 `cluster_fast` at 90% identity [16]. Cluster assignments were compared over all 1,953 sequence pairs using the Rand index, and marginal merges were inspected individually. Family-level venom abundance estimates were obtained from functional venomics of Sri Lankan *D. russelii* [4] and used as external contextual annotations rather than entry-specific weights.

### 2.3. Source-resolved disease-gene collection

The disease vocabulary covered thrombotic microangiopathy, thrombotic thrombocytopenic purpura, atypical hemolytic uremic syndrome, hemolytic uremic syndrome, microangiopathic hemolytic anemia, snakebite envenoming and VICC. Six sources were integrated: GeneCards [17], Open Targets [18], DISEASES curated knowledge [19], DisGeNET CURATED records [20], the Comparative Toxicogenomics Database (CTD) [21] and OMIM [22]. GeneCards results were manually exported on 22 September 2026 and thresholded at the median relevance score for each disease term. Open Targets records were retrieved through the GraphQL API, with score ≥0.05 for the broad collection and score ≥0.3 or association with at least three disease entries for core eligibility. DisGeNET records were retrieved at score ≥0.1, with score ≥0.3 used for core eligibility. CTD results were restricted to a prespecified disease whitelist; non-empty direct evidence qualified for the core, whereas InferenceScore ≥50 qualified for the broad collection. OMIM entries were restricted to phenotype-whitelisted records with mappingKey = 3. DISEASES curated associations and the prespecified four-axis molecules completed the core-eligibility channels. Human gene symbols were mapped to UniProt accessions using MyGene.info [23].

This procedure generated a broad set of 2,190 genes and a core set of 1,042 genes. A gene-level provenance matrix retained all source flags and thresholds. The core set was independently reconstructed from the six evidence channels to verify its composition. Snakebite- and VICC-specific contributions were counted separately from associations derived from related TMA phenotypes. Leave-one-source-out analysis repeated core-set construction after removing each evidence channel. Because GeneCards contributed the largest number of source-specific genes, a no-GeneCards analysis was also performed with the resulting 482-gene background.

### 2.4. Mechanism-typed toxin–host evidence curation

Toxin–host interactions were curated from molecule-specific UniProt/Swiss-Prot annotations and corresponding primary literature. Each record retained the toxin identifier, independent toxin entity, host gene, species, protein activation state, PMID and evidence detail. Interactions were classified as enzymatic cleavage, inhibition, direct binding or activation; these categories were not collapsed into a single numerical evidence score. Records supported only by database annotation without a PMID, family-level extrapolation or similarity inference were labeled separately and excluded from the primary-literature count. STRING neighbors were likewise treated as annotation-based network expansion rather than curated toxin targets.

All 447 rows in the original edge table were audited. Of 49 rows initially labeled as literature evidence, 33 had primary-literature support and formed the main curated edge set. Eleven annotation-only rows, four family-level rows and one similarity-based row were assigned to their respective non-primary channels. Duplicate toxin naming and uncertain subunit attribution were flagged at edge level. In particular, the two RVV-X light chains were treated as components of one toxin complex rather than independent toxin entities, and plasmin was distinguished from plasminogen throughout.

A targeted scoping search was used to extend the vascular interpretation beyond direct toxin–protein edges. Eighteen PubMed queries covering VWF/ADAMTS13, platelet adhesion, complement and clinical TMA were executed on 6 November 2026. The focused archive contained 146 unique PMIDs, of which 45 mechanism-anchor articles underwent detailed review. Evidence was stratified into *Daboia*-specific observations, other-viperid mechanisms, elapid/cobra venom factor mechanisms and host downstream processes. The search queries, hit counts, abstracts and inclusion decisions were archived; broad discovery searches were not presented as a completed systematic review.

### 2.5. Intersection and descriptive network analysis

The 15 host targets with primary-literature support were intersected with the 1,042-gene core collection to define the strict core. This intersection was used as a filtering operation, not as a statistical test. A separate STRING-expanded layer was constructed from human functional associations at combined score ≥0.7 [24], retaining 54 nodes and 321 edges. STRING associations can include text mining and co-expression and were therefore not interpreted as physical toxin–host binding.

Network topology was summarized using Degree, MCC and EPC rankings reimplemented in NetworkX [25,26]. The extended network provided descriptive context for the curated core rather than an independent validation layer. Tied EPC values were retained without forcing a rank order, and no robustness-based ranking or causal hub claim was introduced.

### 2.6. Background-matched enrichment and sensitivity analyses

Enrichment analyses used GO Biological Process 2023 [28], KEGG 2021 Human [29] and Reactome 2022 [30] as gene-set libraries. Exact hypergeometric tests were implemented using log-gamma calculations, with Benjamini–Hochberg correction within each library [31]. Seven prespecified input groups were analyzed against backgrounds matched to their ascertainment. G2 was the primary enrichment analysis, G3–G7 were sensitivity analyses, and G1 was retained as a supporting analysis of the literature-selected targets:

- **G1 (supporting):** 15 curated host targets against 16,662 annotated genes, because these targets were selected from toxin literature independently of the disease-gene collection.
- **G2 (primary):** ten strict-core targets against the 1,042-gene core.
- **G3 (sensitivity):** five hub genes unique to the STRING-expanded layer against the 1,042-gene core.
- **G4 (sensitivity):** the 15-gene union of strict-core and STRING-specific hub genes against the 1,042-gene core.
- **G5 (sensitivity):** the G4 input after removal of ALB against the 1,042-gene core.
- **G6 (sensitivity):** seven strict-core genes remaining after removal of nine prior-labeled axis genes, against the corresponding 1,033-gene background.
- **G7 (sensitivity):** four strict-core genes remaining after removal of all 27 four-axis genes, against the corresponding 1,015-gene background.

For G2–G4, 10,000 equally sized random gene sets were sampled from the 1,042-gene background (seed 20261106). The observed minimum P value and the minimum P value among coagulation-related terms were compared with their respective permutation distributions. Leave-one-source-out analysis distinguished dependence on a database channel from dependence on particular axis genes. Enrichment was additionally recomputed after removing GeneCards, using the 482-gene background and the inputs that remained eligible. g:Profiler custom-background analyses with g:SCS correction were archived on 6 November 2026 as a cross-platform analytical comparison [27]. The local and g:Profiler multiple-testing procedures were reported separately.

### 2.7. Expression-context analysis

Two public datasets were obtained from GEO [32]. GSE121297 compares human umbilical vein endothelial cells exposed to rhodocetin-αβ, a snaclec from *Calloselasma rhodostoma*, with static controls (3 vs 3; Affymetrix HG-U133 Plus 2.0) [33]. GSE248215 compares mouse skeletal muscle collected 24 h after *D. russelii* venom exposure with controls (3 vs 2; NanoString Fibrosis V2 panel, 760 genes) [34]. These datasets represent an endothelial snaclec model and an in vivo inflammatory-myotoxic model, respectively.

For GSE121297, the submitted RMA-normalized log2 series matrix was used. Probes were annotated through g:Profiler, and one probe per gene was selected by the fixed rule of highest mean expression across all six samples, yielding 22,453 genes. For GSE248215, the deposited log2-transformed normalized NanoString matrix was used. Quality control included intensity distributions, multidimensional scaling and raw-P histograms.

Differential expression was analyzed with limma v3.68.5 in R 4.6.2 using classical empirical-Bayes moderation [35]. Benjamini–Hochberg adjustment was performed across tested genes. Sensitivity analyses used `eBayes(trend = TRUE, robust = TRUE)` for both datasets and quantile normalization for GSE121297. Expression changes were integrated as biological context for endothelial activation and inflammatory-myotoxic responses; no cross-tissue meta-analysis was performed.

### 2.8. Structural-context analyses

Experimental structures from the Protein Data Bank [36] and AlphaFold models [37] were used to generate selected structural-context models for curated interactions. Protein identity, chain assignment, activation state and template dependence were checked before interpretation. Model scores and interface descriptors were treated as properties of the generated poses rather than independent demonstrations of binding or stability. The complete model inventory, identity audit, template comparisons and structural outputs are provided in the Supplementary Materials, allowing the main analysis to remain anchored in primary biochemical evidence.

### 2.9. Reproducibility

Source identifiers, access dates, analysis thresholds and random seeds were retained in the project data tables. Scripts for clustering, evidence auditing, core-set reconstruction, enrichment, permutation testing and limma analysis accompany the corresponding output tables. The mechanistic map distinguishes primary-literature edges, annotation-based expansion, cross-species surrogate evidence and untested links. All numerical values in the abstract and main text were traced to the archived result tables.

## Results

### 3.1. A benchmarked toxin and disease-gene resource

The final toxin library comprised 63 sequences spanning all five major venom families. Custom 90%-identity clustering produced 40 clusters, compared with 39 from usearch. The methods agreed on 34 of the 35 within-cluster sequence pairs identified by the custom procedure, yielding a Rand index of 0.996 across all 1,953 pairs. The discrepancies were confined to two marginal merge decisions involving individual PLA2 and CRISP sequences. Thus, the redundancy-reduction procedure was highly concordant with an established clustering implementation while retaining transparent, inspectable differences.

The six-source disease-gene resource contained 2,190 genes, including a core of 1,042 genes. Independent reconstruction from source flags reproduced all 1,042 core assignments with zero omissions or additions. Sixty-five core genes (6.2%) carried a snakebite-specific source annotation and 31 (3.0%) carried a VICC-specific annotation. These counts distinguish the snakebite-specific component from the broader TMA-related background and make the provenance of the core set explicit.

### 3.2. Mechanism-typed curation resolves a strict host-target core

The primary evidence table contained 33 literature-supported interactions across 15 host targets: 15 enzymatic-cleavage, ten inhibition, six direct-binding and two activation edges. Ten targets—COL4A1, F10, F11, F5, FGA, GP1BA, KDR, PLG, PROC and PROS1—mapped to the strict disease-gene core. The other five targets remained part of the curated mechanistic resource: CTRB1, F9 and PRSS1 were absent from the broad disease-gene collection, whereas FGB and FN1 were present but did not meet core thresholds. Their positions therefore reflect disease-gene filtering rather than loss of primary experimental support.

### 3.3. Factor X forms a multi-mechanism convergence node

Factor X showed the clearest convergence of complementary toxin mechanisms. Six primary-literature-supported edges connected four independent toxin entities to factor X or activated factor X: the RVV-X complex, Daboxin P, basic PLA2 VRV-PL-VIIIa and the Kunitz-type inhibitor DrKIn-II [5,6,9,10,12,13]. These edges resolved into three mechanistic classes.

First, zymogen recognition occurs through the light chains of RVV-X, which bind the Gla domain of factor X, and through Daboxin P binding to factor X/Xa. Second, the RVV-X heavy chain cleaves the factor X zymogen to generate FXa. Third, DrKIn-II and basic PLA2 VRV-PL-VIIIa inhibit the activated enzyme. This organization distinguishes factor X from FXa and avoids treating multiple subunits of RVV-X as independent corroboration. The resulting “recognition–activation–inhibition” architecture provides a molecular explanation for the coexistence of procoagulant and anticoagulant activities within the same venom and establishes factor X as a mechanistically resolved component of the VICC core.

### 3.4. Strict-core enrichment defines a calibrated coagulation signal

The primary G2 analysis evaluated the ten strict-core targets against the 1,042-gene core from which they were ascertained. Formation of Fibrin Clot was the leading term (P = 4.74 × 10⁻⁷), with 15 terms at BH < 0.05. Permutation testing distinguished the observed signal from random sampling within the same disease-focused background: the global and coagulation-specific empirical P values were 2.0 × 10⁻⁴ and 1.0 × 10⁻⁴, respectively.

The STRING-based G3 and G4 sensitivity analyses were directionally consistent with the strict-core result. G3 returned Extrinsic Pathway of Fibrin Clot Formation as its leading term, with a coagulation-specific empirical P value of 2.0 × 10⁻⁴. G4 returned Formation of Fibrin Clot, with global and coagulation-specific empirical P values of 1.0 × 10⁻⁴. Removing ALB in G5 retained 21 BH-significant terms, showing that the plasma-network signal was not driven by this generic hub. The supporting G1 analysis of all 15 literature-selected targets against the annotated-genome background is reported in Table 3.

Source-sensitivity analyses showed that the core-set composition did not depend on forced inclusion through the prior channel. Removing that channel left all 1,042 core assignments and all ten strict-core targets unchanged. Open Targets, DISEASES, DisGeNET and CTD removal likewise preserved all ten strict-core targets. GeneCards removal produced a 482-gene core and reduced the strict core to seven targets, identifying GeneCards as the largest single-source contributor. The remaining seven strict-core genes retained Formation of Fibrin Clot as the leading pathway against the 482-gene background (P = 1.94 × 10⁻⁶; ten significant terms), and the ten-gene union input returned P = 1.44 × 10⁻⁷ with 12 significant terms. g:Profiler custom-background analysis returned a leading G2 P value of 1.13 × 10⁻⁵, demonstrating cross-platform analytical consistency.

Axis-gene stress testing answered a distinct question. After removal of nine prior-labeled genes, G6 retained two significant terms, led by Negative Regulation of Blood Coagulation (P = 2.78 × 10⁻⁶). After removal of all 27 four-axis genes, G7 yielded no terms at BH < 0.05. The strict-core signal therefore remained consistent under random background sampling, prior-channel removal and the tested GeneCards removal, while its gene-level enrichment was localized to the prespecified coagulation/endothelial gene set. This combination defines both the reliability and the inferential scope of the map.

### 3.5. Expression datasets add endothelial and inflammatory-myotoxic context

Classical limma analysis identified 43 BH-significant genes in GSE121297 and 75 in GSE248215. The trend-plus-robust variants identified 54 and 131 genes, respectively, including 40 of the 43 and 72 of the 75 genes from the primary analyses. This overlap demonstrates that the principal expression programs were not contingent on one empirical-Bayes parameterization.

In GSE121297, the leading change was SELE (log2FC = 6.25; BH = 1.89 × 10⁻⁴), accompanied by increased ICAM1 (BH = 7.40 × 10⁻³) and chemokines including CXCL5, CXCL3 and CXCL6. VCAM1 showed a large positive effect (log2FC = 4.63) with BH = 0.064 and was therefore retained as an effect-size observation rather than labeled significant. Together, these changes describe a coordinated endothelial-activation program in the snaclec-exposed cells.

In GSE248215, CCL2 was the leading gene (BH = 4.37 × 10⁻³), with TIMP1, HMOX1, VEGFA and other inflammatory and tissue-response genes forming the dominant pattern. SERPINE1 was upregulated (log2FC = 2.07; BH = 0.022 in the primary analysis and 3.73 × 10⁻⁴ in the trend-plus-robust analysis). These findings add an inflammatory-myotoxic tissue context to the endothelial program observed in GSE121297. The two datasets therefore support distinct branches of the mechanistic map while preserving their model- and tissue-specific interpretation.

### 3.6. Structural models provide molecular context

Selected structural models provided molecular context for curated interactions. Protein identity, activation state and template-dependence assessments are reported with the complete model inventory in the Supplementary Structural Methods and associated tables. Structural outputs were not used to increase the evidence grade of a literature-curated edge or to infer efficacy, selectivity or physiological stability.

### 3.7. Vascular evidence stratification defines the next TMA experiments

The targeted vascular literature identified four concrete entry points for extending the map beyond VICC. First, a prospective 146-patient cohort of Russell's viper bites with coagulopathy reported modestly elevated VWF antigen, providing a clinical anchor for vascular involvement [38]. Second, Dabocetin–GPIbα and Rusvikunin–GPIIb/IIIa interactions establish receptor-level routes to platelet modulation [11,39]. Third, cross-species VWF/ADAMTS13 studies provide mechanistic candidates while preserving VWF-independent platelet pathways [40,41]. Fourth, *Daboia* and predominantly *Daboia* in vivo studies have documented C3 depletion and pre-antivenom anaphylatoxin generation, establishing complement activation as a relevant host response [42,43].

These observations define a measurement agenda rather than a patient-level classifier. TMA-stratified clinical sampling should pair VWF antigen with VWF multimers and ADAMTS13 activity. Purified-toxin experiments should combine endothelial VWF-string formation with shear-based platelet adhesion, rather than relying on static aggregation alone. Complement studies should separate direct toxin cleavage from host downstream activation through purified-toxin assays, pathway-selective inhibition and endothelial readouts. Integrating these measurements with the resolved VICC core will test which vascular mechanisms accompany the transition to TMA.

## Discussion

### 4.1. Principal advances

This study converts a heterogeneous venom–host literature into an evidence-calibrated mechanism resource with three principal advances. First, mechanism-typed curation resolves factor X as a multi-mechanism convergence node rather than an undifferentiated network hub. Four independent toxin entities act through zymogen recognition, zymogen activation and FXa inhibition, providing a compact molecular architecture for VICC. Second, source-matched backgrounds, permutation testing and complementary sensitivity analyses define the strict-core signal and delineate its curated-gene dependence. Third, empirical-Bayes expression analysis adds coordinated endothelial and inflammatory-myotoxic programs, connecting the curated network to independently generated biological data.

The resulting map is designed around evidence function. Primary literature supports molecule-specific interactions; STRING provides network context; expression datasets describe host-response programs; and cross-species studies prioritize candidate mechanisms for *Daboia*-specific testing. Keeping these layers distinct makes the strongest findings easier to identify and the next experiments more precise.

### 4.2. Factor X convergence links procoagulant and anticoagulant venom activities

The factor X architecture offers a mechanistic interpretation for the mixed hemostatic effects of Russell's viper venom. RVV-X couples substrate recognition to proteolytic activation, whereas PLA2 and Kunitz components act on factor X/Xa through binding or inhibition [5,6,9,10,12,13]. These interactions target different molecular states and should not be collapsed into a single direction of effect. Procoagulant factor X activation can promote coagulation-factor consumption, while FXa inhibition and other anticoagulant interactions can modify prothrombinase activity and fibrin formation. Their net physiological effect is therefore expected to depend on toxin concentrations, molecular state, timing and local phospholipid or cellular context.

This interpretation also clarifies why network degree alone is insufficient. The importance of factor X in the present map arises from experimentally differentiated mechanisms, not from the number of graph connections. Similar reasoning applies to the broader strict core, where factor V, factor XI, protein C, plasmin and fibrinogen provide complementary points of coagulation and fibrinolysis perturbation. The map consequently generates specific mixture-toxicology questions: which toxin combinations dominate at clinically relevant ratios, whether recognition and inhibition compete for the same substrate pool, and how these interactions change over the course of antivenom treatment. These questions require concentration-resolved biochemical and microvascular assays rather than additional topology scores.

### 4.3. VWF–platelet biology provides a defined experimental sequence

Targeted literature analysis identified concrete entry points for extending the map from VICC to TMA. In *Daboia* envenoming, a 146-patient VICC cohort showing modestly elevated VWF antigen provides a clinical anchor for vascular involvement [38], while Dabocetin–GPIbα and Rusvikunin–GPIIb/IIIa interactions establish receptor-level routes to platelet modulation [11,39]. These receptor interactions are heterogeneous: Dabocetin inhibits ristocetin-induced agglutination, whereas Rusvikunin binding to GPIIb/IIIa can occur through an RGD-independent route. Platelet responses therefore cannot be reduced to a single VWF-dependent switch.

Static binding and aggregation assays define these molecular interactions; shear-based microfluidics, VWF-multimer analysis and paired ADAMTS13-activity measurements will establish their microvascular consequences. Cross-species evidence from *Bothrops* further prioritizes these assays in *Daboia* cohorts. *B. jararaca* experiments demonstrate changes in VWF and ADAMTS13 while also showing that thrombocytopenia can persist independently of VWF [40]. *B. lanceolatus* studies report in vitro reduction of ADAMTS13 activity and generally normal or moderately reduced patient values rather than uniform severe deficiency [41]. Together, these observations convert the VWF–platelet axis from a generalized hypothesis into a defined experimental sequence while retaining VWF-independent platelet pathways.

### 4.4. Complement is organized as a layered host-response hypothesis

The evidence map incorporates complement through four biologically distinct layers. First, *Daboia* and predominantly *Daboia* in vivo studies establish complement involvement as a host response: C3 depletion was observed in experimental envenoming, and increased C3a/C4a/C5a were detected before antivenom administration in a predominantly *Daboia* clinical cohort [42,43]. These findings support early complement activation without assigning a specific toxin or pathway.

Second, other viperid studies provide direct molecular candidates. A *B. pirajai* P-I SVMP can cleave C3, C4 and C5 and generate anaphylatoxins, while *B. atrox* venom and isolated toxins modulate complement pathways and components [44,45]. These experiments establish mechanism-level feasibility across viperids and motivate purified-*Daboia*-toxin cleavage assays rather than direct cross-species extrapolation.

Third, elapid studies and cobra venom factor (CVF) illustrate the diversity of venom–complement interactions. *Naja annulifera* envenoming can engage the C5a–C5aR1 axis, whereas CVF forms a stable convertase with factor B and promotes sustained complement activation [46,47]. These mechanisms remain species- and toxin-specific and are not transferred to *Daboia* snaclecs or SVMPs.

Fourth, host downstream mechanisms extend beyond direct toxin–protein edges. Tissue injury, endothelial activation, host proteolysis, coagulation–complement crosstalk and terminal complement effects may arise without a curated toxin–complement interaction. Purified-toxin cleavage assays, pathway-selective inhibition, endothelial complement-deposition measurements and TMA-stratified clinical sampling will distinguish these routes. The mechanistic map therefore presents complement as a set of testable host-response branches aligned with, but not substituted for, curated toxin–target interactions.

### 4.5. The mechanistic hypothesis map prioritizes decisive experiments

The mechanistic hypothesis map organizes the findings into a sequence from venom exposure to candidate microvascular outcomes. Primary-literature edges define the molecular initiating interactions, with factor X convergence providing the best-resolved VICC module. Coagulation-factor consumption, fibrinolysis perturbation, platelet receptor modulation and endothelial activation form the next mechanistic layer. VWF multimer processing, shear-dependent platelet adhesion and complement–endothelium interactions then define the vascular measurements needed to test TMA-specific mechanisms.

The map also incorporates acute kidney injury through multiple biologically plausible routes: hemodynamic disturbance, inflammatory endothelial injury, pigment and myotoxic injury, and direct renal toxicity. These routes are displayed as parallel branches rather than a single linear pathway. Each arrow is labeled as primary-literature-supported, annotation-based, cross-species surrogate or untested, allowing experimental effort to be directed toward links where new measurements would be most informative.

This structure offers a practical alternative to pathway-dominance claims. A decisive experiment should distinguish between mechanistic alternatives: paired VWF multimer and ADAMTS13 measurements can separate antigen release from impaired processing; microfluidic assays can separate receptor binding from shear-dependent adhesion; and purified-toxin complement assays can separate direct cleavage from host downstream activation. The map therefore functions as an experimental design tool as well as a knowledge summary.

### 4.6. Scope and limitations

This study was designed to map curated knowledge rather than to estimate causal effects in patients. Disease-gene sources and toxin annotations therefore define the inference space, and enrichment was interpreted together with source- and axis-sensitivity analyses. The expression datasets provide endothelial and inflammatory-myotoxic context rather than a clinical TMA cohort. Structural models are used for hypothesis generation, with protein identity, activation state and template dependence documented in the Supplementary Materials. Prospective cohorts integrating VWF multimers, ADAMTS13 activity, flow-based platelet adhesion and complement markers will provide the decisive test of the proposed TMA mechanisms.

## Conclusion

An evidence-calibrated venom–host map resolves a multi-mechanism VICC core in Russell's viper envenoming, centered on complementary modes of factor X perturbation and supported by background-matched enrichment and expression-context analyses. Its principal advance is to convert a heterogeneous literature into an auditable mechanism resource and a focused set of TMA experiments. VWF multimer processing, shear-dependent platelet adhesion and complement–endothelium interactions now constitute concrete, prioritized tests of candidate mechanisms associated with progression to TMA.

## Abbreviations

**ADAMTS13:** A disintegrin and metalloproteinase with a thrombospondin type 1 motif, member 13; **BH:** Benjamini–Hochberg; **CRISP:** Cysteine-rich secretory protein; **CTD:** Comparative Toxicogenomics Database; **CTL:** C-type lectin-like; **CVF:** Cobra venom factor; **EPC:** Edge percolated component; **FXa:** Activated coagulation factor X; **GEO:** Gene Expression Omnibus; **Gla:** γ-Carboxyglutamic acid; **GO:** Gene Ontology.

**GPIbα:** Glycoprotein Ib alpha; **GPIIb/IIIa:** Glycoprotein IIb/IIIa; **KEGG:** Kyoto Encyclopedia of Genes and Genomes; **LAAO:** L-amino acid oxidase; **MCC:** Maximal clique centrality; **NGF:** Nerve growth factor; **OMIM:** Online Mendelian Inheritance in Man; **PDB:** Protein Data Bank; **PLA2:** Phospholipase A2; **RGD:** Arginine-glycine-aspartic acid; **RMA:** Robust multi-array average; **RVV:** Russell's viper venom.

**snaclec:** Snake venom C-type lectin-like protein; **STRING:** Search Tool for the Retrieval of Interacting Genes/Proteins; **SVMP:** Snake venom metalloproteinase; **SVSP:** Snake venom serine proteinase; **TMA:** Thrombotic microangiopathy; **VEGF:** Vascular endothelial growth factor; **VICC:** Venom-induced consumption coagulopathy; **VWF:** von Willebrand factor.

## References

[1] World Health Organization. Snakebite envenoming: a strategy for prevention and control. Geneva: WHO; 2019.

[2] Noutsos T, Currie BJ, Lek RA, Isbister GK. Snakebite associated thrombotic microangiopathy: a systematic review of clinical features, laboratory characteristics, and outcomes. PLoS Negl Trop Dis. 2020;14(12):e0008936. https://doi.org/10.1371/journal.pntd.0008936.

[3] Noutsos T, Currie BJ, Isoardi KZ, Brown SGA, Isbister GK. Snakebite-associated thrombotic microangiopathy: an Australian prospective cohort study [ASP30]. Clin Toxicol (Phila). 2022;60(2):205–213. https://doi.org/10.1080/15563650.2021.1948559.

[4] Tan NH, Fung SY, Tan KY, Yap MK, Gnanathasan CA, Tan CH. Functional venomics of the Sri Lankan Russell's viper (*Daboia russelii*) and its toxinological correlations. J Proteomics. 2015;128:403–423. https://doi.org/10.1016/j.jprot.2015.08.017.

[5] Castro-Amorim J, Oliveira A, Mukherjee AK, Ramos MJ, Fernandes PA. Unraveling the reaction mechanism of Russell's viper venom factor X activator: a paradigm for the reactivity of zinc metalloproteinases? J Chem Inf Model. 2023;63(13):4056–4069. https://doi.org/10.1021/acs.jcim.2c01156.

[6] Chen HS, Chen JM, Lin CW, Khoo KH, Tsai IH. New insights into the functions and N-glycan structures of factor X activator from Russell's viper venom. FEBS J. 2008;275(15):3944–3958. https://doi.org/10.1111/j.1742-4658.2008.06540.x.

[7] Yadav PK, Antonyraj CB, Basheer Ahamed SI, Srinivas S. Understanding Russell's viper venom factor V activator's substrate specificity by surface plasmon resonance and in-silico studies. PLoS One. 2017;12(7):e0181216. https://doi.org/10.1371/journal.pone.0181216.

[8] Nakayama D, Ben Ammar Y, Miyata T, Takeda S. Structural basis of coagulation factor V recognition for cleavage by RVV-V. FEBS Lett. 2011;585(19):3020–3025. https://doi.org/10.1016/j.febslet.2011.08.022.

[9] Cheng AC, Wu HL, Shi GY, Tsai IH. A novel heparin-dependent inhibitor of activated protein C that potentiates consumptive coagulopathy in Russell's viper envenomation. J Biol Chem. 2012;287(19):15739–15748. https://doi.org/10.1074/jbc.M111.323063.

[10] Cheng AC, Tsai IH. Functional characterization of a slow and tight-binding inhibitor of plasmin isolated from Russell's viper venom. Biochim Biophys Acta. 2014;1840(1):153–159. https://doi.org/10.1016/j.bbagen.2013.08.019.

[11] Zhong SR, Jin Y, Wu JB, Chen RQ, Jia YH, Wang WY, Xiong YL, Zhang Y. Characterization and molecular cloning of dabocetin, a potent antiplatelet C-type lectin-like protein from *Daboia russellii siamensis* venom. Toxicon. 2006;47(1):104–112. https://doi.org/10.1016/j.toxicon.2005.10.002.

[12] Sharma M, Iyer JK, Shih N, Majumder M, Mattaparthi VS, Mukhopadhyay R, Doley R. Daboxin P, a major phospholipase A2 enzyme from the Indian *Daboia russelii russelii* venom, targets factor X and factor Xa for its anticoagulant activity. PLoS One. 2016;11(4):e0153770. https://doi.org/10.1371/journal.pone.0153770.

[13] Faure G, Gowda VT, Maroun RC. Characterization of a human coagulation factor Xa-binding site on Viperidae snake venom phospholipases A2 by affinity binding studies and molecular bioinformatics. BMC Struct Biol. 2007;7:82. https://doi.org/10.1186/1472-6807-7-82.

[14] The UniProt Consortium. UniProt: the Universal Protein Knowledgebase in 2025. Nucleic Acids Res. 2025;53(D1):D609–D617. https://doi.org/10.1093/nar/gkae1010.

[15] VenomZone: the venom and toxin knowledge resource. Swiss Institute of Bioinformatics. https://venomzone.expasy.org (accessed 22 September 2026).

[16] Edgar RC. Search and clustering orders of magnitude faster than BLAST. Bioinformatics. 2010;26(19):2460–2461. https://doi.org/10.1093/bioinformatics/btq461.

[17] Stelzer G, Rosen N, Plaschkes I, et al. The GeneCards suite: from gene data mining to disease genome sequence analyses. Curr Protoc Bioinformatics. 2016;54:1.30.1–1.30.33. https://doi.org/10.1002/cpbi.5.

[18] Ochoa D, Hercules A, Carmona M, et al. Open Targets Platform: supporting systematic drug–target identification and prioritisation. Nucleic Acids Res. 2021;49(D1):D1302–D1310. https://doi.org/10.1093/nar/gkaa1027.

[19] Pletscher-Frankild S, Pallejà A, Tsafou K, Binder JX, Jensen LJ. DISEASES: text mining and data integration of disease–gene associations. Methods. 2015;74:83–89. https://doi.org/10.1016/j.ymeth.2014.11.020.

[20] Piñero J, Ramírez-Anguita JM, Saüch-Pitarch J, et al. The DisGeNET knowledge platform for disease genomics: 2019 update. Nucleic Acids Res. 2020;48(D1):D1030–D1038. https://doi.org/10.1093/nar/gkz1021.

[21] Davis AP, Wiegers TC, Johnson RJ, et al. Comparative Toxicogenomics Database (CTD): update 2021. Nucleic Acids Res. 2021;49(D1):D1138–D1143. https://doi.org/10.1093/nar/gkaa891.

[22] Amberger JS, Bocchini CA, Scott AF, Hamosh A. OMIM.org: leveraging knowledge across phenotype–gene relationships. Nucleic Acids Res. 2019;47(D1):D1038–D1043. https://doi.org/10.1093/nar/gky1151.

[23] Xin J, Mark A, Afrasiabi C, et al. High-performance web services for querying gene and variant annotation. Genome Biol. 2016;17:91. https://doi.org/10.1186/s13059-016-0953-9.

[24] Szklarczyk D, Kirsch R, Koutrouli M, et al. The STRING database in 2025: protein networks with directionality of regulation. Nucleic Acids Res. 2025;53(D1):D730–D737. https://doi.org/10.1093/nar/gkae1113.

[25] Chin CH, Chen SH, Wu HH, Ho CW, Ko MT, Lin CY. cytoHubba: identifying hub objects and sub-networks from complex interactome. BMC Syst Biol. 2014;8(Suppl 4):S11. https://doi.org/10.1186/1752-0509-8-S4-S11.

[26] Hagberg AA, Schult DA, Swart PJ. Exploring network structure, dynamics, and function using NetworkX. In: Proceedings of the 7th Python in Science Conference (SciPy); 2008. p. 11–15.

[27] Raudvere U, Kolberg L, Kuzmin I, et al. g:Profiler: a web server for functional enrichment analysis and conversions of gene lists (2019 update). Nucleic Acids Res. 2019;47(W1):W191–W198. https://doi.org/10.1093/nar/gkz369.

[28] Ashburner M, Ball CA, Blake JA, et al. Gene Ontology: tool for the unification of biology. Nat Genet. 2000;25(1):25–29. https://doi.org/10.1038/75556.

[29] Kanehisa M, Goto S. KEGG: Kyoto Encyclopedia of Genes and Genomes. Nucleic Acids Res. 2000;28(1):27–30. https://doi.org/10.1093/nar/28.1.27.

[30] Gillespie M, Jassal B, Stephan R, et al. The Reactome pathway knowledgebase 2022. Nucleic Acids Res. 2022;50(D1):D687–D692. https://doi.org/10.1093/nar/gkab1028.

[31] Benjamini Y, Hochberg Y. Controlling the false discovery rate: a practical and powerful approach to multiple testing. J R Stat Soc B. 1995;57(1):289–300. https://doi.org/10.1111/j.2517-6161.1995.tb02031.x.

[32] Edgar R, Domrachev M, Lash AE. Gene Expression Omnibus: NCBI gene expression and hybridization array data repository. Nucleic Acids Res. 2002;30(1):207–210. https://doi.org/10.1093/nar/30.1.207.

[33] Rezaei M, Martins Cavaco AC, Seebach J, et al. Signals of the Neuropilin-1–MET axis and cues of mechanical force exertion converge to elicit inflammatory activation in coherent endothelial cells. J Immunol. 2019;202(5):1559–1572. https://doi.org/10.4049/jimmunol.1801346.

[34] Oliveira AK, Rucavado A, Escalante T, Gutiérrez JM, Fox JW. A complex pattern of gene expression in tissue affected by viperid snake envenoming: the emerging role of autophagy-related genes. Biomolecules. 2024;14(3):278. https://doi.org/10.3390/biom14030278.

[35] Ritchie ME, Phipson B, Wu D, Hu Y, Law CW, Shi W, Smyth GK. limma powers differential expression analyses for RNA-sequencing and microarray studies. Nucleic Acids Res. 2015;43(7):e47. https://doi.org/10.1093/nar/gkv007.

[36] Berman HM, Westbrook J, Feng Z, et al. The Protein Data Bank. Nucleic Acids Res. 2000;28(1):235–242. https://doi.org/10.1093/nar/28.1.235.

[37] Jumper J, Evans R, Pritzel A, et al. Highly accurate protein structure prediction with AlphaFold. Nature. 2021;596:583–589. https://doi.org/10.1038/s41586-021-03819-2.

[38] Isbister GK, Maduwage K, Scorgie FE, et al. Venom concentrations and clotting factor levels in a prospective cohort of Russell's viper bites with coagulopathy. PLoS Negl Trop Dis. 2015;9(8):e0003968. https://doi.org/10.1371/journal.pntd.0003968.

[39] Kalita B, Dutta S, Mukherjee AK. RGD-independent binding of Russell's viper venom Kunitz-type protease inhibitors to platelet GPIIb/IIIa receptor. Sci Rep. 2019;9(1):8316. https://doi.org/10.1038/s41598-019-44767-2.

[40] Thomazini CM, Sachetto ATA, de Albuquerque CZ, et al. Involvement of von Willebrand factor and botrocetin in the thrombocytopenia induced by *Bothrops jararaca* snake venom. PLoS Negl Trop Dis. 2021;15(9):e0009715. https://doi.org/10.1371/journal.pntd.0009715.

[41] Florentin J, Rapon C, Pierre-Louis O, et al. ADAMTS13 in *Bothrops lanceolatus* snakebite envenoming: crude venom-induced reduction of in vitro enzymatic activity and clinical correlation in snakebite patients. PLoS Negl Trop Dis. 2025;19(10):e0013678. https://doi.org/10.1371/journal.pntd.0013678.

[42] Chugh KS, Pal Y, Ganguly NK. Complement depletion following envenomation by Russell's viper and *Echis carinatus* (saw-scaled viper) in the rhesus monkey. Am J Trop Med Hyg. 1977;26(5 Pt 1):1039–1043. https://doi.org/10.4269/ajtmh.1977.26.1039.

[43] Stone SF, Isbister GK, Shahmy S, et al. Immune response to snake envenoming and treatment with antivenom; complement activation, cytokine production and mast cell degranulation. PLoS Negl Trop Dis. 2013;7(7):e2326. https://doi.org/10.1371/journal.pntd.0002326.

[44] Pidde-Queiroz G, Magnoli FC, Portaro FC, et al. P-I snake venom metalloproteinase is able to activate the complement system by direct cleavage of central components of the cascade. PLoS Negl Trop Dis. 2013;7(10):e2519. https://doi.org/10.1371/journal.pntd.0002519.

[45] Menaldo DL, Bernardes CP, Jacob-Ferreira AL, et al. Effects of *Bothrops atrox* venom and two isolated toxins on the human complement system: modulation of pathways and generation of anaphylatoxins. Mol Immunol. 2016;80:91–100. https://doi.org/10.1016/j.molimm.2016.10.015.

[46] Silva de França F, Villas-Boas IM, Cogliati B, Woodruff TM, Reis EDS, Lambris JD, Tambourgi DV. C5a-C5aR1 axis activation drives envenomation immunopathology by the snake *Naja annulifera*. Front Immunol. 2021;12:652242. https://doi.org/10.3389/fimmu.2021.652242.

[47] Hew BE, Pangburn MK, Vogel CW, Fritzinger DC. Identification of intermolecular bonds between human factor B and cobra venom factor important for C3 convertase stability. Toxicon. 2020;184:68–77. https://doi.org/10.1016/j.toxicon.2020.05.025.

## Tables

### Table 1. Composition of the toxin sequence library

| Toxin family | Entries | External venom abundance (%) [4] |
|---|---:|---:|
| Kunitz-type inhibitors | 21 | 4.6 |
| PLA2 | 16 | 35.0 |
| snaclec/CTL | 8 | 22.4 |
| SVMP/disintegrin | 5 | 6.9 |
| SVSP | 4 | 16.0 |
| CRISP | 4 | 2.0 |
| LAAO | 2 | 5.2 |
| VEGF | 2 | Not separately quantified |
| NGF | 1 | 3.5 |
| **Total** | **63** | **95.6% quantified across reported families** |

### Table 2. Leave-one-source-out reconstruction of the core resource

| Removed evidence channel | Core genes (n) | Strict-core targets (n) | Strict-core genes lost |
|---|---:|---:|---|
| None | 1,042 | 10 | — |
| GeneCards | 482 | 7 | F11, KDR, PROS1 |
| Open Targets | 709 | 10 | None |
| DISEASES curated | 1,042 | 10 | None |
| DisGeNET | 1,041 | 10 | None |
| CTD direct | 1,039 | 10 | None |
| Prior-axis channel | 1,042 | 10 | None |

### Table 3. Background-matched enrichment and permutation summary

| Group | Input (n) | Background (n) | Leading term | Leading P | BH < 0.05 terms | Coagulation empirical P |
|---|---:|---:|---|---:|---:|---:|
| G2 primary: strict core | 10 | 1,042 | Formation of Fibrin Clot | 4.74 × 10⁻⁷ | 15 | 1.0 × 10⁻⁴ |
| G3 sensitivity: STRING-specific hubs | 5 | 1,042 | Extrinsic Pathway of Fibrin Clot Formation | 5.52 × 10⁻⁵ | 3 | 2.0 × 10⁻⁴ |
| G4 sensitivity: union | 15 | 1,042 | Formation of Fibrin Clot | 3.61 × 10⁻¹¹ | 24 | 1.0 × 10⁻⁴ |
| G5 sensitivity: union without ALB | 14 | 1,042 | Formation of Fibrin Clot | 1.70 × 10⁻¹¹ | 21 | Not tested |
| G6 sensitivity: −9 prior-labeled genes | 7 | 1,033 | Negative Regulation of Blood Coagulation | 2.78 × 10⁻⁶ | 2 | Not tested |
| G7 sensitivity: −27 axis genes | 4 | 1,015 | Blood Vessel Morphogenesis | 1.20 × 10⁻³ | 0 | Not tested |
| G1 supporting: curated targets | 15 | 16,662 | Complement and coagulation cascades | 7.39 × 10⁻¹⁸ | 69 | Not applicable |

### Table 4. Prioritized experiments for extending the VICC map to TMA

| Mechanistic question | Current evidence anchor | Decisive measurement |
|---|---|---|
| VWF release versus impaired processing | Modestly elevated VWF antigen in a 146-patient VICC cohort | TMA-stratified VWF antigen, multimers and ADAMTS13 activity |
| Receptor binding versus microvascular adhesion | Dabocetin–GPIbα and Rusvikunin–GPIIb/IIIa interactions | Endothelial VWF strings and shear-based microfluidic platelet adhesion |
| Direct complement cleavage versus host activation | *Daboia* in vivo complement signals and other-viperid cleavage studies | Purified-toxin cleavage, pathway-selective inhibition and endothelial deposition |
| Tissue injury versus microvascular TMA | Endothelial and inflammatory-myotoxic expression programs | Time-resolved clinical phenotyping integrated with vascular and renal markers |

## Figure legends

**Fig. 1. Evidence-calibrated study workflow.** The workflow links the 63-sequence/40-cluster toxin library, the 2,190-gene source-resolved collection with its 1,042-gene core, mechanism-typed literature curation, background-matched enrichment, expression-context analysis and the prioritized TMA experimental agenda.

**Fig. 2. Mechanism-typed venom–host map and factor X convergence.** Solid edges denote primary-literature-supported interactions. The factor X panel resolves six edges from four independent toxin entities into zymogen recognition, zymogen activation and FXa inhibition; RVV-X subunits are treated as one toxin complex.

**Fig. 3. Strict-core enrichment and sensitivity analyses.** G2 is the primary analysis, G3–G7 are sensitivity analyses and G1 is a supporting analysis. Panel a shows leading pathways, panel b shows the 10,000-permutation null distributions, panel c shows leave-one-source-out reconstruction and panel d distinguishes database-channel removal from axis-gene removal.

**Fig. 4. Descriptive STRING-expanded network.** The 54-node/321-edge functional-association network provides context for the ten strict-core targets. Hub candidates are displayed without implying causal dominance or independent experimental validation.

**Fig. 5. Expression-context analysis.** Volcano plots show classical limma results for GSE121297 and GSE248215. Context panels summarize SELE/ICAM1-centered endothelial activation and CCL2/TIMP1/SERPINE1-centered inflammatory-myotoxic responses.

**Fig. 6. Mechanistic hypothesis map from VICC to TMA.** Evidence-graded arrows connect curated toxin–target interactions, coagulation and fibrinolysis perturbation, platelet and endothelial responses, candidate complement branches and microvascular outcomes. VWF multimer processing, shear-dependent adhesion and complement–endothelium assays are highlighted as decisive next experiments; acute kidney injury is represented through parallel mechanistic routes.
