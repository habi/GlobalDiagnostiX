// Scintillator backplate

// Basic length variables
semitransparent = 0.618;
nearlytransparent = 0.309;

CenterSzintillator = [459/2, 380 - 80 - 172/2, 0];

// Toshiba Szintillator
SizeToshiba = [236, 172, 100];
difference(){
	cube([459, 380, 6]);
	translate(CenterSzintillator-SizeToshiba/2){
		cube(SizeToshiba);
	}
}

// Pingseng Szintillator
SizePinseng = [200, 200, 100];
translate([500,0,0]){
	difference(){
		cube([459, 380, 6]);
		translate(CenterSzintillator-SizePinseng/2){
			cube(SizePinseng);
		}
	}
}

// Applied Scintillation Technologies Szintillator
SizeAppScinTech = [106, 106, 100];
translate([1000,0,0]){
	difference(){
		cube([459, 380, 6]);
		translate(CenterSzintillator-SizeAppScinTech/2){
			cube(SizeAppScinTech);
		}
	}
}