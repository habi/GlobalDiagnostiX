// Mockup of OmmatiDiag
/*
 * The mockup was done after the first crude drawing with
 * [Tinkrecad](https://tinkercad.com/things/3utMiKsZhx9) proved to be too
 * inflexible.
 * The basic unit of the detecotor will be the scintillator size, which we
 * chose to be 17" x 17" translating to 430 x 430 mm in SI units.
*/

// Basic length variables [mm]
unitlength = 430;
padding = 20;
height = 100;
semitransparent = 0.618;
nearlytransparent = 0.25;

// Housing
module Housing()
  color ("gray", semitransparent) {
    // box bottom
    cube([unitlength + padding, unitlength + padding,1]);
    // box back walls
    cube([unitlength + padding, 1, height]);
    cube([1, unitlength + padding, height]);
    }
    // box front walls, can (and should be turned off for increased visibility)
    //~ color ("gray", 0.6) {
      //~ translate(v = [0, unitlength + padding, 0]) {
        //~ cube([unitlength + padding, 1, height]);
      //~ }
      //~ translate(v = [unitlength + padding, 0, 0]) {
        //~ cube([1, unitlength + padding, height]); //
      //~ }
    //~ }
Housing();

// Scintillator
module Scintillator()
  translate([padding/2, padding/2, 1]) {
    color ("green", 1) {
      cube([unitlength,unitlength,1]);
      }
    }
Scintillator();

// Ommatidium
module Ommatidium() {
  // FOV of one Ommatidium
  FOVSize = ([unitlength/4, unitlength/3]);
  module FOV()
    color("pink",0.5) cube([FOVSize[0], FOVSize[1], 1], center=true);

  // CMOS (Aptina AR0130)
  CMOSSize = ([1280, 960]);
  pixelsize = 3.75 / 1000; // [um]
  module CMOS()
    color ("blue", semitransparent)
    cube([CMOSSize[0] * pixelsize, CMOSSize[1] * pixelsize, 0.5], center=true);
  translate ([0,0,0]) CMOS();

  // FOV CMOS
  d_cmos_lens = 15;
  d_lens_scintillator = height - d_cmos_lens - 15;
  module CMOSCone()
      color("orange",nearlytransparent)
      cylinder(h = d_cmos_lens,
                r1 = CMOSSize[0] * pixelsize / 2 ,
                r2 = lensdiameter * 2, center=true);
  module CMOSCross() {
    color("red", 1) polyhedron(
      points=[ [0, 0, 0], //origin
        [-CMOSSize[0]*pixelsize/2, 0, d_cmos_lens],     // horizontal_1
        [CMOSSize[0]*pixelsize/2, 0,d_cmos_lens],       // horizontal_2
        [0, -CMOSSize[1] * pixelsize / 2,d_cmos_lens],  // vertical_1
        [0,  CMOSSize[1] * pixelsize / 2,d_cmos_lens]], // vertical_2
      triangles=[[0,1,2], [0,3,4]]);
    }

  mirror([0,0,1]) translate([0,0,-d_cmos_lens])CMOSCross();
  translate([0,0,d_cmos_lens/2])CMOSCone();

  // Lens
  lensdiameter = 4;
  module Lens()
    // the lens is a squashed sphere: http://is.gd/4H9sZf
      scale([2,2,0.5]) sphere(lensdiameter, $fn=50, center=true);
  translate([0, 0, d_cmos_lens]) Lens();

  // FOV Lens
  module LensCone()
    color("orange",nearlytransparent)
    scale([1, 4/3, 1])
    cylinder(h = d_lens_scintillator,
              r1 = lensdiameter * 2,
              r2 = FOVSize[1]/2 * 1.2);
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

translate([unitlength/4/2 + padding/2, unitlength/3/2 + padding/2, height-14])
mirror([0,0,1])
for (xpos=[0:3], ypos = [0:2]) // iterate over x and y
  translate([xpos*unitlength/4, ypos*unitlength/3, 0]) Ommatidium();
