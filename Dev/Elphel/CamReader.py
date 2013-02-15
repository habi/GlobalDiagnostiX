#!/usr/bin/python
# coding=utf8

'''
Script to grab images from the Elphel camera, with several options.
Based on the simplest case (wget http://192.168.0.9/img) and complexified
from there. Due to using RPi.GPIO the script has to be run with 'sudo'
when acquiring a triggered exposure. The script does warn if he user does
not know this. If the user doesn't provide an option, he/she gets help.
'''

from optparse import OptionParser
import os
import sys
import urllib
import time
from pylab import *

# Setup the Options
parser = OptionParser()
usage = 'usage: % prog [options] arg'

parser.add_option('-i', dest='Images',
                  help='how many successive images should I read from the camera?',
                  metavar='123',
                  type=int)
parser.add_option('-o', dest='OutputName',
                  help='Name for the Output-Directory (when option -i) or Output-File '
                  '(when option -t)',
                  metavar='DirectoryName',
                  type='string')
parser.add_option('-s', dest='Show',
                  help='Show the images (Default=Off). Cannot be used together '
                  'with "-i" or "-t"',
                  action='store_true')
parser.add_option('-t', dest='Trigger',
                  help='Use the external trigger and expose for one image'
                  'with given exposure time (in ms).',
                  metavar=516,
                  type=int)
parser.add_option('-v', dest='Verbose',
                  help='Be Chatty',
                  default=0,
                  action='store_true')
(options, args) = parser.parse_args()

if not options.Images and not options.Show and not options.Trigger:
    # Print the OptionParser help if none of the important options are given
    parser.print_help()
    exit()


def query_yes_no(question, default="yes"):
    # from http://code.activestate.com/recipes/577058/
    '''
    Ask a yes/no question via raw_input() and return the answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (default), "no" or None (meaning an answer is
        required by the user).

    The "answer" return value is one of "yes" or "no".
    '''

    valid = {"yes": "yes", "y": "yes", "ye": "yes", "no": "no", "n": "no"}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while 1:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return default
        elif choice in valid.keys():
            return valid[choice]
        else:
            sys.stdout.write("Please type 'yes' or 'no' (or 'y' or 'n').\n")

SubDirName = 'Images'
# Make a subdirectory relative to the current directory to save the images
try:
    os.mkdir(os.path.join(os.getcwd(), SubDirName))
except:
    pass

if options.Images:
    # If we are saving the images in a certain subdirectory, then generate
    # the names according to what the user requested
    if options.OutputName:
        SaveDir = os.path.join(os.getcwd(), SubDirName, options.OutputName)
    else:
        SaveDir = os.path.join(os.getcwd(), SubDirName, str(time.time()))
    try:
        os.mkdir(SaveDir)
    except:
        print 'Directory', SaveDir, 'already exists.'
        if query_yes_no('Are you sure you want to overwrite the files in ' + SaveDir, default='no') == 'no':
            print
            print 'Start again with a different -o parameter'
            sys.exit(1)
        else:
            print 'Ok, you asked for it! Proceeding...'

if options.Show:
    print 'Making the directory', os.path.join(os.getcwd(), SubDirName, 'Snapshots')
    try:
        os.mkdir(os.path.join(os.getcwd(), SubDirName, 'Snapshots'))
    except:
        print 'Directory', os.path.join(os.getcwd(), SubDirName, 'Snapshots'), 'already exists.'

if options.Trigger:
    print 'Making the directory', os.path.join(os.getcwd(), SubDirName, 'Triggered')
    try:
        os.mkdir(os.path.join(os.getcwd(), SubDirName, 'Triggered'))
    except:
        print 'Directory', os.path.join(os.getcwd(), SubDirName, 'Triggered'), 'already exists.'

# According to the Imgsrv-page on the elphel-Wiki one should call
# http://<camera-ip>:8081/towp/save
# first to set the current pointer and save it
# and then to repeat for each image
# http://<camera-ip>:8081/torp/wait/img/next/save
# to set the current pointer to the global read pointer and to wait for
# 3 the image to become available, transfer the image, advance the pointer
# and save it, so that the same URL can be used over and over each time
# providing the next acuired image

CamIP = 'http://192.168.0.9'
StartURL = CamIP + ':8081/towp/save'
ImageURL = CamIP + ':8081/torp/wait/img/next/save'

# The command below sets and saves the current camera pointer.
urllib.urlopen(StartURL)
if options.Images:
    # Save options.Images number of images as fast as possible
    raw_input('Press Enter when you are ready to start! [Enter]')
    StartTime = time.time()
    if not options.Verbose:
        print 'Getting', options.Images, 'images as fast as possible'
        print 'Please stand by'
    for i in range(1, options.Images+1):
        FileName = 'img_' + str('%.04d' % i) + '.jpg'
        if options.Verbose:
            print 'writing image ' + str(i) + '/' + str(options.Images), 'as', os.path.join(SaveDir, FileName)
        # get the url of the camera which spits out an image (ImageURL, set above)
        # and save the image to 'SaveDir' with consecutively numbered images
        urllib.urlretrieve(ImageURL, os.path.join(SaveDir, FileName))
    TimeUsed = time.time() - StartTime
    print 'Saved', options.Images, 'images in', np.round(TimeUsed, decimals=3), 'seconds (' + str(np.round(options.Images/TimeUsed, decimals=3)) + ' img/s)'
elif options.Show:
    # Remove snapshots from prior runs
    removecommand = 'rm ' + os.path.join(os.getcwd(), SubDirName, 'Snapshots', 'Snap*')
    try:
        os.system(removecommand)
        print 'I just removed all snapshots from prior runs'
    except:
        pass
    # Save the current image to disk and display it as fast as possible in a matlotlib-figure
    plt.figure()
    # make matplotlib interactive, so we can just plt.draw() the image into a plt.figure()
    ion()
    plt.show()
    print 'Saving camera images to ' + os.path.join(os.getcwd(), SubDirName, 'Snapshots', 'Snapshot_*.jpg')
    print 'and showing it in a matplotlib-figure'
    print
    print 'rinse, lather, repeat'
    Counter = 0
    StartTime = time.time()
    try:
        while True:
            FileName = 'Snapshot_' + str('%.04d' % Counter) + '.jpg'
            DownScale = 10
            urllib.urlretrieve(CamIP + ':8081/img', os.path.join(os.getcwd(), SubDirName, 'Snapshots', FileName))
            if options.Verbose:
                print 'I have written image', Counter, 'as', os.path.join(os.getcwd(), SubDirName, FileName)
            plt.imshow(plt.imread(os.path.join(os.getcwd(), SubDirName, 'Snapshots', FileName))[::DownScale, ::DownScale, :], origin='lower', interpolation='nearest')
            TimeUsed = time.time() - StartTime
            ImageTitle = str(FileName) + ' written in ' + str(int(np.round(TimeUsed))) + ' s = (' + str(np.round(Counter/TimeUsed, decimals=3)) + ' img/s)' + '\nshown ' + str(DownScale) + 'x downscaled'
            plt.title(ImageTitle)
            Counter += 1
            plt.draw()
    except KeyboardInterrupt:
        print '\nGoodbye'
        # switch back to normal matplotlib behaviour
        ioff()
elif options.Trigger:
    # Set Exposure via PHP call
    CameraCommand = 'wget "' + str(CamIP) + '/parsedit.php?title=Setting+triggered+exposure+parameters'
    CameraCommand += '&AUTOEXP_ON=0'  # turn off auto-exposure
    CameraCommand += '&EXPOS=' + str(options.Trigger*1000)
    # set exposure time to 'Exposure time in microseconds'.
    # We input it in ms, so we multiply by 1000
    CameraCommand += '&WB_EN=0'  # turn off white balance
    CameraCommand += '&WOI_WIDTH=10000&WOI_HEIGHT=10000'
    # reset sensor to full size ("Sensor width is 'reduced' to full sensor
    # if set to 10000")
    CameraCommand += '&TRIG=0"'  # set camera to be UN-triggered
    #~ CameraCommand += '&TRIG=4"'  # set camera to be triggered externally
    CameraCommand += ' --delete-after'  # delete wget output afterwards
    print 'Setting the camera with'
    print '---'
    print CameraCommand
    print '---'
    print 80 * '_'
    print
    print 'I AM NOT DOING ANYTHING, UNCOMMENT LINE 214 TO ACTUALLY PERFORM THE COMMAND'
    #~ os.system(CameraCommand)
    print 80 * '_'
    # Try to import the GPIO library
    try:
        import RPi.GPIO as GPIO
    except:
        print 'I cannot import RPI.GPIO, you have to run the script as root'
        print 'try running it again with'
        print 'sudo', ' '.join(sys.argv)
        # joining the sys.argv list to a string so we can print it
        sys.exit(1)
    # Trigger the camera externally and save one image with the given exposure
    # time.
    # Set up pins as they physically are on the board. Check
    # http://elinux.org/File:GPIOs.png to see what each pin does or which
    # number it actually is
    GPIO.setmode(GPIO.BOARD)
    # Set the very last pin on the bottom right.
    # The last one in the row of P1 is 'Ground'
    GPIO.setup(26, GPIO.OUT)
    print 'As soon as you press the trigger, I will expose the camera'
    print 'with an exposure time of', options.Trigger, 'ms (or', np.round(double(options.Trigger)/1000, decimals=3), 's)'
    raw_input('Simulate a trigger by pressing Enter... [Enter]')
    # Set the pin to high, sleep for options.Trigger time and set it to low
    print
    print 10 * ' ' + 'Blitzflashdiblitzblitz!'
    print
    GPIO.output(26, GPIO.HIGH)
    print 'sleeping for', np.round(double(options.Trigger)/1000, decimals=3), 's, then getting image'
    time.sleep(np.round(double(options.Trigger)/1000, decimals=3))
    GPIO.output(26, GPIO.LOW)
    print
    if options.OutputName:
        FileName = 'Triggered_' + options.OutputName + '_' + str(options.Trigger) + '.jpg'
    else:
        FileName = 'Triggered_' + str(options.Trigger) + '_' + str(time.time()) + '.jpg'
    print FileName
    urllib.urlretrieve('http://192.168.0.9:8081/trig/pointers', os.path.join(os.getcwd(), SubDirName, 'Triggered', FileName))
    # Reset RPi channels after we're done
    GPIO.cleanup()

if options.Images:
    print 'Images have been saved saved to'
    print os.path.join(os.getcwd(), SaveDir, 'img_****.jpg')
elif options.Show:
    print 'Snapshot images have been saved saved to'
    print os.path.join(os.getcwd(), SubDirName, 'Snapshot', FileName)[:-8] + '****.jpg'
elif options.Trigger:
    print 'One triggered image has been saved saved to'
    print os.path.join(os.getcwd(), SubDirName, 'Triggered', FileName)
