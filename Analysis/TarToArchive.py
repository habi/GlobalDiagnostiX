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


def get_git_revision_short_hash():
    hashit = subprocess.Popen(['git', 'rev-parse', '--short', 'HEAD'],
        stdout=subprocess.PIPE)
    output, error = hashit.communicate()
    return output

# Setup
# If Manual selection is true, the user is asked to select one of the
# experiment IDs manually, otherwise the script just goes through all the IDs
# it finds in the starting folder
ManualSelection = False

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
    # See if DarkDeleter.py was already run on this experiment
    DarkDeleterLog = os.path.join(
        os.path.dirname(Experiment[SelectedExperiment]),
        ExperimentID[SelectedExperiment] + '.deletion.log')
    if os.path.isfile(DarkDeleterLog):
        DoArchive = False
        # Did we really delete them? If not, we can repeat the analysis
        for line in open(DarkDeleterLog, 'r'):
            # The last line of the log file tells us if we did it or not...
            if 'Set "ReallyRemove"' in line:
                print 'We have a deletion log file, but did not actually', \
                    'delete the files. Proceeding...'
                DoArchive = True
    else:
        DoArchive = True
    if not DoArchive:
        # If we removed some files it doesn't make sense to archive again
        print
        print '\tWe already ran DarkDeleter.py on experiment', \
            ExperimentID[SelectedExperiment]
        print '\tWe thus do not archive it again.'
        print '\tTake a look at', os.path.join(
            os.path.dirname(Experiment[SelectedExperiment])
                [len(StartingFolder) + 1:],
            ExperimentID[SelectedExperiment] + '.archive.log'), 'for more info'
        print
    else:
        # Archive it!
        logfile = myLogger(os.path.dirname(Experiment[SelectedExperiment]),
            ExperimentID[SelectedExperiment] + '.archive.log')
        logfile.info('Archival log file for Experiment ID %s, archived on %s',
            ExperimentID[SelectedExperiment],
            time.strftime('%d.%m.%Y at %H:%M:%S'))
        logfile.info('\nMade with "%s" at Revision %s',
            os.path.basename(__file__),
            get_git_revision_short_hash())
        logfile.info(80 * '-')
        # Tar the selected folder
        TarCommand = ['tar', '-czf',
            Experiment[SelectedExperiment] + '.tar.gz',
            '-C', os.path.dirname(Experiment[SelectedExperiment]),
            os.path.basename(Experiment[SelectedExperiment])]
        print 'Packing', ExperimentID[SelectedExperiment]
        logfile.info('Packing the original files with')
        logfile.info('---')
        logfile.info(' '.join(TarCommand))
        logfile.info('---')
        packit = subprocess.Popen(TarCommand, stdout=subprocess.PIPE)
        output, error = packit.communicate()
        if output:
            print output
        if error:
            print error
        time.sleep(0.5)
        # FTP the file to the PSI archive
        # We use the bookmark feature of 'lftp' to access the password. It's in
        # ~/.lftp/bookmarks...
        LFTPcommand = 'lftp -e \"mkdir -p ' + \
            os.path.dirname(
                Experiment[SelectedExperiment][len(RootFolder) + 1:]) + \
            ';put ' + str(Experiment[SelectedExperiment]) + '.tar.gz -o ' + \
            os.path.join(
                os.path.dirname(
                    Experiment[SelectedExperiment][len(RootFolder) + 1:]),
                ExperimentID[SelectedExperiment] + '.tar.gz') + ';bye\" Ivan'
        print 'Transferring', \
            ExperimentID[SelectedExperiment] + '.tar.gz to archive'
        print LFTPcommand
        logfile.info('Transferring %s to the PSI archive with',
            ExperimentID[SelectedExperiment] + '.tar.gz')
        logfile.info('---')
        logfile.info(LFTPcommand)
        logfile.info('---')
        os.system(LFTPcommand)
        time.sleep(0.5)
        print 'Deleting archival file', \
            os.path.basename(Experiment[SelectedExperiment]) + '.tar.gz'
        os.remove(Experiment[SelectedExperiment] + '.tar.gz')
        time.sleep(0.5)

print
print 'Archival of', StartingFolder, 'finished'
