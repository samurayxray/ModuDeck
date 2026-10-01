$fn=24;
// Concept mm: componenti e tolleranze da definire.
$fn=40;
difference(){cube([320,230,40]);translate([4,4,3])cube([312,222,40]);for(x=[12,308])for(y=[12,218])translate([x,y,-1])cylinder(h=42,r=2);for(x=[60,140,220])translate([x,225,7])cube([30,8,12]);}
