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
import urllib
import urllib2
import time
import matplotlib.pylab as plt

# Setup the Options
parser = OptionParser()
usage = 'usage: % prog [options] arg'

parser.add_option('-i', dest='Images',
                  help='how many successive images should I read from the '
                  'camera?',
                  metavar='123',
                  type=int)
parser.add_option('-o', dest='OutputName',
                  help='Name for the Output-Directory (when option -i) or '
                  'Output-File (when option -t)',
                  metavar='DirectoryName',
                  type='string')
parser.add_option('-s', dest='Show',
                  help='Show the images (Default=Off). Cannot be used '
                       'together with "-i" or "-t"',
                  action='store_true')
parser.add_option('-e', dest='Exposure',
                  help='Desired exposure time (in ms).',
                  metavar=516,
                  type=int)
parser.add_option('-t', dest='Trigger',
                  help='Work in triggered mode -> camera gives signals',
                  default=0,
                  action='store_true')
parser.add_option('-v', dest='Verbose',
                  help='Be Chatty',
                  default=0,
                  action='store_true')
(options, args) = parser.parse_args()

if not options.Images and not options.Show and not options.Trigger:
    # Print the OptionParser help if none of the important options are given
    if options.Exposure:
        print 'You onyly specified the exposure time. You at least need to',\
            'specify if you want to:'
        print '    * read N images (-i))'
        print '        ', ' '.join(sys.argv), '-i N'
        print '    * show a live image (-s))'
        print '        ', ' '.join(sys.argv), '-s'
        print '    * or work in triggered mode (-t).'
        print '        ', ' '.join(sys.argv), '-t'
    if not options.Exposure:
        parser.print_help()
    exit()

# Startup
CamIP = 'http://192.168.0.9'
StartURL = CamIP + ':8081/towp/save'
ImageURL = CamIP + ':8081/torp/wait/img/next/save'

# See if we can reach the camera, abort if not. This snippet has been adapted
# from http://stackoverflow.com/a/3764660/323100
try:
    urllib2.urlopen(CamIP, timeout=3)
except urllib2.URLError as err:
    print 'If I try to reach the camera, I get "' + str(err.reason) +\
        '"'
    print 'Did you switch the Ethernet port?'
    print 'Use\n~/./Switch.py -e\nto switch to the Elphel camera'
    sys.exit(1)


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
            sys.stdout.write("Please type 'yes' or 'no' (or 'y' or",
                             "'n').\n")


def set_exposure_time(exposuretime):
    '''
    Sets the exposure time of the camera to 'exposuretime' ms
    '''
    # upload PHP script.
    print 'Uploading ~/Dev/Elphel/globaldiagnostix.php to', CamIP + '/var'
    FTPcommand = 'curl -s -T ~/Dev/Elphel/setexposure.php ftp' +\
        CamIP[4:] + '/var/html/ --user root:pass'  # CamIP[4:] deletes 'http'
    if options.Verbose:
        print 'by calling "' + FTPcommand + '"'
    os.system(FTPcommand)
    # Set Exposure via using the PHP file we just uploaded. Exposure time is
    # set in ms. The PHP script will convert ms to us.
    ExposureURL = CamIP + '/var/setexposure.php?exposure=' +\
        str(exposuretime)
    print 'Setting exposure time to', exposuretime, 'ms'
    if options.Verbose:
        print 'by calling "' + ExposureURL + '"'
    urllib.urlretrieve(ExposureURL)
    if options.Verbose:
        print
        print 'You can check if everything worked by looking at "' + CamIP + \
            '/parsedit.php?title=ROI+and+Exposure&WOI_WIDTH&WOI_HEIGHT&' +\
            'AUTOEXP_ON&EXPOS" in the browser'

# Make a subdirectory relative to the current directory to save the images.
# Then make the necessary subdirectories for the different use-cases
SubDirName = 'Images'
try:
    os.mkdir(os.path.join(os.getcwd(), SubDirName))
except:
    pass

if options.Images:
    # If we are saving the images in a certain subdirectory, then generate the
    # names according to what the user requested
    if options.OutputName:
        SaveDir = os.path.join(os.getcwd(), SubDirName, options.OutputName)
    else:
        SaveDir = os.path.join(os.getcwd(), SubDirName, str(time.time()))
    try:
        os.mkdir(SaveDir)
    except:
        print 'Directory', SaveDir, 'already exists.'
        if query_yes_no('Are you sure you want to overwrite the files in ' +\
                        SaveDir, default='no') == 'no':
            print
            print 'Start again with a different -o parameter'
            sys.exit(1)
        else:
            print 'Ok, you asked for it! Proceeding...'
elif options.Show:
    print 'Making the directory', os.path.join(os.getcwd(), SubDirName,
                                               'Snapshots')
    try:
        os.mkdir(os.path.join(os.getcwd(), SubDirName, 'Snapshots'))
    except:
        print 'Directory', os.path.join(os.getcwd(), SubDirName, 'Snapshots'),\
            'already exists.'
elif options.Trigger:
    print 'Making the directory', os.path.join(os.getcwd(), SubDirName,
                                               'Triggered')
    try:
        os.mkdir(os.path.join(os.getcwd(), SubDirName, 'Triggered'))
    except:
        print 'Directory', os.path.join(os.getcwd(), SubDirName, 'Triggered'),\
            'already exists.'

'''
According to http://wiki.elphel.com/index.php?title=Imgsrv#imgsrv_usage one can
call 'http://<camera-ip>:8081/towp/save' to set the current pointer and save it
to the global image pointer. For each subsequent image, one can then repeatedly
call 'http://<camera-ip>:8081/torp/wait/img/next/save' to set the current
pointer to the global read pointer (torp) and to wait for the image at that
pointer to be ready (wait). The image is then transferred (img), the pointer
advanced (next) and saved again (save). This means that the same URL can be
called again and again and always provides the next image.
'''

# The command below sets and saves the current camera pointer.
urllib.urlopen(StartURL)
# set exposure time (if desired)
if options.Exposure:
    set_exposure_time(options.Exposure)

# Start the actual acquisition
if options.Images:
    # Save options.Images number of images as fast as possible
    raw_input('Press Enter when you are ready to start! [Enter]')
    StartTime = time.time()
    if not options.Verbose:
        print 'Getting', options.Images, 'images as fast as possible'
        print 'Please stand by'
    for i in range(1, options.Images + 1):
        FileName = 'img_' + str('%.04d' % i) + '.jpg'
        if options.Verbose:
            print 'writing image ' + str(i) + '/' +\
                str(options.Images), 'as',\
                os.path.join(SaveDir, FileName)
        # get the url of the camera which spits out an image (ImageURL,  set
        # above) and save the image to 'SaveDir' with consecutively numbered
        # images
        urllib.urlretrieve(ImageURL, os.path.join(SaveDir, FileName))
    TimeUsed = time.time() - StartTime
    print 'Saved', options.Images, 'images in', \
        np.round(TimeUsed, decimals=3),\
        'seconds (' + str(np.round(options.Images / TimeUsed, decimals=3)) + \
        ' img/s)'
elif options.Show:
    # Remove snapshots from prior runs
    removecommand = 'rm ' + os.path.join(os.getcwd(), SubDirName, 'Snapshots',
                                         'Snap*')
    try:
        os.system(removecommand)
        print 'I just removed all snapshots from prior runs'
    except:
        pass
    # Save the current image to disk and display it as fast as possible
    # in a matlotlib-figure
    plt.figure()
    # make matplotlib interactive, so we can just plt.draw() the image
    # into a plt.figure()
    ion()
    plt.show()
    print 'Saving camera images to ' + os.path.join(os.getcwd(), SubDirName,
                                                    'Snapshots',
                                                    'Snapshot_*.jpg')
    print 'and showing it in a matplotlib-figure'
    print
    print 'rinse, lather, repeat'
    Counter = 0
    StartTime = time.time()
    try:
        while True:
            FileName = 'Snapshot_' + str('%.04d' % Counter) + '.jpg'
            DownScale = 10
            urllib.urlretrieve(CamIP + ':8081/img', os.path.join(os.getcwd(),
                               SubDirName, 'Snapshots', FileName))
            if options.Verbose:
                print 'I have written image', Counter, 'as',\
                    os.path.join(os.getcwd(), SubDirName, FileName)
            plt.imshow(plt.imread(os.path.join(os.getcwd(), SubDirName,
                                               'Snapshots', FileName)
                                  )[::DownScale, ::DownScale, :],
                       origin='lower', interpolation='nearest')
            TimeUsed = time.time() - StartTime
            ImageTitle = str(FileName) + ' written in ' +\
                str(int(np.round(TimeUsed))) + ' s = (' +\
                r(np.round(Counter / TimeUsed, decimals=3)) +\
                ' img/s) \nshown ' + str(DownScale) + 'x downscaled'
            plt.title(ImageTitle)
            Counter += 1
            plt.draw()
    except KeyboardInterrupt:
        print '\nGoodbye'
        # switch back to normal matplotlib behaviour
        ioff()
elif options.Trigger:
    # if we work in triggered mode, we need to have set the exposure time
    if not options.Exposure:
        print 'You have not specified an exposure time. In triggered mode I',\
            '*need* one. Please start the script again with the added -e',\
            'Option:'
        print ' '.join(sys.argv), '-e ExposureTime'
        sys.exit(1)
    # Try to import the GPIO library
    try:
        import RPi.GPIO as GPIO
    except:
        print
        print 'I cannot import RPI.GPIO, you have to run the script as root'
        print 'try running it again with'
        print 'sudo', ' '.join(sys.argv)
        # joining the sys.argv list to a string so we can print it
        sys.exit(1)
    # Trigger the camera externally and save one image with the given exposure
    # time.
    print 'DID YOU SET THE CAMERA TO TRIG=4?'
    time.sleep(5)
    # Set up pins as they physically are on the board. Check
    # http://elinux.org/File:GPIOs.png to see what each pin does or which
    # number it actually is
    GPIO.setmode(GPIO.BOARD)
    # Set the very last pin on the bottom right.
    # The last one in the row of P1 is 'Ground'
    GPIO.setup(26, GPIO.OUT)
    print 'As soon as you press the trigger, I will expose the camera'
    print 'with an exposure time of', options.Exposure, 'ms (or',\
        np.round(double(options.Exposure) / 1000, decimals=3), 's)'
    raw_input('Simulate a trigger by pressing Enter... [Enter]')
    # Set the pin to high, sleep for options.Exposure time and set it to
    # low
    print
    print 10 * ' ' + 'Blitzflashdiblitzblitz!'
    print
    GPIO.output(26, GPIO.HIGH)
    print 'sleeping for',\
        np.round(double(options.Exposure) / 1000, decimals=3),\
        's, then getting image'
    time.sleep(np.round(double(options.Exposure) / 1000, decimals=3))
    GPIO.output(26, GPIO.LOW)
    print
    if options.OutputName:
        FileName = 'Triggered_' + options.OutputName + '_' +\
            str(options.Exposure) + 'ms.jpg'
    else:
        FileName = 'Triggered_' + str(time.time()) + '_' +\
            str(options.Exposure) + 'ms.jpg'
    print FileName
    urllib.urlretrieve(CamIP + ':8081/trig/pointers',
                       os.path.join(os.getcwd(),
                       SubDirName,
                       'Triggered',
                       FileName))
    # Reset RPi channels after we're done
    GPIO.cleanup()

if options.Images:
    print 'Images have been saved saved to'
    print os.path.join(os.getcwd(), SaveDir, 'img_****.jpg')
elif options.Show:
    print 'Snapshot images have been saved saved to'
    print os.path.join(os.getcwd(), SubDirName, 'Snapshot',
                       FileName)[:-8] + '****.jpg'
elif options.Trigger:
    print 'One triggered image has been saved saved to'
    print os.path.join(os.getcwd(), SubDirName, 'Triggered', FileName)
