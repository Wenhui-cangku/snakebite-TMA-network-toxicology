# Figure 5 small-molecule panel: batimastat x RVV-X (2E3X chain A, -7.64 kcal/mol)
# Usage: pymol -cq fig5_smallmol_RVVX_batimastat.pml   (or File > Run Script in PyMOL GUI)
reinitialize
load RVVX_batimastat_scene.pdb, complex
bg_color white
set ray_opaque_background, 1
hide everything
show cartoon, complex and polymer
color gray90, complex and polymer
set cartoon_transparency, 0.3
select ligand, resn LIG
show sticks, ligand
color tv_green, ligand
set stick_radius, 0.25, ligand
select zn, resn ZN
show spheres, zn
color slate, zn
set sphere_scale, 0.45, zn
select cat, resi 145+146+149+155
show sticks, cat
util.cbay cat
set stick_radius, 0.2, cat
distance zn_his, zn, (cat and name NE2), 3.0
distance zn_chelate, zn, ligand, 2.8
set dash_color, gray50, zn_his
set dash_color, red, zn_chelate
set dash_width, 3
set dash_radius, 0.09
set dash_gap, 0.35
hide labels, zn_his
hide labels, zn_chelate
label cat and resn HIS and name CA, "%s%s" % (resn, resi)
label zn, "Zn2+"
set label_size, 15
set label_color, black
set label_position, (0, 0, 2)
orient (ligand | zn | byres (ligand around 8))
zoom (ligand | zn), 6
set ray_shadows, 0
set antialias, 2
ray 1600, 1200
png fig5_smallmol_RVVX_batimastat.png, dpi=300
