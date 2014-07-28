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

StartingFolder = ('/afs/psi.ch/project/EssentialMed/MasterArbeitBFH/' +
    'XrayImages')

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

ManualSelection = False
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
else:
    AnalyisList = range(len(Experiment))

# Go through each selected experiment
for Counter, SelectedExperiment in enumerate(AnalyisList):
    # Inform the user and start logging
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
    print '    *', Sensor, 'CMOS,'
    print '    *', Lens, 'lens for the'
    print '    *', Modality, 'and calculating their mean'

    logfile.info('Scintillator: %s', Scintillator)
    logfile.info('Sensor: %s', Sensor)
    logfile.info('Lens: %s', Lens)
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
    logfile.info('-----')

    # Calculate final images (if it makes sense, otherwise stop)
    MeanDarkImage = numpy.mean(DarkImages, axis=0)
    if len(RealImages) == 0:
        # If no image above selection threshold, then break the loop, since the
        # result will be bogus
        print
        print 'The brightest image of experiment', \
            ExperimentID[SelectedExperiment], 'has a mean of', \
            round(max(ImageMean), 2), \
            'which is below the selected threshold of', round(Threshold, 2)
        print 'It is probably safe to delete the whole directory...'
        logfile.info('You can delete directory %s',
            Experiment[SelectedExperiment])
        logfile.info('-----')
        SummedImage = numpy.sum(DarkImages, axis=0)
        SummedImage[:,:Size[1]] = max(ImageMax)
        SummedImage[:,Size[1]:] = 0
    else:
        SummedImage = numpy.sum(RealImages, axis=0)

    CorrectedImage = SummedImage - MeanDarkImage

    # Show images to the user
    print 'Showing images'
    logfile.info('Details of the %s images for experiment ID %s',
        NumberOfRadiographies[SelectedExperiment],
        ExperimentID[SelectedExperiment])
    plt.figure(figsize=[NumberOfRadiographies[SelectedExperiment], 5])
    for c, Image in enumerate(Images):
        #~ print str(c + 1).rjust(2) + '/' + str(len(Images)) + ':',
        if Image.mean() > Threshold:
            #~ print 'above threshold'
            plt.subplot(3, len(Images), c + 1)
            logfile.info('%s/%s: Mean: %s,\tMax: %s,\tSTD: %s\t--> Image',
                str(c).rjust(2), len(Radiographies[counter]),
                ("%.2f" % round(ImageMean[c], 2)).rjust(6),
                str(ImageMax[c]).rjust(4),
                ("%.2f" % round(ImageSTD[c], 2)).rjust(6))
            # Denote largest image
            if ImageMean[Counter] == max(ImageMean):
                logfile.info('\tImage %s is on average the brightest image', c)
                logfile.info('    * Max: %s', round(ImageMax[c], 3))
                logfile.info('    * Mean: %s', round(ImageMean[c], 3))
                logfile.info('    * STD: %s', round(ImageSTD[c], 3))
                logfile.info('-----')
        else:
            #~ print 'below threshold'
            plt.subplot(3, len(Images), len(Images) + c + 1)
            logfile.info('%s/%s: Mean: %s,\tMax: %s,\tSTD: %s\t--> Dark',
                str(c).rjust(2), len(Radiographies[counter]),
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
    plt.xlim([-0.5, NumberOfRadiographies[counter] - 0.5])
    plt.legend(loc='best')
    plt.tight_layout()
    plt.subplots_adjust(hspace=.05)
    plt.subplots_adjust(wspace=.05)
    plt.draw()
    # Save figure
    SaveFigName = os.path.join(os.path.dirname(Experiment[SelectedExperiment]),
                'Analysis_' + ExperimentID[SelectedExperiment] +
                '_Overview_All.png')
    plt.savefig(SaveFigName)
    logfile.info('Overview plot saved as %s', os.path.basename(SaveFigName))

    plt.figure(figsize=[16, 9])
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
    print CorrName
    scipy.misc.imsave(CorrName, CorrectedImage)
    logfile.info('Sum of %s images subtracted with the mean of %s dark ' +
        'frames saved as %s', len(RealImages), len(DarkImages), CorrName)

exit()


# Setup
# Show the plot with the means. The plot is saved regardless of this setting
ShowPlot = True
# Load the images as a stack in Fiji
ShowStack = True
# Threshold X to delete folders
#   * with images with a mean smaller than X,
#   * where the darkest and brightest image differ by only X grey levels
#   * and images which are darker than 10X % of the second darkest image
Threshold = 5
# Delete Images or not
Delete = False

# Get list of files in each folder, these are the exposures we acquired
Exposures = [sorted(glob.glob(os.path.join(Folder, '*.jpg')))
             for Folder in FolderList]

# Iterate through each folder, calculate the mean of each image in it and plot
# this mean. 'os.walk' includes the base directory, we thus start from 1.
for i in range(1, len(Exposures)):
    plt.figure(figsize=[16, 9])
    print 20 * '-', i, '/', len(Exposures) - 1, 20 * '-'
    print 'Getting the mean of', len(Exposures[i]), 'Images from', \
        os.path.basename(FolderList[i])
    MeanValue = [plt.imread(Image).mean() for Image in Exposures[i]]
    print 'The mean value of the images varies between', \
        round(min(MeanValue), 2), 'and', round(max(MeanValue), 2)
    print 'A maximum of', round(max(MeanValue), 2), 'was found in image', \
        MeanValue.index(max(MeanValue)), 'which corresponds to', \
        os.path.basename(Exposures[i][MeanValue.index(max(MeanValue))])
    # We plot the mean on the left side of a figure, with some additiona
    # information on it (Maximum and deletion criterion defined by
    # 'Threshold').
    plt.subplot(1, 2, 1)
    plt.plot(MeanValue, label='Mean Value', marker='o')
    plt.axhline(y=max(MeanValue), color='g',
                label=''.join(['Max@', str(round(max(MeanValue), 2))]))
    plt.axhline(y=sorted(MeanValue)[1] * (1 + Threshold / 100), color='r',
                label=''.join(['Deletion<',
                               str(round(sorted(MeanValue)[1] *
                                             (1 + Threshold / 100), 2))]))
    plt.legend(loc=4)
    plt.xlabel('Mean')
    plt.ylabel('Image index')
    plt.title(' '.join(['Mean of', str(len(Exposures[i])),
                        'images in\n',
                        str(os.path.basename(FolderList[i]))]))
    plt.ylim(ymin=0)
    # The right side of the plot shows the image in which we found the highest
    # mean and the two adjacent ones (if present).
    plt.subplot(3, 2, 2)
    try:
        plt.imshow(plt.imread(Exposures[i][MeanValue.index(max(MeanValue)) -
                                           1]), origin='lower')
    except LookupError:
        print os.path.basename(Exposures[i][MeanValue.index(max(MeanValue))]
                                ), '-1 could not be loaded'
    plt.title(' '.join(['maximal value of', str(round(max(MeanValue), 2)),
                        '\nfound in',
                        str(os.path.basename(
                            Exposures[i][MeanValue.index(max(MeanValue))])),
                        '\nshowing this image (middle) and the two adjacent']))
    plt.subplot(3, 2, 4)
    plt.imshow(plt.imread(Exposures[i][MeanValue.index(max(MeanValue))]),
               origin='lower')
    plt.subplot(3, 2, 6)
    try:
        plt.imshow(plt.imread(Exposures[i][MeanValue.index(max(MeanValue)) +
                                           1]), origin='lower')
    except LookupError:
        print os.path.basename(Exposures[i][MeanValue.index(max(MeanValue))]
                                ), '+1 could not be loaded'
    plt.savefig(os.path.join(StartingFolder,
                             os.path.basename(FolderList[i]) + '.pdf'))
    if ShowPlot:
        plt.show()
    # After the plotting, we elete unnecessary files. But we only delete, if we
    # have more than 20 images still present in the current folder
    #   * Delete the whole image directory if *all* images are below
    #   'Threshold' Threshold
    #   * Delete the whole image directory if the darkest and brightest image
    #     have a difference of less than 'Threshold'
    #   * Delete all images with are not 'Threshold'-% brighter than the
    #     *second*-darkest image
    # See if all images are smaller than 'Threshold'. If yes, remove directory
    if max(MeanValue) < Threshold:
        print
        print 'None of the images has a mean larger than the Threshold of', \
            str(Threshold) + '.'
        print 'I am thus deleting the whole directory...'
        shutil.rmtree(FolderList[i])
    # See if brightest and darkest image differ by more than 'Threshold'. If
    # not, delete the whole directory
    elif (max(MeanValue) - min(MeanValue)) < Threshold:
        print
        print 'The mean of the brightest (' + str(round(max(MeanValue), 2)) +\
            ') and the darkest image (' + str(round(min(MeanValue), 2)) +\
            ') have a difference smaller than', str(Threshold) + '.'
        print 'I am thus deleting the whole directory...'
        shutil.rmtree(FolderList[i])
    # Delete images which are darker than a bit more than the second-darkest
    # image, these are generally just noise/background.
    else:
        print 'Looking for images with a mean value between the minimum (' +\
            str(round(min(MeanValue), 2)) + ') and', 100 + Threshold,\
            '% of the second-brightest image (' +\
            str(round(sorted(MeanValue)[1] * (1 + Threshold / 100), 2)) + ')'
        # Create a list of which file can be deleted
        Deletion = [Mean < sorted(MeanValue)[1] * (1 + Threshold / 100)
                    for Mean in MeanValue]
        for File in range(len(Exposures[i])):
            print os.path.basename(Exposures[i][File]), \
                'has a mean of', round(MeanValue[File], 2), 'and',
            if Deletion[File]:
                # Only delete if we have more than 15 images in the folder
                if Delete and len(Exposures[i]) > 15:
                    print 'is deleted'
                    os.remove(Exposures[i][File])
                else:
                    print 'could be deleted'
            else:
                print 'is kept'

    # Open the remaining images as a stack in Fiji, if desired
    if ShowStack:
    # First check if the folder still exists, otherwise don't do anything
        if os.path.isdir(FolderList[i]):
            # Constructing Fiji call. We open Fiji in the current directory (so
            # saving is in that one), open all the images in that directory
            # as stack and save it out as _average.tif and _sum.tif.
            viewcommand = '/scratch/Fiji.app/ImageJ-linux32 -eval' +\
                ' "run(\\"Image Sequence...\\", \\"open=' +\
                os.path.abspath(FolderList[i]) + ' file=snapshot' +\
                ' convert\\"); run(\\"Z Project...\\",' +\
                ' \\"projection=[Average Intensity]\\"); run(\\"Save\\",' +\
                ' \\"save=' + os.path.join(os.path.abspath(FolderList[i]),
                                                           '_average.tif') +\
                '\\"); run(\\"Close\\"); run(\\"Z Project...\\",' +\
                ' \\"projection=[Sum Slices]\\"); run(\\"Save\\", \\"save=' +\
                os.path.join(os.path.abspath(FolderList[i]), '_sum.tif') +\
                '\\"); run(\\"Close\\");"'
            print 'Starting Fiji with the command'
            print '---'
            print viewcommand
            print '---'
            print 'Quit Fiji to proceed...'

            with open(os.devnull, 'wb') as devnull:
                subprocess.call(viewcommand, stdout=devnull,
                                stderr=subprocess.STDOUT, shell=True)
