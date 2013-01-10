#!/usr/bin/python
# coding=utf8
from optparse import OptionParser
import os
import urllib
import time
from pylab import *
from skimage import data, io, filter

# Setup the Options
parser = OptionParser()
usage = 'usage: % prog [options] arg'

parser.add_option('-i',dest='Images',
	help='how many images should I read from the camera?',
	metavar='123',type=int)
parser.add_option('-o',dest='OutPutDir',
	help='Name for the Output-Directory',
	metavar='DirectoryName',type='string')
parser.add_option('-s',dest='Show',
	help='Show the images (Default=Off). It is probably a good idea to use either "-i" or "-s"',
	default=0,
	action='store_true')
parser.add_option('-v',dest='Verbose',
	help='Be Chatty',
	default=0,
	action='store_true')	
(options,args) = parser.parse_args()

if not options.Images and not options.Show: 
	parser.print_help()
	exit()

# Make a subdirectory to the current directory we're in
SubDirName = 'Images'
try:
	os.mkdir(os.path.join(os.getcwd(),SubDirName))
	print 'I just made the directory',os.path.join(os.getcwd(),SubDirName)
except:
	print 'Directory,',os.path.join(os.getcwd(),SubDirName),'already exists.'

# Give out some feedback for the user
if options.Images:
	if options.OutPutDir:
		SaveDir = os.path.join(os.getcwd(),SubDirName,options.OutPutDir)
	else:
		SaveDir = os.path.join(os.getcwd(),SubDirName,str(time.time()))
	try:
		os.mkdir(SaveDir)
	except:
		print 'Directory,',SaveDir,'already exists.'

# Prepare figure if desired
if options.Show:
	ion()

# get options.Images number of images as fast as possible from the camera
if options.Images:
	raw_input('Auf die Plätze, fertig, los [Enter]')
	StartTime = time.time()
	print 'Getting',options.Images,'images as fast as possible'
	for i in range(1,options.Images+1):
		FileName = 'img_' + str('%.04d' % i) + '.jpg'
		if options.Verbose:
			print 'writing image ' + str(i) + '/' + str(options.Images),'as',FileName
		# get the url of the camera which spits out an image
		# save the image to 'SaveDir', with the desired name, set above			
		urllib.urlretrieve("http://192.168.0.9:8081/img",os.path.join(SaveDir,FileName))
	TimeUsed = time.time() - StartTime
	print 'Saved',options.Images,'images in',np.round(TimeUsed,decimals=3),'seconds (' + str(np.round(options.Images/TimeUsed,decimals=3)) + ' img/s)'
else:
	try:
		while True:
			DownScale = 10
			TMPImageName = 'Snapshot'
			urllib.urlretrieve("http://192.168.0.9:8081/last/wait/img",os.path.join(os.getcwd(),SubDirName,TMPImageName + '.jpg'))
			plt.imshow(
				plt.imread(os.path.join(os.getcwd(),SubDirName,TMPImageName + '.jpg'))[::DownScale,::DownScale,:],
				origin='lower'
				)
			plt.title(str(os.path.join(os.getcwd(),SubDirName,TMPImageName + '.jpg | ')) + str(time.strftime('%H:%M:%S')))
			plt.draw()
	except KeyboardInterrupt:
		print 'Goodbye'

if options.Show:
	ioff() # so the shown image in the figure is not closed...

if options.Images:
	print 'Images have been saved saved to'
	print SaveDir
