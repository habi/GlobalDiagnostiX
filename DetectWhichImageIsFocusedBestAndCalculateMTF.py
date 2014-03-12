'''
Script to calculate the Modulation transfer function of some input images

It's based on the idea that once can use a random pattern to calculate the MTF,
as specified by Daniels et al. in http://dx.doi.org/10.1117/12.190433, which
was found through http://stackoverflow.com/q/18823968

The script reads images which were generated with GDX.ini in DevWare. It looks
for the best focused one via the mean (exposure) and standard deviation of each
image in a given (user-selected) folder. This image is then used for
calculating the MTF, giving us some "hard facts" on the quality of the images.
MTF
'''

from __future__ import division
import os
import glob
import numpy
import matplotlib.pyplot as plt

print "Hey ho, let's go"

Root = '/scratch/tmp/DevWareX/'

# Look for sensor folders (saved in DevWare with GDX.ini -> [Python: Acquire X
# images over a given rail distance])
print 'Looking for sensor-folders in', Root, 'and disregarding other folders'
SensorList = [os.path.basename(i) for
    i in sorted(glob.glob(os.path.join(Root, '*')))]
print 'Please select the sensor you want to look at'
for i, item in enumerate(SensorList):
    # Only look for AR130, AR132 and MT9M001 folders
    if item.startswith('AR') or item.startswith('MT9'):
        print i, '-', item
Sensor = []
while Sensor not in range(len(SensorList)):
    Sensor = int(input('Please enter a number: '))

# In this folder, look for lenses (saved as above)
print 'Looking for lens folders in', os.path.join(Root, SensorList[Sensor])
LensList = [os.path.basename(i) for
    i in sorted(glob.glob(os.path.join(Root, SensorList[Sensor], '*')))]
if len(LensList) > 1:
    # Only let the user select if we found more than one lens folder
    print 'Please select the lens you want to look at'
    for i, item in enumerate(LensList):
        print i, '-', item
    Lens = []
    while Lens not in range(len(LensList)):
        Lens = int(input('Please enter a number: '))
else:
    Lens = 0

# And finally, look for folders in which we saved the images
print 'Looking for image folders in', os.path.join(Root, SensorList[Sensor],
                                                    LensList[Lens])
FolderList = [i for i in sorted(glob.glob(os.path.join(Root,
                                                        SensorList[Sensor],
                                                        LensList[Lens], '*')))]
if len(FolderList) > 1:
    # Only let the user select if we found more than one image folder
    print 'Please select the folder of the images you want to look at'
    for i, item in enumerate(FolderList):
        print i, '-', os.path.basename(item)
    Folder = []
    while Lens not in range(len(FolderList)):
        Lens = int(input('Please enter a number: '))
else:
    Folder = 0

# Now we---finally---gan get a list of images to work with, yay!
Images = [i for i in sorted(glob.glob(os.path.join(FolderList[Folder],
                                                      '*.raw')))]
print 'I will work with the', len(Images), '.raw files found in',\
    FolderList[Folder]
print

# Get necessary parameters from the file names
ImageHeight = int(os.path.basename(Images[1]).split('_')[1].split('x')[1])
ImageWidth = int(os.path.basename(Images[1]).split('_')[1].split('x')[0])
#~ Probably get some more parameters, but for now it's enough...

# Iterate through the files, calculate the mean (exposure) and standard
# deviation of each image and plot these values.
print 'Calculating Mean for each of the', len(Images), 'images'
MeanExposure = [numpy.mean(numpy.memmap(x, dtype=numpy.uint16,
                                        shape=(ImageHeight, ImageWidth)))
                for x in Images]

print 'Calculating standard deviation for each of the', len(Images), 'images'
STD = [numpy.std(numpy.memmap(x, dtype=numpy.uint16,
                              shape=(ImageHeight, ImageWidth)))
       for x in Images]

normalize = True
if normalize:
    # Normalize the values around the mean and convert the now array back to a
    # list. This gives more comparable numbers for both the mean and STD.
    MeanExposure = MeanExposure - numpy.mean(MeanExposure)
    MeanExposure = MeanExposure.tolist()
    STD = STD - numpy.mean(STD)
    STD = STD.tolist()

# Plot this thing!
plt.title(' '.join([str(len(Images)), 'Images read from\n',
    os.path.basename(FolderList[Folder])]))
plt.plot(MeanExposure, color='r', alpha=0.5,
    label='Exposure with Max @ Img. ' + \
    str(MeanExposure.index(max(MeanExposure))))
plt.plot(STD, color='b', alpha=0.5,
    label='STD with Max @ Img. ' + str(STD.index(max(STD))))
plt.legend()
plt.savefig('MTF_' + SensorList[Sensor] + '_' + LensList[Lens] + '.png')
plt.show()
