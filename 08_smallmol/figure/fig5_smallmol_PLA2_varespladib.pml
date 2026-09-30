reinitialize
load PLA2_varespladib_scene.pdb, complex
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
select cat, resi 48+49
show sticks, cat
util.cbay cat
set stick_radius, 0.2, cat
select pocket, byres (ligand around 4) and polymer
show sticks, pocket
util.cbag pocket
color gray70, pocket and elem C
set stick_radius, 0.15, pocket
distance polar, ligand, polymer, 3.5, mode=2
set dash_color, red, polar
hide labels, polar
label cat and name CA, "%s%s" % (resn, resi)
set dash_width, 3
set dash_radius, 0.09
set dash_gap, 0.35
set label_size, 15
set label_color, black
set label_position, (0, 0, 2)
orient (ligand | byres (ligand around 8))
zoom ligand, 6
set ray_shadows, 0
set antialias, 2
ray 1600, 1200
png fig5_smallmol_PLA2_varespladib.png, dpi=300
