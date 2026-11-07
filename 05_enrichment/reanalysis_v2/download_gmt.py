"""Download Enrichr GMT snapshots for local enrichment analyses."""
from pathlib import Path
import urllib.request

OUT = Path(__file__).resolve().parent / "gmt"
OUT.mkdir(parents=True, exist_ok=True)
LIBRARIES = ["GO_Biological_Process_2023", "KEGG_2021_Human", "Reactome_2022"]
for library in LIBRARIES:
    destination = OUT / f"{library}.gmt"
    if destination.is_file() and destination.stat().st_size > 1000:
        print("cached", library)
        continue
    url = "https://maayanlab.cloud/Enrichr/geneSetLibrary?mode=text&libraryName=" + library
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=120) as response:
        data = response.read()
    destination.write_bytes(data)
    print("downloaded", library, len(data), "bytes")
print("done")
