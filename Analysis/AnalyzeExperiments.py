# -*- coding: utf-8 -*-

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
from functions import distance
from functions import estimate_image_noise

StartingFolder = ('/afs/psi.ch/project/EssentialMed/MasterArbeitBFH/' +
        'XrayImages/')

# Go through all the results in the folder and show the images.
Files = [os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(StartingFolder)
    for f in files if f.endswith('.image.corrected.stretched.png')]
print 'I found', len(Files), 'images to work with in', StartingFolder

# Select some files
randomizator = True
if randomizator:
    # Randomly select some files
    Files = random.sample(Files, 100)
else:
    # Select every n'th image (http://stackoverflow.com/a/1404229/323100)
    Files = [Files[i] for i in xrange(0, len(Files), 12)]

print 'Reading', len(Files), 'images in', \
    os.path.dirname(os.path.commonprefix(Files))

# Extract data from the images
ExperimentID = [os.path.split(i)[1].split('.')[0] for i in Files]
ExperimentFolder = [os.path.join(os.path.dirname(i),
                                 os.path.basename(i).split('.')[0]) for
    i in Files]
Folder = [os.path.dirname(i) for i in Files]
Images = [plt.imread(i) for i in Files]
Mean = [np.mean(i) * 255 for i in Images]
STD = [np.std(i) * 255 for i in Images]
ScintillatorDistance = [distance(i, ) for i in ExperimentFolder]
#~ Weed out the ones images we cannot read...
#~ for c, i in enumerate(Files):
    #~ print 'rm', os.path.join(Folder[c], '*.png')
    #~ estimate_noise(plt.imread(i))
Noise = [estimate_image_noise(i) * 255 for i in Images]

#~ # Give out info
#~ for c, item in enumerate(ExperimentID):
    #~ print str(c).rjust(2), 'of', len(ExperimentID), '| Mean:', \
        #~ str(round(Mean[c], 1)).rjust(5), '| STD:', \
        #~ str(round(STD[c], 1)).rjust(4), '|', \
        #~ os.path.join(Folder[c],
            #~ ExperimentID[c] + '.image.corrected.stretched.png')

# Sort according to something
sort = 'noise'
HighestFirst = True
if sort == 'std':
    sortedIDs = [x for (y, x) in sorted(zip(STD, ExperimentID),
        reverse=HighestFirst)]
    sortedImages = [x for (y, x) in sorted(zip(STD, Images),
        reverse=HighestFirst)]
    sortedMean = [x for (y, x) in sorted(zip(STD, Mean),
        reverse=HighestFirst)]
    sortedSTD = [x for (y, x) in sorted(zip(STD, STD),
        reverse=HighestFirst)]
    sortedFolder = [x for (y, x) in sorted(zip(STD, Folder),
        reverse=HighestFirst)]
    sortedNoise = [x for (y, x) in sorted(zip(STD, Noise),
        reverse=HighestFirst)]
elif sort == 'mean':
    sortedIDs = [x for (y, x) in sorted(zip(Mean, ExperimentID),
        reverse=HighestFirst)]
    sortedImages = [x for (y, x) in sorted(zip(Mean, Images),
        reverse=HighestFirst)]
    sortedMean = [x for (y, x) in sorted(zip(Mean, Mean),
        reverse=HighestFirst)]
    sortedSTD = [x for (y, x) in sorted(zip(Mean, STD),
        reverse=HighestFirst)]
    sortedFolder = [x for (y, x) in sorted(zip(Mean, Folder),
        reverse=HighestFirst)]
    sortedNoise = [x for (y, x) in sorted(zip(Mean, Noise),
        reverse=HighestFirst)]
    sortedDistance = [x for (y, x) in sorted(zip(Mean, ScintillatorDistance),
        reverse=HighestFirst)]
elif sort == 'id':
    sortedIDs = [x for (y, x) in sorted(zip(ExperimentID, ExperimentID),
        reverse=HighestFirst)]
    sortedImages = [x for (y, x) in sorted(zip(ExperimentID, Images),
        reverse=HighestFirst)]
    sortedMean = [x for (y, x) in sorted(zip(ExperimentID, Mean),
        reverse=HighestFirst)]
    sortedSTD = [x for (y, x) in sorted(zip(ExperimentID, STD),
        reverse=HighestFirst)]
    sortedFolder = [x for (y, x) in sorted(zip(ExperimentID, Folder),
        reverse=HighestFirst)]
    sortedNoise = [x for (y, x) in sorted(zip(ExperimentID, Noise),
        reverse=HighestFirst)]
    sortedDistance = [x for (y, x) in sorted(zip(ExperimentID,
        ScintillatorDistance), reverse=HighestFirst)]
elif sort == 'noise':
    sortedIDs = [x for (y, x) in sorted(zip(Noise, ExperimentID),
        reverse=HighestFirst)]
    sortedImages = [x for (y, x) in sorted(zip(Noise, Images),
        reverse=HighestFirst)]
    sortedMean = [x for (y, x) in sorted(zip(Noise, Mean),
        reverse=HighestFirst)]
    sortedSTD = [x for (y, x) in sorted(zip(Noise, STD),
        reverse=HighestFirst)]
    sortedFolder = [x for (y, x) in sorted(zip(Noise, Folder),
        reverse=HighestFirst)]
    sortedNoise = [x for (y, x) in sorted(zip(Noise, Noise),
        reverse=HighestFirst)]
    sortedDistance = [x for (y, x) in sorted(zip(Noise,
        ScintillatorDistance), reverse=HighestFirst)]
elif sort == 'distance':
    sortedIDs = [x for (y, x) in sorted(zip(ScintillatorDistance,
        ExperimentID), reverse=HighestFirst)]
    sortedImages = [x for (y, x) in sorted(zip(ScintillatorDistance, Images),
        reverse=HighestFirst)]
    sortedMean = [x for (y, x) in sorted(zip(ScintillatorDistance, Mean),
        reverse=HighestFirst)]
    sortedSTD = [x for (y, x) in sorted(zip(ScintillatorDistance, STD),
        reverse=HighestFirst)]
    sortedFolder = [x for (y, x) in sorted(zip(ScintillatorDistance, Folder),
        reverse=HighestFirst)]
    sortedNoise = [x for (y, x) in sorted(zip(ScintillatorDistance, Noise),
        reverse=HighestFirst)]
    sortedDistance = [x for (y, x) in sorted(zip(ScintillatorDistance,
        ScintillatorDistance), reverse=HighestFirst)]

# Select n top items from sorting criterion
n = 10
print 'Selecting', n, 'images, sorted from',
if HighestFirst:
    print 'highest to lowest',
else:
    print 'lowest to highest',
print sort
sortedIDs = sortedIDs[:n]
sortedImages = sortedImages[:n]
sortedMean = sortedMean[:n]
sortedSTD = sortedSTD[:n]
sortedNoise = sortedNoise[:n]
sortedFolder = sortedFolder[:n]
sortedDistance = sortedDistance[:n]

# Give out info
for c, item in enumerate(sortedIDs):
    print str(c).rjust(2), 'of', len(sortedIDs), '| Mean:', \
        str(round(sortedMean[c], 1)).rjust(5), '| STD:', \
        str(round(sortedSTD[c], 1)).rjust(4), '| Noise', \
        str(round(sortedNoise[c], 1)).rjust(4), '| Distance', \
        str(sortedDistance[c]), '| Experiment', \
        sortedIDs[c].rjust(8), '| Image', os.path.join(sortedFolder[c],
            sortedIDs[c] +
            '.image.corrected.stretched.png')[len(StartingFolder):]

plt.figure(figsize=[23, 10])
for c, i in enumerate(sortedImages):
    plt.subplot(2, len(sortedImages) / 2, c + 1)
    plt.imshow(i, cmap='gray', interpolation='bicubic')
    plt.title(' '.join([str(c), '|', sortedIDs[c], '\nMean',
        str(round(sortedMean[c], 1)), '\nSTD',
        str(round(sortedSTD[c], 1)), '\nNoise',
        str(round(sortedNoise[c], 1)), '\nDistance',
        str(sortedDistance[c]), 'mm\n',
        sortedFolder[c].split('/')[8], '-', sortedFolder[c].split('/')[9],
        '-', sortedFolder[c].split('/')[10]]))
    plt.axis('off')
if HighestFirst:
    plt.suptitle(' '.join(['Images sorted from highest to lowest', sort]))
else:
    plt.suptitle(' '.join(['Images sorted from lowest to highest', sort]))

plt.subplots_adjust(wspace=0.05)
plt.subplots_adjust(hspace=0.05)
plt.axis('off')
plt.tight_layout()

print '\nShowing plot'
plt.show()
