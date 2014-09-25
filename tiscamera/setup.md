# Installation
I bought a 5MP USB 2.0 board camera ([DMx 72BUC02](http://www.theimagingsource.com/en_US/products/oem-cameras/usb-cmos-mono/dmm72buc02ml/))
from the Imaging source, to test for the GlobalDiagnostix project.

To make the Imaging science camera work on the RPI, I had to follow the setup
procedure as stated on the [tiscamera page](http://code.google.com/p/tiscamera/wiki/GettingStartedCMOSUVC),
where the Imaging Source provides the source code to work with their cameras on
Linux.

I downloaded the code with
> git clone https://code.google.com/p/tiscamera/

(into /afs/psi.ch/project/EssentialMed/Dev/tiscamera) but could not compile the
code due to missing libraries.

I had to install `libusb` and the `glib` libraries to make compilation work (and
at the same time installed `mplayer` for looking at the video stream)
This was done (on the Raspberry Pi) with
> sudo apt-get install libglib2.0-dev libusb-dev mplayer

and with the following command on SL6
> sudo yum install libglib* libusb* mplayer

Afterwards I did this
> cd tiscamera/tools/euvccam-fw/
> make

plugged in the camera
> sudo ./euvccam-fw -p

looked at the output of this command, which informed me that the camera is there
and can be seen by Raspbian.

To actually look at the image I started `mplayer` with the command below:
> mplayer tv:// -tv driver=v4l2:device=/dev/video0

This gives a 640x480 window (top left) of the total chip (and made me question
my screwdriver skills, because I suspected that I attached the lens holder
completely wrong).
So, to see the whole chip, start mplayer like this
> mplayer tv:// -tv driver=v4l2:width=2592:height=1922:device=/dev/video0·

To save a screenshot of the current image, start mplayer with the -vt option,
and press `s` while the image shows (or `S` for continuous, info from [this
website](https://lorenzod8n.wordpress.com/2007/05/23/screenshots-with-mplayer/).
> mplayer tv:// -tv driver=v4l2:device=/dev/video0 -vf screenshot
