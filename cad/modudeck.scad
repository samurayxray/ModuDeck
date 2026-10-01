// ModuDeck concept. Provisional dimensions in mm; not production-ready.
W=320; D=230; gap=12; exploded=true; phone_open=true;
$fn=24;
module box(x,y,z,p=[0,0,0]) {translate(p) cube([x,y,z]);}
module connector(z){color("gold") box(28,9,3,[W/2-14,D-22,z]);}
module floor(z,h){color([.16,.23,.31]) difference(){box(W,D,h,[0,0,z]);box(W-8,D-8,h,[4,4,z+3]); for(x=[12,W-12])for(y=[12,D-12])translate([x,y,z-1]) cylinder(h=h+2,r=2); } connector(z+h); for(x=[12,W-12]) color("silver") translate([x,1,z+h/2]) rotate([90,0,0]) cylinder(h=3,r=4);}
z_storage=0; z_battery=18+(exploded?gap:0); z_drone=z_battery+24+(exploded?gap:0); z_pc=z_drone+40+(exploded?gap:0);
floor(z_storage,18);for(x=[20,115,210]) color([.4,.5,.6]) box(80,110,8,[x,45,z_storage+4]);
floor(z_battery,24);for(x=[18,118,218])color([.25,.45,.3])box(85,170,14,[x,25,z_battery+4]);
floor(z_drone,40);color([.45,.48,.52])box(90,65,20,[115,80,z_drone+4]);for(x=[85,235])for(y=[65,165]){color("gray")box(60,14,7,[x-30,y-7,z_drone+9]);color("black")translate([x,y,z_drone+15])cylinder(h=4,r=24);}
color([.2,.28,.38])box(W,D,18,[0,0,z_pc]);
for(row=[0:4])for(col=[0:13])color([.6,.65,.7])box(17,14,2,[18+col*20,100+row*18,z_pc+18]);
color("black")box(82,48,1,[92,27,z_pc+18]);color("cyan")box(68,32,1,[99,35,z_pc+19]);
color([.35,.4,.45])translate([90,78,z_pc+20])rotate([phone_open?65:0,0,0])box(86,52,2,[0,-52,0]);
for(row=[0:3])for(col=[0:2])color("silver")box(12,10,2,[188+col*15,28+row*13,z_pc+18]);
for(x=[35,75,115,155])color("black")box(24,2,9,[x,D,z_pc+5]);
for(x=[20,W-20]){color("silver")translate([x,D+3,z_pc+10])rotate([90,0,0])cylinder(h=6,r=3);color("black")translate([x,D+4,z_pc+10])cylinder(h=70,r=2);}
color([.18,.24,.31])translate([0,D-4,z_pc+18])rotate([20,0,0])box(W,8,190);
color([.15,.55,.7])translate([0,D-4,z_pc+18])rotate([20,0,0])box(W-16,1,174,[8,-1,8]);
