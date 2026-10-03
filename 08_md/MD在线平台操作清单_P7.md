# P7 svVEGF×VEGFR2 全原子 MD 操作清单（在线平台）

> 目的：为论文增加真实 MD 层（审核意见第 13 条）。对最关键的 P7 复合物跑全原子 MD，
> 产出 RMSD/RMSF/Rg 轨迹，作为补充材料图 + 正文一句 corroboration。
> 输入文件已备好：`08_md/input/md_P7_fixed_noh.pdb`（376 残基，3063 重原子，已补环）。
> 链 ID：链 A = VEGFR2（198 残基连续），链 B/C = svVEGF 二聚体。

## 平台选择（WebGRO 注册不可用，已实测替代方案）

| 平台 | 地址 | 费用 | 时长上限 | 状态（2026-10-03 实测） | 推荐度 |
|---|---|---|---|---|---|
| **VisualDynamics 3.0** | https://visualdynamics.fiocruz.br | **免费** | 5 ns/次 | 在线 200，Fiocruz 官方运营 | ★★★ 首选 |
| Neurosnap GROMACS | https://neurosnap.ai | 付费 | 自定义 | 在线 200 | ★★ 备选（要 20 ns+ 时） |
| Tamarind Bio GROMACS | https://www.tamarind.bio | 付费 | 微秒级 | 在线 200 | ★ 备选 |
| MDWeb | mdweb.irbbarcelona.org | — | — | 已不可达 | 不可用 |

**首选 VisualDynamics**：BMC Bioinformatics 2023 正式发表（DOI 10.1186/s12859-023-05234-y，130+ 引用），
GROMACS 后端，支持 apoprotein 模式（蛋白–蛋白复合物按 apoprotein 上传即可），
浏览器内直接出 RMSD/RMSF/Rg 图 + 可下载 .xtc/.gro 轨迹。5 ns 虽短，但本研究主动力学证据已由
iMODS edNMA 提供，MD 仅作稳定性抽查，足够回答"pose 是否瞬间散架"。
若要 20 ns 级别，用 Neurosnap（付费）或在 VisualDynamics 跑完 5 ns 后以末帧续跑。

---

## 1. VisualDynamics 注册

1. 打开 https://visualdynamics.fiocruz.br → "Launch App" → 申请账号（Request access）
2. 用机构邮箱（glmu.edu.cn）+ 注明 academic research use
3. 等待批准邮件（Fiocruz 人工审核，一般 1–3 天）

## 2. 提交表单（Apoprotein 模式，逐字段照抄）

| 字段 | 填写 |
|---|---|
| PDB 文件 | 上传 `md_P7_fixed_noh.pdb` |
| Force field | **AMBER94 / AMBER99SB**（列表中有哪个选哪个；勿选 GROMOS 配 PRODRG 的组合） |
| Water model | **TIP3P** |
| Box type | **Cubic / Triclinic**（默认即可） |
| Distance to box edge | 1.0 nm |
| Neutralize | 勾选（自动加 Na⁺/Cl⁻） |
| Ignore hydrogens | 勾选（输入本无氢） |
| 模拟时长 | **5 ns**（上限拉满） |
| Temperature | 300 K |

## 3. 运行与回收

- 每次只能跑一个任务；完成后邮件通知
- 下载：RMSD / RMSF / Rg / SASA 图（网页内直接导出 PNG）+ 轨迹文件
- 结果 zip 放到 `08_md/results_visualdynamics/`

## 4. 结果判读标准（写入论文前自查）

| 指标 | 合格表现 | 含义 |
|---|---|---|
| RMSD | 5 ns 内趋平（±0.1 nm 波动） | 复合物整体稳定 |
| RMSF | 界面残基低于分子均值 | 界面刚性与 iMODS edNMA 互证 |
| Rg | 平稳无持续上升 | 无去折叠/解离 |

若 RMSD 持续爬升 → 如实写 "the pose was not stable over the 5 ns window"，降级该对结论（与 P4 撤回同等诚实标准）。

## 5. 论文接入点（拿到结果后我来写）

- **方法 2.8** 追加：「The P7 complex was subjected to a 5 ns all-atom MD spot-check (VisualDynamics, GROMACS backend, AMBER force field, TIP3P, 300 K).」
- **结果 3.6** 追加 1 句 + **SM** 加 Figure S_MD（RMSD/RMSF/Rg 三联图）
- **局限性**：5 ns 仅稳定性抽查，不替代长程 MD 或自由能计算
- 参考文献追加：Zanchi et al., BMC Bioinformatics 24 (2023) 133, doi:10.1186/s12859-023-05234-y + GROMACS (doi:10.1016/j.softx.2015.06.001)

## 6. 本地保底路线（均不可用/排队过长时）

`08_md/run_md_P7.py`（OpenMM 脚本）已写好，但本机 20 核 CPU 对 17.9 万原子体系仅 ~2–5 ns/day，
跑一次 20 ns 需约一周且期间电脑需不关机——仅在装有 NVIDIA 显卡后再考虑（OpenCL/CUDA 可提速 50–100 倍）。
届时：`python run_md_P7.py smoke` 自检 → `python run_md_P7.py` 长跑（带断点续跑）。


---

## 附录 A. 输入文件预处理记录（✅ 已完成 2026-10-03）

`md_P7_svVEGF_VEGFR2_hdock.pdb` 原始链构成：链 R = VEGFR2（132–329，缺 264–271、278–282 两段 loop），链 A/B = svVEGF 二聚体完整。

**已用 PDBFixer 补环完毕**（UniProt P35968 序列构建 SEQRES，185/185 残基身份核对通过）：
- **`md_P7_fixed_noh.pdb`（3063 重原子，无氢——上传 VisualDynamics 用这个）**
- `md_P7_fixed.pdb`（含氢版 6103 原子，备用）
- 链 ID 已重排：链 A = VEGFR2（198 残基连续），链 B/C = svVEGF 二聚体
- PyMOL 目检通过：补上的 loop 位于 VEGFR2 表面，远离 svVEGF 结合界面
- 预处理脚本：`input/_fix_p7.py`（可复现）

---

## 附录 B. VisualDynamics 提交记录（✅ 2026-10-03 20:15 UTC 提交）

- 平台版本：VisualDynamics **v5.0.9**（注意：与 3.0 版界面不同，无温度/中和选项，MDP 用平台模板自动生成）
- 任务页：https://visualdynamics.fiocruz.br/simulations/657c3177-06f6-4687-834a-dcd4dac7c453
- **Job ID: 525**，Macromolecule 名：mdp7fixednoh，Status: QUEUED → 等待运行
- 表单实际参数：
  | 项 | 值 |
  |---|---|
  | Simulation Type | **Free Protein**（纯蛋白复合物） |
  | PDB | md_P7_fixed_noh.pdb（3063 重原子） |
  | Force Field | **amber99sb-ildn**（AMBER99SB-ILDN，侧链修正版，论文写这个） |
  | Water Model | tip3p |
  | Box Type | cubic |
  | Box Distance | **1.0 nm**（默认 0.1 已改） |
  | 时长 | 固定 5 ns（平台硬性上限） |
- 注意：Commands / MDP Files 预览按钮在提交前处于禁用态，属正常现象，不影响提交
- **取结果**：Status 变 FINISHED 后 → 任务页 Downloads 标签下载 zip → 解压到 `08_md\results_visualdynamics\`
- 论文方法句中的力场描述相应改为 "AMBER99SB-ILDN force field, TIP3P water, cubic box with 1.0 nm solute–box distance"
