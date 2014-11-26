# -*- coding: utf-8 -*-

"""
Script to "grep" the log files for mean/max brightness of all the images for
each set of components.
And to display these values.
"""

from __future__ import division
import glob
import os
import matplotlib.pyplot as plt
import platform
import numpy

if platform.node() == 'anomalocaris':
    RootFolder = '/Volumes/slslc/EssentialMed/MasterArbeitBFH/XrayImages'
else:
    RootFolder = '/afs/psi.ch/project/EssentialMed/MasterArbeitBFH/XrayImages'

# Ask for what to do
Scintillators = ('AppScinTech-HE', 'Pingseng', 'Hamamatsu', 'Toshiba')
Sensors = ('AR0130', 'AR0132', 'MT9M001')
Lenses = ('Computar-11A', 'Framos-DSL219D-650-F2.0',
          'Framos-DSL224D-650-F2.0', 'Framos-DSL311A-NIR-F2.8',
          'Framos-DSL949A-NIR-F2.0', 'Lensation-CHR4020',
          'Lensation-CHR6020', 'Lensation-CM6014N3', 'Lensation-CY0614',
          'TIS-TBL-6C-3MP')

LensCounter = 0
for lens in Lenses:
    LensCounter += 1
    print 'Lens', LensCounter, 'of', len(Lenses), '|', lens
    plt.figure(figsize=[20, 12])
    FolderCounter = 0
    for CurrentScintillator in Scintillators:
        for CurrentSensor in Sensors:
            FolderCounter += 1
            plt.subplot(len(Scintillators), len(Sensors), FolderCounter)
            print 'Folder', FolderCounter, 'of', len(Scintillators) * len(
                Sensors), '|', CurrentScintillator, '|', CurrentSensor, '|', \
                lens, '|',
            LoadStretched = False
            if LoadStretched:
                ImageNames = glob.glob(os.path.join(RootFolder,
                                                    CurrentScintillator,
                                                    CurrentSensor, lens, 'Hand',
                                                    '*.image.corrected.' +
                                                    'stretched.png'))
            else:
                ImageNames = glob.glob(os.path.join(RootFolder,
                                                    CurrentScintillator,
                                                    CurrentSensor, lens, 'Hand',
                                                    '*.image.corrected.png'))
            if len(ImageNames):
                print len(ImageNames), 'images found'
            else:
                print 'No images found for this combination'

            # Extract values
            Images = [plt.imread(image) for image in ImageNames]
            Min = [numpy.min(image) for image in Images]
            Mean = [numpy.mean(image) for image in Images]
            Max = [numpy.max(image) for image in Images]
            STD = [numpy.std(image) for image in Images]

            # plot Mean
            plt.plot(Mean, linestyle='none', marker='.', color='k')
            # plot the mean of the mean
            plt.axhline(numpy.mean(Mean), linestyle='--', color='k')
            # prepare for plotting the mean +- STD as a band around the mean
            MeanPlusSTD = [Mean[i] + STD[i] for i in range(len(Mean))]
            MeanMinusSTD = [Mean[i] - STD[i] for i in range(len(Mean))]
            # fill the band between Mean+STD and Mean-STD
            plt.fill_between(range(len(Mean)), MeanPlusSTD, MeanMinusSTD,
                             alpha=0.309, color='k')

            # Scale all the plots the same way, so we can compare them
            plt.ylim((0, 0.8))
            plt.title(' | '.join([CurrentScintillator, CurrentSensor, lens]))

    # Display
    plt.tight_layout()
    plt.savefig(os.path.join(RootFolder, 'Brightness-Overview_' + lens +
                             '.png'))
    plt.show()
    print
    print 'Done with', lens
    print 80 * '-'