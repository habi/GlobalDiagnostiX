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

from functions import get_experiment_list
from functions import get_git_hash
from functions import myLogger

RootFolder = ('/afs/psi.ch/project/EssentialMed/MasterArbeitBFH/' +
    'XrayImages')
StartingFolder = os.path.join(RootFolder, '20140920')  # 94

ListOfTARs = []
for root, dirnames, filenames in os.walk(os.path.join(RootFolder, StartingFolder)):
  for filename in fnmatch.filter(filenames, '*.gz'):
      ListOfTARs.append(os.path.join(root, filename))

for item in ListOfTARs[:1]:
    print 'unpacking', item
    UnpackCommand = ['tar', '-xf', item, '--directory', os.path.dirname(item)]
    unpackit = subprocess.Popen(UnpackCommand, stdout=subprocess.PIPE)
    output, error = unpackit.communicate()
    if output:
        print output
    if error:
        print error
    print '\nBooyaka!\n'
