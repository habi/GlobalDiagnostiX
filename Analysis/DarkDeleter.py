#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script to delete unused darks of each image.
For each experiment we acquire something like 30 images, from which only about
3 to four contain data, the rest of the images are darks.
We don't have to keep all the darks, one at the beginning, one at the end and
one in the middle is probably plenty.

The detection of folders and other things are based on
DetectWhichImageIsRadiography.py
"""

import glob
import os
import logging
import time
import numpy

# Setup
ReallyRemove = True

# Where shall we start?
RootFolder = ('/afs/psi.ch/project/EssentialMed/MasterArbeitBFH/' +
    'XrayImages')
StartingFolder = os.path.join(RootFolder, '20140724')


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
        not 'Toshiba' in os.path.basename(root) and \
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

AnalyisList = []
AnalyisList = range(len(Experiment))

# Go through each selected experiment
for Counter, SelectedExperiment in enumerate(AnalyisList):
    # Inform the user and start logging
    print 80 * '-'
    #~ print str(Counter + 1) + '/' + str(len(AnalyisList)) + \
        #~ ': Deleting darks experiment', ExperimentID[SelectedExperiment]
    logfile = myLogger(os.path.dirname(Experiment[SelectedExperiment]),
        ExperimentID[SelectedExperiment] + '.deletion.log')

    # Go through the log file. Under the 'Details' section we specify if the
    # image is a 'Dark' or was used ('Image'). Save 'Image's, adjacent 'Dark's
    # and the second 'Dark', delete the rest.
    AnalysisLogFile = os.path.join(
        os.path.dirname(Experiment[SelectedExperiment]),
        'Analysis_' + ExperimentID[SelectedExperiment] + '.log')
    Keepers = []
    for line in open(AnalysisLogFile, 'r'):
        if len(line.split('-->')) == 2:
            FileNumber = int(line.split('/')[0])
            if line.split('--> ')[1].strip() == 'Image':
                # Keep 'Image' and the 'Dark' adjacent to the 'Image's
                Keepers.append(FileNumber - 1)
                Keepers.append(FileNumber)
                Keepers.append(FileNumber + 1)
    print 'For Experiment', ExperimentID[SelectedExperiment], 'in folder', \
        Experiment[SelectedExperiment][len(StartingFolder):]
    # Always keep second image
    Keepers.append(2)
    Keepers = numpy.unique(Keepers)
    print 'We keep', len(Keepers), 'images and delete', \
        NumberOfRadiographies[SelectedExperiment] - len(Keepers),  'images'
    if NumberOfRadiographies[SelectedExperiment] - len(Keepers) > 1:
        # When we have as many files left as we have 'Keepers' we most probably
        # have already done a deletion round, then the 'if' clause above
        # evaluates to 'True'
        logfile.info(
            'Deletion log file for Experiment ID %s, deletion done on %s',
            ExperimentID[SelectedExperiment],
            time.strftime('%d.%m.%Y at %H:%M:%S'))
        logfile.info(80 * '-')
        logfile.info('Grabbing Information from %s', AnalysisLogFile)
        logfile.info(80 * '-')
        logfile.info('In the folder %s we keep image',
            Experiment[SelectedExperiment])
        for line in open(AnalysisLogFile, 'r'):
            if len(line.split('-->')) == 2:
                FileNumber = int(line.split('/')[0]) - 1
                if FileNumber in Keepers:
                    logfile.info('%s/%s | %s | with info "%s"',
                        str(FileNumber).rjust(2),
                        NumberOfRadiographies[SelectedExperiment],
                        os.path.basename(
                            Radiographies[SelectedExperiment][FileNumber - 1]),
                        line.strip())
        logfile.info(80 * '-')
        logfile.info('In the folder %s we delete image',
            Experiment[SelectedExperiment])
        for line in open(AnalysisLogFile, 'r'):
            if len(line.split('-->')) == 2:
                FileNumber = int(line.split('/')[0])
                if FileNumber not in Keepers:
                    logfile.info('%s/%s | %s | with info "%s"',
                        str(FileNumber).rjust(2),
                        NumberOfRadiographies[SelectedExperiment],
                        os.path.basename(
                            Radiographies[SelectedExperiment][FileNumber - 1]),
                        line.strip())
                    # Actually delete the image now
                    if ReallyRemove:
                        os.remove(
                            Radiographies[SelectedExperiment][FileNumber - 1])
    else:
        print 'We have as many Keepers as radiographies in the folder.', \
            'Either it does not make sense to delete any files or we', \
            'already did delete them...'
