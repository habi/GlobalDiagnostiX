# -*- coding: utf-8 -*-

"""
Script to "grep" the log files for mean/max brightness of all the images for
each set of components.
And to display these values.
"""

from __future__ import division
import glob
import os
import re
import matplotlib.pyplot as plt
import time

import functions

RootFolder = ('/afs/psi.ch/project/EssentialMed/MasterArbeitBFH/XrayImages')

# Ask for what to do
Scintillators = ('AppScinTech-HE', 'Pingseng', 'Hamamatsu', 'Toshiba')
Sensors = ('AR0130', 'AR0132', 'MT9M001')
Lenses = ('Computar-11A', 'Framos-DSL219D-650-F2.0',
    'Framos-DSL224D-650-F2.0', 'Framos-DSL311A-NIR-F2.8',
    'Framos-DSL949A-NIR-F2.0', 'Lensation-CHR4020',
    'Lensation-CHR6020', 'Lensation-CM6014N3', 'Lensation-CY0614',
    'TIS-TBL-6C-3MP')
#~ ChosenScintillator = functions.AskUser(
    #~ 'Which scintillator do you want to look at?', Scintillators)
#~ ChosenSensor = functions.AskUser(
    #~ 'Which sensor do you want to look at?', Sensors)
ChosenLens = functions.AskUser(
    'Which lens do you want to look at? ("empty" = "all")',
    Lenses)

plt.figure(figsize=[12, 9])
counter = 0
for i, scintillator in enumerate(Scintillators):
    for k, sensor in enumerate(Sensors):
        counter += 1
        plt.subplot(len(Scintillators), len(Sensors), counter)
        Mean = []
        Max = []
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
        NormalizedMean = [i / max(Mean) for i in Mean]
        NormalizedMax = [i / max(Max) for i in Max]
        normalized = False
        if normalized:
            #~ plt.plot(NormalizedMax, '-o', label='normalized Max')
            plt.plot(NormalizedMean, '-o', label='normalized Mean')
        else:
            #~ plt.plot(Max, '-o', label='Max')
            plt.plot(Mean, '-o', label='Mean')
        plt.legend(loc='best')
        if normalized:
            plt.ylim([0,1])
        else:
            plt.ylim(ymin=0)
        plt.xlim([0, 35])
        plt.title('\n'.join([scintillator, sensor, ChosenLens]))

OutputName = os.path.join(RootFolder, 'Brightness-Overview_' + ChosenLens)
if normalized:
    OutputName += '_normalized'

# Display
plt.tight_layout()
plt.savefig(OutputName + '.png')
plt.show()
