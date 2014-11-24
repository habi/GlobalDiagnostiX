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

import functions

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
ChosenLens = functions.AskUser(
    'Which lens do you want to look at?',
    Lenses)

mycolors = ['#9F5845' ,'#90BA6D', '#966FAD']

plt.figure(figsize=[12, 9])
counter = 0

ShowNormalizedValues = False
ShowMax = False

for i, scintillator in enumerate(Scintillators):
    for k, sensor in enumerate(Sensors):
        counter += 1
        plt.subplot(len(Scintillators), len(Sensors), counter)
        Mean = []
        Max = []
        STD = []
        print 80 * '-'
        print scintillator, '|', sensor, '|', ChosenLens, '|',
        LogFiles = glob.glob(os.path.join(RootFolder, scintillator, sensor,
                                          ChosenLens, 'Hand', '*.analysis.log'))
        try:
            print len(LogFiles), 'log files'
        except:
            print 'No log files found for this combination'
            exit()
        for log in LogFiles:
            for line in open(log, "r"):
                if '* Mean:' in line:
                    Mean.append(float(line.split(':')[1].strip()))
                if '* Max:' in line:
                    Max.append(float(line.split(':')[1].strip()))
                if '* STD:' in line:
                    STD.append(float(line.split(':')[1].strip()))
        if ShowNormalizedValues:
            NormalizedMean = [i / max(Mean) for i in Mean]
            NormalizedMax = [i / max(Max) for i in Max]
            NormalizedSTD = [i / max(STD) for i in STD]
            if ShowMax:
                plt.plot(NormalizedMax, linestyle='none', marker='o',
                    color=mycolors[0], label='normalized Max')
                plt.axhline(numpy.mean(NormalizedMax), linestyle='--',
                    color=mycolors[0], label='mean of normalized Max')
            plt.plot(NormalizedMean, linestyle='none', marker='o',
                color=mycolors[1], label='normalized Mean')
            plt.axhline(numpy.mean(NormalizedMean), linestyle='--',
                color=mycolors[1], label='mean of normalized Mean')
            plt.plot(NormalizedSTD, linestyle='none', marker='o',
                color=mycolors[2], label='normalized STD')
            plt.axhline(numpy.mean(NormalizedSTD), linestyle='--',
                color=mycolors[2], label='mean of normalized STD')
        else:
            if ShowMax:
                plt.plot(Max, linestyle='none', marker='o', color=mycolors[0],
                    label='Mean')
                plt.axhline(numpy.mean(Max), linestyle='--', color=mycolors[0],
                    label='mean Max')
            plt.plot(Mean, linestyle='none', marker='o', color=mycolors[1],
                label='Mean')
            plt.axhline(numpy.mean(Mean), linestyle='--', color=mycolors[1],
                label='mean Mean')
            plt.plot(STD, 'o', linestyle='none', marker='o', color=mycolors[2],
                label='STD')
            plt.axhline(numpy.mean(STD), linestyle='-', color=mycolors[2],
                label='mean STD')
        #~ plt.legend(loc='best')
        #~ plt.suptitle('Green = Mean, Blue = STD')
        if ShowNormalizedValues:
            plt.ylim([0, 1])
        else:
            plt.ylim(ymin=0)
        plt.xlim([0, 35])
        plt.title('\n'.join([scintillator, sensor, ChosenLens]))

OutputName = os.path.join(RootFolder, 'Brightness-Overview_' + ChosenLens)
if ShowNormalizedValues:
    OutputName += '_normalized'

# Display
plt.tight_layout()
plt.savefig(OutputName + '.png')
plt.show()
