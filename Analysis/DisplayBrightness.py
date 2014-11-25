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

# Setup
ShowMax = False
if ShowMax:
    mycolors = ["#A35540", "#95BD56", "#9F5EAB", "#7E9A99"]
else:
    mycolors = ["", "#90BA6D", "#966FAD", "#9F5845"]

for lens in Lenses:
    plt.figure(figsize=[20, 12])
    MaximalNumberOfImages = 0
    MaximalMean = 0
    counter = 0
    for scintillator in Scintillators:
        for sensor in Sensors:
            counter += 1
            plt.subplot(len(Scintillators), len(Sensors), counter)
            print str(counter) + '/' + str(len(Scintillators) * len(
                Sensors)), '|',  scintillator, '|', sensor,  '|', \
                lens, '|',
            LoadStretched = False
            if LoadStretched:
                ImageNames = glob.glob(os.path.join(RootFolder, scintillator,
                                                    sensor, lens, 'Hand',
                                                    '*.image.corrected.' +
                                                    'stretched.png'))
            else:
                ImageNames = glob.glob(os.path.join(RootFolder, scintillator,
                                                    sensor, lens, 'Hand',
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

            # Collect some overview values for presentation later on
            MaximalNumberOfImages = max(MaximalNumberOfImages, len(ImageNames))
            MaximalMean = max(MaximalMean, max(Mean))

            if ShowMax:
                plt.plot(Max, linestyle='none', marker='o', color=mycolors[
                    0], label='Mean')
                plt.axhline(numpy.mean(Max), linestyle='--', color=mycolors[0])
            # Min
            plt.plot(Min, linestyle='none', marker='o', color=mycolors[1],
                     label='Min')
            plt.axhline(numpy.mean(Min), linestyle='--', color=mycolors[1])
            # Mean
            plt.plot(Mean, linestyle='none', marker='o', color=mycolors[2],
                     label='Mean')
            plt.axhline(numpy.mean(Mean), linestyle='--', color=mycolors[2])
            # STD
            plt.plot(STD, linestyle='none', marker='o', color=mycolors[3],
                     label=' STD')
            plt.axhline(numpy.mean(STD), linestyle='--', color=mycolors[3])

            # Setup plots for nice display
            plt.legend(loc='upper center', ncol=4, fontsize=10).get_frame(
                ).set_alpha(0.5)
            # Scale all the plots the same way, so we can compare them
            plt.ylim((0, MaximalMean * 1.1))
            plt.xlim([0, MaximalNumberOfImages])
            plt.title(' | '.join([scintillator, sensor, lens]))

    # Display
    plt.tight_layout()
    plt.savefig(os.path.join(RootFolder, 'Brightness-Overview_' + lens +
                             '.png'))
    plt.show()
    print 'Done with', lens
    print 80 * '-'

