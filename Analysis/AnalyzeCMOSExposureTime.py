#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script to load image sets acquired with equal source exposure time but
differing CMOS exposure time (from 25 ms to 300 ms).
Plotting the brightness of the resulting images should give us a hint on
wether it is advantageous to use shorter or longer exposure times.
"""

from __future__ import division
import glob
import os
import matplotlib.pyplot as plt
import numpy
import logging
import time


def myLogger(Folder, LogFileName):
    """
    Since logging in a loop does always write to the first instaniated file,
    we make a little wrapper around the logger function to have one log file
    per experient ID. Based on http://stackoverflow.com/a/2754216/323100
    """
    logger = logging.getLogger(LogFileName)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(os.path.join(Folder, LogFileName), 'w')
    logger.addHandler(handler)
    return logger

StartingFolder = ('/afs/psi.ch/project/EssentialMed/MasterArbeitBFH/' + 'XrayImages/20140721/Pingseng/MT9M001/Computar-11A/Spine')

Experiment = [x[0] for x in os.walk(StartingFolder)][1:]

print 'I found', len(Experiment), 'experiment IDs in', StartingFolder
print 80 * '-'

# Put necessary values of each folder into lists
Radiographies = [sorted(glob.glob(os.path.join(Folder, '*.raw')))
                 for Folder in Experiment]
NumberOfRadiographies = [len(Radiographies[i])
                         for i in range(len(Experiment))]
Scintillator = [ FileName[0].split('_')[1] for FileName in Radiographies]
Sensor = [FileName[0].split('_')[2]  for FileName in Radiographies]
Size = [[int(FileName[0].split('_')[3].split('x')[1]),
        int(FileName[0].split('_')[3].split('x')[0])]  for FileName in Radiographies]
Lens = [FileName[0].split('_')[4]  for FileName in Radiographies]
SCD = [int(FileName[0].split('_')[5][:-5])  for FileName in Radiographies]
Modality = [FileName[0].split('_')[6]  for FileName in Radiographies]
Voltage = [float(FileName[0].split('_')[7][:-2])  for FileName in Radiographies]
mAs = [float(FileName[0].split('_')[8][:-3])  for FileName in Radiographies]
SourceExposuretime = [float(FileName[0].split('_')[9][:-6])  for FileName in Radiographies]
CMOSExposuretime = [float(FileName[0].split('_')[10][:-6])  for FileName in Radiographies]

plt.ion()
for counter, item in enumerate(Experiment):
    plt.figure(figsize=[NumberOfRadiographies[counter], 5])
    plt.title(os.path.basename(Experiment[counter]))
    print str(counter + 1) + '/' + str(len(Experiment)) + \
        ': Looking at experiment', os.path.basename(Experiment[counter])
    # Write logfile
    logfile = myLogger(os.path.dirname(Experiment[counter]),
        'Exposuretime_' + os.path.basename(Experiment[counter] + '.log'))
    logfile.info('Log file for Experiment ID %s', Experiment[counter])
    logfile.info('Analsyis performed at %s',
        time.strftime('%d.%m.%Y at %H:%M:%S'))
    logfile.info('-----')
    logfile.info('This experiment ID can be found in the subfolder %s',
        Experiment[counter][len(StartingFolder):])
    logfile.info('This folder contains %s .raw files',
        NumberOfRadiographies[counter])
    logfile.info('    *  with a size of %s x %s pixels each', Size[counter][0],
        Size[counter][1])
    logfile.info('    *  recorded with an exposure time of %s ms',
        CMOSExposuretime[counter])
    print 'Loading', len(Radiographies[counter]), 'images'
    Images = [numpy.fromfile(Image, dtype=numpy.uint16).reshape(Size[counter])
              for Image in Radiographies[counter]]
    ImageMax = [numpy.fromfile(Image, dtype=numpy.uint16).reshape(Size[counter]).max()
                for Image in Radiographies[counter]]
    ImageMean = [numpy.fromfile(Image, dtype=numpy.uint16).reshape(Size[counter]).mean()
                 for Image in Radiographies[counter]]
    ImageSTD = [numpy.fromfile(Image, dtype=numpy.uint16).reshape(Size[counter]).std()
                for Image in Radiographies[counter]]
    [ logfile.info('Image %s of %s: Mean %s, Max: %s, STD: %s', c,
            len(Radiographies[counter]), round(ImageMean[c], 2), ImageMax[c],
            round(ImageSTD[c],2)) for c, i in enumerate(Radiographies[counter])]

    for c, Image in enumerate(Images):
        # Select images which are a bit brighter than the mean of the darkest
        if Image.mean() > numpy.min(ImageMean) * 1.618:
            plt.subplot(3, len(Images), 1 + c)
        else:
            plt.subplot(3, len(Images), len(Images) + 1 + c)
        plt.imshow(Image, cmap='gray')
        plt.axis('off')
        plt.title(' '.join(['Img', str(ImageSTD.index(Image.std())), '\nMean',
            str(int(round(ImageMean[c])))]))
    plt.subplot(313)
    plt.plot(ImageMax, marker='o', label='max')
    plt.plot(ImageMean, label='mean')
    plt.plot(ImageSTD, label='STD')
    plt.xlim([-0.5, NumberOfRadiographies[counter] - 0.5])
    plt.legend(loc='best')
    plt.tight_layout()
    plt.subplots_adjust(hspace = .05)
    plt.subplots_adjust(wspace = .05)
    #~ plt.subplots_adjust(left = .001)
    #~ plt.subplots_adjust(right = 1-.001)
    #~ plt.subplots_adjust(bottom = .001)
    #~ plt.subplots_adjust(top = 1-.001)
    plt.draw()
    plt.savefig(os.path.join(os.path.dirname(Experiment[counter]),
        'Exposuretime_' + os.path.basename(Experiment[counter]) + '.png'))
plt.ioff()
plt.show()
