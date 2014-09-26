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
    StartingFolder = RootFolder
else:
    # If running on Ivans machine, look on the connected harddisk
    StartingFolder = ('/Volumes/WINDOWS/Aptina/Hamamatsu/AR0130/Computar-11A/')
    StartingFolder = ('/Volumes/exFAT')

# Go through all the results in the folder and show the images.
Files = [os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(StartingFolder)
    for f in files if f.endswith('.image.corrected.stretched.png')]
print 'I found', len(Files), 'images to work with in', StartingFolder

# Select every n'th image (http://stackoverflow.com/a/1404229/323100)
Files = [Files[i] for i in xrange(0, len(Files), 156)]

# Grab data from these files
ExperimentID = [os.path.split(i)[1].split('.')[0] for i in Files]
Images = [plt.imread(i) for i in Files]
Mean = [np.mean(i) * 255 for i in Images]
STD = [np.std(i) * 255 for i in Images]

print 'Working with', len(Files), 'images in', \
    os.path.dirname(os.path.commonprefix(Files))
for c, item in enumerate(Files):
    print c, 'of', len(Files)
    print '\t', \
        str(item)[len(os.path.dirname(os.path.commonprefix(Files))) + 1:]
    print '\tMean:', round(Mean[c], 1)
    print '\tSTD:', round(STD[c], 1)

# Sort according to something
sort = 'std'
if sort == 'std':
    sortedIDs = [x for (y, x) in sorted(zip(STD, ExperimentID),
        reverse=True)]
    sortedImages = [x for (y, x) in sorted(zip(STD, Images), reverse=True)]
    sortedMean = [x for (y, x) in sorted(zip(STD, Mean), reverse=True)]
    sortedSTD = [x for (y, x) in sorted(zip(STD, STD), reverse=True)]
elif sort == 'mean':
    sortedIDs = [x for (y, x) in sorted(zip(Mean, ExperimentID),
        reverse=True)]
    sortedImages = [x for (y, x) in sorted(zip(Mean, Images), reverse=True)]
    sortedMean = [x for (y, x) in sorted(zip(Mean, Mean), reverse=True)]
    sortedSTD = [x for (y, x) in sorted(zip(Mean, STD), reverse=True)]
elif sort == 'id':
    sortedIDs = [x for (y, x) in sorted(zip(ExperimentID, ExperimentID),
        reverse=True)]
    sortedImages = [x for (y, x) in sorted(zip(ExperimentID, Images),
        reverse=True)]
    sortedMean = [x for (y, x) in sorted(zip(ExperimentID, Mean),
        reverse=True)]
    sortedSTD = [x for (y, x) in sorted(zip(ExperimentID, STD),
        reverse=True)]

plt.figure(figsize=[23, 8])
bins = 255
for c, i in enumerate(sortedImages):
    sys.stdout.write(''.join(['\rImage %d/' % c, str(len(Images))]))
    plt.subplot(2, len(Files), c + 1)
    plt.imshow(i, cmap='bone')
    plt.title(' '.join([sortedIDs[c], '\nMean', str(round(sortedMean[c], 1)),
        '\nSTD', str(round(sortedSTD[c], 1))]))
    plt.axis('off')
    plt.subplot(2, len(Files), c + len(Files) + 1)
    plt.hist(i.flatten(), bins, histtype='stepfilled')
    plt.ylim([0, 1.2e5])
    sys.stdout.flush()

print '\nShowing plot'

plt.tight_layout()
plt.show()
