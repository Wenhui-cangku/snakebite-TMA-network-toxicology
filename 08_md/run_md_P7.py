# -*- coding: utf-8 -*-
"""
P7 svVEGF x VEGFR2 all-atom MD (OpenMM, CPU).
Stages: minimize -> NVT 100 ps -> NPT 100 ps -> production 20 ns (2 fs, HBonds).
Outputs: traj.dcd (10 ps/frame), log.csv (every 100 ps), checkpoint (restartable).
Run:  python run_md_P7.py            (full run)
      python run_md_P7.py smoke      (100 minim steps + 1000 NVT steps only)
"""
import os, sys, time
from openmm.app import *
from openmm import *
from openmm.unit import *

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
SMOKE = len(sys.argv) > 1 and sys.argv[1] == "smoke"

PDB_IN = os.path.join("input", "md_P7_fixed_noh.pdb")
OUT_PREFIX = "P7_md"
NS_PROD = 20.0
DT = 0.002 * picoseconds
STEPS_PER_PS = int(1.0 * picoseconds / DT)          # 500
REPORT_PS = 100.0
REPORT_STEPS = int(REPORT_PS * STEPS_PER_PS)         # 50 000
FRAME_PS = 10.0
FRAME_STEPS = int(FRAME_PS * STEPS_PER_PS)           # 5 000

def log(msg):
    print(time.strftime("[%H:%M:%S]"), msg, flush=True)

# ---------- build system ----------
if not os.path.exists("system_built.done"):
    log("loading " + PDB_IN)
    pdb = PDBFile(PDB_IN)
    ff = ForceField("amber14-all.xml", "amber14/tip3pfb.xml")
    modeller = Modeller(pdb.topology, pdb.positions)
    log("adding hydrogens (pH 7.4)")
    modeller.addHydrogens(ff, pH=7.4)
    log("adding solvent box (padding 1.0 nm, 0.15 M NaCl)")
    modeller.addSolvent(ff, model="tip3p", padding=1.0 * nanometer,
                        ionicStrength=0.15 * molar)
    log("atoms total: %d" % modeller.topology.getNumAtoms())
    system = ff.createSystem(modeller.topology, nonbondedMethod=PME,
                             nonbondedCutoff=1.0 * nanometer, constraints=HBonds)
    with open("system.xml", "w") as f:
        f.write(XmlSerializer.serialize(system))
    with open("solvated.pdb", "w") as f:
        PDBFile.writeFile(modeller.topology, modeller.positions, f)
    open("system_built.done", "w").write("ok")
    log("system built and saved")
else:
    log("system exists, reloading")
    system = XmlSerializer.deserialize(open("system.xml").read())
    pdb = PDBFile("solvated.pdb")
    modeller = type("m", (), {"topology": pdb.topology, "positions": pdb.positions})

# ---------- simulation ----------
platform = Platform.getPlatformByName("CPU")
props = {"Threads": str(os.cpu_count())}
integrator = LangevinMiddleIntegrator(300 * kelvin, 1.0 / picosecond, DT)
sim = Simulation(modeller.topology, system, integrator, platform, props)
sim.context.setPositions(modeller.positions)

if os.path.exists(OUT_PREFIX + ".chk"):
    log("resuming from checkpoint")
    sim.loadCheckpoint(OUT_PREFIX + ".chk")
else:
    log("minimizing")
    sim.minimizeEnergy(maxIterations=100 if SMOKE else 5000)
    pos = sim.context.getState(getPositions=True).getPositions()
    with open("minimized.pdb", "w") as f:
        PDBFile.writeFile(modeller.topology, pos, f)
    log("minimized -> minimized.pdb")

    log("NVT equilibration 100 ps")
    sim.context.setVelocitiesToTemperature(300 * kelvin)
    sim.step(1000 if SMOKE else int(100 * STEPS_PER_PS))
    log("NPT equilibration 100 ps")
    if not SMOKE:
        system.addForce(MonteCarloBarostat(1 * bar, 300 * kelvin))
        sim.context.reinitialize(preserveState=True)
        sim.step(int(100 * STEPS_PER_PS))
    log("equilibration done")

if SMOKE:
    e = sim.context.getState(getEnergy=True).getPotentialEnergy()
    log("SMOKE OK, potential = %.1f kJ/mol" % e.value_in_unit(kilojoule_per_mole))
    sys.exit(0)

# ---------- production ----------
sim.reporters.append(DCDReporter(OUT_PREFIX + ".dcd", FRAME_STEPS, append=True))
sim.reporters.append(StateDataReporter(
    OUT_PREFIX + "_log.csv", REPORT_STEPS, step=True, time=True,
    potentialEnergy=True, temperature=True, volume=True, speed=True,
    remainingTime=True, totalSteps=int(NS_PROD * 1000 * STEPS_PER_PS),
    separator=",", append=True))
sim.reporters.append(CheckpointReporter(OUT_PREFIX + ".chk", REPORT_STEPS))

log("production %.0f ns started (frame every %.0f ps)" % (NS_PROD, FRAME_PS))
t0 = time.time()
sim.step(int(NS_PROD * 1000 * STEPS_PER_PS))
log("production done in %.1f h" % ((time.time() - t0) / 3600))
open("production.done", "w").write("ok")
