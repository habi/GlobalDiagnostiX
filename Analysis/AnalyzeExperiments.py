"""
Script to load the results of DetectWhichImageIsRadiography.py and show it in
such a way that we can make a conclusion.
"""

import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import random

from functions import myLogger
from functions import get_git_hash

StartingFolder= ('/afs/psi.ch/project/EssentialMed/MasterArbeitBFH/' +
        'XrayImages')

# Go through all the results in the folder and show the images.
Files = [os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(StartingFolder)
    for f in files if f.endswith('.image.corrected.stretched.png')]
print 'I found', len(Files), 'images to work with in', StartingFolder

# Select some files
randomizator = True
if randomizator:
    # Randomly select some files
    Files = random.sample(Files, 15)
else:
    # Select every n'th image (http://stackoverflow.com/a/1404229/323100)
    Files = [Files[i] for i in xrange(0, len(Files), 100)][:10]

# Extract data from the images
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
sort = 'mean'

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

# full screen figure
plt.figure(figsize=[25, 25])

for c, i in enumerate(sortedImages):
    sys.stdout.write(''.join(['\rImage %d/' % (c + 1), str(len(Images))]))
    if len(Files) > 10:
        plt.subplot(int(np.ceil(len(Files) / 4)),
            int(np.ceil(len(Files) / 3)), c + 1)
    else:
        plt.subplot(2, 5, c + 1)
    plt.imshow(i, cmap='bone')
    currentDirName = os.path.dirname(Files[ExperimentID.index(sortedIDs[1])])[
        len(os.path.dirname(os.path.commonprefix(Files))) + 1:]
    plt.title(' '.join([sortedIDs[c], '| Mean', str(round(sortedMean[c], 1)), '| STD',
        str(round(sortedSTD[c], 1))]))
    plt.subplots_adjust(wspace=0.05)
    plt.subplots_adjust(hspace=0.05)
    plt.axis('off')
    plt.suptitle(' '.join(['sorted by', sort]))
    #~ plt.subplot(2, len(Files), c + len(Files) + 1)
    #~ plt.hist(i.flatten(), bins=256, histtype='stepfilled')
    #~ plt.ylim([0, 1.2e5])
    sys.stdout.flush()

print '\nShowing plot'

plt.tight_layout()
plt.show()
