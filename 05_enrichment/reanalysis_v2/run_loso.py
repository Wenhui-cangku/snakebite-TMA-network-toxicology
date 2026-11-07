"""Reconstruct the disease core and run leave-one-source-out checks."""
from __future__ import annotations

import json
import os
from pathlib import Path

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
OUT = Path(os.environ.get("LOSO_OUT", SCRIPT_DIR)).resolve()
OUT.mkdir(parents=True, exist_ok=True)
SOURCES = ["GC", "OT", "DISEASES", "DGN", "CTD", "PRIOR"]

flags = pd.read_csv(SCRIPT_DIR / "core_evidence_flags.csv")
inputs = json.loads((SCRIPT_DIR / "analysis_inputs.json").read_text(encoding="utf-8"))
flags["sym"] = flags["sym"].str.upper()
core_documented = set(flags.loc[flags["in_core_doc"].astype(bool), "sym"])
reconstructed = set(flags.loc[flags[SOURCES].any(axis=1), "sym"])
assert len(flags) == 2190
assert len(core_documented) == 1042
assert reconstructed == core_documented

strict10 = set(inputs["strict10"])
literature15 = set(inputs["L2_15"])
rows = []
for dropped in [None] + SOURCES:
    used = [source for source in SOURCES if source != dropped]
    core = set(flags.loc[flags[used].any(axis=1), "sym"])
    strict = sorted(strict10 & core)
    literature = sorted(literature15 & core)
    rows.append({
        "dropped_source": dropped or "none(full core)",
        "core_n": len(core),
        "strict_core_n": len(strict),
        "strict_core_genes": ";".join(strict),
        "L2_targets_in_core_n": len(literature),
        "lost_from_documented_core": len(core_documented - core),
    })
result = pd.DataFrame(rows)
result.to_csv(OUT / "loso_core_summary.csv", index=False, encoding="utf-8-sig")
print(result.to_string(index=False))
print("Core reconstruction and LOSO checks passed")
