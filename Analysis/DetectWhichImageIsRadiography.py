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
import subprocess
import matplotlib.pyplot as plt
import numpy
import shutil


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

StartingFolder = ('/afs/psi.ch/project/EssentialMed/' +
    'MasterArbeitBFH/XrayImages')

Experiment = []
ExperimentID = []
for root, dirs, files in os.walk(StartingFolder):
    #~ print 'Looking for experiment IDs in folder', os.path.basename(root)
    if len(os.path.basename(root)) == 7 and \
        not 'MT9' in os.path.basename(root) and \
        not 'AR0' in os.path.basename(root):
        Experiment.append(root)
        ExperimentID.append(os.path.basename(root))

print 'I found', len(Experiment), 'experiment IDs'

# Get list of files in each folder, these are all the radiographies we acquired
Radiographies = [sorted(glob.glob(os.path.join(Folder, '*.raw')))
                 for Folder in Experiment]

NumberOfRadiographies = [len(Radiographies[i])
                         for i in range(len(Experiment))]

# Inform user what we found
print 'We found these experiment IDs in', os.path.commonprefix(Experiment)
for counter, i in enumerate(Experiment):
    print os.path.basename(i)
    print '    * with', NumberOfRadiographies[counter], 'images'
    print '    * in the folder', \
        os.path.dirname(os.path.relpath(i, StartingFolder))

# Concatenate the list for display purposes:
# http://stackoverflow.com/a/22642307/323100
Choices = ['{} with {} images'.format(x,y) for x,y in zip(ExperimentID, NumberOfRadiographies)]
Choice = AskUser('Which one do you want to look at?', Choices)
SelectedExperiment = Choices.index(Choice)

Scintillator = Radiographies[SelectedExperiment][0].split('_')[1]
Sensor = Radiographies[SelectedExperiment][0].split('_')[2]
Size = [int(Radiographies[SelectedExperiment][0].split('_')[3].split('x')[1]),
        int(Radiographies[SelectedExperiment][0].split('_')[3].split('x')[0])]
Lens = Radiographies[SelectedExperiment][0].split('_')[4]
SCD = int(Radiographies[SelectedExperiment][0].split('_')[5][:-5])
Modality = Radiographies[SelectedExperiment][0].split('_')[6]
Voltage = float(Radiographies[SelectedExperiment][0].split('_')[7][:-2])
mAs = float(Radiographies[SelectedExperiment][0].split('_')[8][:-3])
SourceExposuretime = float(Radiographies[SelectedExperiment][0].split('_')[9][:-6])
CMOSExposuretime = float(Radiographies[SelectedExperiment][0].split('_')[10][:-6])


print 'Loading', NumberOfRadiographies[SelectedExperiment], \
    'images of experiment ID', ExperimentID[SelectedExperiment], \
    'conducted with the', Scintillator, 'scintillator, ', Sensor, 'CMOS,', \
    Lens, 'lens for the', Modality, 'and calculating their mean'

plt.ion()
plt.figure()
for Counter, File in enumerate(Radiographies[SelectedExperiment]):
    Image = numpy.fromfile(File, dtype=numpy.uint16).reshape(Size)
    #~ Image -= numpy.mean(FromFile)
    plt.imshow(Image,cmap='gray')
    plt.title(' '.join(['Image', str(Counter), '/',
                        str(NumberOfRadiographies[SelectedExperiment])]))
    plt.draw()


plt.ioff()
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
