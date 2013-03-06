# Raspberry Pi setup from scratch
I plugged in a cheap 4 GB SD card I just had lying around, brought the system up and running and cobbled together bits and pieces.
This document here describes the full setup of a Raspbian system to use for the [GlobalDiagnostiX](http://globaldiagnostix.org) project.
The aim is to be able to interact with an [Elphel](http://elphel.com) camera and to acquire images from a scintillator screen using a (commercial) x-ray source.

## Prerequisites
- According to the [Embedded Linux Wiki](http://elinux.org/RPi_SD_cards), a Transcend 16GB SDHC card is working well. Order one from [Digitec](https://www.digitec.ch/ProdukteDetails2.aspx?Reiter=Details&Artikel=194092) for (currently) 24 CHF.
- Download the [Raspbian Installer](http://www.raspbian.org/RaspbianInstaller) onto the SD card.
- Plug in this SD card and boot your Raspberry Pi from it to install a current version of [Raspbian](http://www.raspbian.org/).
- Follow the [directions from the Installer page])(http://www.raspbian.org/RaspbianInstaller), they are not always self-explaining in the GUI.
- Give the root user a sensible password and make a new user, for day-to-day use (I chose user 'gdx', with a sensible password).
- Wait for a long while for the setup to complete.

## Further setup
	apt-get update
	apt-get upgrade
	apt-get install geany, git, imagemagick, scipy, numpy
	
