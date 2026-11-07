# -*- coding: utf-8 -*-
"""Follow-up: enrichment after dropping GeneCards channel + g:Profiler custom-background platform check."""
import os, json, urllib.request
import numpy as np
import pandas as pd
from scipy.special import gammaln

from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
OUT = str(Path(os.environ.get("REANALYSIS_OUT", SCRIPT_DIR)).resolve())
os.makedirs(OUT, exist_ok=True)

flag = pd.read_csv(SCRIPT_DIR / "core_evidence_flags.csv")
inputs = json.loads((SCRIPT_DIR / "analysis_inputs.json").read_text(encoding="utf-8"))
SOURCES = ['GC','OT','DISEASES','DGN','CTD','PRIOR']
use = [s for s in SOURCES if s != 'GC']
core_noGC = sorted(set(flag.loc[flag[use].any(axis=1), 'sym']))
print("noGC core:", len(core_noGC))

strict10 = sorted(inputs["strict10"])
union15 = sorted(set(strict10) | {'F2','F3','F7','F8','ALB'})
strict_noGC = sorted(set(strict10) & set(core_noGC))
union_noGC = sorted(set(union15) & set(core_noGC))
print("strict_noGC:", strict_noGC)
print("union_noGC:", union_noGC)

def load_gmt(p):
    t = {}
    for line in open(p, encoding="utf-8"):
        a = line.rstrip("\n").split("\t")
        if len(a) >= 3: t[a[0]] = {g.strip().upper() for g in a[2:] if g.strip()}
    return t
def logC(n,k): return gammaln(n+1)-gammaln(k+1)-gammaln(n-k+1)
def hyper_sf(K,M,n,N):
    sf = np.zeros(K.shape); lM = logC(M,N)
    for j in range(N+1):
        with np.errstate(divide='ignore',invalid='ignore'):
            pj = np.exp(logC(n,j)+logC(M-n,N-j)-lM)
        pj = np.where(np.isfinite(pj),pj,0.0)
        sf += (K<=j)*pj[None,:]
    return np.minimum(sf,1.0)
def bh(p):
    p=np.asarray(p,float); n=len(p); o=np.argsort(p); r=p[o]
    a=np.minimum.accumulate((r*n/(np.arange(n)+1))[::-1])[::-1]
    out=np.empty(n); out[o]=np.minimum(a,1); return out

libs = {l: load_gmt(str(SCRIPT_DIR / "gmt" / (l + ".gmt"))) for l in ["GO_Biological_Process_2023","KEGG_2021_Human","Reactome_2022"]}
bg = core_noGC; bgset=set(bg); idx={g:i for i,g in enumerate(bg)}
for gname, genes in [("noGC_strict7", strict_noGC), ("noGC_union", union_noGC)]:
    N=len(genes); rows=[]
    for lib, terms in libs.items():
        names,sizes,K = [],[],[]
        for name, gg0 in terms.items():
            gg = gg0 & bgset
            if len(gg)>=3:
                names.append(name); sizes.append(len(gg)); K.append(len(gg & set(genes)))
        sizes=np.array(sizes,float); K=np.array(K,float)
        p = hyper_sf(K[None,:], len(bg), sizes, N)[0]; q=bh(p)
        for i,nm in enumerate(names):
            if K[i]>0: rows.append({"library":lib,"term":nm,"overlap":int(K[i]),"term_n":int(sizes[i]),"p":p[i],"BH_q":q[i]})
    df = pd.DataFrame(rows).sort_values("p")
    df.to_csv(os.path.join(OUT, "enrichment_%s.csv" % gname), index=False, encoding="utf-8-sig")
    print("%s N=%d bg=%d BH<0.05=%d top=%s p=%.2e" % (gname,N,len(bg),(df['BH_q']<0.05).sum(),df.iloc[0]['term'][:50],df.iloc[0]['p']))

# ---- g:Profiler custom background ----
def gost(query, background=None, tag=""):
    payload = {"organism":"hsapiens","query":query,"sources":["GO:BP","KEGG","REAC"],
               "user_threshold":1.0,"significance_threshold_method":"g_SCS"}
    if background is not None:
        payload["domain_scope"]="custom"; payload["background"]=background
    req = urllib.request.Request("https://biit.cs.ut.ee/gprofiler/api/gost/profile/",
        data=json.dumps(payload).encode(), headers={"Content-Type":"application/json","User-Agent":"ref-check/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        res = json.loads(r.read().decode())
    rows = [{"source":x["source"],"term":x["name"],"p":x["p_value"],"term_size":x["term_size"],
             "query_size":x["query_size"],"intersection":x["intersection_size"]} for x in res["result"]]
    df = pd.DataFrame(rows).sort_values("p")
    df.to_csv(os.path.join(OUT, "gprofiler_%s.csv" % tag), index=False, encoding="utf-8-sig")
    print("g:Profiler %-18s terms=%4d top=%s p=%.2e | g:SCS<0.05 n=%d" %
          (tag, len(df), df.iloc[0]['term'][:45], df.iloc[0]['p'], (df['p']<0.05).sum()))
    return df

if os.environ.get("SKIP_GPROFILER") == "1":
    print("g:Profiler requests skipped because SKIP_GPROFILER=1")
else:
    try:
        full_core = sorted(set(flag.loc[flag[SOURCES].any(axis=1), "sym"]))
        gost(strict10, full_core, "G2_strict10_bg1042")
        gost(union15, full_core, "G4_union15_bg1042")
        gost(union15, None, "G4_union15_genome_replication")
    except Exception as e:
        print("g:Profiler failed:", repr(e))
print("DONE")
