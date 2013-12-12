#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script to load the set of images acquired in the x-ray lab.
Since we acquire lots of images before, during and after exposure it's really
annoying to manually sift through all the images in all the directories and
look for the 'best' exposure.
This script loads computes the mean of each image in each directory and gives
out the maximum of the this mean.
This should be the 'best' exposed image of all the exposures.
"""

import glob
import os
from pylab import *

StartingFolder = '/afs/psi.ch/user/h/haberthuer/EssentialMed/Dev/Images/tis'
#~ StartingFolder = '/afs/psi.ch/project/EssentialMed/Images/' +\
    #~ '12-GOTTHARD_and_TIS/TIS/'

# Get list of (only) directories in StartingFolder
# http://stackoverflow.com/a/973488
ListOfFolders = [x[0] for x in os.walk(StartingFolder)]

Exposures = [glob.glob(os.path.join(Folder, '*.jpg'))
             for Folder in ListOfFolders]

# os.walk includes the base directory, thus go from 1 to end...
for i in range(1, len(Exposures)):
    print 20 * '-'
    print 'Getting the mean of', len(Exposures[i]), 'Images from',\
        os.path.basename(ListOfFolders[i])
    #~ Min = [ plt.imread(Image).min() for Image in Exposures[i]]
    MeanValue = [plt.imread(Image).mean() for Image in Exposures[i]]
    #~ Max = [ plt.imread(Image).max() for Image in Exposures[i]]
    print 'MeanValue of images vary between', round(min(MeanValue), 2), 'and',\
        round(max(MeanValue), 2)
    print 'The maximum is found in image', MeanValue.index(max(MeanValue)),\
        'which corresponds to',\
        os.path.basename(Exposures[i][MeanValue.index(max(MeanValue))])

    plt.plot(MeanValue)
    plt.title(' '.join(['MeanValue value of', str(len(Exposures[i])),
                        'images in', str(os.path.basename(ListOfFolders[i])),
                        '\nmaximal value found in',
                        str(os.path.basename(
                            Exposures[i][MeanValue.index(max(MeanValue))]))]))
    plt.savefig(os.path.join(StartingFolder,
                             os.path.basename(ListOfFolders[i]) + '.pdf'))
    plt.savefig(os.path.join(StartingFolder,
                             os.path.basename(ListOfFolders[i]) + '.png'))
    #~ plt.show()
