// Concept only. Provisional dimensions in mm.
$fn=32;
cube([90,65,20]);for(x=[-30,120])for(y=[-15,80])translate([x,y,10]){cube([30,12,6]);translate([15,6,6])cylinder(h=3,r=22);}
