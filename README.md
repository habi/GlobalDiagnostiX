This repo tracks some stuff I've written as part of my work as a member of the [GlobalDiagnostiX](http://globaldiagnostix.org)-alliance

I'm trying to work with an [Elphel](http://elphel.com)-camera connected to a [Raspberry Pi](http://raspberrypi.org), the code in this repo currently deals only with this.

* CamReader.py: Script to read the camera and either save the images, show them or do a triggered exposure
* elphel.py: First iteration of a script to read out the camera. First proof of concept experiments were performed with this
* GPIO.py: Test-Script to set the GPIO of the Raspberry Pi
* README.md: This file
* Switch.py: Switch the network interface from DHCP to 192.168.0.9, for switching between PSI network and hooking up the Elphel camera
* SyncToAFS.cmd: rsync all changes to the PSI AFS, so we have a backup on the PSI system.
* TriggeredExposure.py: Script to use the internal clock of the camera to trigger the anode rotation, x-ray pulse and the exposure. Then read out the image
