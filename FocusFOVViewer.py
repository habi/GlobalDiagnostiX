"""
Script to view the images from the lens-test (FOV and distance)
The 'old' version from the first lenses was before git commit a100d19

We load the RAW images in the folder for each sensor and give out some
information on the images (distance, exposure time, etc) in a nice image

The images were acquired with the INI file part "[Python: Focus-Distance-Test
for Ivan]" of GDX.ini in DevWare
"""
from __future__ import division
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, \
     AnnotationBbox

BaseDir = '/afs/psi.ch/project/EssentialMed/Images/Lens_FOV_and_Distance'

SensorList = []
for item in os.listdir(BaseDir):
    if not os.path.isfile(os.path.join(BaseDir, item)):
        SensorList.append(item)

for Sensor in SensorList:
    print Sensor
    ImageFiles = sorted(glob.glob(os.path.join(BaseDir, Sensor, '*.raw')))
    Lens = [os.path.basename(item).split('_')[1] for item in ImageFiles]
    ImageSize = [[int(os.path.basename(item).split('_')[2].split('x')[1]),
                  int(os.path.basename(item).split('_')[2].split('x')[0])]
                  for item in ImageFiles]
    # The RAW files are "16-bit Unsigned" with the "Width" and "Height" in
    # "Little-Endian byte order"
    ImageData = [np.fromfile(item, dtype=np.uint16).reshape(
        ImageSize[ImageFiles.index(item)])
        for item in ImageFiles]
    SDD = [int(os.path.basename(item).split('_')[3].split('mm')[0])
        for item in ImageFiles]
    ExposureTime = [int(os.path.basename(item).split('_')[4].split('ms')[0])
        for item in ImageFiles]
    # Original images
    plt.figure(figsize=(16, 9))
    for counter, item in enumerate(ImageFiles):
        print str(counter + 1).zfill(len(str(len(ImageFiles)))) + '/' + \
            str(len(ImageFiles)) + '| Distance', str(SDD[counter]).rjust(3), \
            'mm | Exp.', str(ExposureTime[counter]).rjust(2), 'ms | Lens', \
            Lens[counter]
        plt.subplot(3, int(np.ceil(len(ImageFiles) / 3)), counter + 1)
        # Show images
        plt.imshow(ImageData[counter], cmap=plt.cm.gray)
        # increase contrast
        #~ plt.imshow(ImageData[counter], cmap=plt.cm.gray, vmin=512,
                   #~ vmax=rawimage.max() * 0.9)
        # draw contour
        #~ plt.contour(ImageData[counter], [rawimage.max() / 2])
        ImageTitle = str(Lens[counter]), '\nExp. time', \
            str(ExposureTime[counter]), 'ms, Dist.', str(SDD[counter]), 'mm'
        plt.title(' '.join(ImageTitle))
        plt.axis('off')
    plt.draw()
    # Save plot to an image we can view
    ImageOverview = os.path.join(BaseDir, Sensor + '_Images.png')
    plt.savefig(ImageOverview)
    print 'Overview image saved to', ImageOverview
    print 'SDD varies from', min(SDD), 'to', max(SDD), 'mm'
    print 'Exposure times vary from', min(ExposureTime), 'to',\
        max(ExposureTime), 'ms'
    # Scatter plot with and without images, according to
    # http://matplotlib.org/examples/pylab_examples/demo_annotation_box.html
    plt.figure(figsize=(16, 9))
    ax = plt.subplot(121)
    for counter, item in enumerate(ImageFiles):
        imagebox = OffsetImage(ImageData[counter], zoom=0.1, cmap=plt.cm.gray)
        SubImage = AnnotationBbox(imagebox,
                                  [SDD[counter], ExposureTime[counter]], pad=0)
        ax.add_artist(SubImage)
    plt.xlim([0, max(SDD)])
    plt.ylim([0, max(ExposureTime)])
    plt.xlabel('Szintillator-Sensor-Distance [mm]')
    plt.ylabel('Exposure time [ms]')
    ax.grid(True)
    # Scatter plot
    plt.subplot(122)
    plt.plot(SDD, ExposureTime, linestyle='', marker='o')
    plt.title(Sensor)
    plt.xlabel('Szintillator-Sensor-Distance [mm]')
    plt.ylabel('Exposure time [ms]')
    plt.grid(True)
    plt.draw()
    ImageDistances = os.path.join(BaseDir, Sensor + '_Scatterplot.png')
    plt.savefig(ImageDistances)
    print 'Overview image saved to', ImageDistances
    print 80 * '-'
    plt.show()
