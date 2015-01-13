# -*- coding: utf-8 -*-

"""
Quickly grab images from the Elphel camera we have on loan
"""

from optparse import OptionParser
import os
import urllib
import time

parser = OptionParser()
usage = 'usage: % prog [options] arg'

parser.add_option('-i', dest='Images', help='how many images should I save?',
                  metavar='1234', type=int)
(options, args) = parser.parse_args()

# Make a subdirectory to the current directory we're in
try:
    os.mkdir(os.path.join(os.getcwd(), 'Elphel'))
except OSError:
    print 'Elphel-directory already exists'
SaveDir = os.path.join(os.getcwd(), 'Elphel', str(time.time()))
os.mkdir(SaveDir)

# get options.Images number of images as fast as possible from the camera
for i in range(options.Images):
    print 'writing image', i, '/', len(range(options.Images))
    # get the url of the camera which spit out an image
    # save the image to 'SaveDir', with an unique name based on the current
    # time
    urllib.urlretrieve("http://192.168.0.9:8081/wait/img",
                       os.path.join(SaveDir, str(time.time()) + '.jpg'))

print 'saved to', SaveDir
