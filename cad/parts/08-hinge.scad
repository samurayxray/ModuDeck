// Concept only. Provisional dimensions in mm.
$fn=32;
difference(){union(){cube([45,12,3]);translate([0,6,6])rotate([0,90,0])cylinder(h=45,r=5);}translate([-1,6,6])rotate([0,90,0])cylinder(h=47,r=2);}
