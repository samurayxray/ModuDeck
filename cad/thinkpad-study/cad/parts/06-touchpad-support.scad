// ModuDeck donor chassis study: NOT a verified ThinkPad fit.
// Millimetres. 370x240 is an unconfirmed owner measurement.
$fn=32; W=370; D=240; t=3;
module plate(w,d,h){cube([w,d,h]);}
module shell(w,d,h){difference(){cube([w,d,h]);translate([t,t,t])cube([w-2*t,d-2*t,h]);}}
module hole(x,y,h){translate([x,y,-1])cylinder(d=3.4,h=h+2);}
module rail(n){difference(){cube([n,12,6]);for(x=[10:20:n-10])hole(x,6,6);}}
module rear(){difference(){cube([W-6,3,25]);translate([W/2-23,-1,6])cube([40,5,14]);for(x=[10,W-16])translate([x,-1,12])rotate([-90,0,0])cylinder(d=3.4,h=5);}}
module tray(){difference(){shell(W,D,30);translate([3,D-4,3])cube([W-6,6,27]);for(x=[15,W-15],y=[15,D-15])hole(x,y,30);}}
difference(){cube([110,80,3]);for(x=[8,102],y=[8,72])hole(x,y,3);}
