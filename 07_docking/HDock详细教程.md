# HDock 详细教程（Phase 5B · P7 svVEGF → VEGFR2 模板对接）

日期：2026-09-28 ｜ 平台：http://hdock.phys.hust.edu.cn/ （华中科技大学，免费学术使用）
适用：P7（svVEGF × VEGFR2）——有同源复合体模板 3V2A（VEGF-A × VEGFR2），HDock 的**模板对接**正适合这种情形。
也可作为 P4/P5 的第三方盲对接交叉验证（可选，方法相同、不填模板即可）。

## 0. 本教程特有的准备（已替你算好）

从 3V2A 晶体复合体实测的界面残基（5 Å 接触阈值），用于"结合位点残基"栏：

- **受体 VEGFR2（R 链，132–329）界面残基 26 个**（照抄进受体结合位点栏）：
  `133,135,137,195,196,215,216,217,218,219,220,221,253,254,255,256,257,258,273,274,275,276,288,311,312,313`
- 配体侧 svVEGF 与 VEGF-A 为同源蛋白但编号不同，**配体结合位点栏留空**，由模板比对自动处理（手动映射易错，不如交给服务器）；
- 模板 = **3V2A**，由服务器混合算法**自动匹配**（页面无模板填写栏；只要 "Template-free docking only" 不勾选即可）。我们的受体就是 3V2A R 链本身、配体与 A 链 VEGF-A 同源，模板命中是大概率事件；
- 完整 3V2A 已存 `prepared/3V2A_full.pdb`（R 链 132–329 = VEGFR2 D2 域；A 链 13–107 = VEGF-A），供最后 PyMOL 叠合验证用。

## 1. 提交步骤

1. 打开 http://hdock.phys.hust.edu.cn/ ，右上角可注册账号（保留历史记录）；**不注册也能跑**（留邮箱收通知即可）；
2. 进入 **Docking** 页面，Docking type 选 **Protein–protein**（默认）；
3. **Input Receptor**：选 Upload，上传 `07_docking/prepared/H_VEGFR2_3V2A_R.pdb`；
4. **Input Ligand**：选 Upload，上传 `07_docking/prepared/T_svVEGF_1WQ9_AB.pdb`（svVEGF 同源二聚体，整文件上传）；
5. 展开 **Advanced Options (Optional)**（按真实界面逐项）：
   - **Template-free docking only**：⚠️ **不要勾**！本页面没有单独的模板 PDB 填写栏——HDOCK 的混合算法会自动在模板库中匹配同源模板（本体系的受体就是 3V2A R 链、配体与 VEGF-A 同源，3V2A 会被自动用作模板）；勾选此项会退化为纯盲对接；
   - Symmetric multimer docking：留空；
   - SAXS experimental data file：留空；
   - 点开 **"▸ Specify the residues of the binding site"**：**受体栏**粘贴 §0 的 26 个残基号（逗号分隔）；**配体栏留空**（配体侧由模板比对自动处理）；
6. 邮箱已填则核对无误 → Jobname 填 `P7_svVEGF_VEGFR2` → **Submit**，记录返回的 **Job ID / 结果页 URL**（截图存档）。

## 2. 等待与取结果

- 单对通常 **1–3 小时**（队列波动），完成有邮件；
- 结果页给出 Top10/Top100 模型，每个含 **Docking score**（越负越好）与 **Confidence score**：
  - **> 0.7 = 高置信**；0.5–0.7 = 中等；< 0.5 = 低置信（不作支持证据）；
- 若用了模板，还会给出与模板的 **ligand RMSD**（< 10 Å 说明姿态与 VEGF-A 模板一致）；
- 下载 **Model 1**（排名第一模型）PDB，存 `07_docking/results/hdock/P7/model1.pdb`。

## 3. 质控（PyMOL，3 分钟）

```
load results/hdock/P7/model1.pdb, model
load prepared/3V2A_full.pdb, template
super model and resn+chain *, template and chain R   # 或直接 align 按受体链叠合
```
肉眼核对：模型中 svVEGF 是否落在 VEGFR2 D2 域的**同一结合面**（即 3V2A 中 VEGF-A 的位置）。姿态一致 + ligand RMSD < 10 Å = 模板对接可信。

## 4. 判定与回填

- **判定（对接指南 §4 同标准）**：Confidence score > 0.7 且姿态覆盖 §0 界面残基区 = 结构层面支持 P7；
- 回填给我：Docking score、Confidence score、ligand RMSD、model1.pdb 存放确认；
- 我汇总进 `docking_results.csv`、`Phase5_报告.md`、Excel（v16），并出 P7 复合体面板。

## 5. 常见问题

| 症状 | 处理 |
|---|---|
| 模板映射失败/报序列比对错误 | 勾选 "Template-free docking only" 重跑纯盲对接（结合位点残基约束仍保留），结果照常用，解读时注明 |
| 结果页打不开/超时 | HDock 结果保留约 2 周，错峰访问；记下 Job ID 可从主页 "Retrieve" 找回 |
| 想顺便验证 P4/P5 | 同一流程传对应文件、不填模板即可（P4 受体 H_GP1BA_1M10_A.pdb / 配体 T_snaclecQ38L02_AF.pdb；P5 受体 H_FXa_2W26_AB.pdb / 配体 T_PLA2_1KPM_A.pdb） |
| 排队超过 24 h | 正常（公共服务器），先推进 ClusPro/HADDOCK 线 |

## 6. 引用（写入 Methods）

Yan Y, Tao H, He J, Huang SY. The HDOCK server for integrated protein–protein docking. *Nat Protoc* 2020;15:1829–1852.
