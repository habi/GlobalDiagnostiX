# OTF/MTF calculation for the Elphel Camera

This does not work on the Raspberry Pi (yet), since I wasn't able to compile the ImageJ plugins from Elphel.

# On a powerful machine
* get the Elphel ImageJ plugins by issuing `git clone git://elphel.git.sourceforge.net/gitroot/elphel/ImageJ-Elphel ImageJ-Elphel` (maybe add it later to your `.gitignore`)
* Follow the directions on the [Elphel Wiki](http://wiki.elphel.com/index.php?title=Measure_OTF_of_the_lens-sensor_system#B_-_generate) to generate a test pattern.
* Take an image with the stated camera settings (Set them with [this link here](http://192.168.0.9/parsedit.php?embed=0.1&title=OTF+Settings&GTAB_R&GTAB_G&GTAB_GB&GTAB_B&QUALITY) (use gamma.php (also in the repo to set Gamma to 1.0 and black to 0.0).
* Analyze the image according to the [guidelines given by Elphel]http://wiki.elphel.com/index.php?title=Measure_OTF_of_the_lens-sensor_system#ImageJ)
