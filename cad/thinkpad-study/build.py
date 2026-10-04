from pathlib import Path
import subprocess, json, zipfile
root=Path(__file__).parent
parts=root/'cad/parts'
common='''// ModuDeck donor chassis study: NOT a verified ThinkPad fit.
// Millimetres. 370x240 is an unconfirmed owner measurement.
$fn=32; W=370; D=240; t=3;
module plate(w,d,h){cube([w,d,h]);}
module shell(w,d,h){difference(){cube([w,d,h]);translate([t,t,t])cube([w-2*t,d-2*t,h]);}}
module hole(x,y,h){translate([x,y,-1])cylinder(d=3.4,h=h+2);}
module rail(n){difference(){cube([n,12,6]);for(x=[10:20:n-10])hole(x,6,6);}}
module rear(){difference(){cube([W-6,3,25]);translate([W/2-23,-1,6])cube([40,5,14]);for(x=[10,W-16])translate([x,-1,12])rotate([-90,0,0])cylinder(d=3.4,h=5);}}
module tray(){difference(){shell(W,D,30);translate([3,D-4,3])cube([W-6,6,27]);for(x=[15,W-15],y=[15,D-15])hole(x,y,30);}}
'''
designs=[
('01-pc-lower-shell','shell(W,D,35);',1,'Main donor enclosure; board holes and ventilation still to measure'),
('02-top-deck-blank','plate(W,D,3);',1,'Blank deck; keyboard and touchpad cutouts intentionally pending'),
('03-display-back','shell(W,225,12);',1,'Provisional display housing; panel dimensions pending'),
('04-display-frame','difference(){cube([W,225,3]);translate([12,12,-1])cube([W-24,201,5]);}',1,'Provisional frame; active display area not measured'),
('05-keyboard-mount-rail','rail(160);',2,'Adjustable mounting rail; keyboard support to measure'),
('06-touchpad-support','difference(){cube([110,80,3]);for(x=[8,102],y=[8,72])hole(x,y,3);}',1,'Generic touchpad platform; original module fit pending'),
('07-board-mount-rail','rail(160);',2,'Generic rail; retain original mounting pattern after measurement'),
('08-board-standoff','difference(){cylinder(d=10,h=8);translate([0,0,-1])cylinder(d=3.4,h=10);}',8,'Generic spacer; quantity and height pending'),
('09-empty-tray-lower','tray();',1,'Empty bottom layer'),
('10-empty-tray-middle','tray();',1,'Empty middle layer'),
('11-empty-tray-upper','tray();',1,'Empty top layer'),
('12-rear-cable-panel','rear();',3,'Rear removable cable opening; fasteners require mating features'),
('13-alignment-guide','difference(){cube([20,12,6]);hole(10,6,6);}',12,'Separate alignment block; mating seats to adapt'),
('14-cable-clamp','difference(){cube([24,14,10]);translate([7,-1,3])cube([10,16,8]);hole(3.5,7,10);hole(20.5,7,10);}',4,'Cable saddle; cable diameter to confirm'),
('15-foot','difference(){cylinder(d=22,h=10);translate([0,0,-1])cylinder(d=3.4,h=12);}',4,'Foot requires rubber pad'),
('16-side-joining-tab','difference(){cube([35,4,45]);for(z=[10,35])translate([17.5,-1,z])rotate([-90,0,0])cylinder(d=3.4,h=6);}',12,'External join tab; mating hole positions pending'),
('17-handle','difference(){cube([120,18,30]);translate([12,-1,8])cube([96,20,23]);for(x=[6,114])hole(x,9,30);}',1,'Concept carry grip; NOT load tested'),
('18-hinge-mount-block','difference(){cube([40,20,12]);hole(8,10,12);hole(32,10,12);}',2,'Mount blank for original metal hinges; drilling to measure')]
manifest=[]
for name,code,qty,note in designs:
    source=parts/(name+'.scad');source.write_text(common+code+'\n')
    result=subprocess.run(['openscad','-o',str(parts/(name+'.stl')),str(source)],capture_output=True,text=True)
    if result.returncode: raise RuntimeError(name+result.stderr)
    manifest.append(dict(name=name,quantity=qty,price=0,note=note))
(root/'parts.json').write_text(json.dumps(manifest,indent=2))
readme='''# ModuDeck: ThinkPad donor study

18 separate parametric OpenSCAD parts and matching STL meshes. This is a preliminary layout, NOT print-ready donor-specific CAD. No phone or drone. Three empty trays. Printed price fields are numeric 0 at the owner's request.

Envelope: 370 x 240 mm, supplied by owner but not confirmed as closed-laptop measurements. Screen size, deck openings, cooling clearance, port openings, component holes, tray mating features and connector mounting remain unmeasured. DO NOT print the whole set before checking these. Solid deck is a blank, not a working keyboard opening. Tray through-holes are provisional; rear panel and alignment-block mating features still need adaptation. Carry handle is not load tested.

Reuse original motherboard, screen cable, keyboard/touchpad cables, cooling assembly and metal hinges as a connected donor set. Do not assume keyboard/touchpad are USB. Keep original cooling intact. Adapter and donor operation are unverified. No electrical rebuild is specified here.

Large enclosure parts exceed many hobby printer beds; splitting with properly designed joints is a pending task. First print a small fit coupon after measuring hardware. This study provides separate parts, not fabrication certification.

Rebuild: `python3 build.py` (OpenSCAD required).

## Parts

'''
for p in manifest:readme+=f"- {p['name']}: {p['quantity']} pcs; price 0. {p['note']}.\n"
(root/'README.md').write_text(readme)
with zipfile.ZipFile(root/'ModuDeck-ThinkPad-parts.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in root.rglob('*'):
        if p.is_file() and p.suffix!='.zip':z.write(p,p.relative_to(root))
print(json.dumps({'parts':len(manifest),'stl':len(list(parts.glob('*.stl')))}))
