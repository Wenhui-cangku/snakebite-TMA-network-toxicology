# Manual Export Guide for Blocked Databases (GeneCards / DisGeNET / OMIM / CTD)

> Verified 2026-09-22: the four databases below cannot be scraped programmatically (anti-bot / registration required). Export them manually in a browser following this guide, place the files into `snakebite_TMA/02_disease_genes/manual/`; they will then be merged into the master table with threshold sensitivity analysis.

## 1. GeneCards (primary threshold source; most important)

1. Open https://www.genecards.org/ and search each of the 6 terms separately:
   `thrombotic microangiopathy`, `snakebite envenoming`, `venom-induced consumption coagulopathy`, `microangiopathic hemolytic anemia`, `atypical hemolytic uremic syndrome`, `thrombotic thrombocytopenic purpura`
2. On the results page click **"Export"** (Excel/CSV; free account login required).
3. Name files `genecards_<term abbreviation>.xlsx` (e.g. `genecards_tma.xlsx`).
4. **Record the hit total and export time for each term** (as filename annotations or reported directly).

## 2. DisGeNET

1. Register a free academic account at https://disgenet.com/ → generate an API key on your profile page;
2. Provide the API key for batch re-runs;
3. Threshold per protocol: score ≥ 0.1.

## 3. OMIM

1. Open https://www.omim.org/, register a free account and apply for an API key (academic approval is immediate);
2. Or search each disease term on the web and record MIM numbers plus the "Gene/Locus" association table (screenshot/export);
3. Provide the key or the exported files.

## 4. CTD (Comparative Toxicogenomics Database)

1. Open https://ctdbase.org/ → **Batch Query** tool;
2. Input type: `Disease`; paste the 6 terms one by one (or MeSH IDs: HUS=D006463, TTP=D011697, Snake Bites=D012909);
3. Report: `genes_curated`; Format: `TSV`; download as `ctd_<term>.tsv`;
4. The export includes fields sorted by inference score.

## What happens after delivery

Merge the four databases → UniProt ID normalisation → union/intersection with the existing 750-gene master table → GeneCards ≥median (or ≥10) primary-threshold sensitivity analysis → update PRISMA line B and the data management table.
