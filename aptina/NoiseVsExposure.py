'''
Script to visualize the "Noise vs. Exposure" data from DevWare

According to section 2.2.4.7 of the DevWareX help (http://is.gd/mt7FyF) we get
signal levels and different kinds of noise measurements by using the "Sensor
Control" > "Diagnostics" > "Noise vs. Exposure" tool.

The analyis report gives
- Signal
- RMS Dyn (temporal noise), Avg Dyn (temporal noise)
- FPN (fixed pattern noise), Col FPN (columnwise FPN), Row FPN (rowwise FPN)
- Col Dyn (columnwise temporal noise) and Row Dyn (rowwise temporal noise).

See the wiki page linkes above to see how the values are calulated.
'''

import glob
import os
import numpy
import matplotlib.pyplot as plt


def AskUser(Blurb, Choices):
    """ Ask for input. Based on function in MasterThesisIvan.ini """
    print(Blurb)
    for Counter, Item in enumerate(sorted(Choices)):
        print '    * [' + str(Counter) + ']:', Item
    Selection = []
    while Selection not in range(len(Choices)):
        try:
            Selection = int(input(' '.join(['Please enter the choice you',
                                            'want [0-' +
                                            str(len(Choices) - 1) +
                                            ']:'])))
        except:
            print 'You actually have to select *something*'
        if Selection not in range(len(Choices)):
            print 'Try again with a valid choice'
    print 'You selected', sorted(Choices)[Selection]
    return sorted(Choices)[Selection]

Root = '/afs/psi.ch/project/EssentialMed/Images/NoiseVsExposure'
DataFiles = [os.path.basename(i) for
    i in glob.glob(os.path.join(Root, '*.txt'))]

# Which plot do we show?
whichone = DataFiles.index(AskUser('Which file should I show you?', DataFiles))

# Tell what we do
Sensor = DataFiles[whichone][:-4].split('_')[0]
Lens = DataFiles[whichone][:-4].split('_')[1]
FramesPerSample = DataFiles[whichone][:-4].split('_')[2]
MaximumExposure = DataFiles[whichone][:-4].split('_')[3]
Decades = DataFiles[whichone][:-4].split('_')[4]
SamplesPerDecade = DataFiles[whichone][:-4].split('_')[5]

print 'We are showing the data from the', Sensor, 'CMOS with the',  Lens, \
    'lens. The analysis was done with', FramesPerSample, \
    'frames per sample,', MaximumExposure, 'ms maximum exposure over', \
    Decades, 'decades with', SamplesPerDecade, 'samples per decade.'
print
print 'If the exposure has not been recorded in "log scale" (you will see',\
    'it in the plots), the "Decades" correspond to the "minimal exposure"',\
    'and the "samples per decade" correspond to the "numbers of samples".'

# Generate figure title, so we can distinguish the output
Title = Sensor, Lens, FramesPerSample, 'Frames per Sample', MaximumExposure, \
    'ms Maximum Exposure', Decades, 'Decades', SamplesPerDecade, \
    'Samples/Decade'

# Load the data from the file
File = os.path.join(Root, DataFiles[whichone])
Data = numpy.loadtxt(File, skiprows=3)
## First line gives the full range. Read it with the snippet based on
## http://stackoverflow.com/a/1904455
with open(File, 'r') as f:
    FullRange = int(f.readline().split('=')[1])

# Plot the data
Labels = ['Exposure time [ms]',
    'Signal',
    'RMS Dyn (temporal noise)',
    'Avg Dyn (temporal noise)',
    'FPN (fixed pattern noise)',
    'columnwise FPN',
    'rowwise FPN',
    'columnwise temporal noise',
    'rowwise temporal noise']
## The title of the plot is split over all the suplots, otherwise it destroys
## the layout due to its long length
plt.figure(' '.join(Title), figsize=(16, 9))
## Signal
plt.subplot(131)
plt.plot(Data[:, 0], Data[:, 1], 'o-', label=Labels[1])
plt.axhline(FullRange, linestyle='--', label='Full range')
plt.xlabel(Labels[0])
plt.ylabel(Labels[1])
plt.legend(loc='best')
plt.title(' '.join(Title[:2]))

## Fixed pattern noise
plt.subplot(132)
for i in range(4, 7):
    plt.plot(Data[:, 0], Data[:, i], 'o-', label=Labels[i])
plt.plot(Data[:, 0], Data[:, 1] / max(Data[:, 1]) * max(Data[:, 4]), '--',
    label='"Signal" scaled to FPN')
plt.xlabel(Labels[0])
plt.ylabel('FPN')
plt.legend(loc='best')
plt.title(' '.join(Title[2:6]))

# Temporal noise
plt.subplot(133)
for i in [2, 3, 7, 8]:
    plt.plot(Data[:, 0], Data[:, i], 'o-', label=Labels[i])
plt.plot(Data[:, 0], Data[:, 1] / max(Data[:, 1]) * max(Data[:, 2]), '--',
    label='"Signal" scaled to RMS Dyn')
plt.legend(loc='best')
plt.xlabel(Labels[0])
plt.ylabel('Dyn')
plt.title(' '.join(Title[6:]))
plt.tight_layout()
plt.savefig(os.path.join(Root, DataFiles[whichone][:-4] + '.png'),
            Transparent=True, bbox_inches='tight')
plt.draw()
plt.show()
