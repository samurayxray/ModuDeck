$fn=24;
difference(){cube([120,20,30]);translate([14,-1,8])cube([92,22,23]);for(x=[7,113])translate([x,21,15])rotate([90,0,0])cylinder(h=22,r=2.5);}
