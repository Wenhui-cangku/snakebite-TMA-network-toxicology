# -*- coding: utf-8 -*-
"""
Phase 5A - structure preprocessing: chain extraction, water/ligand removal (catalytic ZN retained), generation of the docking-pair list
Output: 07_docking/prepared/*.pdb + docking_pairs.csv
"""
from pathlib import Path
import os

SRC = str(Path(__file__).resolve().parents[1] / "07_docking" / "structures")
DST = str(Path(__file__).resolve().parents[1] / "07_docking" / "prepared")
os.makedirs(DST, exist_ok=True)

# (source file, chains to keep, HET to keep (except HOH), output name, description)
JOBS = [
    ("2E3X_toxin_RVV-X_complex.pdb", {"A", "B", "C"}, {"ZN"}, "T_RVVX_2E3X_ABC.pdb", "RVV-X full complex (heavy-chain SVMP + light-chain snaclec ×2), catalytic Zn retained"),
    ("3S9C_toxin_RVV-Vγ+FV_fragment.pdb", {"A"}, set(), "T_RVVV_3S9C_A.pdb", "RVV-Vγ catalytic chain (chain B is the co-crystallized FV fragment = direct structural evidence)"),
    ("1KPM_toxin_PLA2_VRV-PL-VIIIa.pdb", {"A"}, set(), "T_PLA2_1KPM_A.pdb", "PLA2 VRV-PL-VIIIa single copy"),
    ("2H4C_toxin_daboiatoxin.pdb", {"A", "B"}, set(), "T_daboiatoxin_2H4C_AB.pdb", "daboiatoxin heterodimer single copy"),
    ("1WQ9_toxin_svVEGF.pdb", {"A", "B"}, set(), "T_svVEGF_1WQ9_AB.pdb", "svVEGF homodimer"),
    ("AF-B8K1W0_daborhagin-K.pdb", {"A"}, set(), "T_daborhaginK_AF.pdb", "daborhagin-K AlphaFold (mean pLDDT 84.0)"),
    ("AF-Q38L02_snaclec.pdb", {"A"}, set(), "T_snaclecQ38L02_AF.pdb", "snaclec Q38L02 AlphaFold (mean pLDDT 88.9)"),
    ("AF-H6VC06_Kunitz.pdb", {"A"}, set(), "T_KunitzH6VC06_AF.pdb", "Kunitz H6VC06 AlphaFold (mean pLDDT 88.6)"),
    ("7KVE_host_FV.pdb", {"B"}, set(), "H_FV_7KVE_B.pdb", "human coagulation factor V full length (cryoEM 3.3 Å)"),
    ("2W26_host_FXa.pdb", {"A", "B"}, set(), "H_FXa_2W26_AB.pdb", "human FXa (rivaroxaban RIV removed)"),
    ("3GHG_host_fibrinogen.pdb", {"A", "B", "C"}, set(), "H_FIB_3GHG_ABC.pdb", "human fibrinogen half-molecule (A=α/FGA, B=β/FGB, C=γ/FGG)"),
    ("1M10_host_GP1BA-VWF.pdb", {"A"}, set(), "H_GP1BA_1M10_A.pdb", "GP1BA extracellular segment"),
    ("1M10_host_GP1BA-VWF.pdb", {"A", "B"}, set(), "H_GP1BA_VWF_1M10_AB.pdb", "GP1BA-VWF A1 complex (template)"),
    ("3V2A_host_VEGFR2-VEGF.pdb", {"R"}, set(), "H_VEGFR2_3V2A_R.pdb", "VEGFR2/KDR extracellular region"),
    ("1QRZ_host_plasminogen.pdb", {"A"}, set(), "H_PLG_1QRZ_A.pdb", "plasminogen catalytic domain"),
    ("1PPB_host_thrombin.pdb", {"L", "H"}, set(), "H_F2_1PPB_LH.pdb", "thrombin α (light+heavy chains)"),
]

for src, keep_chains, keep_het, out, note in JOBS:
    lines = []
    with open(os.path.join(SRC, src)) as f:
        for line in f:
            if line.startswith(("ATOM", "TER")):
                if line[21] in keep_chains:
                    lines.append(line)
            elif line.startswith("HETATM"):
                if line[17:20].strip() in keep_het and line[21] in keep_chains:
                    lines.append(line)
    with open(os.path.join(DST, out), "w") as f:
        f.writelines(lines)
        f.write("END\n")
    print(f"{out:34s} {len(lines):6d} lines  {note}")

# pair list
import csv
pairs = [
    ["P1", "T_RVVX_2E3X_ABC.pdb", "H_FXa_2W26_AB.pdb", "RVV-X → FX (activation cleavage at Arg-Ile)", "literature 1.0 (Q7LZ61/Q4PRD1/Q4PRD2)", "HADDOCK: toxin Zn catalytic domain HEXXHXXGXXH motif surface + FX heavy-chain N-terminal activation peptide region (residue numbers verified in PyMOL); ClusPro direct submission"],
    ["P2", "T_RVVV_3S9C_A.pdb", "H_FV_7KVE_B.pdb", "RVV-Vγ → FV (cleaves Arg1545-Ser1546)", "literature 1.0 (P18965)", "HADDOCK: SVSP catalytic triad (His57/Asp102/Ser195, chymotrypsin numbering) + around FV Arg1545; note: 3S9C chain B already has an FV-fragment co-crystal = direct structural evidence; docking serves as full-length validation"],
    ["P3", "T_daborhaginK_AF.pdb", "H_FIB_3GHG_ABC.pdb", "daborhagin-K → fibrinogen Aα", "literature 1.0 (B8K1W0, PMID 18554518)", "AF model (pLDDT 84); HADDOCK: Zn catalytic motif surface + FGA chain C-terminus; ClusPro direct submission"],
    ["P4", "T_snaclecQ38L02_AF.pdb", "H_GP1BA_1M10_A.pdb", "snaclec → GP1BA (inhibits ristocetin-induced aggregation)", "literature 1.0 (Q38L02)", "AF model (pLDDT 88.9); GP1BA passive residues defined from template 1M10 (VWF-A1 binding site)"],
    ["P5", "T_PLA2_1KPM_A.pdb", "H_FXa_2W26_AB.pdb", "PLA2 VRV-PL-VIIIa → FXa (anticoagulant IC50=130nM)", "literature 1.0 (P59071, PMID 18062812)", "PLA2 interface region (non-catalytic-site binding) + FXa surface exosite"],
    ["P6", "T_KunitzH6VC06_AF.pdb", "H_PLG_1QRZ_A.pdb", "Kunitz → plasmin (Ki=0.19nM)", "literature 1.0 (H6VC06)", "AF model (pLDDT 88.6); Kunitz reactive-loop P1 residue vs PLG catalytic triad (His603/Asp646/Ser741)"],
    ["P7", "T_svVEGF_1WQ9_AB.pdb", "H_VEGFR2_3V2A_R.pdb", "svVEGF → VEGFR2/KDR", "literature 1.0 (P67861)", "template reference 3V2A chain A (VEGF-A) binding pose; HDock template docking optional"],
]
with open(os.path.join(DST, "..", "docking_pairs.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["pair_id", "toxin(ligand)", "host_target(receptor)", "biological_proposition", "L2_evidence", "HADDOCK/ClusPro_submission_notes"])
    w.writerows(pairs)
print("\ndocking_pairs.csv: 7 pairs")
