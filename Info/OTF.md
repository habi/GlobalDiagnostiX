# OTF/MTF calculation for the Elphel Camera

This does not work on the Raspberry Pi (yet), since I wasn't able to compile the ImageJ plugins from Elphel.

# On a powerful machine
* get the Elphel ImageJ plugins by issuing `git clone git://elphel.git.sourceforge.net/gitroot/elphel/ImageJ-Elphel ImageJ-Elphel` (maybe add it later to your `.gitignore`)
* Follow the directions on the [Elphel Wiki](http://wiki.elphel.com/index.php?title=Measure_OTF_of_the_lens-sensor_system#B_-_generate) to generate a test pattern.
* Take an image with the stated camera settings
* Analyze the image according to the [guidelines given by Elphel]http://wiki.elphel.com/index.php?title=Measure_OTF_of_the_lens-sensor_system#ImageJ)
