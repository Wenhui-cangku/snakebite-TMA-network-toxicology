# Phase 5C (Optional Enhancement): Molecular Dynamics (MD) Simulation SOP

Updated: 2026-09-30 | Corresponding plan item: Figure 6 (MD validation of docking-pose stability)
Nature: **optional enhancement**. Without MD the main conclusions are unaffected (honestly declared in the paper's Limitations); adding it significantly strengthens reviewer persuasiveness.

---

## 0. Compute reality and route selection (choose a route before starting)

| Route | Hardware | Time per 100 ns/complex | Cost | Best for |
|---|---|---|---|---|
| A Cloud GPU (AutoDL etc., RTX 3090/4090) | rent GPU | P7/P4 ~6–12 h; P2 ~1–2 days | ~¥2/h, < ¥200 total | **Recommended** |
| B Local WSL2 + GROMACS (CPU 20 cores) | own machine | P7/P4 ~2–4 days; P2 ~1–2 weeks | ¥0 but ties up the machine | when not in a hurry |
| C Lightweight alternative (browser, same-day results) | none | 5–10 min per complex | ¥0 | **See §7**: iMODS normal-mode analysis + PRODIGY affinity prediction, usable as Figure-6-level evidence |

**4 starting structures prepared locally** (`08_md/input/`, already pure-ATOM, chains normalized, statistics below):

| File | Complex | Atoms | Chains | Notes |
|---|---|---|---|---|
| `md_P2_RVVV_FV_haddock.pdb` | RVV-Vγ×FV (HADDOCK both criteria met) | 15,894 | A=RVV-Vγ(234) B=FV(1374) | B-chain 713→1536 gap = FV B-domain-missing construct, intrinsic to the crystal structure, **normal** |
| `md_P7_svVEGF_VEGFR2_hdock.pdb` | svVEGF×VEGFR2 (HDock 0.897) | 2,870 | A/B=svVEGF dimer, R=VEGFR2(185) | Two small gaps in chain R = crystal missing loops, acceptable |
| `md_P4_snaclec_GP1BA_cluspro.pdb` | snaclec×GP1BA (ClusPro 59-member cluster) | 3,475 | A=GP1BA(505–703) B=snaclec(154) | Smallest; good for a trial run |
| `md_batimastat_RVVX_pose.pdb` | batimastat pose (coordinates only) | 324 | — | Small-molecule MD: see §6 (advanced, optional) |

**Recommended simulation scale**: 3 protein complexes × 100 ns × 1 run each (add 3 replicates if reviewers request).
Priority order: **P7 → P4 → P2** (P7 smallest and most complete evidence chain; P2 largest, last).

---

## 1. Environment setup (routes A/B)

```bash
# Ubuntu 22.04 (cloud image or WSL2)
sudo apt update && sudo apt install -y gromacs mpi-default-bin
gmx --version   # 2022+ is fine; GPU cloud images ship with CUDA acceleration

# Force field: CHARMM36-jul2022 (protein + ions + TIP3P water, full set)
wget https://charmm-gui.org/archive/charmm36/charmm36-jul2022.ff.tgz
tar xzf charmm36-jul2022.ff.tgz   # extract into the working directory
```

## 2. Standard protein-complex workflow (P7 as example; swap filenames for P4/P2)

```bash
MD=~/md/P7; mkdir -p $MD && cd $MD
cp 08_md/input/md_P7_svVEGF_VEGFR2_hdock.pdb complex.pdb

# 1) Topology (-ignh ignores H, rebuilt by the force field; termini default to neutral caps — drop -ter interactivity if unwanted)
gmx pdb2gmx -f complex.pdb -o processed.gro -p topol.top \
    -ff charmm36-jul2022 -water tip3p -ignh

# 2) Box and solvent (complex 1.2 nm from box walls)
gmx editconf -f processed.gro -o boxed.gro -c -d 1.2 -bt dodecahedron
gmx solvate -cp boxed.gro -cs spc216.gro -p topol.top -o solvated.gro

# 3) Ions (0.15 M NaCl physiological concentration, auto-neutralize charge)
gmx grompp -f ions.mdp -c solvated.gro -p topol.top -o ions.tpr
gmx genion -s ions.tpr -p topol.top -pname NA -nname CL \
    -neutral -conc 0.15 -o solv_ions.gro <<< "SOL"

# 4) Energy minimization (converge at 50 kJ/mol/nm)
gmx grompp -f minim.mdp -c solv_ions.gro -p topol.top -o em.tpr
gmx mdrun -deffnm em

# 5) NVT 100 ps → NPT 100 ps (heavy-atom position restraints)
gmx grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr
gmx mdrun -deffnm nvt
gmx grompp -f npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p topol.top -o npt.tpr
gmx mdrun -deffnm npt

# 6) Production 100 ns (2 fs step = 50,000,000 steps; GPU: -nb gpu -pme gpu)
gmx grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top -o md_100ns.tpr
gmx mdrun -deffnm md_100ns -nb gpu -pme gpu -bonded gpu
```

Templates for the five parameter files `ions.mdp / minim.mdp / nvt.mdp / npt.mdp / md.mdp` are in `08_md/mdp/` (attached in this directory).

## 3. Analysis commands (run after each simulation finishes)

```bash
# PBC correction (do this first, otherwise RMSD artifacts)
gmx trjconv -s md_100ns.tpr -f md_100ns.xtc -o md_nojump.xtc -pbc nojump <<< "System"
gmx trjconv -s md_100ns.tpr -f md_nojump.xtc -o md_center.xtc -pbc mol -center -ur compact <<< "Protein / System"

# RMSD (complex backbone vs starting conformation)
gmx rms -s md_100ns.tpr -f md_center.xtc -o rmsd.xvg -tu ns <<< "Backbone / Backbone"
# RMSF (per-chain interface flexibility)
gmx rmsf -s md_100ns.tpr -f md_center.xtc -o rmsf.xvg -res <<< "Backbone"
# Radius of gyration
gmx gyrate -s md_100ns.tpr -f md_center.xtc -o rg.xvg <<< "Protein"
# Interface hydrogen-bond count (between chains A/B or A/R)
gmx hbond -s md_100ns.tpr -f md_center.xtc -num hbond.xvg <<< "chain_A / chain_B"
# Key interface residue distances (e.g. P2 cleavage site 1543-1548 to the RVV-Vγ catalytic region)
gmx distance -s md_100ns.tpr -f md_center.xtc -oav keydist.xvg -select '...'
```

## 4. MM-GBSA binding free energy (gmx_MMPBSA)

```bash
pip install gmx_MMPBSA  # requires python 3.9-3.11
# mmpbsa.in template at 08_md/mdp/mmpbsa.in (GB OBC2, salt 0.15 M, equilibrated segment 50–100 ns, every 10 frames)
mpirun -np 10 gmx_MMPBSA -O -i mmpbsa.in -cs md_100ns.tpr -ct md_center.xtc \
    -ci index.ndx -cg 1 2 -cp topol.top -o FINAL_RESULTS.dat
```
Interpretation: ΔG_bind < −20 kcal/mol and stable over the equilibrated segment → strong support; −10 to −20 → moderate support; > −10 or contradicting docking ranks → honestly state "not supported at the free-energy level".

## 5. Suggested Figure 6 layout (4 panels)

| Panel | Content | Data source |
|---|---|---|
| A | RMSD curves of the 3 complexes (100 ns, plateau judgement) | rmsd.xvg |
| B | P7 RMSF per residue (low flexibility at interface residues = stable) | rmsf.xvg + interface list coloring |
| C | Interface H-bond count over time (P2/P4/P7, three lines) | hbond.xvg |
| D | MM-GBSA ΔG bar chart (complex × energy decomposition) | FINAL_RESULTS.dat |

Plotting scripts can reuse the matplotlib style of `04_network/robustness_analysis.py` (`setup_plot()` + 300 dpi + SVG).

## 6. Small-molecule MD (optional, advanced)

batimastat×RVV-X (crystal contains catalytic Zn²⁺):
- Ligand topology: upload `md_batimastat_RVVX_pose.pdb` to the CGenFF server (https://cgenff.com) to get `.str`, convert with `cgenff_charmm2gmx.py` into a GROMACS topology and merge into topol.top;
- **Zn²⁺ must use a bonded model** (Zn-His/Glu coordination distance restraints, or parameters generated by MCPB.py) — with a non-bonded model the Zn will drift; if this layer cannot be done properly, better not to do it: docking + chelation geometry already suffice for the small-molecule layer in the paper.

## 7. Route C: lightweight alternative (doable today, browser only)

1. **iMODS normal-mode analysis** (https://imods.iqf.csic.es): upload the complex PDB → get deformability / B-factor / eigenvalue / covariance plots; commonly used in this field as "complex stability" evidence. 5 minutes per complex; archive screenshots;
2. **PRODIGY** (https://wenmr.science.uu.nl/prodigy/): upload the complex PDB → predicted ΔG/Kd; adds an independent affinity-evidence layer for the 7 docking pairs (weaker than MM-GBSA but zero cost).

If time allows, **recommended combination: Route C today for results into the draft (labeled as NMA/prediction-level evidence), Route A as revision or follow-up work** — avoid letting MD delay submission.

## 8. QC checklist

- [ ] EM converged (Fmax < 1000 kJ/mol/nm); density/volume stable after NPT
- [ ] RMSD plateaus in the last 50 ns (drift < 0.05 nm); otherwise extend or check for conformational collapse
- [ ] Interface H-bond count never drops to zero (zero = complex dissociation, conformation not credible — must be reported honestly)
- [ ] MM-GBSA uses the equilibrated segment; energy decomposition inspects key interface-residue contributions
- [ ] All .mdp/.tpr/trajectory files archived; version recorded in the data-management table
