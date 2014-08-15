#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script to `tar` each experiment folder and send it to ftp://archivftp.psi.ch/
for archival.

The small bash script I wrote got much too complicated, thus I'm switching
to a python script. The detection of folders and other things are based on
DetectWhichImageIsRadiography.py
"""

import glob
import os
import logging
import time
import subprocess

# Setup
# If Manual selection is true, the user is asked to select one of the
# experiment IDs manually, otherwise the script just goes through all the IDs
# it finds in the starting folder
ManualSelection = False

# Where shall we start?
# Where shall we start?
RootFolder = ('/afs/psi.ch/project/EssentialMed/MasterArbeitBFH/' +
    'XrayImages')
StartingFolder = os.path.join(RootFolder, '20140731')

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
        not 'Toshiba' in os.path.basename(root) and \
        not 'MT9' in os.path.basename(root) and \
        not 'AR0' in os.path.basename(root):
        Experiment.append(root)
        ExperimentID.append(os.path.basename(root))

print 'I found', len(Experiment), 'experiment IDs in', StartingFolder
print 80 * '-'

AnalyisList = []
if ManualSelection:
    # Ask the user which experimentID to show
    ## Concatenate the list for display purposes:
    ## http://stackoverflow.com/a/22642307/323100
    Choice = AskUser('Which experiment do you want to archive?', ExperimentID)
    AnalyisList.append(ExperimentID.index(Choice))
    print
else:
    AnalyisList = range(len(Experiment))

# Go through each selected experiment
for Counter, SelectedExperiment in enumerate(AnalyisList):
    # Inform the user and start logging
    print 80 * '-'
    print str(Counter + 1) + '/' + str(len(AnalyisList)) + \
        ': Archiving experiment', ExperimentID[SelectedExperiment]
    logfile = myLogger(os.path.dirname(Experiment[SelectedExperiment]),
        ExperimentID[SelectedExperiment] + '.archive.log')
    logfile.info('Archival log file for Experiment ID %s, archived on %s',
        ExperimentID[SelectedExperiment],
        time.strftime('%d.%m.%Y at %H:%M:%S'))
    logfile.info(80 * '-')
    # Tar the selected folder
    TarCommand = ['tar', '-cPzf', Experiment[SelectedExperiment] + '.tar.gz',
        Experiment[SelectedExperiment]]
    print 'Packing', ExperimentID[SelectedExperiment], 'with the command', \
        ' '.join(TarCommand)
    logfile.info('Packing the original files with')
    logfile.info('---')
    logfile.info(' '.join(TarCommand))
    logfile.info('---')
    packit = subprocess.Popen(TarCommand, stdout=subprocess.PIPE)
    output, error = packit.communicate()
    print output
    # FTP the file to the PSI archive
    #~ LFTPcommand = ['lftp', '-e', "'put",
        #~ Experiment[SelectedExperiment] + '.tar;', "bye'", '-u',
        #~ 'EssentialMed,ACTUALPASSWORD', '-v', 'archivftp:ExperimentsIvan']
    #~ print 'Transferring', ExperimentID[SelectedExperiment] + '.tar',\
        #~ 'with the command', ' '.join(LFTPcommand)
    #~ logfile.info('Transferring %s to the PSI archive with',
        #~ ExperimentID[SelectedExperiment] + '.tar')
    #~ logfile.info('---')
    #~ logfile.info(' '.join(LFTPcommand))
    #~ logfile.info('---')
