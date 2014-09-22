"""
Script to load the results of DetectWhichImageIsRadiography.py and show it in
such a way that we can make a conclusion.
"""

import sys
import os
import matplotlib.pyplot as plt
import numpy as np

from functions import myLogger
from functions import get_git_hash

# Where shall we start?
if 'linux' in sys.platform:
    # If running at the office, grep AFS
    RootFolder = ('/afs/psi.ch/project/EssentialMed/MasterArbeitBFH/' +
        'XrayImages')
    StartingFolder = os.path.join(RootFolder, '20140921')  # 4
else:
    # If running on Ivans machine, look on the connected harddisk
    StartingFolder = ('/Volumes/WINDOWS/Aptina/Hamamatsu/AR0130/Computar-11A/')
    StartingFolder = ('/Volumes/exFAT')

# Go through all the results in the folder and show the images.
Files = [os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(StartingFolder)
    for f in files if f.endswith('.image.corrected.stretched.png')]
print 'I found', len(Files), 'images to work with in', StartingFolder

Files = Files[:6]
print 'Working with the first', len(Files), 'images'

ExperimentID = [ os.path.split(i)[1].split('.')[0] for i in Files]
Images = [ plt.imread(i) for i in Files]
Mean = [ np.mean(i) * 255 for i in Images]
STD = [ np.std(i) * 255 for i in Images]

# Sort according to defined value
sortedIDs = [x for (y,x) in sorted(zip(Mean,ExperimentID), reverse=True)]
sortedImages = [x for (y,x) in sorted(zip(Mean,Images), reverse=True)]
sortedSTD = [x for (y,x) in sorted(zip(Mean,STD), reverse=True)]

plt.figure(figsize=[16, 16])
bins = 255
for c, i in enumerate(Images):
    print c + 1, 'Displaying image'
    plt.subplot(4, len(Files), c + 1)
    plt.imshow(i, cmap='bone')
    plt.title(' '.join([ExperimentID[c], '\n', str(round(Mean[c], 3)), '|',
        str(round(STD[c], 3))]))
    plt.axis('off')
    plt.subplot(4, len(Files), c + len(Files) + 1)
    print '  Generating histogram'
    plt.hist(i.flatten(), bins, fc='k', ec='k')
    plt.ylim([0,1.2e5])
for c, i in enumerate(sortedImages):
    print c + 1, 'Displaying images sorted by Mean'
    plt.subplot(4, len(Files), c + 2 * len(Files) + 1 )
    plt.imshow(i, cmap='bone')
    plt.title(' '.join([sortedIDs[c], '\n', str(round(sorted(Mean,reverse=True)[c], 3)), '|',
        str(round(sortedSTD[c], 3))]))
    plt.axis('off')
    plt.subplot(4, len(Files), c + 3 * len(Files) + 1 )
    print '  Generating histogram'
    plt.hist(i.flatten(), bins, fc='k', ec='k')
    plt.ylim([0,1.2e5])

plt.tight_layout()
plt.show()
