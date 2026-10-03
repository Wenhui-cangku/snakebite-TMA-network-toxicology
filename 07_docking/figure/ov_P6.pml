# Overview: P6 Kunitz x Plasmin - full complex view (template-style left panel)
reinitialize
load p6_cluster1_1.pdb, cplx
bg_color white
set ray_opaque_background, 1
hide everything
show cartoon, cplx and chain B
color gray90, cplx and chain B
set cartoon_transparency, 0.35, cplx and chain B
show cartoon, cplx and chain A
color forest, cplx and chain A
select triad, cplx and chain B and resi 603+646+741
show sticks, triad
color yellow, triad
set stick_radius, 0.25, triad
select rloop, cplx and chain A and resi 38-42
show sticks, rloop
color tv_red, rloop
set stick_radius, 0.25, rloop
set cartoon_fancy_helices, 1
orient cplx
turn y, -25
turn z, 15
zoom cplx, 3
set ray_shadows, 0
set antialias, 2
ray 1200, 1200
png ov_P6.png, dpi=300
quit
