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
import logging
import time
import sys
from functions import get_git_hash


def processimage(inputimage, clip=3):
    """
    Clip image brightness to "mean +- 3 STD" (by default). Another value can
    be given. This is applied to the input images if the -c commandline
    parameter is given.
    """
    return numpy.clip(inputimage,
                      numpy.mean(inputimage) - (clip * numpy.std(inputimage)),
                      numpy.mean(inputimage) + (clip * numpy.std(inputimage)))

if 'anomalocaris' in platform.node():
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

# Set up logging
LogFileName = os.path.join(RootFolder, 'BrightnessOutput', 'Logfile.log')
log = logging.getLogger(LogFileName)
log.setLevel(logging.INFO)
handler = logging.FileHandler(LogFileName, 'w')
log.addHandler(handler)

# Start
log.info('Analsyis performed at %s', time.strftime('%d.%m.%Y at %H:%M:%S'))
log.info('Analsyis performed with ' + sys.argv[0] + ' version %s', get_git_hash())
log.info('\n' + 80 * '-')
log.info('{0: <15}'.format('Scintillator') + '{0: <8}'.format('Sensor') +
         '{0: <24}'.format('Lens') + '{0: <8}'.format('Mean') +
         '{0: <8}'.format('Max'))
plt.ion()
for CounterLens, CurrentLens in enumerate(Lenses):
    log.info(80 * '-')
    print 'Lens', CounterLens + 1, 'of', len(Lenses), '|', CurrentLens
    CombinationCounter = 0
    for CounterScintillator, CurrentScintillator in enumerate(Scintillators):
        for CounterSensor, CurrentSensor in enumerate(Sensors):
            CombinationCounter += 1
            print '\tFolder', CombinationCounter, 'of',\
                len(Scintillators) * len(Sensors), '|', CurrentScintillator, \
                '|', CurrentSensor, '|', CurrentLens, '|',
            ImageNames = sorted(glob.glob(
                os.path.join(RootFolder, CurrentScintillator, CurrentSensor,
                             CurrentLens, 'Hand', '*.image.corrected.png')))
            if len(ImageNames):
                print len(ImageNames), 'images found'
            else:
                print 'No images found for this combination!'

            # Extract values
            Images = [plt.imread(image) for image in ImageNames]
            CropImages = True
            if CropImages:
                Ycrop = (Images[0].shape[0] - 500) / 2
                Xcrop = (Images[0].shape[1] - 500) / 2
                Images = [plt.imread(image)[Ycrop:-Ycrop, Xcrop:-Xcrop] for
                          image in ImageNames]
            Min = [numpy.min(image) for image in Images]
            Mean = [numpy.mean(image) for image in Images]
            Max = [numpy.max(image) for image in Images]
            STD = [numpy.std(image) for image in Images]

            # Log values
            log.info('{0: <15}'.format(CurrentScintillator) +
                     '{0: <8}'.format(CurrentSensor) +
                     '{0: <24}'.format(CurrentLens) +
                     '{0: <8}'.format(str(round(numpy.mean(Mean), 5))) +
                     '{0: <8}'.format(str(round(numpy.max(Mean), 5))))

            OverViewFigure = plt.figure(0, figsize=[20, 12])
            OverViewPlot = plt.subplot(len(Scintillators), len(Sensors),
                                       CombinationCounter)

            # Plot Mean
            OverViewPlot.plot(Mean, linestyle='-', marker='.', color='k',
                              label='Max: %0.3f' % numpy.max(Mean))
            # Prepare for plotting the mean +- STD as a band around the mean
            MeanPlusSTD = [Mean[i] + STD[i] for i in range(len(Mean))]
            MeanMinusSTD = [Mean[i] - STD[i] for i in range(len(Mean))]
            # Fill the band between Mean+STD and Mean-STD
            OverViewPlot.fill_between(range(len(Mean)), MeanPlusSTD,
                                      MeanMinusSTD, alpha=0.309, color='k')

            # Plot the mean of the mean and the band between the mean of the
            # mean +- the mean of the STD
            OverViewPlot.axhline(numpy.mean(Mean), linestyle='-', color='r',
                                 label='Mean: %0.3f' % numpy.mean(Mean))
            OverViewPlot.fill_between(range(len(Mean)),
                                      numpy.mean(Mean) + numpy.mean(STD),
                                      numpy.mean(Mean) - numpy.mean(STD),
                                      alpha=0.309, color='r')

            # Scale all the plots the same way, so we can compare them
            plt.ylim((0, 0.75))
            plt.xlim((0, len(Images) - 1))
            OverViewPlot.legend(loc='upper left')
            plt.title(' | '.join([CurrentScintillator, CurrentSensor,
                                  CurrentLens]))
            plt.pause(0.1)
            plt.draw()

            # Show all the images of this component combination , so that we
            # can quickly see which ones are good and which ones are not
            LensFigure = plt.figure(CombinationCounter, figsize=[12, 13])
            plt.suptitle(' | '.join([CurrentScintillator, CurrentSensor,
                                     CurrentLens]))
            DisplayStrechedImages = True
            for c, i in enumerate(Images):
                ImagesPlot = plt.subplot(6, 6, c + 1)
                if DisplayStrechedImages:
                    ImagesPlot.imshow(processimage(i), cmap='bone_r',
                                      interpolation='bicubic')
                else:
                    ImagesPlot.imshow(i, cmap='bone_r',
                                      interpolation='bicubic')
                ImagesPlot.axis('off')
                plt.title('\n'.join([os.path.basename(ImageNames[c]).split(
                    '.')[0], 'Mean ' + str(round(Mean[c], 2))]))
            try:
                os.makedirs(os.path.join(RootFolder, 'BrightnessOutput',
                                         CurrentLens))
            except OSError:
                pass
            LensFigure.savefig(os.path.join(RootFolder, 'BrightnessOutput',
                                            CurrentLens, 'Images_' +
                                            CurrentScintillator + '_' +
                                            CurrentSensor + '_' +
                                            CurrentLens + '.png'))
            plt.pause(0.1)
            plt.draw()
    # Display
    OverViewFigure.tight_layout()
    OverViewFigure.savefig(os.path.join(RootFolder, 'BrightnessOutput',
                                        'Overview_' + CurrentLens + '.png'))
    print
    print 'Done with', CurrentLens
    print 80 * '-'
    plt.pause(0.1)
    plt.draw()
    plt.ioff()
    # plt.show()
    plt.close('all')

print 'Done with everything'
