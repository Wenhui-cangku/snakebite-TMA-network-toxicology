# -*- coding: utf-8 -*-
"""
Phase 5A - 结构预处理：按链提取、去水去配体（保留催化 ZN），生成对接配对清单
输出: 07_docking/prepared/*.pdb + docking_pairs.csv
"""
from pathlib import Path
import os

SRC = str(Path(__file__).resolve().parents[1] / "07_docking" / "structures")
DST = str(Path(__file__).resolve().parents[1] / "07_docking" / "prepared")
os.makedirs(DST, exist_ok=True)

# (源文件, 保留链, 保留HET(除HOH), 输出名, 说明)
JOBS = [
    ("2E3X_毒素_RVV-X复合体.pdb", {"A", "B", "C"}, {"ZN"}, "T_RVVX_2E3X_ABC.pdb", "RVV-X 全复合体(重链SVMP+轻链snaclec×2), 保留催化Zn"),
    ("3S9C_毒素_RVV-Vγ+FV片段.pdb", {"A"}, set(), "T_RVVV_3S9C_A.pdb", "RVV-Vγ 催化链(B链为共结晶FV片段=直接结构证据)"),
    ("1KPM_毒素_PLA2_VRV-PL-VIIIa.pdb", {"A"}, set(), "T_PLA2_1KPM_A.pdb", "PLA2 VRV-PL-VIIIa 单拷贝"),
    ("2H4C_毒素_daboiatoxin.pdb", {"A", "B"}, set(), "T_daboiatoxin_2H4C_AB.pdb", "daboiatoxin 异二聚体单拷贝"),
    ("1WQ9_毒素_svVEGF.pdb", {"A", "B"}, set(), "T_svVEGF_1WQ9_AB.pdb", "svVEGF 同源二聚体"),
    ("AF-B8K1W0_daborhagin-K.pdb", {"A"}, set(), "T_daborhaginK_AF.pdb", "daborhagin-K AlphaFold(平均pLDDT 84.0)"),
    ("AF-Q38L02_snaclec.pdb", {"A"}, set(), "T_snaclecQ38L02_AF.pdb", "snaclec Q38L02 AlphaFold(平均pLDDT 88.9)"),
    ("AF-H6VC06_Kunitz.pdb", {"A"}, set(), "T_KunitzH6VC06_AF.pdb", "Kunitz H6VC06 AlphaFold(平均pLDDT 88.6)"),
    ("7KVE_宿主_FV.pdb", {"B"}, set(), "H_FV_7KVE_B.pdb", "人凝血因子V全长(cryoEM 3.3Å)"),
    ("2W26_宿主_FXa.pdb", {"A", "B"}, set(), "H_FXa_2W26_AB.pdb", "人FXa(去利伐沙班RIV)"),
    ("3GHG_宿主_纤维蛋白原.pdb", {"A", "B", "C"}, set(), "H_FIB_3GHG_ABC.pdb", "人纤维蛋白原半体(A=α/FGA,B=β/FGB,C=γ/FGG)"),
    ("1M10_宿主_GP1BA-VWF.pdb", {"A"}, set(), "H_GP1BA_1M10_A.pdb", "GP1BA 胞外段"),
    ("1M10_宿主_GP1BA-VWF.pdb", {"A", "B"}, set(), "H_GP1BA_VWF_1M10_AB.pdb", "GP1BA-VWF A1 复合体(模板)"),
    ("3V2A_宿主_VEGFR2-VEGF.pdb", {"R"}, set(), "H_VEGFR2_3V2A_R.pdb", "VEGFR2/KDR 胞外区"),
    ("1QRZ_宿主_纤溶酶原.pdb", {"A"}, set(), "H_PLG_1QRZ_A.pdb", "纤溶酶原催化域"),
    ("1PPB_宿主_凝血酶.pdb", {"L", "H"}, set(), "H_F2_1PPB_LH.pdb", "凝血酶α(轻+重链)"),
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
    print(f"{out:34s} {len(lines):6d} 行  {note}")

# 配对清单
import csv
pairs = [
    ["P1", "T_RVVX_2E3X_ABC.pdb", "H_FXa_2W26_AB.pdb", "RVV-X → FX (激活切割Arg-Ile)", "literature 1.0 (Q7LZ61/Q4PRD1/Q4PRD2)", "HADDOCK: 毒素Zn催化域HEXXHXXGXXH基序表面+FX重链N端激活肽区(PyMOL核对残基号); ClusPro直接提交"],
    ["P2", "T_RVVV_3S9C_A.pdb", "H_FV_7KVE_B.pdb", "RVV-Vγ → FV (切割Arg1545-Ser1546)", "literature 1.0 (P18965)", "HADDOCK: SVSP催化三联体(His57/Asp102/Ser195 糜蛋白酶编号) + FV Arg1545周围; 注: 3S9C B链已有FV片段共结晶=直接结构证据, 对接作全长验证"],
    ["P3", "T_daborhaginK_AF.pdb", "H_FIB_3GHG_ABC.pdb", "daborhagin-K → 纤维蛋白原Aα", "literature 1.0 (B8K1W0, PMID 18554518)", "AF模型(pLDDT 84); HADDOCK: Zn催化基序表面 + FGA链C端; ClusPro直接提交"],
    ["P4", "T_snaclecQ38L02_AF.pdb", "H_GP1BA_1M10_A.pdb", "snaclec → GP1BA (抑制瑞斯托霉素聚集)", "literature 1.0 (Q38L02)", "AF模型(pLDDT 88.9); 参考模板1M10(VWF-A1结合位点)定义GP1BA被动残基"],
    ["P5", "T_PLA2_1KPM_A.pdb", "H_FXa_2W26_AB.pdb", "PLA2 VRV-PL-VIIIa → FXa (抗凝IC50=130nM)", "literature 1.0 (P59071, PMID 18062812)", "PLA2界面区(非催化位点结合) + FXa表面外位点"],
    ["P6", "T_KunitzH6VC06_AF.pdb", "H_PLG_1QRZ_A.pdb", "Kunitz → 纤溶酶 (Ki=0.19nM)", "literature 1.0 (H6VC06)", "AF模型(pLDDT 88.6); Kunitz反应环P1残基对PLG催化三联体(His603/Asp646/Ser741)"],
    ["P7", "T_svVEGF_1WQ9_AB.pdb", "H_VEGFR2_3V2A_R.pdb", "svVEGF → VEGFR2/KDR", "literature 1.0 (P67861)", "模板参考3V2A A链(VEGF-A)结合姿态; HDock模板对接可选"],
]
with open(os.path.join(DST, "..", "docking_pairs.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["配对ID", "毒素(配体)", "宿主靶点(受体)", "生物学命题", "L2证据", "HADDOCK/ClusPro提交要点"])
    w.writerows(pairs)
print("\ndocking_pairs.csv: 7 对")
