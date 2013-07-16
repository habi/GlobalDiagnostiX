# Raspberry Pi setup from scratch
I plugged in a cheap 4 GB SD card I just had lying around, brought the system up and running and cobbled together bits and pieces and got a working system.
This document here describes *all* the necessary steps to get up and runnig with a virgin SD card.
If you follow all the steps in this document, you should have a RPi ready to use for the [GlobalDiagnostiX](http://globaldiagnostix.org) project.
The aim is to be able to interact with several cameras ([Elphel](http://elphel.com), [Awaiba](http://www.awaiba.com/), [The Imaging Source](http://www.theimagingsource.com/)) and to acquire images from a scintillator screen using a (commercial) x-ray source.

## Prerequisites
- According to the [Embedded Linux Wiki](http://elinux.org/RPi_SD_cards), a Transcend 16GB SDHC card is working well. Order one from [Digitec](https://www.digitec.ch/ProdukteDetails2.aspx?Reiter=Details&Artikel=194092) for (currently) 24 CHF.
- Download the [BerryBoot Installer](http://www.berryterminal.com/doku.php/berryboot) and unzip it onto your SD card
- Boot your Raspberry Pi from this SD card to install a current version of [Raspbian](http://www.raspbian.org/) or any other operating system.
- Reboot. This will then go through `raspi-config` to reconfigure locales, keyboard and timezone (if necessary)
- `sudo /etc/ntp.conf` to add the timeservers of PSI to the configuration, so we have the correct time. Add the lines below as first `server` entries
    # Permit time synchronization with our time source, but do not
    # permit the source to query or modify the service on this system.
    server pstime1.psi.ch
    restrict pstime1.psi.ch mask 255.255.255.255 nomodify notrap noquery
    server pstime2.psi.ch
    restrict pstime2.psi.ch mask 255.255.255.255 nomodify notrap noquery
    server pstime3.psi.ch
    restrict pstime3.psi.ch mask 255.255.255.255 nomodify notrap noquery

## Further setup
- Update the repositories and upgrade the system to the newest packages with `sudo apt-get update && sudo apt-get upgrade`. 
This will will take a *long* time
- Reboot
- Install git and pull the GlobalDiagnostiX repository into your home folder.
This should also take care of the `git` configuration, since we're also pulling the `.gitconfig` from the repo.

        sudo apt-get install git
        cd
        sudo rm -r * # to remove *EVERYTHING* from your home directory
        sudo rm -r .* # REALLY, EVERYTHING!
        git clone https://github.com/habi/GlobalDiagnostiX.git ~ # clone the GitHub repo into your home directory
        nano SetupPi.md # change something in the file
        git commit -a;git push # commit the change and push it back to the repo to see if that works

- Install other packages with the lines below. This will take either take a *very* long time or go quite quickly if the command above took long. Anways, go and have a coffe....
You can either do it line by line (below, with explanations) or just copy the oneliner at the bottom which does everything in one go.

        sudo apt-get install libblas-dev	# good for scipy and numpy, see also http://raspberrypi.stackexchange.com/a/1730
        sudo apt-get install liblapack-dev	# ditto
        sudo apt-get install python-dev		# we want to develop in python
        sudo apt-get install libatlas-base-dev	# speeds up execution according to http://is.gd/H7zqxv
        sudo apt-get install gfortran		# compiler for scipy and numpy
        sudo apt-get install python-setuptools	# helps with download, build and installation of Python packages
        sudo apt-get install python-scipy	# install scipy
        sudo apt-get install python-numpy	# install numpy
        sudo apt-get install python-matplotlib	# no plotting without it
        sudo apt-get install ipython		# interactive Pythoning
        sudo apt-get install geany		# my preferred Python IDE
        sudo apt-get install imagemagick	# do some image magic
        sudo apt-get install imagej		# view and work with images
        sudo apt-get install chromium-browser	# faster than Midori according to http://is.gd/8Hgfcc
        sudo apt-get install screen		# Nice terminal multiplexer
        sudo apt-get install telnet 		# so we can `telnet` to the camera as 'root'/'pass'
        sudo apt-get install ftp		# so we can `ftp`stuff to the camera
        sudo apt-get install gftp		# so we can graphically `ftp`stuff to the camera
        sudo apt-get install gedit		# graphical text editor
        sudo apt-get install tkdiff		# a graphical tool to diff files
        sudo apt-get isntall mplayer vlc	# install two movie players, to look at camera output

Here's the oneliner:

        sudo apt-get install libblas-dev liblapack-dev python-dev libatlas-base-dev gfortran python-setuptools python-scipy python-numpy python-matplotlib ipython geany imagemagick openjdk-6-jre openjdk-6-jdk imagej chromium-browser screen telnet ftp gftp gedit tkdiff mplayer vlc

# Tweaks
- Num Lock on boot (according to [RPi-forum](http://is.gd/Fa0DxF)
	- `sudo nano /etc/kbd/config`
	- CTRL+V two or three times to go to line 67
	- remove the comment in front of "LEDS=+num"
- Install and set up `pep8`
	- `sudo easy_install pep8`
	- Follow [this guide](http://www.venkysblog.com/pep8-and-pylint-in-geany) to set up `pep8` in Geany.
- [Generate and setup SSH keys](https://help.github.com/articles/generating-ssh-keys) for easy commiting to Github
- Buy a small monitor
	- I bought http://bit.ly/10N9MbN and used a 12V power supply we had at TOMCAT.
	- Setup the composite (yellow) output to support the resolution of the monitor (PAL or NTSC, 480x272)
		- Go to 'Edit menu' in the BerryBoot boot menu, click on the arrow on top right to go to 'Advanced configuration' and edit the config.txt. See [this post in the RPI forum](http://raspberrypi.org/phpBB3//viewtopic.php?f=26&t=16403) for a screenshot.
		- add `framebuffer_width=480` and `sdtv_aspect=3`, according to the [Video mode options](http://elinux.org/RPiconfig#Video_mode_options)
		- Reboot with 'Exit'
        - Have fun!

