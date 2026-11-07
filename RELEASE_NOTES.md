# Release notes: v2026.11.07-JVAT

This version provides the English data, result tables, portable analysis scripts, supplementary files and figure sources for the JVAT reanalysis archive.

## Main contents

- A 447-row edge-level evidence audit and a 63-record toxin library.
- Custom/usearch clustering comparison with the corrected pairwise Rand index of 0.996.
- Source-resolved disease-gene flags and reproducible core definitions.
- Matched-background enrichment, 10,000-permutation summaries and sensitivity analyses.
- Classical limma expression analyses and analysis-ready matrices.
- Descriptive network and structural-context inventories.
- Six manuscript figure pairs and their cached permutation nulls.

## Reproduction and integrity

Run `python validate_archive.py` from the archive root. `MANIFEST.csv` records the size and SHA256 of every payload file other than the manifest itself. Analysis scripts support separate output directories so archived results can remain unchanged during checks.

The version-specific public URL and Zenodo DOI are properties of the published release and should be cited only after the release is publicly accessible.
