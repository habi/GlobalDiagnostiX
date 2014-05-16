// Box
color ("gray", 0.618) {
	cube([450,450,1]);
	cube([450,1,100]);
	cube([1,450,100]);
	translate(v = [0, 450, 0]) { 
 		cube([450,1,100]);
		}
	}

// Scintillator
translate(v = [15, 15, 1]) { 
	color ("green", 0.25) {
		cube([400,400,1]);
		}
	}

// Optical modules
//color ("brown", 0.618) {
//	cube([12.8,9.6,1]);
//	}
//sphere(d=15);

//cylinder(h = 65, r1 = 430/4, r2 = 430/3, center = false);