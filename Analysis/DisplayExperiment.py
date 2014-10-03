"""
Script to display only some experiments, based on either choice of ID or choice
of component
"""

import os
import matplotlib.pyplot as plt
import numpy as np

ID = [
    8466438,
    8466246,
    8596690,
    8595968,
    5808743,
    5814382,
    5814190,
    9078293,
    9074884,
    9071872,
    8466170,
]

RootFolder = ('/afs/psi.ch/project/EssentialMed/MasterArbeitBFH/' +
    'XrayImages')

# Get all folders (Experiment) and ExperimentIDs inside StartingFolder
# Setup progress bar
print 'Looking for the folder with the Experiment ID'
Folder = []
ExperimentID = []
for root, dirs, files in os.walk(RootFolder):
    # Go through all the directories
    try:
        # If the last foldername is a number,
        int(os.path.basename(root))
        # see if it's in the list of IDs above,
        if int(os.path.basename(root)) in ID:
            print 'Experiment', os.path.basename(root), 'found in', \
                os.path.dirname(root)
            Folder.append(root)
            ExperimentID.append(int(os.path.basename(root)))
            #~ print len(Folder), len(ExperimentID), len(ID)
        # otherwise just pass
    except:
        continue

# Warn the user if we were not able to find an image...
if len(ExperimentID) != len(ID):
    for i in ID:
        if i not in ExperimentID:
            print '\nExperiment ID', i, 'was not found in', RootFolder
            exit('Hope it is  only a typo...')

# Extract data from the images
print 'Reading and preparing images'
Images = [plt.imread(i + '.image.corrected.stretched.png') for i in Folder]
Mean = [np.mean(i) * 255 for i in Images]
STD = [np.std(i) * 255 for i in Images]

plt.figure(figsize=[20,3])
for c, i in enumerate(Images):
    print 'Reading and preparing image', c, 'of', len(Folder)
    plt.subplot(1, len(Folder), c + 1)
    plt.imshow(i, cmap='bone')
    title = '\n'.join(['ID ' + str(ExperimentID[c]),
        'Mean ' + str(round(Mean[c],1)), 'STD ' + str(round(STD[c],1))])
    plt.title(title)
    plt.axis('off')
plt.tight_layout()
plt.show()
