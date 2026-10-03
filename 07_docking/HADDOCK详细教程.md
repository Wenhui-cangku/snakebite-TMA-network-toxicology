# HADDOCK 2.4 网页版详细教程（Phase 5B · 带生化约束对接）

日期：2026-09-28 ｜ 适用范围：P1 / P2 / P3 / P6 四对（有明确催化/切割位点约束）
P4 / P5 / P7 无明确催化残基约束，以 ClusPro 盲对接为主（见 `对接提交指南.md` §1、§3），本教程不涉及。

**上传文件已全部备好**：`07_docking/prepared/haddock/` 下 8 个文件，命名即配对，直接上传即可，不要再改动。
所有活性残基号均已用脚本从 PDB 文件实测核对（非 UniProt 编号），可直接照抄。

---

## 1. 注册账号（今天就做，审核要 1–2 天）

1. 打开 https://wenmr.science.uu.nl/haddock2.4/
2. 点 **Register**：填姓名、单位、邮箱，建议绑定 ORCID（无 ORCID 可先在 https://orcid.org 免费注册，5 分钟）；
3. 用途一栏写学术用途（如 "protein-protein docking for snake venom toxin–host target interaction study"）；
4. 提交后等人工审核邮件（通常 1–2 个工作日），审核通过才能提交任务。

> ⏰ **时间提示**：注册审核是本阶段唯一"卡住就全停"的环节，务必最先做。审核期间可并行跑 ClusPro（无需审核）。

## 2. 总体流程

```
登录 → Submit a new job → 界面级别选 guru
→ Molecule 1 = 毒素（配体）→ 填活性残基
→ Molecule 2 = 宿主（受体）→ 填活性残基
→ 被动残基勾自动 → 采样参数保持默认 → 提交
→ 邮件通知（数小时–1 天）→ 结果页下载 cluster1 top1
```

## 3. 逐步操作

### Step 1 进入提交页
登录后顶部菜单 **Submit** → "HADDOCK2.4 submission"。界面级别（Interface level）选 **guru**（只有 guru/expert 才能手动填活性残基；easy 界面不行）。

> 首次选 guru 会跳转**权限申请页**（"restricted to users with certain attributes"）：下拉框选 Guru，Description 栏粘贴以下文字（416/550 字符、59 词），Submit 后等人工审核邮件（1–2 个工作日）：
> ```
> We study interactions between Russell's viper (Daboia russelii) venom toxins and human coagulation proteins (factor Xa, factor V, fibrinogen, plasminogen). Known catalytic residues (SVMP zinc motif, SVSP catalytic triad, Kunitz reactive loop) and cleavage sites will be used as active/passive residue restraints to guide docking. Guru access is needed to define these residues manually. Academic use only. Thank you.
> ```

### Step 2 填写 Molecule 1（毒素）
- ⚠️ **页面是三页向导式**（Input data → Input parameters → Docking parameters），**必须每页填完点底部 Next 解锁下一页**，直接点顶部 Tab 会报 "No data have been found from previous step(s)"；
- **Which chain of the structure must be used?**：选 **All**（P1 三聚体整文件提交；残基 145–155 只有 A 链有，已核实无歧义）；
- **Molecule 1 PDB file**：上传 `prepared/haddock/PX_T_*.pdb`；Kind 选 "Protein or Protein-Ligand"；coarse-grain / cyclic / Fix at it0 / 末端带电 **全部保持关闭**；Segment ID 保持默认；
- **Active residues**（在第 2 页 "Input parameters" 的 "Active/Passive residues – Selection #1" 折叠区）：按 §4 速查表照抄，逗号分隔，例如 `145,146,149,155`；
- **Passive residues**：留空，并勾选 ☑ **"Define passive residues automatically around the active residues"**（让服务器自动取活性残基周围的表面邻居）；
- 其余（Histidine protonation、Semi-flexible、Fully-flexible、EM restraints）保持默认，服务器自动处理。

### Step 3 填写 Molecule 2（宿主）
同 Step 2（Selection #2 折叠区），上传 `P1_H_FXa_A.pdb` 等宿主文件，填宿主侧活性残基。

### Step 4 运行参数（全部保持默认）
- Sampling：it0（刚性对接）= 1000、it1（半柔性精修）= 200、water（水合精修）= 200 —— **默认值即可，不要改**；
- 二硫键：服务器自动检测，不用管；
- 高级约束（ambig restraints / tbl 文件）：留空，我们用不上。

### Step 5 提交与等待
- 提交后记录 **Job ID 和结果页 URL**（截图存 `results/haddock/` 也行）；
- 4 对可**全部并行提交**，互不排队冲突（共享账号队列，但每对独立返回）；
- 每对通常数小时–1 天，完成有邮件通知。

### Step 6 下载结果
结果页按 cluster 排名（cluster 1 = 最优）。下载：
- **cluster1 的 top1 结构**（文件名形如 `cluster1_1.pdb`）；
- 页面上的统计：cluster1 的 **HADDOCK score**、**cluster size**、**Z-score**。

存放到 `07_docking/results/haddock/P1/`（P2、P3、P6 同理，文件夹不存在就新建）。

## 4. 四对参数速查表（直接照抄）

### P1　RVV-X → FXa（激活切割命题）
| 项目 | 文件 | 活性残基（照抄） | 依据 |
|---|---|---|---|
| Molecule 1 毒素 | `P1_T_RVVX_noZn.pdb`（三聚体，已去 Zn） | `145,146,149,155` | Zn 催化基序 HELSHNLGMYH（145–155）的催化 His145/Glu146/His149 + 配位 His155，已实测 |
| Molecule 2 宿主 | `P1_H_FXa_A.pdb`（仅 A 链） | `16,17,18,19,20,21` | 重链 N 端 IVGGQE…，即**激活切割产生的新 N 端** |

> ⚠️ **编号陷阱（已替你踩过）**：2W26 用**糜蛋白酶编号**，不是 UniProt 编号。FX 激活切割位点 Arg194–Ile195（成熟 FX 编号）切割后产生的新 N 端就是本文件的 Ile16；文件里的 194/195 是催化区的 Asp194/Ser195，**千万别填**。

### P2　RVV-Vγ → FV（切割 Arg1545–Ser1546 命题）
| 项目 | 文件 | 活性残基（照抄） | 依据 |
|---|---|---|---|
| Molecule 1 毒素 | `P2_T_RVVV.pdb` | `42,193,194,195,196,197` | 催化 His（原 41 号，2026-09-28 重编号后为 **42**）+ GDSGG 基序（193–197，含 Ser195），已实测 |
| Molecule 2 宿主 | `P2_H_FV_B.pdb` | `1543,1544,1545,1546,1547,1548` | 切割位点 Arg1545–Ser1546（已实测 1545=ARG、1546=SER）±2 |

> 注：3S9C 的 B 链本身就是 FV 片段共结晶（直接结构证据），本对接是对全长 FV 的验证补充，结果解读时写明。

### P3　daborhagin-K → 纤维蛋白原 Aα（α-纤溶命题）
| 项目 | 文件 | 活性残基（照抄） | 依据 |
|---|---|---|---|
| Molecule 1 毒素 | `P3_T_daborhaginK.pdb`（AF 模型） | `339,340,343,349` | Zn 催化基序 HEIGHNLGLTH（339–349）催化残基，已实测 |
| Molecule 2 宿主 | `P3_H_FIB_A.pdb`（仅 FGA 链） | `195,196,197,198,199,200` | 结构中 Aα 链 C 端表面（…PSDRQ） |

> ⚠️ **局限（写入论文）**：3GHG 晶体只含 FGA 27–200，真实切割区在 αC 域（约 221–610，结构外）。此处约束用的是结构内最佳代理位置，结果解读为"结合可行性"而非"精确切割位点"。宿主只用 A 链是为了避免与 B/C 链编号重叠导致约束歧义，解读时注明缺失 β/γ 链背景。

### P6　Kunitz → 纤溶酶（Ki = 0.19 nM 抑制命题）
| 项目 | 文件 | 活性残基（照抄） | 依据 |
|---|---|---|---|
| Molecule 1 毒素 | `P6_T_Kunitz.pdb`（AF 模型） | `38,39,40,41,42` | 反应环 31–46（CNLAPESGRCRAHLRR，已实测）的环尖端区，候选 P1 = Arg39/Arg41 |
| Molecule 2 宿主 | `P6_H_PLG_A.pdb` | `603,646,741` | 催化三联体 His603/Asp646/Ser741，已实测 |

> 可选质控：PyMOL 打开 `P6_T_Kunitz.pdb`，执行 `select loop, resi 31-46` → `show surface, loop`，肉眼确认 38–42 在环尖端最暴露处；若发现更靠尖端的残基，拍照记录后微调活性残基列表即可。

## 5. 结果判读（照抄进 Methods 的标准）

| 指标 | 含义 | 通过线 |
|---|---|---|
| HADDOCK score | 加权能项（越低越好） | **≤ −100** |
| Cluster size | 最优簇成员数 | 越大越稳，< 4 提示不可靠 |
| Z-score | 相对随机姿态的显著性 | ≤ −2.0 为佳 |

**判定（与 `对接提交指南.md` §4 一致）**：HADDOCK score ≤ −100 **且** Top1 界面覆盖上表的功能位点（PyMOL 打开 cluster1_1.pdb 肉眼核对）= 结构层面支持该互作。

## 6. 常见问题

| 症状 | 处理 |
|---|---|
| **"multiple chains with overlapping numbering: A7 - B7"** | 已修复（2026-09-28）：`P1_T_RVVX_noZn.pdb` 的 B 链 +1000、C 链 +2000，重新上传同名文件即可 |
| **"multiple residues with number 61 in chain A / duplicated atom names"** | 已修复（2026-09-28）：`P1_H_FXa_A.pdb`、`P2_T_RVVV.pdb` 的插入残基（61A、36A 等）已顺序重编号；P2 毒素活性残基改用新号 `42,193,194,195,196,197`（教程 §4 已更新），其余不变 |
| 提交报 Zn/配体相关错误 | P1 已用去 Zn 版（`P1_T_RVVX_noZn.pdb`），正常不会再报；若仍报，把报错截图发我 |
| 报"残基号不存在/歧义" | 检查是否传错文件（宿主必须用 haddock/ 下的单链版，不要用 prepared/ 根目录的多链版） |
| Cluster size 很小、score 偏高 | 不强行判定阴性；记录实际数值，以 ClusPro 结果为主综合判定（指南 §4） |
| 队列超过 2 天无动静 | 正常现象（公共服务器排队），先跑别的对；超过 5 天可重提 |
| 想改采样数提高精度 | 不建议。默认 it0=1000/it1=200/water=200 是官方验证过的；改了反而难与文献比较 |

## 7. 跑完后回填给我

每对给我 4 样东西（发消息列出来即可）：
1. cluster1 的 HADDOCK score、cluster size、Z-score；
2. `cluster1_1.pdb` 已存到 `results/haddock/PX/` 的确认；
3. PyMOL 肉眼核对结论：界面是否覆盖功能位点（是/否 + 截图更好）；
4. 任何报错或异常。

我来做：汇总 `docking_results.csv`、交叉判定、PyMOL 出 Figure 5 面板、写进 `Phase5_报告.md` 并同步 Excel v14。
