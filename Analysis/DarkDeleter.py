# -*- coding: utf-8 -*-

"""
Script to delete unused darks of each image.
For each experiment we acquire something like 30 images, from which only about
3 to 4 contain data, the rest of the images are darks.
We don't have to keep all the darks; this script deletes all but one at the
beginning and the two darks adjacent to the images with signal.

The detection of folders and other things are based on
DetectWhichImageIsRadiography.py
"""

import glob
import os
import time
import numpy
import sys

from functions import get_experiment_list
from functions import AskUser
from functions import get_git_hash
from functions import myLogger

# Setup
ReallyRemove = True

# If running at the office, grep AFS
RootFolder = ('/afs/psi.ch/project/EssentialMed/MasterArbeitBFH/' +
    'XrayImages')
# Look for images of only one scintillator
StartingFolder = os.path.join(RootFolder, 'AppScinTechHE')
StartingFolder = os.path.join(RootFolder, 'Hamamatsu')
StartingFolder = os.path.join(RootFolder, 'Pingseng')
StartingFolder = os.path.join(RootFolder, 'Toshiba')
# Look through all folders
StartingFolder = RootFolder

# Look for all folders matching the naming convention
Experiment, ExperimentID = get_experiment_list(StartingFolder)
print 'I found', len(Experiment), 'experiment IDs in', StartingFolder

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
    # See if TarToArchive.py was already run on this experiment
    ArchivalLog = os.path.join(
        os.path.dirname(Experiment[SelectedExperiment]),
        ExperimentID[SelectedExperiment] + '.archive.log')
    if not os.path.isfile(ArchivalLog):
        ReallyRemove = False
        print 'I could not find an archival log file for experiment', \
            ExperimentID[SelectedExperiment], 'at', ArchivalLog
        print 'I thus set "ReallyRemove" to false'
        print
        print 'Please archive the data for this Experiment with',\
            'TarToArchive.py, then run this script again'
        time.sleep(5)
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
        ExperimentID[SelectedExperiment] + '.analysis.log')
    if not os.path.isfile(AnalysisLogFile):
        print 'The analysis of experiment', \
            ExperimentID[SelectedExperiment], 'has not been done yet'
        print 'Run DetectWhichImageIsRadiography.py on', \
            Experiment[SelectedExperiment]
        break
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
        Experiment[SelectedExperiment][len(StartingFolder) + 1:]
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
        logfile.info('\nMade with "%s" at Revision %s',
            os.path.basename(__file__), get_git_hash())
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

    if not ReallyRemove:
        print '\nWe did not really remove anything, set "ReallyRemove" at', \
            'the beginnig of the script to "True"'
        logfile.info(80 * '-')
        logfile.info('We did not really remove anything')
        logfile.info(' '.join(['Set "ReallyRemove" on line 22 of the script',
            'to "True" at the beginnig of the script to really delete the',
            'superfluous files']))

if ReallyRemove:
    print
    print 'Deletion of unnecessary darks of', StartingFolder, 'finished'
