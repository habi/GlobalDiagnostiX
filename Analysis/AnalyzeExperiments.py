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

StartingFolder = ('/afs/psi.ch/project/EssentialMed/MasterArbeitBFH/' +
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
    Files = random.sample(Files, 265)
else:
    # Select every n'th image (http://stackoverflow.com/a/1404229/323100)
    Files = [Files[i] for i in xrange(0, len(Files), 12)]

print 'Reading', len(Files), 'images in', \
    os.path.dirname(os.path.commonprefix(Files))

# Extract data from the images
ExperimentID = [os.path.split(i)[1].split('.')[0] for i in Files]
Folder = [os.path.join(os.path.dirname(i)) for i in Files]
Images = [plt.imread(i) for i in Files]
Mean = [np.mean(i) * 255 for i in Images]
STD = [np.std(i) * 255 for i in Images]

#~ # Give out info
#~ for c, item in enumerate(ExperimentID):
    #~ print str(c).rjust(2), 'of', len(ExperimentID), '| Mean:', \
        #~ str(round(Mean[c], 1)).rjust(5), '| STD:', \
        #~ str(round(STD[c], 1)).rjust(4), '|', \
        #~ os.path.join(Folder[c],
            #~ ExperimentID[c] + '.image.corrected.stretched.png')

# Sort according to something
sort = 'mean'
if sort == 'std':
    sortedIDs = [x for (y, x) in sorted(zip(STD, ExperimentID),
        reverse=True)]
    sortedImages = [x for (y, x) in sorted(zip(STD, Images), reverse=True)]
    sortedMean = [x for (y, x) in sorted(zip(STD, Mean), reverse=True)]
    sortedSTD = [x for (y, x) in sorted(zip(STD, STD), reverse=True)]
    sortedFolder = [x for (y, x) in sorted(zip(STD, Folder), reverse=True)]
elif sort == 'mean':
    sortedIDs = [x for (y, x) in sorted(zip(Mean, ExperimentID),
        reverse=True)]
    sortedImages = [x for (y, x) in sorted(zip(Mean, Images), reverse=True)]
    sortedMean = [x for (y, x) in sorted(zip(Mean, Mean), reverse=True)]
    sortedSTD = [x for (y, x) in sorted(zip(Mean, STD), reverse=True)]
    sortedFolder = [x for (y, x) in sorted(zip(Mean, Folder), reverse=True)]
elif sort == 'id':
    sortedIDs = [x for (y, x) in sorted(zip(ExperimentID, ExperimentID),
        reverse=True)]
    sortedImages = [x for (y, x) in sorted(zip(ExperimentID, Images),
        reverse=True)]
    sortedMean = [x for (y, x) in sorted(zip(ExperimentID, Mean),
        reverse=True)]
    sortedSTD = [x for (y, x) in sorted(zip(ExperimentID, STD),
        reverse=True)]
    sortedFolder = [x for (y, x) in sorted(zip(ExperimentID, Folder),
        reverse=True)]

# Select n top items from sorting criterion
n = 10
print 'Selecting', n, 'images, sorted by', sort
sortedIDs = sortedIDs[:n]
sortedImages = sortedImages[:n]
sortedMean = sortedMean[:n]
sortedSTD = sortedSTD[:n]
sortedFolder = sortedFolder[:n]

# Give out info
for c, item in enumerate(sortedIDs):
    print str(c).rjust(2), 'of', len(sortedIDs), '| Mean:', \
        str(round(sortedMean[c], 1)).rjust(5), '| STD:', \
        str(round(sortedSTD[c], 1)).rjust(4), '|', \
        os.path.join(sortedFolder[c],
            sortedIDs[c] + '.image.corrected.stretched.png')

plt.figure(figsize=[23, 10])
for c, i in enumerate(sortedImages):
    plt.subplot(2, len(sortedImages) / 2, c + 1)
    plt.imshow(i, cmap='gray')
    plt.title(' '.join([str(c), '|', sortedIDs[c], '\nMean',
        str(round(sortedMean[c], 1)), '\nSTD',
        str(round(sortedSTD[c], 1)), '\n',
        sortedFolder[c].split('/')[8], '-', sortedFolder[c].split('/')[9],
        '-', sortedFolder[c].split('/')[10]]))
    plt.axis('off')
plt.suptitle(' '.join(['sorted by', sort]))
plt.tight_layout()
plt.show()
exit()


# full screen figure
plt.figure(figsize=[23, 10])

for c, i in enumerate(sortedImages):
    sys.stdout.write(''.join(['\rImage %d/' % (c + 1), str(len(Images))]))
    if len(Files) > 10:
        plt.subplot(int(np.ceil(len(Files) / 4)),
            int(np.ceil(len(Files) / 3)), c + 1)
    else:
        plt.subplot(1, len(sortedImages), c + 1)
    plt.imshow(i, cmap='bone')
    currentDirName = os.path.dirname(Files[ExperimentID.index(sortedIDs[1])])[
        len(os.path.dirname(os.path.commonprefix(Files))) + 1:]
    plt.title(' '.join([sortedIDs[c], '| Mean', str(round(sortedMean[c], 1)),
        '| STD', str(round(sortedSTD[c], 1))]))
    plt.subplots_adjust(wspace=0.05)
    plt.subplots_adjust(hspace=0.05)
    plt.axis('off')
    #~ plt.subplot(2, len(Files), c + len(Files) + 1)
    #~ plt.hist(i.flatten(), bins=256, histtype='stepfilled')
    #~ plt.ylim([0, 1.2e5])
    sys.stdout.flush()

print '\nShowing plot'
plt.suptitle(' '.join(['sorted by', sort]))
plt.tight_layout()
plt.show()
