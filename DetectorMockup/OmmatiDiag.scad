// Mockup of OmmatiDiag
/*
 * The mockup was done after the first crude drawing with
 * [Tinkercad](https://tinkercad.com/things/3utMiKsZhx9) proved to be too
 * inflexible.
 * The basic unit of the detector will be the scintillator size, which we
 * chose to be 17" x 17" translating to 430 x 430 mm in SI units.
*/

// Generate screenshot on the Mac with
// /Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD OmmatiDiag.scad --render --imgsize=1024,768 --projection=p -o Screenshot.png
viewport_distance = 2000;

// Basic length variables [mm]
unitlength = 430;
padding = 20;
height = 100;
overscan = 1.1;
semitransparent = 0.618;
nearlytransparent = 0.309;

// dimlines.scad is used to easily draw dimensional measurements
// http://www.cannymachines.com/entries/9/openscad_dimensioned_drawings
include <dimlines.scad>

DIM_LINE_WIDTH = .025 * unitlength;
DIM_SPACE = .1 * unitlength;

module Scalebar()
    translate([unitlength + 100 , padding/2, 0]){
        rotate([0,0,90])
            dimensions(unitlength, line_width=DIM_LINE_WIDTH, loc=0);
    }

// Housing
module Housing()
  color ("gray", alpha=nearlytransparent) {
    // box bottom
    cube([unitlength + padding, unitlength + padding,1]);
    // box back walls
    cube([unitlength + padding, 1, height]);
    cube([1, unitlength + padding, height]);
    // box front walls, can (and should be turned off for increased visibility)
    translate(v = [0, unitlength + padding, 0]) {
      cube([unitlength + padding, 1, height]);
    }
    translate(v = [unitlength + padding, 0, 0]) {
     cube([1, unitlength + padding, height]); //
    }
    }

// Scintillator
module Scintillator()
  translate([padding/2, padding/2, 1]) {
    color ("green") {
      cube([unitlength,unitlength,1]);
      }
    }

// CMOS Backplate
module Backplate()
  translate([(unitlength+padding)/2 + 5, (unitlength+padding)/2 + 5, height-15]) {
    color ("red", alpha=semitransparent) {
      cube([350,320,1],center=true);
      }
    }

// Ommatidium
module Ommatidium() {
  // FOV of one Ommatidium
  FOVSize = ([unitlength/4, unitlength/3]);
  module FOV()
    color("red")
        cube([FOVSize[0] * overscan, FOVSize[1] * overscan, 1], center=true);

  // CMOS (Aptina AR0130)
  CMOSSize = ([1280, 960]);
  pixelsize = 3.75 / 1000; // [um]
  module CMOS()
    color ("blue")
      cube([CMOSSize[0] * pixelsize, CMOSSize[1] * pixelsize, 0.5], center=true);
  translate ([0,0,0]) CMOS();

  // Ommatidium back plate
  module Ommatidiumplate()
    color ("red")
      cube([15, 20, 1], center=true);
  translate ([5,7,0]) Ommatidiumplate();

  // FOV CMOS
  d_cmos_lens = 15;
  d_lens_scintillator = height - d_cmos_lens - 15;
  module CMOSCone()
      color("orange", alpha=nearlytransparent)
      cylinder(h = d_cmos_lens,
                r1 = CMOSSize[0] * pixelsize / 2 ,
                r2 = lensdiameter * 2, center=true);
  module CMOSCross() {
    color("blue", alpha=semitransparent)
    polyhedron(
      points=[ [0, 0, 0], //origin
        [-CMOSSize[0]*pixelsize/2, 0, d_cmos_lens],     // horizontal_1
        [CMOSSize[0]*pixelsize/2, 0,d_cmos_lens],       // horizontal_2
        [0, -CMOSSize[1] * pixelsize / 2,d_cmos_lens],  // vertical_1
        [0,  CMOSSize[1] * pixelsize / 2,d_cmos_lens]], // vertical_2
      faces=[[0,1,2], [0,3,4]]);
    }

  mirror([0,0,1]) translate([0,0,-d_cmos_lens])
    CMOSCross();
  translate([0,0,d_cmos_lens/2])
    CMOSCone();

  // Lens
  lensdiameter = 4;
  module Lens()
    // the lens is a squashed sphere: http://is.gd/4H9sZf
    scale([2,2,0.5]) sphere(lensdiameter, $fn=50, center=true);
  translate([0, 0, d_cmos_lens]) Lens();

  // FOV Lens
  module LensCone()
    color("orange", alpha=nearlytransparent)
    scale([1, 4/3, 1])
    cylinder(h = d_lens_scintillator,
              r1 = lensdiameter * 2,
              r2 = FOVSize[1]/2 * 1.2);
  module LensCross() {
    color("blue", alpha=semitransparent) polyhedron(
      points=[ [0, 0, 0], //origin
        [-FOVSize[0]/2 * overscan, 0, d_lens_scintillator],   // horizontal_1
        [FOVSize[0]/2 * overscan, 0,d_lens_scintillator],     // horizontal_2
        [0, -FOVSize[1]/2 * overscan ,d_lens_scintillator],   // vertical_1
        [0,  FOVSize[1]/2 * overscan,d_lens_scintillator]],  // vertical_2
      faces=[[0,1,2], [0,3,4]]);
    }
    
    translate([0,0,d_cmos_lens])
        LensCross();
    translate([0,0,d_cmos_lens + d_lens_scintillator])
        FOV();
    translate([0,0,d_cmos_lens])
         LensCone();

}

rotate([0,0,$t*360])
    translate([-(unitlength+padding)/2,-(unitlength+padding)/2,0]){
        Scalebar();
        Scintillator();
        translate([unitlength/4/2 + padding/2, unitlength/3/2 + padding/2, height-14])
            mirror([0,0,1])
            for (xpos=[0:3], ypos = [0:2]) // iterate over x and y
                translate([xpos*unitlength/4, ypos*unitlength/3, 0])
                    Ommatidium();
        Backplate();
        Housing();
};
