# -*- coding: utf-8 -*-

"""
Script to `tar` each experiment folder and send it to ftp://archivftp.psi.ch/
for archival.

The small bash script I wrote got much too complicated, thus I'm switching
to a python script. The detection of folders and other things are based on
DetectWhichImageIsRadiography.py
"""

import os
import time
import subprocess

import functions

# Setup
# If Manual selection is true, the user is asked to select one of the
# experiment IDs manually, otherwise the script just goes through all the IDs
# it finds in the starting folder
ManualSelection = False

# Where shall we start?
RootFolder = '/afs/psi.ch/project/EssentialMed/MasterArbeitBFH/XrayImages'
case = 1
if case == 1:
    # Look through all folders
    StartingFolder = RootFolder
elif case == 2:
    # Look for images of only one scintillator
    Scintillators = ('AppScinTech-HE', 'Pingseng', 'Hamamatsu', 'Toshiba')
    ChosenScintillator = functions.AskUser(
        'Which scintillator do you want to look at?', Scintillators)
    StartingFolder = os.path.join(RootFolder, ChosenScintillator)
elif case == 3:
    # Ask for what to do
    Scintillators = ('AppScinTech-HE', 'Pingseng', 'Hamamatsu', 'Toshiba')
    Sensors = ('AR0130', 'AR0132', 'MT9M001')
    Lenses = ('Computar-11A', 'Framos-DSL219D-650-F2.0',
              'Framos-DSL224D-650-F2.0', 'Framos-DSL311A-NIR-F2.8',
              'Framos-DSL949A-NIR-F2.0', 'Lensation-CHR4020',
              'Lensation-CHR6020', 'Lensation-CM6014N3', 'Lensation-CY0614',
              'TIS-TBL-6C-3MP', '')
    ChosenScintillator = functions.AskUser(
        'Which scintillator do you want to look at?', Scintillators)
    ChosenSensor = functions.AskUser(
        'Which sensor do you want to look at?', Sensors)
    ChosenLens = functions.AskUser(
        'Which lens do you want to look at? ("empty" = "all")',
        Lenses)
    StartingFolder = os.path.join(RootFolder, ChosenScintillator,
                                  ChosenSensor, ChosenLens)

# Look for all folders matching the naming convention
Experiment, ExperimentID = functions.get_experiment_list(StartingFolder)
print 'I found', len(Experiment), 'experiment IDs in', StartingFolder

AnalyisList = []
if ManualSelection:
    # Ask the user which experimentID to show
    # Concatenate the list for display purposes:
    # http://stackoverflow.com/a/22642307/323100
    Choice = functions.AskUser('Which experiment do you want to archive?',
                               ExperimentID)
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
            os.path.dirname(Experiment[SelectedExperiment])[len(
                StartingFolder):], ExperimentID[SelectedExperiment] +
            '.archive.log'), 'for more info'
        print
    else:
        # Archive it!
        logfile = functions.myLogger(
            os.path.dirname(Experiment[SelectedExperiment]),
            ExperimentID[SelectedExperiment] + '.archive.log')
        logfile.info('Archival log file for Experiment ID %s, archived on '
                     '%s', ExperimentID[SelectedExperiment],
                     time.strftime('%d.%m.%Y at %H:%M:%S'))
        logfile.info('\nMade with "%s" at Revision %s', os.path.basename(
            __file__), functions.get_git_hash())
        logfile.info(80 * '-')
        # Tar the selected folder
        TarCommand = ['tar', '-czf', Experiment[SelectedExperiment] +
                      '.tar.gz', '-C',
                      os.path.dirname(Experiment[SelectedExperiment]),
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
        logfile.info('Transferring %s to the PSI archive with', ExperimentID[
            SelectedExperiment] + '.tar.gz')
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
