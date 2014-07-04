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

BaseDir = '/afs/psi.ch/project/EssentialMed/Images/Lens_FOV_and_Distance'

SensorList = [os.path.basename(i) for
    i in sorted(glob.glob(os.path.join(BaseDir, '*')))]

for Sensor in SensorList:
    print Sensor
    Images = sorted(glob.glob(os.path.join(BaseDir, Sensor, '*.raw')))
    Lens = [os.path.basename(item).split('_')[1] for item in Images]
    ImageWidth = [int(os.path.basename(item).split('_')[2].split('x')[0])
        for item in Images]
    ImageHeight = [int(os.path.basename(item).split('_')[2].split('x')[1])
        for item in Images]
    SDD = [int(os.path.basename(item).split('_')[3].split('mm')[0])
        for item in Images]
    ExposureTime = [int(os.path.basename(item).split('_')[4].split('ms')[0])
        for item in Images]
    # Original images
    plt.figure(1)
    for counter, item in enumerate(Images):
        print str(counter + 1).zfill(len(str(len(Images)))) + '/' + \
            str(len(Images)) + '| Distance', str(SDD[counter]).rjust(3), \
            'mm | Exp.', str(ExposureTime[counter]).rjust(2), 'ms | Lens', \
            Lens[counter]
        # The RAW files are "16-bit Unsigned" with the "Width" and "Height" in
        # "Little-Endian byte order"
        Size = [ImageHeight[counter], ImageWidth[counter]]
        rawimage = np.fromfile(Images[counter], dtype=np.uint16).reshape(Size)
        plt.subplot(3, int(np.ceil(len(Images) / 3)), counter + 1)
        # increase contrast
        plt.imshow(rawimage, cmap=plt.cm.gray, vmin=512,
                   vmax=rawimage.max() * 0.9)
        # draw contour
        plt.contour(rawimage, [rawimage.max() / 2])
        ImageTitle = str(Lens[counter]), '\nExp. time', \
            str(ExposureTime[counter]), 'ms, Dist.', str(SDD[counter]), 'mm'
        plt.title(' '.join(ImageTitle))
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(os.path.join(BaseDir,
                    'SensorLensCombination_' + Sensor + '.png'))
    plt.show()
    print
