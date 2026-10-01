// Concept only. Provisional dimensions in mm.
$fn=32;
difference(){cube([320,230,40]);translate([4,4,3])cube([312,222,40]);for(x=[12,308])for(y=[12,218])translate([x,y,-1])cylinder(h=42,r=2);}
