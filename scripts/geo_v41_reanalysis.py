# -*- coding: utf-8 -*-
"""
v41 GEO re-analysis (post-audit correction, 2026-10-02)
- GSE121297: static rhodocetin-ab (RCab) vs static control, 3 vs 3, Affymetrix HG-U133 Plus 2.0 (GPL570)
- GSE248215: D. russelii venom 24 h vs PBS, 3 vs 2, NanoString Fibrosis V2 panel (760 genes)
Corrections vs the pre-v41 pipeline:
  1) one fixed probe per gene: highest mean expression across ALL samples in the contrast
     (the old code took the per-sample max probe, so a gene could come from different probes
     in different samples);
  2) method named as what it is: Welch's t-tests in Python + Benjamini-Hochberg correction
     (not limma).
Outputs (official v41 result files, reproducible byte-level from this script):
  06_geo/GSE121297_deg_static_rcab_vs_ctrl_v41reanalysis.csv  (22,453 genes)
  06_geo/GSE248215_deg_DR24h_vs_ctrl_v41reanalysis.csv        (760 genes)
It also rewrites the legacy standard-name files (same rows/statistics, original
column names) so older figure scripts stay consistent with the v41 pipeline:
  06_geo/GSE121297_deg_static_rcab_vs_ctrl.csv   (symbol/log2FC/p_value/adj_p/mean_ctrl/mean_rcab)
  06_geo/GSE248215_deg_DR24h_vs_ctrl.csv         (symbol/log2FC/p_value/adj_p)
Note on probe annotation: one probe per gene is selected by the highest mean across
the six contrast samples; a probe that maps to several symbols contributes to each of
those symbols (22,453 genes total). An earlier archived run (kept as
..._archived21183.csv) additionally resolved multi-symbol probe conflicts, yielding
21,183 genes; log2FC and raw P values of all shared genes are identical, BH values
shift only through the changed denominator, and the conclusion (0 genes at
BH-adjusted P < 0.05) is unchanged.
"""
import gzip, pickle
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

BASE = Path(__file__).resolve().parents[1]
GEO = BASE / '06_geo'

def bh_adjust(pvals):
    p = np.asarray(pvals, dtype=float)
    n = len(p)
    order = np.argsort(p)
    ranked = p[order]
    q = ranked * n / (np.arange(n) + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    out = np.empty(n)
    out[order] = np.clip(q, 0, 1)
    return out

def welch_table(df, treat_cols, ctrl_cols):
    """df: genes x samples (log2-scale); returns gene/log2FC/p_raw/p_BH sorted by p_raw."""
    t = df[treat_cols].to_numpy(dtype=float)
    c = df[ctrl_cols].to_numpy(dtype=float)
    log2fc = t.mean(axis=1) - c.mean(axis=1)
    with np.errstate(invalid='ignore'):
        stat, p = stats.ttest_ind(t, c, axis=1, equal_var=False, nan_policy='omit')
    p = np.where(np.isnan(p), 1.0, p)
    res = pd.DataFrame({'gene': df.index, 'log2FC': log2fc, 'p_raw': p})
    res['p_BH'] = bh_adjust(res['p_raw'].to_numpy())
    return res.sort_values('p_raw').reset_index(drop=True)

# ---------- GSE121297 (GPL570, 3 vs 3 static) ----------
CTRL = ['GSM3430994', 'GSM3430995', 'GSM3430996']
RCAB = ['GSM3430997', 'GSM3430998', 'GSM3430999']
mat = pickle.load(open(GEO / 'gse121297_gpl570_matrix.pkl', 'rb'))
mat = mat[CTRL + RCAB]
p2s = pd.read_csv(GEO / 'gpl570_probe2symbol.csv')
p2s = p2s.dropna(subset=['symbol'])
p2s = p2s[p2s['symbol'].astype(str).str.strip() != '']
m = mat.merge(p2s[['probe', 'symbol']], left_index=True, right_on='probe')
m = m.set_index('probe')
# fixed probe rule: highest mean across all 6 samples (chosen before testing)
m['row_mean'] = m[CTRL + RCAB].mean(axis=1)
best = m.sort_values('row_mean', ascending=False).drop_duplicates('symbol')
g = best.set_index('symbol')[CTRL + RCAB]
res1 = welch_table(g, RCAB, CTRL)
res1.to_csv(GEO / 'GSE121297_deg_static_rcab_vs_ctrl_v41reanalysis.csv', index=False)
print('GSE121297 genes:', len(res1), 'BH<0.05:', int((res1.p_BH < 0.05).sum()))

# legacy standard-name companion (original column names, same v41 statistics)
legacy1 = res1.rename(columns={'gene': 'symbol', 'p_raw': 'p_value', 'p_BH': 'adj_p'})
legacy1 = legacy1.merge(
    pd.DataFrame({'symbol': g.index,
                  'mean_ctrl': g[CTRL].mean(axis=1).to_numpy(),
                  'mean_rcab': g[RCAB].mean(axis=1).to_numpy()}),
    on='symbol', how='left')
legacy1[['symbol', 'log2FC', 'p_value', 'adj_p', 'mean_ctrl', 'mean_rcab']].to_csv(
    GEO / 'GSE121297_deg_static_rcab_vs_ctrl.csv', index=False)

# ---------- GSE248215 (NanoString, 3 vs 2, DR 24 h vs Control) ----------
with gzip.open(GEO / 'GSE248215_normalized_data.txt.gz', 'rt') as f:
    ns = pd.read_csv(f, sep='\t')
ns = ns.set_index('Gene Name')
treat = [c for c in ns.columns if c.startswith('DR-') and c.endswith('-24h')]
ctrl = [c for c in ns.columns if c.startswith('Control')]
print('GSE248215 treat cols:', treat, '| ctrl cols:', ctrl)
g2 = ns[treat + ctrl].apply(pd.to_numeric, errors='coerce').dropna()
res2 = welch_table(g2, treat, ctrl)
res2.to_csv(GEO / 'GSE248215_deg_DR24h_vs_ctrl_v41reanalysis.csv', index=False)
print('GSE248215 genes:', len(res2), 'BH<0.05:', int((res2.p_BH < 0.05).sum()))

# legacy standard-name companion
legacy2 = res2.rename(columns={'gene': 'symbol', 'p_raw': 'p_value', 'p_BH': 'adj_p'})
legacy2[['symbol', 'log2FC', 'p_value', 'adj_p']].to_csv(
    GEO / 'GSE248215_deg_DR24h_vs_ctrl.csv', index=False)
