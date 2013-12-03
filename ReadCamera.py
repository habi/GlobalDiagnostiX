#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script to read out the TIScamera using python.
Probably using a wrapper to interface to Mplayer
"""

from optparse import OptionParser
import sys
import os
import subprocess
import time
from pylab import *

# Use Pythons Optionparser to define and read the options, and also
# give some help to the user
parser = OptionParser()
usage = "usage: %prog [options] arg1 arg2"
parser = OptionParser(usage=usage)
parser.add_option("-v", "--verbose", dest="verbose",
                  action="store_true", default=False,
                  help="Be chatty. (default: %default)")
parser.add_option("-c", "--camera", dest="camera",
                  default="tis", type='str', metavar='name',
                  help="Camera to use; at the moment 'tis', 'aptina' and "
                       "'awaiba', even when the two latter options are not "
                       "implemented yet... (default: %default)")
parser.add_option("-e", "--exposure", dest="exposuretime",
                  metavar='125', type='float',
                  help="Exposure time [ms] (?)")
parser.add_option("-p", "--preview", dest="preview",
                  action="store_true", default=False,
                  help="Preview image (default: %default)")
parser.add_option("-i", "--images", dest="images",
                  default=5, type="int",
                  help="How many images should ffmpeg save at the end? "
                       "(default: %default)")
(options, args) = parser.parse_args()

if len(sys.argv[1:]) == 0:
    print "You need to enter at least one option, here's the help"
    parser.print_help()
    sys.exit()

if not options.exposuretime:
    print 'You need to supply an exposure time we should use.'
    print 'Enter the command like so:'
    print '    ', ' '.join(sys.argv), "-e exposuretime"
    sys.exit()

print 80 * "-"
print "Hey ho, let's go!"

# Check at which /dev/video we have a camera
for device in range(5):
    if os.path.exists('/dev/video' + str(device)):
        CameraPath = '/dev/video' + str(device)
        if options.verbose:
            print 'Found a camera on', CameraPath
        break
    else:
        if options.verbose:
            print 'Nothing found at /dev/video' + str(device)

if options.verbose:
    print "We are trying to work with the '" + options.camera + "' camera"
    print
    print "Getting available sizes"

# Get available output sizes of the currently connected camera using v4l2-ctl
process = subprocess.Popen(['v4l2-ctl', '--device=' + CameraPath,
                            '--list-formats-ext'], stdout=subprocess.PIPE)
output, error = process.communicate()
width = []
height = []
for line in output.split("\n"):
    if line and line.split()[0].startswith("Size"):
        width.append(int(line.split()[2].split("x")[0]))
        height.append(int(line.split()[2].split("x")[1]))
for size in range(len(width)):
    if options.verbose:
        print "    *", width[size], "x", height[size], "px"
if options.camera == "tis":
    CMOSwidth = max(width)
    CMOSheight = max(height)
elif options.camera == 'aptina':
    CMOSwidth = 123
    CMOSheight = 456
elif options.camera == 'awaiba':
    CMOSwidth = 123
    CMOSheight = 456
print "We are using a", CMOSwidth, "x", CMOSheight, "px detector size to",\
    "proceed."

#~ Set exposure time
#~ According to http://goo.gl/D8MHsW and http://is.gd/zaxWn7, the exposure time
#~ is set in "100 µs units, where the value 1 stands for 1/10000th of a second,
#~ 10000 for 1 second [...]". The user sets the exposure time in ms (1000 µs)
#~ 1 s = 10⁶ µs = 10⁴ units -> 1000 ms = 10⁴ units. From ms to units -> * 10
if options.verbose:
    print 'The desired exposure time is', options.exposuretime, 'ms',
else:
    print 'Setting exposure time to', options.exposuretime, 'ms'
options.exposuretime = options.exposuretime * 10
if options.verbose:
    print '(corresponding to', int(options.exposuretime), '"100 µs units").'

if options.verbose:
    process = subprocess.Popen(['v4l2-ctl', '--device=' + CameraPath, '-L'],
                               stdout=subprocess.PIPE)
    output, error = process.communicate()
    for line in output.split("\n"):
        if line and line.split()[0].startswith("exp"):
            print "The camera was set from an exposure time of",\
                line.split("=")[-1], "units",

#~ Use 'v4l2-ctl -c exposure_absolute=time' to set exposure time
process = subprocess.Popen(["v4l2-ctl", '--device=' + CameraPath,
                            "-c", "exposure_absolute=" +
                            str(options.exposuretime)], stdout=subprocess.PIPE)
if options.verbose:
    process = subprocess.Popen(['v4l2-ctl', '--device=' + CameraPath, '-L'],
                               stdout=subprocess.PIPE)
    output, error = process.communicate()
    for line in output.split("\n"):
        if line and line.split()[0].startswith("exp"):
            print "to", line.split("=")[-1], "units."

# Construct a general NULL pointer, used for the subprocesses
DEVNULL = open(os.devnull, 'w')
# Show the stream if desired
if options.preview:
    # Setting preview to 720p, since bigger doesn't work with mplayer
    previewwidth = 1280
    previewheight = 720
    print "I'm now showing you a", previewwidth, "x", previewheight, "px",\
        "preview image from the upper left corner of the sensor."
    # mplayer command based on TIScamera page: http://is.gd/5mJEM7
    mplayercommand = "mplayer tv:// -tv width=" + str(previewwidth) +\
        ":device=" + CameraPath + " -geometry 50%:50% -title 'Previewing" +\
        " top left edge (" + str(previewwidth) + "x" + str(previewwidth) +\
        " px), with an exposure time of " + str(options.exposuretime / 10) +\
        " ms' -nosound"
    if options.verbose:
        print 'Previewing images with'
        print
        print mplayercommand
        print
    print "Exit with pressing the 'q' key!"
    subprocess.call(mplayercommand, stdout=DEVNULL, stderr=subprocess.STDOUT,
                    shell=True)

# Save output to a file, load that and display it.
# We save option.images images, since we often demand an image from the camera
# while it is in the middle of a circle, thus it's a corrupted image...
Runtime = str(int(time.time()))
try:
    # Generating necessary directories
    os.makedirs(os.path.join('Images', options.camera, Runtime))
except:
    print os.path.join('Images', options.camera, Runtime),\
        'cannot be generated'
    sys.exit(1)

# ffmpeg command based on http://askubuntu.com/a/102774
print "Getting", options.images, "images from the camera"
Hz = int(round(1 / (options.exposuretime / 10 / 1000)))
ffmpegcommand = "ffmpeg -f video4linux2 -s " + str(CMOSwidth) + "x" +\
    str(CMOSheight) + " -i " + CameraPath + " -vframes " +\
    str(options.images) + " -r " + str(Hz) + " " +\
    os.path.join('Images', options.camera, Runtime) + "/snapshot_%03d.jpg"
if options.verbose:
    print 'Saving images with'
    print
    print ffmpegcommand
    print
t0 = time.time()
subprocess.call(ffmpegcommand, stdout=DEVNULL, stderr=subprocess.STDOUT,
                shell=True)
t1 = time.time()
print "in", str(round(t1 - t0, 3)), "seconds (" +\
    str(round(options.images / (t1-t0), 3)) + " images per second)"

filename = os.path.join('Images', options.camera, Runtime,
                        "snapshot_%03d" % (int(round(options.images / 2.0))) +
                        ".jpg")
image = plt.imread(filename)
plt.imshow(image, origin="lower")
figuretitle = "Snapshot", str(int(round(options.images / 2.0))), "of",\
    str(options.images), "from",\
    os.path.join("Images", options.camera, Runtime),\
    "\nwith an exposure time of", str(options.exposuretime), "ms"
if options.preview:
    plt.axhspan(ymin=CMOSheight-previewheight, ymax=CMOSheight,
                xmin=0, xmax=float(previewwidth)/CMOSwidth,
                facecolor='r', alpha=0.5)
    plt.xlim([0, CMOSwidth])
    plt.ylim([0, CMOSheight])
    #~ Add to title-tuple with comma: http://stackoverflow.com/a/4913789
    figuretitle += "\nred=preview area",
plt.title(' '.join(figuretitle))
plt.show()

print 'Images saved to', os.path.abspath(os.path.join('Images', options.camera,
                                                      Runtime,
                                                      'snapshot*.jpg'))
print 80 * "-"
print "done"
