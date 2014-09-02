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
import logging
import time
import numpy

# Setup
ReallyRemove = True

# Where shall we start?
RootFolder = ('/afs/psi.ch/project/EssentialMed/MasterArbeitBFH/' +
    'XrayImages')
#~ StartingFolder = os.path.join(RootFolder, '20140721')
#~ StartingFolder = os.path.join(RootFolder, '20140722')
#~ StartingFolder = os.path.join(RootFolder, '20140724')
#~ StartingFolder = os.path.join(RootFolder, '20140730')
#~ StartingFolder = os.path.join(RootFolder, '20140731')
#~ StartingFolder = os.path.join(RootFolder, '20140818')
#~ StartingFolder = os.path.join(RootFolder, '20140819')
#~ StartingFolder = os.path.join(RootFolder, '20140820')
#~ StartingFolder = os.path.join(RootFolder, '20140822')
#~ StartingFolder = os.path.join(RootFolder, '20140823')
#~ StartingFolder = os.path.join(RootFolder, '20140825')
#~ StartingFolder = os.path.join(RootFolder, '20140829')
#~ StartingFolder = os.path.join(RootFolder, '20140831')
StartingFolder = os.path.join(RootFolder, '20140901')

# Testing
StartingFolder = os.path.join(RootFolder, '20140731', 'Toshiba', 'AR0132',
    'Lensation-CHR6020')
# Testing
#~ StartingFolder = RootFolder


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


def get_git_revision_short_hash():
    import subprocess
    hashit = subprocess.Popen(['git', 'rev-parse', '--short', 'HEAD'],
        stdout=subprocess.PIPE)
    output, error = hashit.communicate()
    return output

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
            ExperimentID[SelectedExperiment]
        print 'I thus set "ReallyRemove" to false'
        print
        print 'Please archive the data first with TarToArchive.py, then', \
            'run this script again'
        break
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
            os.path.basename(__file__), get_git_revision_short_hash())
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
