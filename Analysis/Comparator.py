"""
Script to compare the contents of Ivans HD with the stuff present on AFS.
Due to space shortage, some folders might have been missed during copying.

And since a large part of the folders were already processed, we cannot just
use `rsync` or that will copy over all the files that already were deleted.
So we use a little routine to find missing folders and rsync only those one
after the other.
This should also take care of the speed issue should the script to have to run
several times.
"""

import os
import subprocess
import errno


def readit(InputFolder):
    '''
    Get all folders (Experiment) and ExperimentIDs inside StartingFolder
    '''
    print 'Looking for Experiment ID folders in', InputFolder
    print 'This will take a while'
    Folder = []
    ExperimentID = []
    for root, dirs, files in os.walk(InputFolder):
        # Go through all the directories and see if the last foldername is a
        # number
        try:
            if int(os.path.basename(root)):
                Folder.append(root)
                ExperimentID.append(int(os.path.basename(root)))
        # otherwise just continue
        except ValueError:
            continue

    return Folder, ExperimentID

# Read *all* experiment IDs from HD
RootFolderHD = ('/media/WINDOWS/Aptina')
FolderHD, IDHD = readit(RootFolderHD)

# Read *all* experiment IDs from AFS
RootFolderAFS = ('/afs/psi.ch/project/EssentialMed/MasterArbeitBFH/XrayImages')
FolderAFS, IDAFS = readit(RootFolderAFS)

for counter, experiment in enumerate(IDHD):
    print 5 * '-', '|', str(counter + 1) + '/' + str(len(IDHD)), '|', 60 * '-'
    if experiment not in IDAFS:
        InputPath = FolderHD[IDHD.index(experiment)]
        OutputPath = os.path.dirname(os.path.join(RootFolderAFS,
            FolderHD[IDHD.index(experiment)][len(RootFolderHD) + 1:]))
        print 'Experiment', experiment, 'was not found on AFS'
        print
        print 'It should be moved from'
        print InputPath
        print 'to'
        print OutputPath
        # rsync can only mkdir ONE level, so we first make the path to copy to
        try:
            os.makedirs(OutputPath)
        except OSError as e:
            if e.errno != errno.EEXIST:
                # If the error is not about the directory existing, raise it
                # again
                raise
        rsynccommand = ['rsync', '-ar', InputPath, OutputPath]
        print
        print 'rsyncing it now with the command'
        print ' '.join(rsynccommand)
        synchronizeit = subprocess.Popen(rsynccommand, stdout=subprocess.PIPE)
        output, error = synchronizeit.communicate()
        if error:
            print 'The below error happened'
            print error
            break
    else:
        print 'Experiment', experiment, 'from'
        print FolderHD[IDHD.index(experiment)]
        print 'is already on AFS at'
        print FolderAFS[IDAFS.index(experiment)]
    print 'Done with experiment', experiment

print 80 * '-'
print 'Done with all', len(IDHD), 'experiment IDs on', RootFolderHD
