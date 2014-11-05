#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script to load a bunch of images and caculate the focus of them, based on the
standard deviation of the gray values. The image with the smallest standard
deviation (from the same scene!) should be the one focused best.
"""

from __future__ import division
import glob
import os
import subprocess
import matplotlib.pyplot as plt
import shutil
import sys
import numpy

# Setup
Root = '/afs/psi.ch/project/EssentialMed/Images/13-Aptina_Focus_Test/'
#~ Root = '/Volumes/WINDOWS'
#~ Root = '/scratch/tmp/DevWareX/AR0130'
#~ Root = '/scratch/tmp/DevWareX/A-1300'

Directories = sorted([x[0] for x in os.walk(Root)][1:])

print 'I found these folders in', Root
print 'Which folder do you want to analyze?'
for item in enumerate(Directories):
    print str(item[0]) + ':', os.path.basename(item[1]), 'containing'
    print '   ', len(glob.glob(os.path.join(item[1], '*.raw'))), \
        'raw and'
    print '   ', len(glob.glob(os.path.join(item[1], '*.png'))), 'png files'

ChosenFolder = []
while ChosenFolder not in range(len(Directories)):
    ChosenFolder = int(raw_input('Enter [0:' + str(len(Directories) - 1) +
                                 ']: '))

# Get list of files. These are the images we acquired of which
# one has the best focus
Images = sorted(glob.glob(os.path.join(Directories[ChosenFolder], '*.png')))
if not Images:
    print 'I cannot find any png images in', \
        os.path.basename(Directories[ChosenFolder])
    print 'Did you save the images as RAW and not convert them yet?'
    sys.exit('Please try again...')
else:
    print 'I will work with the', \
        len(glob.glob(os.path.join(Directories[ChosenFolder], '*.png'))),\
        'png files in', Directories[ChosenFolder]
# Discard some images
Images = Images[3:]

print
print 'I will use', len(Images), '*.png images in', Directories[ChosenFolder]

# Iterate through the files, calculate the standard deviation of each image and
# plot this.
print 'Calculating Mean of each of', len(Images), 'images'
MeanExposure = [numpy.mean(plt.imread(x)) for x in Images]

print 'Calculating standard deviation of each of', len(Images), 'of images'
STD = [numpy.std(plt.imread(x)) for x in Images]

normalize = True
if normalize:
    # Normalize the values around the mean and convert the now array back to a
    # list
    MeanExposure = MeanExposure - numpy.mean(MeanExposure)
    MeanExposure = MeanExposure.tolist()
    STD = STD - numpy.mean(STD)
    STD = STD.tolist()

plt.figure(figsize=(16, 9))
plt.subplot(311)
plt.title(' '.join([str(len(Images)), 'Images read from',
    os.path.basename(Directories[ChosenFolder])]))
# Plot values
plt.plot(MeanExposure, color='r', alpha=0.5,
    label='Exposure with Max @ Img. ' + \
    str(MeanExposure.index(max(MeanExposure))))
plt.plot(STD, color='b', alpha=0.5,
    label='STD with Max @ Img. ' + str(STD.index(max(STD))))
# Print details and plot positions of 'Details' chosen images
Details = 10
for i in range(1, len(Images), int(round(len(Images) / Details))):
    print str(i).zfill(2), '|',
    if normalize:
        print 'normalized',
    print 'Exp', str(round(MeanExposure[i], 4)), '|',
    if normalize:
        print 'normalized',
    print 'STD of', round(STD[i], 4)
    plt.plot(i, MeanExposure[i], color='r', marker='.')
    plt.plot(i, STD[i], color='b', marker='.')
    plt.annotate(i, xy=(i, STD[i]), xytext=(0, 15),
                 textcoords='offset points', ha='center', va='top')
# Plot and mark worst and best image: http://stackoverflow.com/a/5147430/323100
plt.plot(STD.index(min(STD)), min(STD), color='b', marker='v')
plt.annotate(os.path.basename(Images[STD.index(min(STD))]),
    xy=(STD.index(min(STD)), min(STD)), xytext=(0, 30),
    textcoords='offset points', ha='center', va='bottom',
    bbox=dict(boxstyle='round,pad=0.5', fc='b', alpha=0.125),
    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.79'))
plt.plot(STD.index(max(STD)), max(STD), color='b', marker='^')
plt.annotate(os.path.basename(Images[STD.index(max(STD))]),
    xy=(STD.index(max(STD)), max(STD)), xytext=(0, 30),
    textcoords='offset points', ha='center', va='bottom',
    bbox=dict(boxstyle='round,pad=0.5', fc='b', alpha=0.125),
    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.79'))
plt.xlim([0, len(Images) - 1])
plt.legend(loc='best')
print
print 'Image', str(MeanExposure.index(max(MeanExposure))), '(' + \
    os.path.basename(Images[MeanExposure.index(max(MeanExposure))]) +\
    ') is the brightest.'
print 'Image', str(STD.index(max(STD))), '(' + \
    os.path.basename(Images[STD.index(max(STD))]) + ') has the largest STD.'
print
print 'Use Image'
print Images[STD.index(max(STD))]
print 'for further tests'

# Display selection of images
Counter = Details + 1
for i in range(1, len(Images), int(round(len(Images) / Details))):
    plt.subplot(3, 10, Counter)
    plt.imshow(plt.imread(Images[i]), cmap='gray')
    #~ plt.title(os.path.basename(Images[i]))
    plt.title('Img ' + str(i))
    Counter += 1
# Display worst and best image
plt.subplot(3, 2, 5)
plt.imshow(plt.imread(Images[STD.index(min(STD))]), cmap='gray')
plt.title('worst@' + os.path.basename(Images[STD.index(min(STD))]))
plt.subplot(3, 2, 6)
plt.imshow(plt.imread(Images[STD.index(max(STD))]), cmap='gray')
plt.title('best@' + os.path.basename(Images[STD.index(max(STD))]))
plt.savefig(Directories[ChosenFolder] + '.png')
plt.show()
