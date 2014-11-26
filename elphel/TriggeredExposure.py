#!/usr/bin/python
# coding=utf8

"""
Script to use the internal clock of the Elphel camera to trigger the anode
heating, x-ray pulse, exposure of the camera and readout using the GPIOs from
the Raspberry Pi.
Based on CamReader.py after detailed discussions with Alexandre Poltorak from
Elphel when he was visiting PSI.
"""

from optparse import OptionParser
import sys
import urllib
import time
import os


# Setup the Options
parser = OptionParser()
usage = 'usage: % prog [options] arg'
parser.add_option('-e', dest='ExposureTime',
                  help='Desired exposure time for the camera (in ms)',
                  metavar='123',
                  type=int)
parser.add_option('-t', dest='Test',
                  help='Testrun. Good if you do not run it on the RPi',
                  default=0, action='store_true')
(options, args) = parser.parse_args()

# Try to import the GPIO library
try:
    import RPi.GPIO as GPIO
except:
    # If testing, we are probably not on the RPi, omitting exit
    if options.Test is False:
        print 'I cannot import RPI.GPIO, you have to run the script as root'
        print 'try running it again with'
        # Joining the sys.argv list to a string. Print it as a help to the user
        print 'sudo', ' '.join(sys.argv)
        exit(1)
    else:
        print 'TESTING: I would try to import the RPi.GPIO library here'

if not options.ExposureTime:
    # Print the OptionParser help if none of the important options are given
    parser.print_help()
    exit()

# Setup Parameters
AnodeSpinupTime = 2  # in seconds
InputPin = 22
AnodePin = 24
XraySourcePin = 26
# Expose the camera this much longer than the x-ray pulse
CameraExposureFactor = 1.2

SubDirName = 'Radiographies'
# Make a subdirectory relative to the current directory to save the images
try:
    os.mkdir(os.path.join(os.getcwd(), SubDirName))
except:
    pass

"""
The script will do this:
- Set exposure time of the camera
- Spin up anode with a 3.2V signal over one pin (hope that's enough, since
    we measured 4.2V over the trigger in the x-ray lab)
- Wait for camera signaling to be ready with an exposure
- Trigger camera exposure, marginally longer than x-ray pulse, so we catch all
    photons
- Trigger x-ray pulse with another 3.2V signal over another pin
- Download image from from camera and save it someplace sensible
- Process the Image, or show it
"""

# http://wiki.elphel.com/index.php?title=Imgsrv#imgsrv_usage describes what
# the StartURL and ImageURL commands do; some pointery thingies.
CamIP = 'http://192.168.0.9'
StartURL = CamIP + ':8081/towp/save'
ImageURL = CamIP + ':8081/torp/wait/img/next/save'

"""
Set exposure time, either via wget or PHP call to something along the lines of
snapfull.php.
Could probably be done bit more clever. This works for now, ask the Elphel
support mailing list for a more clever way.
"""
CameraCommand = 'wget "' + str(CamIP) + '/parsedit.php?'
CameraCommand += '&AUTOEXP_ON=0'  # turn off auto-exposure
# set exposure time to 'Exposure time in microseconds'.
# We input it in ms, so we multiply by 1000
CameraCommand += '&EXPOS=' + str(options.ExposureTime * 1000)
# reset sensor to full size ("Sensor width is 'reduced' to full sensor
# if set to 10000"). Just make sure we get the full image
CameraCommand += '&WOI_WIDTH=10000&WOI_HEIGHT=10000'
# set camera to be UN-triggered, i.e. internally triggered
CameraCommand += '&TRIG=0"'
#~ CameraCommand += '&TRIG=4"'  # set camera to be triggered externally
# get rid of the 'wget' output after it is finished.
CameraCommand += ' --delete-after'
if options.Test:
    print 'TESTING: I would set up the camera with'
    print '---'
    print CameraCommand
    print '---'
else:
    os.system(CameraCommand)

# Inform the user what will happen
print 'As soon as you confirm with [Enter], I will trigger everything like so:'
print '    - I will spin up the anode for', AnodeSpinupTime, 'seconds'
print '    - Meanwhile I will prepare the camera'
print '    - I will trigger the camera to acquire an image with an exposure', \
    ' time of', int(options.ExposureTime * CameraExposureFactor), \
    'ms (or', \
    round(float(int(options.ExposureTime * CameraExposureFactor)) / 1000, 3), \
    's,', CameraExposureFactor, 'x longer than the set exposure time)'
print '    - I will trigger the x-ray pulse for', options.ExposureTime, 'ms'
print '    - I will save the image to ', os.path.join(os.getcwd(), SubDirName)

# Go!
raw_input('Simulate a trigger by pressing Enter... [Enter]')
print

# Prepare the camera
# First set the pointer
if options.Test:
    print 'TESTING: Calling', StartURL, 'to set the camera pointers'
else:
    urllib.urlopen(StartURL)
# Set up RPi pins as they are on the board (pysical location). Check
# http://elinux.org/File:GPIOs.png to see what each pin does or which
# number it actually is.
if options.Test:
    print 'TESTING: Setting up board pins layout and "AnodePin"'
    print 'TESTING: Spinning up anode'
else:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(AnodePin, GPIO.OUT)
    # Set the 'AnodePin' to HIGH to spin up the anode
    GPIO.output(AnodePin, GPIO.HIGH)
    # wait for half a second until the anode is ready
    time.slee(0.5)
# Wait for camera signaling that it is ready by listening on the input port
if options.Test:
    print 'TESTING: Setting up "InputPin"'
else:
    GPIO.setup(InputPin, GPIO.IN)
if options.Test:
    print 'TESTING: Waiting for signal from camera on "InputPin"'
    print 'TESTING: Setting "XraySourcePin" to high'
    print 'TESTING: Sleeping for "options.ExposureTime"'
else:
    while True:
        # Wait for camera to signal readyness on the InputPin, then go!
        if GPIO.input(InputPin):
            # Trigger x-ray pulse with another 4V signal over another pin
            GPIO.output(XraySourcePin, GPIO.HIGH)
            time.sleep(options.ExposureTime)
            print 'Do something sensible here'
# Wait for afterglow (exact time TBD) to catch all photons
time.sleep(0.01)

# Get image from camera and save it with current epoch time as filename, to
# avoid duplicates
ImageName = time.time()
if options.Test:
    print 'TESTING: I would save', ImageURL, 'to', \
        os.path.join(SubDirName, str(ImageName) + '.jpg')
else:
    urllib.urlretrieve(ImageURL,
                       os.path.join(SubDirName, str(ImageName) + '.jpg'))

# Reset RPi channels after we're done
if options.Test:
    print 'TESTING: Cleaning up GPIO pins'
else:
    GPIO.cleanup()

print
# 38 = 80 / 2 - len('Done') / 2, with 80 being the line length
print 38 * ' ' + 'DONE!'
print
# Process the Image, and/or show it afterwards.
print 'Your image has been saved to', \
      os.path.abspath(os.path.join(SubDirName, str(ImageName) + '.jpg'))
print 'The image name "' + str(ImageName) + \
    '.jpg" also tells you that the image was saved on', \
    time.strftime("%d %B %Y %Y at %H:%M:%S", time.localtime(ImageName))

"""
ImageName is in epoch seconds, time.localtime converts it to local time,
time.mktime back to epoch, time.ctime to a nice human readable string. As
specified on http://docs.python.org/2/library/time.html
"""
print
print 'Thanks for working with us.'
