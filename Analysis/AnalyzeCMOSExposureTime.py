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
import scipy.misc  # for saving png or tif at the end
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

StartingFolder = ('/afs/psi.ch/project/EssentialMed/MasterArbeitBFH/' +
                  'XrayImages/20140721/Pingseng/MT9M001/Computar-11A/Spine')

Experiment = [x[0] for x in os.walk(StartingFolder)][1:]

print 'I found', len(Experiment), 'experiment IDs in', StartingFolder
print 80 * '-'

# Put necessary values of each folder into lists
Radiographies = [sorted(glob.glob(os.path.join(Folder, '*.raw')))
                 for Folder in Experiment]
NumberOfRadiographies = [len(Radiographies[i])
                         for i in range(len(Experiment))]
Scintillator = [FileName[0].split('_')[1] for FileName in Radiographies]
Sensor = [FileName[0].split('_')[2]  for FileName in Radiographies]
Size = [[int(FileName[0].split('_')[3].split('x')[1]),
        int(FileName[0].split('_')[3].split('x')[0])]
        for FileName in Radiographies]
Lens = [FileName[0].split('_')[4]  for FileName in Radiographies]
SCD = [int(FileName[0].split('_')[5][:-5])  for FileName in Radiographies]
Modality = [FileName[0].split('_')[6]  for FileName in Radiographies]
Voltage = [float(FileName[0].split('_')[7][:-2]) for FileName in Radiographies]
mAs = [float(FileName[0].split('_')[8][:-3])  for FileName in Radiographies]
SourceExposuretime = [float(FileName[0].split('_')[9][:-6])
                      for FileName in Radiographies]
CMOSExposuretime = [float(FileName[0].split('_')[10][:-6])
                    for FileName in Radiographies]

# Prepare empty arrays for endresult
TotalSummedBrightness = numpy.empty(len(Experiment))
TotalMax = numpy.empty(len(Experiment))
TotalMean = numpy.empty(len(Experiment))
TotalSTD = numpy.empty(len(Experiment))
CorrectedImages = numpy.empty([Size[0][0], Size[0][1], len(Experiment)])

# Results for each exposure time
plt.ion()
for counter, item in enumerate(Experiment):
    # First figure shows single frames and plot of max, mean and STD with an
    # appropriate size
    plt.figure(figsize=(NumberOfRadiographies[counter], 5))
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
    logfile.info('\t* with a size of %s x %s pixels each', Size[counter][1],
        Size[counter][0])
    logfile.info('\t* recorded with an exposure time of %s ms',
        CMOSExposuretime[counter])
    logfile.info('-----')
    print 'Loading', len(Radiographies[counter]), 'images'
    # Load all images and calculate max, mean and STD. Write info to logfile
    Images = [numpy.fromfile(Image, dtype=numpy.uint16).reshape(Size[counter])
              for Image in Radiographies[counter]]
    ImageMax = [i.max() for i in Images]
    ImageMean = [i.mean() for i in Images]
    ImageSTD = [i.std() for i in Images]
    # Initialize Images with the full size of the dataset and set every value
    # to either zero or NAN. This way we can afterwards either just sum the
    # images or use numpy.nanmean (which ignores NaNs) to calculate the mean of
    # the dark images
    DarkImage = numpy.empty([Size[counter][0], Size[counter][1],
        NumberOfRadiographies[counter]])
    DarkImage[:] = numpy.NAN
    SummedImage = numpy.zeros([Size[counter][0], Size[counter][1],
        NumberOfRadiographies[counter]])
    DarkCounter = 0
    ImageCounter = 0
    Threshold = numpy.min(ImageMean) * 1.618
    # Go through each image and put it either to SummedImage or DarkImage. This
    # can probably be done in a more pythonic way, but a loop works just fine.
    for c, Image in enumerate(Images):
        print 'Image', c + 1, 'of', NumberOfRadiographies[counter],
        # Select images which are a bit brighter than the mean of the darkest
        if Image.mean() > Threshold:
            ImageCounter += 1
            plt.subplot(3, len(Images), 1 + c)
            SummedImage[:, :, c] = Image
            print 'contains image data'
            logfile.info('%s of %s: Mean: %s,\tMax: %s,\tSTD: %s\t--> Image',
                str(c).rjust(2), len(Radiographies[counter]),
                ("%.2f" % round(ImageMean[c], 2)).rjust(6),
                str(ImageMax[c]).rjust(4),
                ("%.2f" % round(ImageSTD[c], 2)).rjust(6))
        else:
            DarkCounter += 1
            plt.subplot(3, len(Images), len(Images) + 1 + c)
            # We probably need to add something like the mean dark image
            # For the moment just adding "part" of the dark image fo the total
            # dataset...
            DarkImage[:, :, c] = Image
            print 'is a dark image'
            logfile.info('%s of %s: Mean: %s,\tMax: %s,\tSTD: %s\t--> Dark',
                str(c).rjust(2), len(Radiographies[counter]),
                ("%.2f" % round(ImageMean[c], 2)).rjust(6),
                str(ImageMax[c]).rjust(4),
                ("%.2f" % round(ImageSTD[c], 2)).rjust(6))
        # Show each frame (either on bottom or top)
        plt.imshow(Image, cmap='gray')
        plt.axis('off')
        plt.title(' '.join(['Img', str(ImageSTD.index(Image.std())), '\nMean',
            str(int(round(ImageMean[c])))]))
    logfile.info('-----')
    logfile.info('We have')
    logfile.info('\t* %s dark images (Mean below or equal to Threshold of %s)',
        DarkCounter, round(Threshold, 2))
    logfile.info('\t* %s images (Mean above Threshold of %s)', ImageCounter,
        round(Threshold, 2))
    logfile.info('-----')
    # Show max, mean and STD below, with some alignment tweaks so they line up
    plt.subplot(313)
    plt.plot(ImageMax, marker='o', label='max')
    plt.plot(ImageMean, marker='o', label='mean')
    plt.plot(ImageSTD, marker='o', label='STD')
    plt.title(' '.join(['Image characteristics for an exposure time of',
        ("%.2f" % CMOSExposuretime[counter]).zfill(6), 'ms']))
    plt.axhline(Threshold, label='selection threshold', color='g',
        linestyle='--')
    plt.xlim([-0.5, NumberOfRadiographies[counter] - 0.5])
    plt.legend(loc='best')
    plt.tight_layout()
    plt.subplots_adjust(hspace=.05)
    plt.subplots_adjust(wspace=.05)
    print 'Saving image with all frames and values'
    plt.savefig(os.path.join(os.path.dirname(Experiment[counter]),
        'Exposuretime_' + os.path.basename(Experiment[counter]) + '.png'))
    logfile.info('In %s you now have these images:',
        os.path.dirname(Experiment[counter]))
    logfile.info('\t* Overview image as %s',
        'Exposuretime_' + os.path.basename(Experiment[counter]) + '.png')
    # Second figure with Darks and Projections
    # Calculate the sum or mean of the images from above.
    SummedImage = numpy.sum(SummedImage, axis=2)
    DarkImage = numpy.nanmean(DarkImage, axis=2)
    # Show image
    plt.figure(figsize=(16, 6))
    plt.subplot(131)
    plt.imshow(DarkImage, cmap='gray')
    plt.axis('off')
    plt.title(' '.join(['Sum of', str(DarkCounter), 'dark images @',
        ("%.2f" % CMOSExposuretime[counter]).zfill(6), 'ms']))
    plt.subplot(132)
    plt.imshow(SummedImage, cmap='gray')
    plt.axis('off')
    plt.title(' '.join(['Sum of', str(ImageCounter), 'images @',
        ("%.2f" % CMOSExposuretime[counter]).zfill(6), 'ms']))
    plt.subplot(133)
    plt.imshow(SummedImage - DarkImage, cmap='gray')
    plt.axis('off')
    plt.title(' '.join(['Sum of images - sum of dark images @',
                        ("%.2f" % CMOSExposuretime[counter]).zfill(6), 'ms']))
    plt.subplots_adjust(left=.05)
    plt.subplots_adjust(right=1 - .05)
    plt.subplots_adjust(bottom=.05)
    plt.subplots_adjust(top=1 - .05)
    plt.tight_layout()
    # Save figure and single frames as images
    print 'Saving image showing dark, frames and corrected frames'
    plt.savefig(os.path.join(os.path.dirname(Experiment[counter]),
        'Exposuretime_' + os.path.basename(Experiment[counter]) +
        '_Images.png'))
    logfile.info('\t* Dark/Sum/Corrected figure as %s',
        'Exposuretime_' + os.path.basename(Experiment[counter]) +
        '_Images.png')
    print 'Saving mean dark frame'
    scipy.misc.imsave(os.path.join(os.path.dirname(Experiment[counter]),
        'Exposuretime_' + os.path.basename(Experiment[counter]) +
        '_Frame-Dark_' + ("%.2f" % CMOSExposuretime[counter]).zfill(6) +
        'ms.tif'), DarkImage)
    logfile.info('\t* Mean dark frames as %s',
        'Exposuretime_' + os.path.basename(Experiment[counter]) +
        '_Frame-Dark_' + ("%.2f" % CMOSExposuretime[counter]).zfill(6) +
        'ms.tif')
    print 'Saving summed images frame'
    scipy.misc.imsave(os.path.join(os.path.dirname(Experiment[counter]),
        'Exposuretime_' + os.path.basename(Experiment[counter]) +
        '_Frame-Images_' + ("%.2f" % CMOSExposuretime[counter]).zfill(6) +
        'ms.tif'), SummedImage)
    logfile.info('\t* Summed images frame as %s',
        'Exposuretime_' + os.path.basename(Experiment[counter]) +
        '_Frame-Images_' + ("%.2f" % CMOSExposuretime[counter]).zfill(6) +
        'ms.tif')
    print 'Saving summed images minus mean dark frame'
    scipy.misc.imsave(os.path.join(os.path.dirname(Experiment[counter]),
        'Exposuretime_' + os.path.basename(Experiment[counter]) +
        '_Frame-Corrected_' + ("%.2f" % CMOSExposuretime[counter]).zfill(6) +
        'ms.tif'), SummedImage - DarkImage)
    logfile.info('\t* Corrected images frame as %s',
        'Exposuretime_' + os.path.basename(Experiment[counter]) +
        '_Frame-Corrected_' + ("%.2f" % CMOSExposuretime[counter]).zfill(6) +
        'ms.tif')
    # Save the max, mean and std of the corrected image for inter-exposure-time
    # analyisis
    # Add up all pixels for corrected image
    TotalSummedBrightness[counter] = numpy.sum(SummedImage - DarkImage)
    # Save max, mean and std of corrected image
    TotalMax[counter] = (SummedImage - DarkImage).max()
    TotalMean[counter] = (SummedImage - DarkImage).mean()
    TotalSTD[counter] = (SummedImage - DarkImage).std()
    CorrectedImages[:, :, counter] = SummedImage - DarkImage

    # Close images if desired, otherwise you need to manually clos'em
    autopilot = False
    if autopilot:
        plt.draw()
        plt.close('all')
    else:
        plt.ioff()
        plt.show()

# reread all corrected images
CorrectedImages = glob.glob(os.path.join(StartingFolder, '*Frame-Corrected_*'))

# Sort all lists according to the exposure time:
# http://stackoverflow.com/a/6618543/323100
CorrectedImages = [x for (y, x) in
    sorted(zip(CMOSExposuretime, CorrectedImages))]
TotalMax = numpy.asarray([x for (y, x) in
    sorted(zip(CMOSExposuretime, TotalMax))])
TotalMean = numpy.asarray([x for (y, x) in
    sorted(zip(CMOSExposuretime, TotalMean))])
TotalSTD = numpy.asarray([x for (y, x) in
    sorted(zip(CMOSExposuretime, TotalSTD))])
TotalSummedBrightness = numpy.asarray([x for (y, x) in
    sorted(zip(CMOSExposuretime, TotalSummedBrightness))])

print 'Displaying final result'
# Final result
plt.ioff()
plt.figure(figsize=(16, 9))
for i in range(len(Experiment)):
    plt.subplot(2, len(Experiment), i + 1)
    plt.imshow(plt.imread(CorrectedImages[i]), cmap='gray')
    plt.title(' '.join([str(i), '\n', str(sorted(CMOSExposuretime)[i]),
        'ms']))
    plt.axis('off')
    plt.subplots_adjust(hspace=.05)
    plt.subplots_adjust(wspace=.05)
    plt.subplots_adjust(left=.05)
    plt.subplots_adjust(right=1 - .05)
    plt.subplots_adjust(bottom=.05)
    plt.subplots_adjust(top=1 - .05)
plt.subplot(212)
plt.plot(TotalSummedBrightness, marker='o', label='Total Brightness')
plt.plot(TotalMax, marker='o', label='Total Max')
plt.plot(TotalMean, marker='o',
    label='Total Mean (brightness *per* pixel)')
plt.plot(TotalSTD, marker='o', label='Total STD')
plt.xlim([-0.5, len(Experiment) - 0.5])
plt.legend(loc='best')
plt.savefig(os.path.join(StartingFolder, 'Exposuretime_Result.png'))
plt.show()
