#!/usr/bin/python
# coding=utf8

# Script to grab images from the Elphel camera
# Based on the simplest case (wget http://192.168.0.9/img) and complexified from there.

from optparse import OptionParser
import os
import urllib
import time
from pylab import *

# Setup the Options
parser = OptionParser()
usage = 'usage: % prog [options] arg'

parser.add_option('-i',dest='Images',
	help='how many successive images should I read from the camera?',
	metavar='123',type=int)
parser.add_option('-o',dest='OutPutDir',
	help='Name for the Output-Directory',
	metavar='DirectoryName',type='string')
parser.add_option('-s',dest='Show',
	help='Show the images (Default=Off). It is probably a good idea to use either "-i" or "-s"',
	action='store_true')
parser.add_option('-t',dest='Trigger',
	help='Use the external trigger and expose for one image with given exposure time (in ms). Only works if you set the camera to be triggered beforehand',
	metavar=516,type=int)
parser.add_option('-v',dest='Verbose',
	help='Be Chatty',
	default=0,
	action='store_true')	
(options,args) = parser.parse_args()

if not options.Images and not options.Show and not options.Trigger:
	# Print the OptionParser help if none of the important options are given 
	parser.print_help()
	exit()

# Make a subdirectory relative to the current directory
SubDirName = 'Images'
try:
	os.mkdir(os.path.join(os.getcwd(),SubDirName))
	print 'I just made made the directory',os.path.join(os.getcwd(),SubDirName)
except:
	print 'Directory',os.path.join(os.getcwd(),SubDirName),'already exists.'

# Give out some feedback for the user
if options.Images:
	if options.OutPutDir:
		SaveDir = os.path.join(os.getcwd(),SubDirName,options.OutPutDir)
	else:
		SaveDir = os.path.join(os.getcwd(),SubDirName,str(time.time()))
	try:
		os.mkdir(SaveDir)
	except:
		print 'Directory',SaveDir,'already exists.'

print

ImageURL = 'http://192.168.0.9:8081/img'

if options.Images:
	# get options.Images number of images as fast as possible from the camera
	raw_input('Auf die Plätze, fertig, los [Enter]')
	StartTime = time.time()
	if not options.Verbose:
		print 'Getting',options.Images,'images as fast as possible'
		print 'Please stand by'
	for i in range(1,options.Images+1):
		# FileName = 'img_' + str('%.04d' % i) + '.jpg'
                FileName = urllib.urlopen('http://192.168.0.9:8081/frame').read(10) + '.jpg'
		if options.Verbose:
			print 'writing image ' + str(i) + '/' + str(options.Images),'as',FileName
		# get the url of the camera which spits out an image (ImageURL, set above)
		# save the image to 'SaveDir', with the desired name, set above			
		urllib.urlretrieve(ImageURL,os.path.join(SaveDir,FileName))
	TimeUsed = time.time() - StartTime
	print 'Saved',options.Images,'images in',np.round(TimeUsed,decimals=3),'seconds (' + str(np.round(options.Images/TimeUsed,decimals=3)) + ' img/s)'
elif options.Show:
	# Save the current image to disk and display it as fast as possible in a matlotlib-figure
	plt.figure()
	ion() # make matplotlib interactive, so we can just plt.draw() the image into a plt.figure()
	TMPImageName = 'Snapshot'
	print 'Saving camera image to ' + os.path.join(os.getcwd(),SubDirName,TMPImageName) + '.jpg and showing it ASAP'
	print 'rinse, lather, repeat'
	try:
		while True:
			DownScale = 100
			urllib.urlretrieve(ImageURL,os.path.join(os.getcwd(),SubDirName,TMPImageName + '.jpg'))
			plt.imshow(
				plt.imread(os.path.join(os.getcwd(),SubDirName,TMPImageName + '.jpg'))[::DownScale,::DownScale,:],
				origin='lower',interpolation='none'
				)
			FrameNumber = urllib.urlopen('http://192.168.0.9:8081/frame').read(10)
			# plt.title(str(os.path.join(os.getcwd(),SubDirName,TMPImageName + '.jpg | ')) + str(time.strftime('%H:%M:%S')))
			plt.title(os.path.join(os.getcwd(),SubDirName,TMPImageName + '.jpg') + '\nFrame Number ' + FrameNumber + ', Downscaled ' + str(DownScale) + 'x')
			plt.draw()
	except KeyboardInterrupt:
		print 'Goodbye'
		ioff() # swich back to normal matplotlib behaviour
		sys.exit()
elif options.Trigger:
	# Trigger the camera externally and save one image with the set exposure time
        print 'As soon as you press the trigger, I will expose the camera with an exposure time of',options.Trigger,'ms'
	print 
	print 'Blitzflashdiblitzblitz'
	print
	print 'Info from http://wiki.elphel.com/index.php?title=Trigger'
	print 'After setting "TRIG=4" in advance, we enable the trigger with'
	print 'getting http://192.168.0.9:8081/trig/pointers'
	urllib.urlopen('http://192.168.0.9:8081/trig/pointers')
        sys.exit()

if options.Images:
	print 'Images have been saved saved to'
	print SaveDir
