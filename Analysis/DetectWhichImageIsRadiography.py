#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script to load the set of images acquired in the x-ray lab.
Since we acquire images before, during and after exposure it is really annoying
to manually sift through all the images in all the directories and to look for
the 'best' exposure.
This script loads each image in each directory, computes the mean of the images
and gives out the maximum of the this mean. This should be the 'best' exposed
image(s) of all the exposures.
Optionally, the stack of the best images can be opened in Fiji.
"""

from __future__ import division
import glob
import os
import matplotlib.pyplot as plt
import numpy
import logging
import time
import scipy.misc  # for saving png or tif at the end

# Setup
# If Manual selection is true, the user is asked to select one of the
# experiment IDs manually, otherwise the script just goes through all the IDs
# it finds in the starting folder
ManualSelection = False
# Where shall we start?
StartingFolder = ('/afs/psi.ch/project/EssentialMed/MasterArbeitBFH/' +
    'XrayImages')


def AskUser(Blurb, Choices):
    """ Ask for input. Based on function in MasterThesisIvan.ini """
    print(Blurb)
    for Counter, Item in enumerate(sorted(Choices)):
        print '    * [' + str(Counter) + ']:', Item
    Selection = []
    while Selection not in range(len(Choices)):
        try:
            Selection = int(input(' '.join(['Please enter the choice you',
                                            'want [0-' +
                                            str(len(Choices) - 1) +
                                            ']:'])))
        except:
            print 'You actually have to select *something*'
        if Selection not in range(len(Choices)):
            print 'Try again with a valid choice'
    print 'You selected', sorted(Choices)[Selection]
    return sorted(Choices)[Selection]


def myLogger(Folder, LogFileName):
    """
    Since logging in a loop does always write to the first instaniated file,
    we make a little wrapper around the logger function to have one log file
    per experient ID. Based on http://stackoverflow.com/a/2754216/323100
    """
    logger = logging.getLogger(LogFileName)
    # either set INFO or DEBUG
    #~ logger.setLevel(logging.DEBUG)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(os.path.join(Folder, LogFileName), 'w')
    logger.addHandler(handler)
    return logger


# Look for all folders matching the naming convention
Experiment = []
ExperimentID = []
for root, dirs, files in os.walk(StartingFolder):
    #~ print 'Looking for experiment IDs in folder', os.path.basename(root)
    if len(os.path.basename(root)) == 7 and \
        not 'MT9' in os.path.basename(root) and \
        not 'AR0' in os.path.basename(root):
        Experiment.append(root)
        ExperimentID.append(os.path.basename(root))

print 'I found', len(Experiment), 'experiment IDs in', StartingFolder
print 80 * '-'

# Get list of files in each folder, these are all the radiographies we acquired
# The length of this list is then obviously the number of radiographies
Radiographies = [sorted(glob.glob(os.path.join(Folder, '*.raw')))
                 for Folder in Experiment]
NumberOfRadiographies = [len(Radiographies[i])
                         for i in range(len(Experiment))]

# Warn if a directory is empty, i.e. contains 0 NumberOfRadiographies
# This most probably happened if DevWare crashed
EmptyOnes = [item == 0 for item in NumberOfRadiographies]
for counter, i in enumerate(Experiment):
    if EmptyOnes[counter]:
        print
        print 'Empty directory', i, 'found!'
        os.rmdir(i)
        exit(' '.join(['I deleted this folder, just start again. I will',
            'proceed or delete the next empty folder...']))

AnalyisList = []
if ManualSelection:
    # Ask the user which experimentID to show
    ## Concatenate the list for display purposes:
    ## http://stackoverflow.com/a/22642307/323100
    Choices = ['{} with {} images'.format(x, y)
               for x, y in zip(ExperimentID, NumberOfRadiographies)]
    Choice = AskUser('Which one do you want to look at?', Choices)
    AnalyisList.append(Choices.index(Choice))
    print
    plt.ion()
else:
    AnalyisList = range(len(Experiment))

# Go through each selected experiment
for Counter, SelectedExperiment in enumerate(AnalyisList):
    # Inform the user and start logging
    print 80 * '-'
    print str(Counter + 1) + '/' + str(len(AnalyisList)) + \
        ': Looking at experiment', ExperimentID[SelectedExperiment]
    logfile = myLogger(os.path.dirname(Experiment[SelectedExperiment]),
        'Analysis_' + ExperimentID[SelectedExperiment] + '.log')
    logfile.info('Log file for Experiment ID %s, Analsyis performed at %s',
        ExperimentID[SelectedExperiment],
        time.strftime('%d.%m.%Y at %H:%M:%S'))
    logfile.info('-----')
    logfile.info('All image files are to be found in %s', StartingFolder)
    logfile.info('This experiment ID can be found in the subfolder %s',
        Experiment[SelectedExperiment][len(StartingFolder):])
    logfile.info('-----')

    # Grab the information from the filenames
    Scintillator = Radiographies[SelectedExperiment][0].split('_')[1]
    Sensor = Radiographies[SelectedExperiment][0].split('_')[2]
    Size = [int(Radiographies[SelectedExperiment][0].split('_')[3].
        split('x')[1]),
            int(Radiographies[SelectedExperiment][0].split('_')[3].
        split('x')[0])]
    Lens = Radiographies[SelectedExperiment][0].split('_')[4]
    SCD = int(Radiographies[SelectedExperiment][0].split('_')[5][:-5])
    Modality = Radiographies[SelectedExperiment][0].split('_')[6]
    Voltage = float(Radiographies[SelectedExperiment][0].split('_')[7][:-2])
    mAs = float(Radiographies[SelectedExperiment][0].split('_')[8][:-3])
    SourceExposuretime = \
        float(Radiographies[SelectedExperiment][0].split('_')[9][:-6])
    CMOSExposuretime = \
        float(Radiographies[SelectedExperiment][0].split('_')[10][:-6])

    # Inform the user some more and log some more
    print '    * with', NumberOfRadiographies[SelectedExperiment], 'images'
    print '    * in the folder', \
        os.path.dirname(os.path.relpath(Experiment[SelectedExperiment],
                        StartingFolder))

    print '    * conducted with the', Scintillator, 'scintillator,'
    print '    *', Sensor, 'CMOS with an exposure time of', CMOSExposuretime,\
        'ms'
    print '    * source exposure time of', SourceExposuretime, 'ms'
    print '    *', Lens, 'lens for the'
    print '    *', Modality, 'and calculating their mean'

    logfile.info('Scintillator: %s', Scintillator)
    logfile.info('Sensor: %s', Sensor)
    logfile.info('Lens: %s', Lens)
    logfile.info('Image size: %s x %s px', Size[1], Size[0])
    logfile.info('Scintillator-Sensor distance: %s mm', SCD)
    logfile.info('Modality: %s', Modality)
    logfile.info('Source kV: %s', Voltage)
    logfile.info('Source mAs: %s', mAs)
    logfile.info('Source expsure time: %s ms', SourceExposuretime)
    logfile.info('CMOS exposure time: %s ms', CMOSExposuretime)
    logfile.info('-----')

    # Read images and calculate max, mean, STD and dark/img-threshold
    print 'Reading images,',
    Images = [numpy.fromfile(Image, dtype=numpy.uint16).reshape(Size)
                 for Image in Radiographies[SelectedExperiment]]
    print 'calculating max,',
    ImageMax = [i.max() for i in Images]
    print 'calculating mean',
    ImageMean = [i.mean() for i in Images]
    print 'and standard deviation'
    ImageSTD = [i.std() for i in Images]
    Threshold = numpy.min(ImageMean) * 1.618

    # Split images in "real" and dark images
    print 'Selecting dark frames and image frames'
    RealImages = [i for i in Images if i.mean() > Threshold]
    DarkImages = [i for i in Images if i.mean() <= Threshold]
    logfile.info('We have')
    logfile.info('\t* %s dark images (Mean below or equal to Threshold of %s)',
        len(DarkImages), round(Threshold, 2))
    logfile.info('\t* %s images (Mean above Threshold of %s)', len(RealImages),
        round(Threshold, 2))
    for c, Image in enumerate(Images):
        if ImageMean[c] == max(ImageMean):
            logfile.info('With image %s being the brightest one', c + 1)
            logfile.info('\t* Filename: %s',
                os.path.basename(Radiographies[SelectedExperiment][c]))
            logfile.info('\t* Max: %s', round(ImageMax[c], 3))
            logfile.info('\t* Mean: %s', round(ImageMean[c], 3))
            logfile.info('\t* STD: %s', round(ImageSTD[c], 3))
    logfile.info('-----')

    # Calculate final images (if it makes sense, otherwise stop)
    MeanDarkImage = numpy.mean(DarkImages, axis=0)
    if len(RealImages) == 0:
        # If no image above selection threshold, then break the loop, since the
        # result will be bogus
        print
        print '\tImage', ImageMean.index(max(ImageMean)), 'is the brightest',\
            'image of experiment', ExperimentID[SelectedExperiment]
        print '\tIts mean of',  round(max(ImageMean), 2), \
            'is below the selection threshold of', round(Threshold, 2)
        print '\tIt is probably safe to delete the whole directory...'
        logfile.info('You can delete directory %s',
            Experiment[SelectedExperiment])
        logfile.info('-----')
        print '\tI am using this *single* image as "result"'
        print
        SummedImage = Images[ImageMean.index(max(ImageMean))]
        logfile.info('Using image %s with a mean of %s as result',
            ImageMean.index(max(ImageMean)),
            round(ImageMean[ImageMean.index(max(ImageMean))], 2))
        logfile.info('-----')
    else:
        SummedImage = numpy.sum(RealImages, axis=0)

    CorrectedImage = SummedImage - MeanDarkImage

    # Show images to the user
    if ManualSelection:
        print 'Showing images'
    else:
        print 'Writing images'
    logfile.info('Details of the %s images for experiment ID %s',
        NumberOfRadiographies[SelectedExperiment],
        ExperimentID[SelectedExperiment])
    plt.figure(num=1, figsize=[NumberOfRadiographies[SelectedExperiment], 5])
    for c, Image in enumerate(Images):
        if Image.mean() > Threshold:
            #~ print 'above threshold'
            plt.subplot(3, len(Images), c + 1)
            logfile.info('%s/%s: Mean: %s,\tMax: %s,\tSTD: %s\t--> Image',
                str(c + 1).rjust(2), len(Radiographies[Counter]),
                ("%.2f" % round(ImageMean[c], 2)).rjust(6),
                str(ImageMax[c]).rjust(4),
                ("%.2f" % round(ImageSTD[c], 2)).rjust(6))
        else:
            #~ print 'below threshold'
            plt.subplot(3, len(Images), len(Images) + c + 1)
            logfile.info('%s/%s: Mean: %s,\tMax: %s,\tSTD: %s\t--> Dark',
                str(c + 1).rjust(2), len(Radiographies[Counter]),
                ("%.2f" % round(ImageMean[c], 2)).rjust(6),
                str(ImageMax[c]).rjust(4),
                ("%.2f" % round(ImageSTD[c], 2)).rjust(6))
        plt.imshow(Image, cmap='gray')
        plt.axis('off')
        plt.title(' '.join(['img', str(c), '\nmx', str(round(ImageMax[c], 1)),
            '\nmn', str(round(ImageMean[c], 1))]))
    logfile.info('-----')
    plt.subplot(313)
    plt.plot(ImageMax, marker='o', label='max')
    plt.plot(ImageMean, marker='o', label='mean')
    plt.plot(ImageSTD, marker='o', label='STD')
    plt.title(' '.join(['Image characteristics for an exposure time of',
        ("%.2f" % CMOSExposuretime).zfill(6), 'ms']))
    plt.axhline(Threshold, label='selection threshold', color='g',
        linestyle='--')
    plt.xlim([-0.5, NumberOfRadiographies[Counter] - 0.5])
    plt.legend(loc='best')
    plt.tight_layout()
    plt.subplots_adjust(hspace=.05)
    plt.subplots_adjust(wspace=.05)
    # Save figure
    plt.draw()
    SaveFigName = os.path.join(os.path.dirname(Experiment[SelectedExperiment]),
                'Analysis_' + ExperimentID[SelectedExperiment] +
                '_Overview_All.png')
    plt.savefig(SaveFigName)
    logfile.info('Overview plot saved as %s', os.path.basename(SaveFigName))

    plt.figure(num=2, figsize=[16, 9])
    # Show images above threshold
    for ctr, i in enumerate(RealImages):
        plt.subplot(3, len(RealImages), ctr + 1)
        plt.imshow(i, cmap='gray')
        plt.axis('off')
        plt.title(' '.join(['Proj', str(ctr)]))
    # Show images below threshold
    for ctr, d in enumerate(DarkImages):
        plt.subplot(3, len(DarkImages), len(DarkImages) + ctr + 1)
        plt.imshow(d, cmap='gray')
        plt.axis('off')
        plt.title(' '.join(['Drk', str(ctr)]))
    # Show average darks
    plt.subplot(337)
    plt.imshow(MeanDarkImage, cmap='gray')
    plt.axis('off')
    plt.title(' '.join(['Average of', str(len(DarkImages)), 'dark images']))
    # Show summed projections
    plt.subplot(338)
    plt.imshow(SummedImage, cmap='gray')
    plt.axis('off')
    plt.title(' '.join([str(len(RealImages)), 'summed projections']))
    plt.subplot(339)
    plt.imshow(CorrectedImage, cmap='gray')
    plt.axis('off')
    plt.title(' '.join([str(len(RealImages)), 'projections -',
        str(len(DarkImages)), 'darks']))
    # Save figure
    plt.draw()
    SaveFigName = os.path.join(os.path.dirname(Experiment[SelectedExperiment]),
                'Analysis_' + ExperimentID[SelectedExperiment] +
                '_Overview_DarkFlatsCorrected.png')
    plt.savefig(SaveFigName)
    logfile.info('Dark/Flats/Corrected plot saved as %s',
        os.path.basename(SaveFigName))
    logfile.info('-----')
    if ManualSelection:
        plt.show()

    # Save corrected images
    print 'Saving mean dark frame'
    DarkName = os.path.join(os.path.dirname(Experiment[SelectedExperiment]),
                'Analysis_' + ExperimentID[SelectedExperiment] + '_Dark.tif')
    scipy.misc.imsave(DarkName, MeanDarkImage)
    logfile.info('Mean of %s dark frames saved as %s', len(DarkImages),
        DarkName)
    print 'Saving summed images'
    SummedName = os.path.join(os.path.dirname(Experiment[SelectedExperiment]),
                'Analysis_' + ExperimentID[SelectedExperiment] + '_Images.tif')
    scipy.misc.imsave(SummedName, SummedImage)
    logfile.info('Sum of %s image frames saved as %s', len(RealImages),
        SummedName)
    print 'Saving corrected image'
    CorrName = os.path.join(os.path.dirname(Experiment[SelectedExperiment]),
                'Analysis_' + ExperimentID[SelectedExperiment] +
                '_Corrected.tif')
    scipy.misc.imsave(CorrName, CorrectedImage)
    logfile.info('Sum of %s images subtracted with the mean of %s dark ' +
        'frames saved as %s', len(RealImages), len(DarkImages), CorrName)

    if ManualSelection:
        plt.ioff()
        plt.show()
    else:
        plt.close(1)
        plt.close(2)
