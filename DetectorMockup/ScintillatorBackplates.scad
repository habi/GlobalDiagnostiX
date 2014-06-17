// Scintillator backplate

// Basic length variables
CenterSzintillator = [459/2, 380 - 80 - 172/2, 0];
screwheight = 20;
screwradius = 3;

// Toshiba Szintillator
SizeToshiba = [236, 172, 20];
color ("black", 1) {
  translate(CenterSzintillator+SizeToshiba/2+[screwradius+2,-20,-SizeToshiba[2]]){
    cylinder(h = screwheight , r=3);
  }
  translate(CenterSzintillator+SizeToshiba/2+[screwradius+2,-SizeToshiba[1]+20,-13]){
    cylinder(h = screwheight , r=3);
  }
  translate(CenterSzintillator-SizeToshiba/2-[screwradius+2,-20,0]){
    cylinder(h = screwheight , r=3);
  }
  translate(CenterSzintillator-SizeToshiba/2-[screwradius+2,-SizeToshiba[1]+20,0]){
    cylinder(h = screwheight , r=3);
  }
  translate(CenterSzintillator-SizeToshiba/2-[-20,-SizeToshiba[1]-screwradius,0]){
    cylinder(h = screwheight , r=3);
  }
  translate(CenterSzintillator-SizeToshiba/2-[-SizeToshiba[0]+20,-SizeToshiba[1]-screwradius,0]){
    cylinder(h = screwheight , r=3);
  }
}
difference(){
  cube([459, 380, 6]);
  translate(CenterSzintillator-SizeToshiba/2){
    cube(SizeToshiba);
  }
}

// Pingseng Szintillator
SizePinseng = [200, 200, 20];
translate([500,0,0]){
  color ("black", 1) {
    translate(CenterSzintillator+SizePinseng/2+[screwradius+2,-20,-20]){
      cylinder(h = screwheight , r=3);
    }
    translate(CenterSzintillator+SizePinseng/2+[screwradius+2,-SizePinseng[1]+20,-SizePinseng[2]]){
      cylinder(h = screwheight , r=3);
    }
    translate(CenterSzintillator-SizePinseng/2-[screwradius+2,-20,0]){
      cylinder(h = screwheight , r=3);
    }
    translate(CenterSzintillator-SizePinseng/2-[screwradius+2,-SizePinseng[1]+20,0]){
      cylinder(h = screwheight , r=3);
    }
    translate(CenterSzintillator-SizePinseng/2-[-20,-SizePinseng[1]-screwradius,0]){
      cylinder(h = screwheight , r=3);
    }
    translate(CenterSzintillator-SizePinseng/2-[-SizePinseng[0]+20,-SizePinseng[1]-screwradius,0]){
      cylinder(h = screwheight , r=3);
    }
  }
  difference(){
    cube([459, 380, 6]);
    translate(CenterSzintillator-SizePinseng/2){
      cube(SizePinseng);
    }
  }
}

// Applied Scintillation Technologies Szintillator
SizeAppScinTech = [106, 106, 20];
translate([1000,0,0]){
  color ("black", 1) {
    translate(CenterSzintillator+SizeAppScinTech/2+[screwradius+2,-20,-20]){
      cylinder(h = screwheight , r=3);
    }
    translate(CenterSzintillator+SizeAppScinTech/2+[screwradius+2,-SizeAppScinTech[1]+20,-SizeAppScinTech[2]]){
      cylinder(h = screwheight , r=3);
    }
    translate(CenterSzintillator-SizeAppScinTech/2-[screwradius+2,-20,0]){
      cylinder(h = screwheight , r=3);
    }
    translate(CenterSzintillator-SizeAppScinTech/2-[screwradius+2,-SizeAppScinTech[1]+20,0]){
      cylinder(h = screwheight , r=3);
    }
    translate(CenterSzintillator-SizeAppScinTech/2-[-20,-SizeAppScinTech[1]-screwradius,0]){
      cylinder(h = screwheight , r=3);
    }
    translate(CenterSzintillator-SizeAppScinTech/2-[-SizeAppScinTech[0]+20,-SizeAppScinTech[1]-screwradius, 0]){
      cylinder(h = screwheight , r=3);
    }
  }
  difference(){
    cube([459, 380, 6]);
    translate(CenterSzintillator-SizeAppScinTech/2){
      cube(SizeAppScinTech);
    }
  }
}
