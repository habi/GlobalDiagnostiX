This repo tracks some stuff I've written as part of my work as a member of the [GlobalDiagnostiX](http://globaldiagnostix.org)-alliance

I'm trying to work with an [Elphel](http://elphel.com)-camera connected to a [Raspberry Pi](http://raspberrypi.org), the code in this repo currently deals only with this.

* /Dev/Elphel/CamReader.py: Script to read the camera and either save the images, show them or do a triggered exposure
* /Dev/Elphel/elphel.py: First iteration of a script to read out the camera. First proof of concept experiments were performed with this
* /Dev/Elphel/GPIO.py: Test-Script to set the GPIO of the Raspberry Pi
* /Dev/Elphel/TriggeredExposure.py: Script to use the internal clock of the camera to trigger the anode rotation, x-ray pulse and the exposure. Then read out the image
* LICENSE: (un)license
* README.md: The file you're looking at now
* SetupPi.md: HowTo for setting up a Raspberry Pi from scratch, to use with these scripts to download images from an Elphel camera and to trigger an x-ray exposure
* Switch.py: Switch the network interface from DHCP to 192.168.0.9, for switching between PSI network and hooking up the Elphel camera
* SyncToAFS.cmd: rsync all changes to the PSI AFS, so we have a backup on the PSI system.

