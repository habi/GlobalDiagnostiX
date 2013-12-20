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
import shutil

#~ StartingFolder = '/afs/psi.ch/user/h/haberthuer/EssentialMed/Dev/Images/tis'
StartingFolder = '/afs/psi.ch/project/EssentialMed/Images/' +\
    '12-GOTTHARD_and_TIS/TIS/'

# Get list of (only) directories in StartingFolder
# http://stackoverflow.com/a/973488
ListOfFolders = [x[0] for x in os.walk(StartingFolder)]

Exposures = [glob.glob(os.path.join(Folder, '*.jpg'))
             for Folder in ListOfFolders]

# os.walk includes the base directory, thus go from 1 to end...
for i in range(1, len(Exposures)):
    plt.figure(figsize=[16, 9])
    print 20 * '-', i, '/', len(Exposures) - 1, 20 * '-'
    print 'Getting the mean of', len(Exposures[i]), 'Images from',\
        os.path.basename(ListOfFolders[i])
    #~ Min = [ plt.imread(Image).min() for Image in Exposures[i]]
    MeanValue = [plt.imread(Image).mean() for Image in Exposures[i]]
    #~ Max = [ plt.imread(Image).max() for Image in Exposures[i]]
    print 'The mean value of the images varies between',\
        round(min(MeanValue), 2), 'and', round(max(MeanValue), 2)
    print 'A maximum of', round(max(MeanValue), 2), 'was found in image',\
        MeanValue.index(max(MeanValue)), 'which corresponds to',\
        os.path.basename(Exposures[i][MeanValue.index(max(MeanValue))])
    plt.subplot(1, 2, 1)
    plt.plot(MeanValue)
    plt.xlabel('Mean')
    plt.ylabel('Image index')
    plt.title(' '.join(['Mean of', str(len(Exposures[i])),
                        'images in\n',
                        str(os.path.basename(ListOfFolders[i]))]))
    plt.subplot(1, 2, 2)
    plt.imshow(plt.imread(Exposures[i][MeanValue.index(max(MeanValue))]),
               origin='lower')
    plt.title(' '.join(['maximal value of', str(round(max(MeanValue), 2)),
                        '\nin',
                        str(os.path.basename(
                            Exposures[i][MeanValue.index(max(MeanValue))]))]))
    plt.savefig(os.path.join(StartingFolder,
                             os.path.basename(ListOfFolders[i]) + '.pdf'))
    #~ plt.savefig(os.path.join(StartingFolder,
                             #~ os.path.basename(ListOfFolders[i]) + '.png'))
    plt.show()

    # Delete unnecessary files
    # Proceed with caution!
    # Go through all the files, if they are *not* close to the selected one,
    # then delete them. But only do this if we've found the 'best' exposure not
    # in the first or last X images AND the mean is a meaningful value.
    Delete = False
    Threshold = 10
    if max(MeanValue) < Threshold:
        print
        print 'None of the images has a mean larger than the threshold of',\
            Threshold,
        if Delete:
            print 'thus deleting the whole directory...'
            shutil.rmtree(ListOfFolders[i])
        else:
            print 'one could delete', ListOfFolders[i]
        print
    else:
        # Delete the images if it's not in the first or last ten
        if (MeanValue.index(max(MeanValue)) > 10 or (len(Exposures[i]) - MeanValue.index(max(MeanValue))) > 10):
            for k in Exposures[i]:
                NumberoOfImagesToKeep = 5
                if k not in Exposures[i][MeanValue.index(max(MeanValue)) - NumberoOfImagesToKeep - 1:
                                        MeanValue.index(max(MeanValue)) + NumberoOfImagesToKeep]:
                    if Delete:
                        os.remove(k)
                    else:
                        print 'I would remove', k
            if not Delete:
                print 'if you set Delete=True on line 61 of the script.'
    # Open remaining images as stack in ImageJ
    # First check if the folder still exists or we deleted it above. Then open
    # ImageJ with all the files in the folder as a stack, scaled to 25%
    ShowStack = False
    if ShowStack:
        if os.path.isdir(ListOfFolders[i]):
            viewcommand = 'imagej -e "run(\\"Image Sequence...\\", \\"open=' +\
                os.path.abspath(ListOfFolders[i]) + ' scale=25\\");"'
            print 'Starting ImageJ with the command'
            print '---'
            print viewcommand
            print '---'
            print 'Quit ImageJ to proceed!'
            os.system(viewcommand)
