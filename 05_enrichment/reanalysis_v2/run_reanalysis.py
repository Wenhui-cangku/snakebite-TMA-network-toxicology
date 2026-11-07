# -*- coding: utf-8 -*-
"""
Matched-background enrichment and permutation analysis:
- custom-background hypergeometric enrichment (background = 1,042-gene core set)
- four input layers separately + no-ALB + no-forced-inclusion variants
- 10,000x permutation test from the same background (global min-p and coagulation-term min-p)
All local, no external API. Enrichr GMT libraries cached in ./gmt.
"""
import os, re, json, time
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.special import gammaln

SCRIPT_DIR = Path(__file__).resolve().parent
OUT = str(Path(os.environ.get("REANALYSIS_OUT", SCRIPT_DIR)).resolve())
os.makedirs(OUT, exist_ok=True)
GMT = str(SCRIPT_DIR / "gmt")
N_PERM = int(os.environ.get("N_PERM", "10000"))
if N_PERM < 1:
    raise ValueError("N_PERM must be positive")
SEED = 20261106
rng = np.random.default_rng(SEED)

# ---------------- gene sets ----------------
def load_gmt(path):
    terms = {}
    for line in open(path, encoding="utf-8"):
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 3: continue
        name = parts[0]
        genes = {g.strip().upper() for g in parts[2:] if g.strip()}
        if genes: terms[name] = genes
    return terms

libs = {}
for lib in ["GO_Biological_Process_2023", "KEGG_2021_Human", "Reactome_2022"]:
    libs[lib] = load_gmt(os.path.join(GMT, lib + ".gmt"))
    print(lib, len(libs[lib]), "terms")

universe = set()
for t in libs.values():
    for g in t.values(): universe |= g
print("annotated universe:", len(universe))

# ---------------- core set & forced-inclusion tags ----------------
inputs = json.loads((SCRIPT_DIR / "analysis_inputs.json").read_text(encoding="utf-8"))
bg_full = sorted(inputs["core1042"])
prior9 = sorted(inputs["prior9"])
forced27 = sorted(inputs["forced27"])
assert len(bg_full) == 1042 and len(prior9) == 9 and len(forced27) == 27

L2_15 = sorted(inputs["L2_15"])
strict10 = sorted(inputs["strict10"])
hubs5 = list(inputs["hubs5"])
union15 = sorted(set(strict10) | set(hubs5))

groups = [
    # name, genes, background, rationale
    ("G1_L2curated15", L2_15, "genome", "targets selected by toxin literature only; genome background justified"),
    ("G2_strictcore10", strict10, "core1042", "strict-core targets vs eligible-gene background"),
    ("G3_STRINGhubs5", hubs5, "core1042", "STRING-expanded hubs only"),
    ("G4_union15", union15, "core1042", "original combined input, corrected background"),
    ("G5_union14_noALB", sorted(set(union15) - {'ALB'}), "core1042", "ALB hub-artifact removed"),
    ("G6_strict7_noPrior9", sorted(set(strict10) - set(prior9)), "core1033", "drop 9 prior-tagged forced genes from input and background"),
    ("G7_strict4_noForced27", sorted(set(strict10) - set(forced27)), "core1015", "drop all 27 axis-prior genes from input and background"),
]
backgrounds = {
    "genome": sorted(universe),
    "core1042": bg_full,
    "core1033": sorted(set(bg_full) - set(prior9)),
    "core1015": sorted(set(bg_full) - set(forced27)),
}

pd.DataFrame([
    {"group": g, "n_input": len(gs), "background": b, "n_background": len(backgrounds[b]),
     "genes": ";".join(gs), "rationale": r}
    for g, gs, b, r in groups
]).to_csv(os.path.join(OUT, "sets_definition.csv"), index=False, encoding="utf-8-sig")

# ---------------- exact hypergeometric via log-gamma (vectorized) ----------------
def logC(n, k):
    return gammaln(n + 1) - gammaln(k + 1) - gammaln(n - k + 1)

def hypergeom_sf_matrix(K, M, n_vec, N):
    """P(X >= K) for each element of K (chunk x terms), n_vec = term sizes."""
    sf = np.zeros(K.shape, dtype=np.float64)
    logCM = logC(M, N)
    for j in range(0, N + 1):
        with np.errstate(divide='ignore', invalid='ignore'):
            lp = logC(n_vec, j) + logC(M - n_vec, N - j) - logCM
            pj = np.exp(lp)
        pj = np.where(np.isfinite(pj), pj, 0.0)
        sf += (K <= j) * pj[None, :]
    return np.minimum(sf, 1.0)

def bh(p):
    p = np.asarray(p, dtype=float)
    n = len(p)
    order = np.argsort(p)
    ranked = p[order]
    adj = ranked * n / (np.arange(n) + 1)
    adj = np.minimum.accumulate(adj[::-1])[::-1]
    out = np.empty(n); out[order] = np.minimum(adj, 1.0)
    return out

# ---------------- per-group enrichment ----------------
def prepare_terms(bg_set):
    """Return per library: names, term sizes within bg, membership index matrix data."""
    bg = sorted(bg_set)
    idx = {g: i for i, g in enumerate(bg)}
    prep = {}
    for lib, terms in libs.items():
        names, sizes, members = [], [], []
        for name, genes in terms.items():
            gg = genes & bg_set
            if len(gg) >= 3:
                names.append(name); sizes.append(len(gg))
                members.append(sorted(idx[g] for g in gg))
        prep[lib] = (names, np.array(sizes, dtype=float), members, bg)
    return prep

def enrichment_for_group(gname, genes, bkey, prep_cache):
    bg_set = set(backgrounds[bkey])
    if bkey not in prep_cache:
        prep_cache[bkey] = prepare_terms(bg_set)
    prep = prep_cache[bkey]
    bg = prep["GO_Biological_Process_2023"][3]
    idx = {g: i for i, g in enumerate(bg)}
    in_bg = [g for g in genes if g in idx]
    N = len(in_bg)
    rows = []
    for lib, (names, sizes, members, _) in prep.items():
        M = len(bg)
        K = np.array([len(set(memb) & {idx[g] for g in in_bg}) for memb in members], dtype=float)
        p = hypergeom_sf_matrix(K[None, :], M, sizes, N)[0]
        q = bh(p)
        for i, name in enumerate(names):
            if K[i] > 0:
                rows.append({"library": lib, "term": name, "overlap": int(K[i]),
                             "input_n": N, "term_n_in_bg": int(sizes[i]), "bg_n": M,
                             "p": p[i], "BH_q": q[i],
                             "overlap_genes": ";".join(sorted(g for g in in_bg if idx[g] in set(members[i])))})
    df = pd.DataFrame(rows).sort_values("p")
    df.to_csv(os.path.join(OUT, "enrichment_%s.csv" % gname), index=False, encoding="utf-8-sig")
    return df, N

prep_cache = {}
summary = []
for gname, genes, bkey, _ in groups:
    t0 = time.time()
    df, N = enrichment_for_group(gname, genes, bkey, prep_cache)
    nsig = int((df['BH_q'] < 0.05).sum()) if len(df) else 0
    top = df.iloc[0] if len(df) else None
    summary.append({"group": gname, "input_in_bg": N, "bg": bkey,
                    "n_terms_tested_with_overlap": len(df), "n_BH<0.05": nsig,
                    "top_term": top['term'] if top is not None else "",
                    "top_p": top['p'] if top is not None else np.nan,
                    "top_BH_q": top['BH_q'] if top is not None else np.nan})
    print("%-22s N=%2d bg=%-8s terms=%4d BH<0.05=%3d top=%s (p=%.2e) [%.1fs]" %
          (gname, N, bkey, len(df), nsig, summary[-1]['top_term'][:45], summary[-1]['top_p'], time.time()-t0))

pd.DataFrame(summary).to_csv(os.path.join(OUT, "enrichment_summary_by_group.csv"), index=False, encoding="utf-8-sig")

# ---------------- permutation test ----------------
COAG = re.compile(r"coagulat|hemostasi|haemostasi|fibrin|platelet|thromb|blood clot|clotting", re.I)

def permutation(gname, genes, bkey, prep_cache, n_perm=N_PERM):
    bg_set = set(backgrounds[bkey])
    prep = prep_cache[bkey]
    bg = prep["GO_Biological_Process_2023"][3]
    idx = {g: i for i, g in enumerate(bg)}
    M = len(bg); N = len([g for g in genes if g in idx])
    # pooled term table
    names_all, sizes_all, memb_all = [], [], []
    for lib, (names, sizes, members, _) in prep.items():
        names_all += names; sizes_all += list(sizes); memb_all += members
    sizes_all = np.array(sizes_all, dtype=float)
    T = len(names_all)
    coag_mask = np.array([bool(COAG.search(n)) for n in names_all])
    # dense membership matrix T x M as float32 (T~7000, M~1000 -> ~28MB)
    A = np.zeros((T, M), dtype=np.float32)
    for i, memb in enumerate(memb_all):
        A[i, memb] = 1.0
    # observed
    obs_vec = np.zeros(M, dtype=np.float32)
    for g in genes:
        if g in idx: obs_vec[idx[g]] = 1.0
    K_obs = A @ obs_vec
    p_obs = hypergeom_sf_matrix(K_obs[None, :], M, sizes_all, N)[0]
    min_obs = float(p_obs.min())
    min_coag_obs = float(p_obs[coag_mask].min()) if coag_mask.any() else np.nan
    # random sets
    min_rand = np.empty(n_perm); min_coag_rand = np.empty(n_perm)
    chunk = 250
    done = 0
    while done < n_perm:
        c = min(chunk, n_perm - done)
        perm_idx = np.argsort(rng.random((c, M)), axis=1)[:, :N]
        X = np.zeros((c, M), dtype=np.float32)
        np.put_along_axis(X, perm_idx, 1.0, axis=1)
        K = (X @ A.T)
        P = hypergeom_sf_matrix(K, M, sizes_all, N)
        min_rand[done:done+c] = P.min(axis=1)
        min_coag_rand[done:done+c] = P[:, coag_mask].min(axis=1)
        done += c
    emp = (1 + (min_rand <= min_obs).sum()) / (n_perm + 1)
    emp_c = (1 + (min_coag_rand <= min_coag_obs).sum()) / (n_perm + 1)
    res = {"group": gname, "N": N, "bg": bkey, "n_perm": n_perm,
           "observed_min_p": min_obs, "permutation_empirical_p_global": float(emp),
           "random_min_p_median": float(np.median(min_rand)),
           "random_min_p_q05": float(np.quantile(min_rand, 0.05)),
           "observed_min_coag_p": min_coag_obs,
           "permutation_empirical_p_coag": float(emp_c),
           "random_coag_min_p_median": float(np.median(min_coag_rand)),
           "frac_random_with_coag_p_lt_1e-10": float((min_coag_rand < 1e-10).mean()),
           "n_coag_terms": int(coag_mask.sum())}
    print("PERM %-16s N=%2d  obs min p=%.2e  empirical global p=%.4f | coag obs=%.2e empirical=%.4f | random coag median=%.2e, P(random<1e-10)=%.3f" %
          (gname, N, min_obs, emp, min_coag_obs, emp_c, res["random_coag_min_p_median"], res["frac_random_with_coag_p_lt_1e-10"]))
    return res

perm_results = []
for gname, genes, bkey in [("G2_strictcore10", strict10, "core1042"),
                            ("G4_union15", union15, "core1042"),
                            ("G3_STRINGhubs5", hubs5, "core1042")]:
    t0 = time.time()
    perm_results.append(permutation(gname, genes, bkey, prep_cache))
    print("   (%.1fs)" % (time.time() - t0))

pd.DataFrame(perm_results).to_csv(os.path.join(OUT, "permutation_results.csv"), index=False, encoding="utf-8-sig")
json.dump({"seed": SEED, "n_perm": N_PERM, "results": perm_results},
          open(os.path.join(OUT, "permutation_results.json"), "w", encoding="utf-8"), indent=1)
print("ALL DONE")
