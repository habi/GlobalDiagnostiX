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

# Where shall we start?
RootFolder = ('/afs/psi.ch/project/EssentialMed/MasterArbeitBFH/' +
    'XrayImages')
StartingFolder = os.path.join(RootFolder, '20140721')
#~ StartingFolder = os.path.join(RootFolder, '20140722')
#~ StartingFolder = os.path.join(RootFolder, '20140724')
#~ StartingFolder = os.path.join(RootFolder, '20140730')
#~ StartingFolder = os.path.join(RootFolder, '20140731')
#~ StartingFolder = os.path.join(RootFolder, '20140818')
#~ StartingFolder = os.path.join(RootFolder, '20140819')
#~ StartingFolder = os.path.join(RootFolder, '20140820')
#~ StartingFolder = os.path.join(RootFolder, '20140822')
#~ StartingFolder = os.path.join(RootFolder, '20140823')
#~ StartingFolder = os.path.join(RootFolder, '20140825')
StartingFolder = os.path.join(RootFolder)

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
SSD = [float(linecache.getline(i, 13).split(':')[1].split('mm')[0].strip())
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
#~ for i in LogFiles:
    #~ print i
    #~ print float(linecache.getline(i, 25).split(':')[1].strip())
    #~ print 80*'-'
#~ exit()

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

# Plot figure
## CMOS-Distance
fig = plt.figure(figsize=[16, 9])
fig.suptitle(' '.join(['Data from', str(len(LogFiles)),
    'log files from', StartingFolder, 'colored by STD']))
ax = fig.add_subplot(121, projection='3d')
plot = ax.scatter(
    SSD, Mean, Max,
    'o', c=STD, edgecolor='', cmap='hot', s=250, alpha=0.5)
for x, y, z, label in zip(
    SSD, Mean, Max,
    zip(Sensor, Lens)):
    ax.text(x, y + 0.2, z + 0.2, ' / '.join(label), alpha=0.25)

#~ ax.set_xlim([66, 222])
#~ ax.set_ylim([0, 750])
#~ ax.set_zlim([0, 1000])

ax.set_xlabel('Scintillator-CMOS distance [mm]')
ax.set_ylabel('Mean Brightness of best image')
ax.set_zlabel('Max Brightness of best image')
plt.title('Modality')

# Select only a subset of items to present in the second plot, according to
# http://stackoverflow.com/a/3555387/323100
MaskedX = [item for item, flag in zip(Max, Scintillator) if 'AppS' in flag]
MaskedY = [item for item, flag in zip(Mean, Scintillator) if 'AppS' in flag]
MaskedZ = [item for item, flag in zip(STD, Scintillator) if 'AppS' in flag]
MaskedC = [item for item, flag in zip(STD, Scintillator) if 'AppS' in flag]
MaskedI = [str(item) for item, flag in zip(ExperimentID, Scintillator) if
    'AppS' in flag]

## AppScinTech
ax = fig.add_subplot(122, projection='3d')
plot = ax.scatter(
    MaskedX, MaskedY, MaskedZ,
    'o', c=MaskedC, cmap='hot', s=250)
for x, y, z, label in zip(
    MaskedX, MaskedY, MaskedZ,
    zip(MaskedI)):
    ax.text(x, y + 0.2, z + 0.2, ' / '.join(label), alpha=0.25)

ax.set_xlabel('Max')
ax.set_ylabel('Mean')
ax.set_zlabel('STD')
plt.title(' '.join([str(len(MaskedX)),
    'values where Scintillator=AppScinTech']))

plt.tight_layout()

OutputImage = os.path.join(StartingFolder, '_Overview.png')
print 'Saving figure as', OutputImage
plt.savefig(OutputImage, transparent=False)

plt.show()
