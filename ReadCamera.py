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
                  help="Be chatty. Off by default")
parser.add_option("-c", "--camera", dest="camera",
                  default="tis", metavar='name',
                  help="Camera to use; at the moment 'tis', 'aptina' and "
                       "'awaiba', even when the two latter options are not "
                       "implemented yet... [default: %default]")
parser.add_option("-e", "--exposure", dest="exposure",
                  metavar='58',
                  help="Exposure time [cycles] (?)")
parser.add_option("-s", "--show", dest="show",
                  action="store_true", default=False,
                  help="Show the stream (default=off)")
parser.add_option("-i", "--images", dest="images",
                  default=5, type="int",
                  help="How many images should ffmpeg save at the end?")
(options, args) = parser.parse_args()

if len(sys.argv[1:]) == 0:
    print "You need to enter at least one options, here's the help"
    parser.print_help()
    sys.exit()

if not options.exposure:
    print 'You need to supply an exposure time we should use.'
    print 'Enter the command like so:'
    print '    ', ' '.join(sys.argv), "-e exposuretime"
    sys.exit()

print 80 * "-"
print "Hey ho, let's go!"

if options.verbose:
    print "We are trying to work with the '" + options.camera + "' camera"
    print
    print "Getting available sizes"
else:
    print "The '" + options.camera + "' camera provides these sizes"

# Get available output sizes of the currently connected camera using v4l2-ctl
process = subprocess.Popen(['v4l2-ctl', '--list-formats-ext'],
                           stdout=subprocess.PIPE)
output, error = process.communicate()
width = []
height = []
for line in output.split("\n"):
    if line and line.split()[0].startswith("Size"):
        width.append(int(line.split()[2].split("x")[0]))
        height.append(int(line.split()[2].split("x")[1]))

for size in range(len(width)):
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

print "We are using", CMOSwidth, "x", CMOSheight, "px to proceed"

#~ Get current exposure time and set it to the desired one
#~ Use 'v4l2-ctl -L' to get exposure time
if options.verbose:
    process = subprocess.Popen(['v4l2-ctl', '-L'], stdout=subprocess.PIPE)
    output, error = process.communicate()
    for line in output.split("\n"):
        if line and line.split()[0].startswith("exp"):
            print "The current exposure time is", line.split("=")[-1], "cycles"

#~ Use 'v4l2-ctl -c exposure_absolute=time' to set exposure time
process = subprocess.Popen(["v4l2-ctl",
                            "-c", "exposure_absolute=" +
                            str(options.exposure)], stdout=subprocess.PIPE)
process = subprocess.Popen(['v4l2-ctl', '-L'], stdout=subprocess.PIPE)
output, error = process.communicate()
for line in output.split("\n"):
    if line and line.split()[0].startswith("exp"):
        print "The exposure time has been set to", line.split("=")[-1],\
            "cycles"

# Show the stream if desired
if options.show:
    print "I'm now showing you the stream from the camera using mplayer."
    print "Exit with pressing the 'q' key!"
    # mplayer command based on official TIScamera page: http://is.gd/5mJEM7
    subprocess.call(["mplayer tv:// -tv driver=v4l2:width=" + str(CMOSwidth) +
                     ":height=" + str(CMOSheight) + ":device=/dev/video0"],
                    stdout=FNULL, stderr=subprocess.STDOUT, shell=True)


# Save output to a file, load that and display it.
IMAGES = 15
# We save IMAGES images, since we often demand an image from the camera while
# it is in the middle of a circle, thus it's a corrupted image...
FNULL = open(os.devnull, 'w')
# ffmpeg command based on http://askubuntu.com/a/102774
print "Getting", options.images, "images from the camera"
subprocess.call(["ffmpeg -f video4linux2 -s " + str(CMOSwidth) + "x" +
                 str(CMOSheight) + " -i /dev/video0 -vframes " +
                 str(options.images) + " snapshot_%03d.jpg"], stdout=FNULL,
                stderr=subprocess.STDOUT, shell=True)

filename = "snapshot_%03d" % (int(round(options.images / 2.0))) + ".jpg"
image = plt.imread(filename)
plt.imshow(image, origin="lower")
plt.title(' '.join([filename, "(middle one) with an exposure time of",
                    options.exposure, "cycles"]))
plt.show()

print 80 * "-"
print "done"
