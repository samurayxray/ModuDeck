// Concept only. Provisional dimensions in mm.
$fn=32;
difference(){cube([280,3,18]);for(x=[25,65,105,145])translate([x,-1,4])cube([24,5,9]);for(x=[8,272])translate([x,4,9])rotate([90,0,0])cylinder(h=6,r=3);}
