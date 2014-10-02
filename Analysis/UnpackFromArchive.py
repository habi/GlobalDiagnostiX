# -*- coding: utf-8 -*-

"""
Once the analysis of a folder has been done, we use the TarToArchive.py script
to pack it up and sent to the PSI tape archive, the DarkDeleter.py script is
then used to delete all the unnecessary files.

If you want to get some stuff back, it's annoying manual work to go in each
folder and unpack the tar files.

This script should alleviate this problem.
"""

import os
import subprocess
import sys
import fnmatch
import glob

from functions import get_experiment_list
from functions import get_git_hash
from functions import myLogger

RootFolder = ('/afs/psi.ch/project/EssentialMed/MasterArbeitBFH/' +
    'XrayImages')

ListOfTARs = []
for root, dirnames, filenames in os.walk(os.path.join(RootFolder)):
    for filename in fnmatch.filter(filenames, '*.gz'):
        ListOfTARs.append(os.path.join(root, filename))

for counter, item in enumerate(ListOfTARs):
    print counter, 'of', len(ListOfTARs), '| unpacking', item
    UnpackCommand = ['tar', '-xf', item, '--directory', os.path.dirname(item)]
    unpackit = subprocess.Popen(UnpackCommand, stdout=subprocess.PIPE)
    output, error = unpackit.communicate()
    if output:
        print output
    if error:
        print error
    print 'Unpacking done, now removing', item
    try:
        os.remove(item)
    except:
        print 'It is already gone!'
    ExperimentID = os.path.splitext(os.path.splitext(item)[0])[0]
    DeletionLog = ExperimentID + '.deletion.log'
    print 'Deletion done, now also removing', os.path.basename(DeletionLog), \
        'and results from Analyis (all', \
        os.path.basename(ExperimentID) + '*.png)'
    try:
        os.remove(DeletionLog)
        for i in glob.glob(ExperimentID + '*.png'):
            try:
                os.remove(i)
            except:
                print 'The analysis images are already gone!'
    except:
            print 'The log file is already gone!'
    print
