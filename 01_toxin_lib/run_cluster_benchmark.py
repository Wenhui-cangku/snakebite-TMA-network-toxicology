"""Benchmark custom 90%-identity clusters with usearch cluster_fast."""
from __future__ import annotations

import itertools
import json
import math
import os
from pathlib import Path
import subprocess

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
OUT = Path(os.environ.get("CLUSTER_OUT", SCRIPT_DIR / "cluster_benchmark")).resolve()
OUT.mkdir(parents=True, exist_ok=True)
USEARCH = os.environ.get("USEARCH_BIN", "usearch")

seqs: dict[str, str] = {}
ac = None
sequence: list[str] = []
with (SCRIPT_DIR / "all_toxins_raw.fasta").open(encoding="utf-8") as handle:
    for raw_line in handle:
        line = raw_line.strip()
        if line.startswith(">"):
            if ac and len("".join(sequence)) >= 30:
                seqs[ac] = "".join(sequence)
            header = line[1:]
            ac = header.split("|")[1] if "|" in header else header.split()[0]
            sequence = []
        else:
            sequence.append(line)
if ac and len("".join(sequence)) >= 30:
    seqs[ac] = "".join(sequence)
assert len(seqs) == 63, f"Expected 63 sequences, found {len(seqs)}"

fasta = OUT / "toxins_63.fasta"
with fasta.open("w", encoding="utf-8") as handle:
    for accession, seq in sorted(seqs.items(), key=lambda item: -len(item[1])):
        handle.write(f">{accession}\n{seq}\n")

command = [
    USEARCH, "-cluster_fast", str(fasta), "-id", "0.9",
    "-centroids", str(OUT / "usearch_centroids.fasta"),
    "-uc", str(OUT / "usearch_clusters.uc"), "-quiet",
]
try:
    completed = subprocess.run(command, capture_output=True, text=True)
except FileNotFoundError as exc:
    raise RuntimeError("Set USEARCH_BIN to the usearch v11.0.667 executable") from exc
if completed.returncode != 0:
    raise RuntimeError(f"usearch failed: {completed.stderr[:1000]}")

members: dict[int, list[str]] = {}
with (OUT / "usearch_clusters.uc").open(encoding="utf-8") as handle:
    for line in handle:
        fields = line.rstrip("\n").split("\t")
        if len(fields) < 9 or fields[0] not in {"S", "H"}:
            continue
        members.setdefault(int(fields[1]), []).append(fields[8])
assert len(members) == 39, f"Expected 39 usearch clusters, found {len(members)}"

library = pd.read_csv(SCRIPT_DIR / "toxin_library.csv")
custom: dict[str, list[str]] = {}
for row in library.itertuples(index=False):
    custom.setdefault(str(row.custom_cluster_id), []).append(str(row.uniprot_or_genbank_accession))
assert len(custom) == 40 and sum(map(len, custom.values())) == 63

usearch_pairs = {pair for group in members.values()
                 for pair in itertools.combinations(sorted(set(group)), 2)}
custom_pairs = {pair for group in custom.values()
                for pair in itertools.combinations(sorted(set(group)), 2)}
shared = custom_pairs & usearch_pairs
only_custom = sorted(custom_pairs - usearch_pairs)
only_usearch = sorted(usearch_pairs - custom_pairs)
total_pairs = math.comb(len(seqs), 2)
agreeing = total_pairs - len(only_custom) - len(only_usearch)
rand_index = agreeing / total_pairs
assert (len(custom_pairs), len(usearch_pairs), len(shared)) == (35, 41, 34)
assert (len(only_custom), len(only_usearch)) == (1, 7)
assert round(rand_index, 3) == 0.996

with (OUT / "cluster_comparison.txt").open("w", encoding="utf-8") as handle:
    handle.write("usearch 11.0.667 -cluster_fast -id 0.9 vs custom greedy 90% clustering\n")
    handle.write(f"usearch clusters: {len(members)} | custom clusters: {len(custom)}\n")
    handle.write(f"same-cluster pairs custom={len(custom_pairs)} usearch={len(usearch_pairs)} shared={len(shared)}\n")
    handle.write(f"only custom: {only_custom}\nonly usearch: {only_usearch}\n")
    handle.write(f"Rand index: {agreeing}/{total_pairs} = {rand_index:.12f} (0.996 to three decimals)\n")
    handle.write("\nusearch membership:\n")
    for cid, group in sorted(members.items()):
        handle.write(f"  C{cid} ({len(group)}): {','.join(sorted(set(group)))}\n")
    handle.write("\ncustom membership:\n")
    for cid, group in sorted(custom.items()):
        handle.write(f"  {cid} ({len(group)}): {','.join(sorted(set(group)))}\n")

summary = {
    "sequences": len(seqs), "custom_clusters": len(custom), "usearch_clusters": len(members),
    "custom_pairs": len(custom_pairs), "usearch_pairs": len(usearch_pairs),
    "shared_pairs": len(shared), "custom_only_pairs": len(only_custom),
    "usearch_only_pairs": len(only_usearch), "agreeing_pairs": agreeing,
    "total_pairs": total_pairs, "rand_index": rand_index,
}
(OUT / "cluster_benchmark_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
print(json.dumps(summary, indent=2))
