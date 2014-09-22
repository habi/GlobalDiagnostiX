# -*- coding: utf-8 -*-

"""
This script loads the log files gerated with http://git.io/Ydwc8A and plots
the exposure time, brightness of the brightest image and scintillator-CMOS-
distance in 3D.

This should help to visualize the results and come to a conclusion on which
combination of components is the best to use
"""
import glob
import os
import linecache
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy
import sys

# Where shall we start?
if 'linux' in sys.platform:
    # If running at the office, grep AFS
    RootFolder = ('/afs/psi.ch/project/EssentialMed/MasterArbeitBFH/' +
        'XrayImages')
    #~ StartingFolder = os.path.join(RootFolder, '20140721')  # 11
    #~ StartingFolder = os.path.join(RootFolder, '20140722')  # 44
    #~ StartingFolder = os.path.join(RootFolder, '20140724')  # 91
    #~ StartingFolder = os.path.join(RootFolder, '20140730')  # 30
    #~ StartingFolder = os.path.join(RootFolder, '20140731')  # 262
    #~ StartingFolder = os.path.join(RootFolder, '20140818')  # 20
    #~ StartingFolder = os.path.join(RootFolder, '20140819')  # 64
    #~ StartingFolder = os.path.join(RootFolder, '20140820')  # 64
    #~ StartingFolder = os.path.join(RootFolder, '20140822')  # 149
    #~ StartingFolder = os.path.join(RootFolder, '20140823')  # 6
    #~ StartingFolder = os.path.join(RootFolder, '20140825')  # 99
    #~ StartingFolder = os.path.join(RootFolder, '20140829')  # 4
    #~ StartingFolder = os.path.join(RootFolder, '20140831')  # 309
    #~ StartingFolder = os.path.join(RootFolder, '20140901')  # 149
    #~ StartingFolder = os.path.join(RootFolder, '20140903')  # 30
    #~ StartingFolder = os.path.join(RootFolder, '20140907')  # 277
    #~ StartingFolder = os.path.join(RootFolder, '20140914')  # 47
    StartingFolder = RootFolder
else:
    # If running on Ivans machine, look on the connected harddisk
    StartingFolder = ('/Volumes/WINDOWS/Aptina/Hamamatsu/AR0130/Computar-11A/')
    StartingFolder = ('/Volumes/exFAT')

# Generate a list of log files, based on http://stackoverflow.com/a/14798263
LogFiles = [os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(StartingFolder)
    for f in files if f.endswith('analysis.log')]

print 'I found', len(LogFiles), 'log files in', StartingFolder

# Grab all the necessary parameters from the log files
ExperimentID = \
    [int(linecache.getline(i, 1).split('ID')[1].split(',')[0].strip())
    for i in LogFiles]
Sensor = [linecache.getline(i, 10).split(':')[1].strip() for i in LogFiles]
Scintillator = [linecache.getline(i, 9).split(':')[1].strip()
    for i in LogFiles]
Lens = [str(linecache.getline(i, 11).split(':')[1].strip()) for i in LogFiles]
SDD = [float(linecache.getline(i, 13).split(':')[1].split('mm')[0].strip())
    for i in LogFiles]
Modality = [linecache.getline(i, 14).split(':')[1].strip()
    for i in LogFiles]
Exposuretime = [float(linecache.getline(i, 18)
    .split(':')[1].split('ms')[0].strip()) for i in LogFiles]
Max = [float(linecache.getline(i, 25).split(':')[1].strip())
    for i in LogFiles]
Mean = [float(linecache.getline(i, 26).split(':')[1].strip())
    for i in LogFiles]
STD = [float(linecache.getline(i, 27).split(':')[1].strip())
    for i in LogFiles]

# Information about what we did
print 'In these log files, we have data for'
print '\t-', len(set(Scintillator)), 'scintillators:'
for i in set(Scintillator):
    print '\t\t-', i
print '\t-', len(set(Sensor)), 'sensors:'
for i in set(Sensor):
    print '\t\t-', i
print '\t-', len(set(Lens)), 'lenses:'
for i in numpy.unique(Lens):
    print '\t\t-', i
print '\t- ', len(set(Modality)), 'modalities:'
for i in set(Modality):
    print '\t\t-', i


def subset(Selector, label=False):
    '''
    Select only a subset of items to present in the second plot, according to
    http://stackoverflow.com/a/3555387/323100
    '''
    MaskedX = [item for item, flag in zip(SDD, Scintillator) if Selector in
        flag]
    MaskedY = [item for item, flag in zip(Mean, Scintillator) if Selector in
        flag]
    MaskedZ = [item for item, flag in zip(STD, Scintillator) if Selector in
        flag]
    MaskedC = [item for item, flag in zip(STD, Scintillator) if Selector in
        flag]
    MaskedI = [str(item) for item, flag in zip(ExperimentID, Scintillator) if
        Selector in flag]
    plot = ax.scatter(
        MaskedX, MaskedY, MaskedZ,
        'o', c=MaskedC, cmap='hot', s=250)
    if label:
        for x, y, z, label in zip(MaskedX, MaskedY, MaskedZ, MaskedI):
            ax.text(x, y, z, label)
    ax.set_xlabel('Scintillator-CMOS distance [mm]')
    ax.set_ylabel('Mean brightness of best image')
    ax.set_zlabel('Standard deviation')

    ax.set_xlim([50, 300])
    ax.set_ylim([0, 500])
    ax.set_zlim([0, 100])

    plt.title(' '.join([str(len(MaskedX)),
        'images for', Selector]))
    return Selector

## Do the plot
fig = plt.figure(figsize=[16, 9])
# Plot figure
## Setup plot
plt.xkcd()
textalpha = 0.618

## Subplot Hamamatsu
ax = fig.add_subplot(221, projection='3d')
subset('Hamamatsu')

## Subplot Pingseng
ax = fig.add_subplot(222, projection='3d')
subset('Pingseng')

## Subplot Toshiba
ax = fig.add_subplot(223, projection='3d')
subset('Toshiba')

## Subplot AppScinTech
ax = fig.add_subplot(224, projection='3d')
subset('AppScinTech')

plt.tight_layout()
OutputImage = os.path.join(StartingFolder, 'Overview.png')
print 'Saving figure as', OutputImage
plt.savefig(OutputImage, transparent=True)

plt.show()
