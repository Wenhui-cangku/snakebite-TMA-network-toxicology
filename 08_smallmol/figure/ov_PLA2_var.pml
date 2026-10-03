# Overview: varespladib x PLA2 - whole protein view (template-style left panel)
reinitialize
load PLA2_varespladib_scene.pdb, complex
bg_color white
set ray_opaque_background, 1
hide everything
show cartoon, complex and polymer
color gray90, complex and polymer
set cartoon_transparency, 0.35
select ligand, resn LIG
show sticks, ligand
color tv_green, ligand
set stick_radius, 0.35, ligand
select cat, resi 48+49
show sticks, cat
color yellow, cat
set stick_radius, 0.25, cat
set cartoon_fancy_helices, 1
orient complex
zoom complex, 8
set ray_shadows, 0
set antialias, 2
ray 1200, 1200
png ov_PLA2_var.png, dpi=300
quit
