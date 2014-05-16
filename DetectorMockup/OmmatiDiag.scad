// Mockup of OmmatiDiag
/*
 * The mockup was done after the first crude drawing with
 * [Tinkrecad](https://tinkercad.com/things/3utMiKsZhx9) proved to be too
 * inflexible.
 * The basic unit of the detecotor will be the scintillator size, which we
 * chose to be 17" x 17" translating to 430 x 430 mm in SI units.
*/

// Basic length variables [mm]
length = 430;
padding = 20;
height = 100;



// Housing
module Housing()
  color ("gray", 0.618) {
    // box bottom
    cube([length + padding, length + padding,1]);
    // box back walls
    cube([length + padding, 1, height]);
    cube([1, length + padding, height]);
    }

    // box front walls, can (and should be turned off for increased visibility)
    /*
    color ("gray", 0.6) {
      translate(v = [0, length + padding, 0]) {
        cube([length + padding, 1, height]);
      }
      translate(v = [length + padding, 0, 0]) {
        cube([1, length + padding, height]); //
      }
    }
    */

//Housing();

// Scintillator
module Scintillator()
  translate(v = [padding/2, padding/2, 1]) {
    color ("green", 0.25) {
      cube([length,length,1]);
      }
    }
//~ Scintillator();

// Ommatidium
module Ommatidium() {
  // FOV of one Ommatidium
  FOVSize = ([430/4, 430/3]);
  module FOV()
    color("pink",0.5) cube([FOVSize[0], FOVSize[1], 1], center=true);

  // CMOS (Aptina AR0130)
  CMOSSize = ([1280,960]);
  pixelsize = 3.75 / 1000; // [um]
  module CMOS()
    color ("blue", 0.618) cube([CMOSSize[0] * pixelsize ,CMOSSize[1] * pixelsize, 0.5], center=true);
  translate ([0,0,0]) CMOS();

  // FOV CMOS
  d_cmos_lens = 5;
  d_lens_scintillator = 20;
  module CMOSCone()
      color("green",0.5) cylinder(h = d_cmos_lens, r1 = CMOSSize[0] * pixelsize / 2 , r2 = lensdiameter * 2, center=true);
  module CMOSCross() {
    color("red", 1) polyhedron(
      points=[ [0, 0, 0], //origin
        [-CMOSSize[0]*pixelsize/2, 0, d_cmos_lens],                 // horizontal_1
        [CMOSSize[0]*pixelsize/2, 0,d_cmos_lens], // horizontal_2
        [0, -CMOSSize[1] * pixelsize / 2,d_cmos_lens],                    // vertical_1
        [0,  CMOSSize[1] * pixelsize / 2,d_cmos_lens]],  // vertical_2
      triangles=[[0,1,2], [0,3,4]]);
    }

  mirror([0,0,1]) translate([0,0,-d_cmos_lens])CMOSCross();
  translate([0,0,d_cmos_lens/2])CMOSCone();

  // Lens (http://is.gd/4H9sZf)
  lensdiameter = 2;
  module Lens()
    // the lens is a squashed sphere which we translate to the middle of the CMOS
      scale([2,2,0.5]) sphere(lensdiameter, $fn=50, center=true);
  translate([0, 0, d_cmos_lens]) Lens();

  // FOV Lens
  module LensCone()
    color("green",0.5) cylinder(h = d_lens_scintillator, r1 = lensdiameter * 2 , r2 = FOVSize[1]/2);
  module LensCross() {
    color("red", 1) polyhedron(
      points=[ [0, 0, 0], //origin
        [-FOVSize[0]/2, 0, d_lens_scintillator],   // horizontal_1
        [FOVSize[0]/2, 0,d_lens_scintillator],     // horizontal_2
        [0, -FOVSize[1]/2 ,d_lens_scintillator],   // vertical_1
        [0,  FOVSize[1]/2 ,d_lens_scintillator]],  // vertical_2
      triangles=[[0,1,2], [0,3,4]]);
    }
  translate([0,0,d_cmos_lens]) LensCross();
  translate([0,0,d_cmos_lens]) LensCone();
  translate([0,0,d_cmos_lens + d_lens_scintillator]) FOV();
}

Ommatidium();
