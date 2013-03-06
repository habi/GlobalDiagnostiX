# Raspberry Pi setup from scratch
I plugged in a cheap 4 GB SD card I just had lying around, brought the system up and running and cobbled together bits and pieces.
This document here describes the full setup of a Raspbian system to use for the [GlobalDiagnostiX](http://globaldiagnostix.org) project.
The aim is to be able to interact with an [Elphel](http://elphel.com) camera and to acquire images from a scintillator screen using a (commercial) x-ray source.

## Prerequisites
- According to the [Embedded Linux Wiki](http://elinux.org/RPi_SD_cards), a Transcend 16GB SDHC card is working well. Order one from [Digitec](https://www.digitec.ch/ProdukteDetails2.aspx?Reiter=Details&Artikel=194092) for (currently) 24 CHF.
- Download the [BerryBoot Installer](http://www.berryterminal.com/doku.php/berryboot) and unzip it onto your SD card
- Boot your Raspberry Pi from this SD card to install a current version of [Raspbian](http://www.raspbian.org/) or any other operating system.
- Reboot, and go through `raspi-config` to reconfigure locales, keyboard and timezone if necessary

## Further setup
	sudo apt-get update				                # update the repositories
	sudo apt-get upgrade				            # upgrade the system to the newest packages
	sudo apt-get install libblas-dev		        # good for scipy and numpy, see also http://raspberrypi.stackexchange.com/a/1730
	sudo apt-get install liblapack-dev              # ditto
	sudo apt-get install python-dev                 # we want to develop in python
	sudo apt-get install libatlas-base-dev          # speeds up execution according to http://is.gd/H7zqxv
	sudo apt-get install gfortran                   # compiler for scipy and numpy
	sudo apt-get install python-setuptools          # helps with download, build and installation of Python packages
	sudo apt-get install python-scipy               # install scipy
	sudo apt-get install python-numpy               # install numpy
	sudo apt-get install python-matplotlib          # no plotting without it
	sudo apt-get install ipython                    # interactive Pythoning
	sudo apt-get install geany                      # my preferred Python IDE
	sudo apt-get install imagemagick                # do some image magic
	sudo apt-get install git                        # version that code!
	sudo apt-get install chromium-browser           # faster than Midori according to http://is.gd/8Hgfcc

# Tweaks
- set up git (username, email)
- set up pep8
- do we need to boot into the X-server every time?
