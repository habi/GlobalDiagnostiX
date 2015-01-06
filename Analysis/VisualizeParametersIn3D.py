# -*- coding: utf-8 -*-

"""
VisualizeParametersin3D.py | David Haberthür <david.haberthuer@psi.ch>

This script loads the log files gerated with http://git.io/Ydwc8A and plots
the exposure time, brightness of the brightest image and scintillator-CMOS-
distance in 3D.

This should help to visualize the results and come to a conclusion on which
combination of components is the best to use
"""

import os
import linecache
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
import numpy
import sys

# Where shall we start?
if 'linux' in sys.platform:
    # If running at the office, grep folders from AFS
    RootFolder = '/afs/psi.ch/project/EssentialMed/MasterArbeitBFH/XrayImages'
    # Look for images of only one scintillator
    StartingFolder = os.path.join(RootFolder, 'AppScinTechHE')
    StartingFolder = os.path.join(RootFolder, 'Hamamatsu')
    StartingFolder = os.path.join(RootFolder, 'Pingseng')
    StartingFolder = os.path.join(RootFolder, 'Toshiba')
    # Look through all folders
    StartingFolder = RootFolder
else:
    # If running on Ivans machine, look on the connected harddisk
    StartingFolder = '/Volumes/WINDOWS/Aptina/Hamamatsu/AR0130/Computar-11A/'
    StartingFolder = '/Volumes/exFAT'

# Generate a list of log files, based on http://stackoverflow.com/a/14798263
LogFiles = [os.path.join(dirpath, f)
            for dirpath, dirnames, files in os.walk(StartingFolder)
            for f in files if f.endswith('analysis.log')]

print 'I found', len(LogFiles), 'log files in', StartingFolder
print 'Reading *all* necessary values from them.'

# Grab all the necessary parameters from the log files
ExperimentID = \
    [int(linecache.getline(i, 1).split('ID')[1].split(',')[0].strip()) for i
     in LogFiles]
Sensor = [linecache.getline(i, 10).split(':')[1].strip() for i in LogFiles]
Scintillator = [linecache.getline(i, 9).split(':')[1].strip() for i in LogFiles]
Lens = [str(linecache.getline(i, 11).split(':')[1].strip()) for i in LogFiles]
SDD = [float(linecache.getline(i, 13).split(':')[1].split('mm')[0].strip())
       for i in LogFiles]
Modality = [linecache.getline(i, 14).split(':')[1].strip() for i in LogFiles]
Exposuretime = [float(linecache.getline(i, 18).split(
    ':')[1].split('ms')[0].strip()) for i in LogFiles]
Max = [float(linecache.getline(i, 25).split(':')[1].strip()) for i in LogFiles]
Mean = [float(linecache.getline(i, 26).split(':')[1].strip()) for i in LogFiles]
STD = [float(linecache.getline(i, 27).split(':')[1].strip()) for i in LogFiles]

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

print
print 'Values go from'
print 'Exptime\t', min(Exposuretime), '-', max(Exposuretime)
print 'SDD\t', min(SDD), '-', max(SDD)
print 'Mean\t', min(Mean), '-', max(Mean)
print 'Max\t', min(Max), '-', max(Max)
print 'STD\t', min(STD), '-', max(STD)
print

histograms = False
if histograms:
    plt.figure(figsize=(16, 9))
    plt.subplot(151)
    plt.hist(Exposuretime, bins=128, normed=False, histtype='stepfilled')
    plt.title('Exposure times')
    plt.subplot(152)
    plt.hist(SDD, bins=128, normed=False, histtype='stepfilled')
    plt.title('Scintillator-detector distances')
    plt.subplot(153)
    plt.hist(Mean, bins=128, normed=False, histtype='stepfilled')
    plt.title('Image mean')
    plt.subplot(154)
    plt.hist(Max, bins=128, normed=False, histtype='stepfilled')
    plt.title('Image max')
    plt.subplot(155)
    plt.hist(STD, bins=128, normed=False, histtype='stepfilled')
    plt.title('Image standard deviation')
    plt.tight_layout()
    plt.draw()


def subset_seletor(selector, label=False):
    """
    Select only a subset of items to present in the second plot, according to
    http://stackoverflow.com/a/3555387/323100
    """
    maskedx = [item for item, flag in zip(SDD, Scintillator) if selector in
               flag]
    maskedy = [item for item, flag in zip(Mean, Scintillator) if selector in
               flag]
    maskedz = [item for item, flag in zip(STD, Scintillator) if selector in
               flag]
    maskedc = [item for item, flag in zip(STD, Scintillator) if selector in
               flag]
    maskedi = [str(item) for item, flag in zip(ExperimentID, Scintillator) if
               selector in flag]
    currentaxis = fig.gca()
    currentaxis.scatter(maskedx, maskedy, maskedz, 'o', s=250, c=maskedc)
    if label:
        for x, y, z, label in zip(maskedx, maskedy, maskedz, maskedi):
            currentaxis.text(x, y, z, label)

    currentaxis.set_xlabel('Scintillator-CMOS distance [mm]')
    currentaxis.set_ylabel('Mean brightness')
    currentaxis.set_zlabel('Standard deviation')

    currentaxis.set_xlim([50, 300])
    currentaxis.set_ylim([0, 500])
    currentaxis.set_zlim([0, 200])

    plt.title(' '.join([str(len(maskedx)), 'images for', selector]))
    return selector

## Prepare the plot
fig = plt.figure(figsize=(16, 9))
# Plot figure
## Setup plot
#~ plt.xkcd()
textalpha = 0.618

## Subplot Hamamatsu
ax1 = fig.add_subplot(221, projection='3d')
subset_seletor('Hamamatsu', label=False)

## Subplot Pingseng
ax2 = fig.add_subplot(222, projection='3d')
subset_seletor('Pingseng', label=False)

## Subplot Toshiba
ax3 = fig.add_subplot(223, projection='3d')
subset_seletor('Toshiba', label=False)

## Subplot AppScinTech
ax4 = fig.add_subplot(224, projection='3d')
subset_seletor('AppScinTech', label=False)

plt.tight_layout()

Animate = False
if Animate:
    # Initialization function: Initialize plot, move the camera
    def init():
        azimuth = 45
        elevation = 30
        for ax in (ax1, ax2, ax3, ax4):
            ax.azim = azimuth
            ax.elev = elevation
        return ax1, ax2, ax3, ax4,

    # Animation function.
    def animate_camera(framenumber):
        for ax in (ax1, ax2, ax3, ax4):
            ax.azim = 45 + 40 * numpy.sin(numpy.radians(framenumber))
            ax.elev = 30 + 10 * numpy.sin(numpy.radians(framenumber))
        print 'animating frame', framenumber, 'of', numframes
        return ax1, ax2, ax3, ax4,

    # Call the actual animation function.
    numframes = 360
    Movie = animation.FuncAnimation(fig, animate_camera, init_func=init,
                                    frames=numframes, interval=10, blit=True)

    # Save the animation as an mp4.
    Movie.save('scintillators.mp4', fps=24, extra_args=['-vcodec', 'libx264'])

    plt.show()
else:
    # Choose view
    # Like in movie: 66/15
    # Brightness-Distance 0/90
    # STD-Distance 90/0
    # STD-Brightness 0/0
    Azimuth = 45
    Elevation = 30
    for axis in (ax1, ax2, ax3, ax4):
        axis.azim = Azimuth
        axis.elev = Elevation
    ImageName = 'Overview_az_' + str(Azimuth) + '_el_' + str(Elevation) + \
        '.png'
    plt.savefig(ImageName, transparent=True)
    plt.show()
