# -*- coding: utf-8 -*-

"""
Script to "grep" the log files for mean/max brightness of all the images for
each set of components.
And to display these values.
"""

from __future__ import division
import glob
import os
import platform

import matplotlib.pyplot as plt
import numpy


if platform.node() == 'anomalocaris':
    # RootFolder = '/Volumes/slslc/EssentialMed/MasterArbeitBFH/XrayImages'
    RootFolder = '/Users/habi/Desktop/XrayImages/Volumes/slslc/EssentialMed' \
                 '/MasterArbeitBFH/XrayImages'
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
plt.ion()
plt.show()
for CurrentLens in Lenses:
    LensCounter += 1
    print 'Lens', LensCounter, 'of', len(Lenses), '|', CurrentLens
    print
    CombinationCounter = 0
    for CurrentScintillator in Scintillators:
        for CurrentSensor in Sensors:
            OverViewFigure = plt.figure(LensCounter, figsize=[20, 12])
            CombinationCounter += 1
            Axis1 = plt.subplot(len(Scintillators), len(Sensors),
                                CombinationCounter)
            print 'Folder', CombinationCounter, 'of', len(Scintillators) * len(
                Sensors), '|', CurrentScintillator, '|', CurrentSensor, '|', \
                CurrentLens, '|',
            LoadStretched = False
            if LoadStretched:
                ImageNames = glob.glob(os.path.join(RootFolder,
                                                    CurrentScintillator,
                                                    CurrentSensor,
                                                    CurrentLens, 'Hand',
                                                    '*.image.corrected.' +
                                                    'stretched.png'))
            else:
                ImageNames = glob.glob(os.path.join(RootFolder,
                                                    CurrentScintillator,
                                                    CurrentSensor,
                                                    CurrentLens, 'Hand',
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

            # Plot Mean
            plt.plot(Mean, linestyle='none', marker='.', color='k')
            # Prepare for plotting the mean +- STD as a band around the mean
            MeanPlusSTD = [Mean[i] + STD[i] for i in range(len(Mean))]
            MeanMinusSTD = [Mean[i] - STD[i] for i in range(len(Mean))]
            # Fill the band between Mean+STD and Mean-STD
            plt.fill_between(range(len(Mean)), MeanPlusSTD, MeanMinusSTD,
                             alpha=0.309, color='k')

            # Plot the mean of the mean and the band between the mean of the
            # mean +- the mean of the STD
            Axis1.axhline(numpy.mean(Mean), linestyle='--', color='k')
            Axis1.fill_between(range(len(Mean)), numpy.mean(Mean) +
                               numpy.mean(STD), numpy.mean(Mean) -
                               numpy.mean(STD), alpha=0.309, color='r')

            # Scale all the plots the same way, so we can compare them
            plt.ylim((0, 0.75))
            plt.title(' | '.join([CurrentScintillator, CurrentSensor,
                                  CurrentLens]))

            # Show all the images of this component combination , so that we
            # can quickly see which ones are good and which ones are not
            LensFigure = plt.figure(CombinationCounter + LensCounter,
                                    figsize=[16, 9])
            plt.suptitle(' | '.join([CurrentScintillator, CurrentSensor,
                                     CurrentLens]))
            for c, i in enumerate(Images):
                Axis2 = plt.subplot(5, len(Images) / 4, c + 1)
                Axis2.imshow(i, cmap='bone')
                Axis2.axis('off')
                plt.title(':'.join([str(c),
                                    os.path.basename(ImageNames[c]).split(
                                        '.')[0]]))
            try:
                os.makedirs(os.path.join(RootFolder, 'BrightnessOutput',
                                         CurrentLens))
            except OSError:
                pass
            LensFigure.savefig(os.path.join(RootFolder, 'BrightnessOutput',
                                            CurrentLens, 'Images_' +
                                            CurrentScintillator + '_' +
                                            CurrentSensor + '_' + CurrentLens
                                            + '.png'))
            plt.title(' | '.join([CurrentScintillator, CurrentSensor,
                                  CurrentLens]))
            plt.draw()

    # Display
    OverViewFigure = plt.figure(LensCounter, figsize=[20, 12])
    OverViewFigure.savefig(os.path.join(RootFolder,  'BrightnessOutput',
                                        CurrentLens, 'Overview_' +
                                        CurrentLens + '.png'))
    print
    print 'Done with', CurrentLens
    print 80 * '-'
    plt.draw()

print 'Done with everything'