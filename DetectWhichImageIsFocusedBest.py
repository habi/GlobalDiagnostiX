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
Root = '/scratch/tmp/DevWareX'


Dir = ['1391779038_0027ms_120img', '1391779188_0030ms_160img',
    '1391779241_0100ms_240img']

Folder = os.path.join(Root, Dir[1])

# Get list of files in each folder, these are the images we acquired of which
# one has the best focus
Images = sorted(glob.glob(os.path.join(Folder, '*.png')))

print 'I found', len(Images), '*.png images in', Folder

# Iterate through the files, calculate the standard deviation of each image and
# plot this.
print 'Reading Means of images'
Mean = [numpy.mean(plt.imread(x)) for x in Images]
print 'Reading Standard deviations of images'
STD = [numpy.std(plt.imread(x)) for x in Images]

plt.subplot(211)
plt.plot(Mean, label='Mean', color='r')
plt.plot(STD, label='STD', color='b')
Details = 10
for i in range(1, len(Images), int(round(len(Images) / Details))):
    plt.plot(i, Mean[i], color='r', marker='x')
    plt.plot(i, STD[i], color='b', marker='x')
plt.plot(STD.index(max(STD)), max(STD), color='g', marker='o', label='Max')
plt.legend(loc='best')
print 'Image', str(STD.index(max(STD))) + ':',\
    os.path.basename(Images[STD.index(max(STD))]), 'has the largest STD.'
Counter = Details + 1
for i in range(1, len(Images), int(round(len(Images) / Details))):
    plt.subplot(2, 10, Counter)
    plt.imshow(plt.imread(Images[i]), cmap='gray')
    plt.title(os.path.basename(Images[i]))
    Counter += 1

plt.show()
