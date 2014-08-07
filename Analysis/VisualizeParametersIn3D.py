#!/usr/bin/python
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
StartingFolder = ('/afs/psi.ch/project/EssentialMed/MasterArbeitBFH/' +
    'XrayImages')

# Testing
#~ StartingFolder = ('/afs/psi.ch/project/EssentialMed/MasterArbeitBFH/' +
    #~ '/XrayImages/20140725/')
# Testing

# Generate a list of log files, based on http://stackoverflow.com/a/14798263
LogFiles = [os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(StartingFolder)
    for f in files if f.startswith('Analysis') and f.endswith('.log')]

print 'I found', len(LogFiles), 'log files in', StartingFolder

# Grab all the necessary parameters from the log files
ExperimentID = [linecache.getline(i, 1).split('ID')[1].split(',')[0].strip()
    for i in LogFiles]
Sensor = [linecache.getline(i, 7).split(':')[1].strip()
    for i in LogFiles]
Scintillator = [linecache.getline(i, 6).split(':')[1].strip()
    for i in LogFiles]
Lens = [str(linecache.getline(i, 8).split(':')[1].strip()) for i in LogFiles]
SSD = [float(linecache.getline(i, 10).split(':')[1].split('mm')[0].strip())
    for i in LogFiles]
Modality = [linecache.getline(i, 11).split(':')[1].strip()
    for i in LogFiles]
Exposuretime = [float(linecache.getline(i, 15)
    .split(':')[1].split('ms')[0].strip()) for i in LogFiles]
Max = [float(linecache.getline(i, 22).split(':')[1].strip())
    for i in LogFiles]
Mean = [float(linecache.getline(i, 23).split(':')[1].strip())
    for i in LogFiles]
STD = [float(linecache.getline(i, 24).split(':')[1].strip())
    for i in LogFiles]

# Information about what we did
print 'In these log files, we have data for'
print '\t- ', len(set(Scintillator)), 'scintillators: ',
for i in set(Scintillator):
    print i + ',',
print '\n\t- ', len(set(Sensor)), 'sensors:',
for i in set(Sensor):
    print i + ',',
print '\n\t- ', len(set(Lens)), 'lenses:',
for i in set(Lens):
    print i + ',',
print '\n\t- ', len(set(Modality)), 'modalities:',
for i in set(Modality):
    print i + ',',
print

# Possibility to select only one value
SelectedLens = 'Lensation-CVM0411ND'
Selection = numpy.ma.masked_where(numpy.asarray(Lens) != SelectedLens, Lens)
print
print 'If we select only the', SelectedLens, 'lens we display', \
    len(Selection.compressed()), 'experiments with the IDs'
for i in numpy.ma.masked_array(ExperimentID, Selection.mask).compressed():
    print '\t-', i
    print '\t\tin folder', \
        os.path.dirname(LogFiles[ExperimentID.index(i)])[len(StartingFolder) +  1:]
    print '\t\twith a mean of', Mean[ExperimentID.index(i)]

# Display information about the selected experiments

# Plot figure
fig = plt.figure()
ax = fig.gca(projection='3d')
plot = ax.scatter(
    numpy.ma.masked_array(Exposuretime, Selection.mask),
    numpy.ma.masked_array(SSD, Selection.mask),
    numpy.ma.masked_array(Mean, Selection.mask),
    'o', c=Mean, cmap='hot', s=250)
for x, y, z, label in zip(
    numpy.ma.masked_array(Exposuretime, Selection.mask),
    numpy.ma.masked_array(SSD, Selection.mask),
    numpy.ma.masked_array(Mean, Selection.mask),
    zip(Scintillator, ExperimentID)):
    ax.text(x, y, z + 0.05, '|'.join(label))

ax.set_xlabel('Exposure time [ms]')
ax.set_ylabel('Scintillator-CMOS distance [mm]')
ax.set_zlabel('Mean brightness of brightest image')
#~ ax.set_xlim([0,100]
#~ ax.set_ylim([0,750])
#~ ax.set_zlim([0,100])

cbar = fig.colorbar(plot, ticks=[min(Mean), 0, max(Mean)])
plt.title(' '.join(['Data from', str(len(LogFiles)), 'log files']))

plt.show()
