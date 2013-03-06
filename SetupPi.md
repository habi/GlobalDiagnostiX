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
- Update the repositories and upgrade the system to the newest packages with:
	sudo apt-get update && sudo apt-get upgrade

- Reboot
- Install git and pull the GlobalDiagnostiX repository into your home folder. This should also take care of the `git` configuration, since we're also pulling `.gitconfig`.

	sudo apt-get install git
	cd; git clone git@github.com:habi/GlobalDiagnostiX.git

- Copy the lines below from `~/SetupPi.md` to install all the other repositories. This will long, go and have a coffe! You can either do it line by line (below, with explanations) or just copy the line at the bottom which does everything in one go. In the second case you can go and have two coffees...

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
	sudo apt-get install chromium-browser           # faster than Midori according to http://is.gd/8Hgfcc

    sudo apt-get install libblas-dev liblapack-dev python-dev libatlas-base-dev gfortran python-setuptools python-scipy python-numpy python-matplotlib ipython geany imagemagick chromium-browser

# Tweaks
- set up pep8
- do we need to boot into the X-server every time?
