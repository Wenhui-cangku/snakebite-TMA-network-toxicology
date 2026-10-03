# Overview: P7 svVEGF x VEGFR2 - full complex view (for template-style left panel)
reinitialize
load p7_scene.pdb, hdock
load p7_3v2a_template.pdb, tpl
bg_color white
set ray_opaque_background, 1
hide everything
show cartoon, hdock and chain R
color gray90, hdock and chain R
set cartoon_transparency, 0.35, hdock and chain R
show cartoon, hdock and (chain A or chain B)
color tv_blue, hdock and chain A
color cyan, hdock and chain B
show cartoon, tpl and chain A
color orange, tpl and chain A
set cartoon_transparency, 0.55, tpl and chain A
hide everything, tpl and chain R
select ifr, hdock and chain R and resi 133+135+137+195+196+215+216+217+218+219+220+221+253+254+255+256+257+274+311+312+313
show sticks, ifr
color yellow, ifr
set stick_radius, 0.18, ifr
set cartoon_fancy_helices, 1
orient hdock
zoom (hdock | tpl and chain A), 10
set ray_shadows, 0
set antialias, 2
ray 1200, 1200
png ov_P7.png, dpi=300
quit
