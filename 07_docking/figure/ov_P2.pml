# Overview: P2 RVV-Vgamma x FV - full complex view (template-style left panel)
reinitialize
load p2_cluster1_1.pdb, cplx
bg_color white
set ray_opaque_background, 1
hide everything
show cartoon, cplx and chain B
color gray90, cplx and chain B
set cartoon_transparency, 0.35, cplx and chain B
show cartoon, cplx and chain A
color marine, cplx and chain A
select cleave, cplx and chain B and resi 1543-1548
show sticks, cleave
color yellow, cleave
set stick_radius, 0.25, cleave
select cat, cplx and chain A and resi 42+195
show sticks, cat
color tv_red, cat
set stick_radius, 0.25, cat
set cartoon_fancy_helices, 1
orient cplx
turn y, -20
zoom cplx, 10
set ray_shadows, 0
set antialias, 2
ray 1200, 1200
png ov_P2.png, dpi=300
quit
