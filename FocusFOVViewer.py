"""
Script to show some of the images from the Focus/FOV test.
Images in the given folder were saved with the
"[Python: Capture Multiple Exposures]" part of GDX.ini in DevWare of Aptina
"""
from __future__ import division
import os
import glob
import numpy as np
import matplotlib.pyplot as plt

Root = "/afs/psi.ch/project/EssentialMed/Images/13-Aptina_Focus_Test/FocusFOV"
#~ Root = "/scratch/tmp/DevWareX/FocusFOV"  # normalized images

SensorList = [os.path.basename(i) for
    i in sorted(glob.glob(os.path.join(Root, '*')))]

for Sensor in SensorList:
    Images = sorted(glob.glob(os.path.join(Root, Sensor, '*.raw')))
    Height = [int(os.path.basename(i).split('_')[1].split('x')[1])
        for i in Images]
    Width = [int(os.path.basename(i).split('_')[1].split('x')[0])
        for i in Images]
    Lens = [os.path.basename(i).split('_')[2] for i in Images]
    SDD = [float(os.path.basename(i).split('_')[3].split('mm')[0])
        for i in Images]
    Focus = [float(os.path.basename(i).split('_')[4]) for i in Images]
    Aperture = [float(os.path.basename(i).split('_')[5][:-1]) for i in Images]
    ExposureTime = [os.path.basename(i).split('_')[6].split('ms')[0]
        for i in Images]

    #~ Open the RAW files in Fiji as "16-bit Unsigned" with the "Width" and
    #~ "Height" given in the DevWare-window and with "Little-Endian byte order"
    print 80 * "-"
    print os.path.join(Root, Sensor)
    plt.figure(figsize=(32, 18))
    for i, item in enumerate(Images):
        print str(i).zfill(2) + "/" + str(len(Images)), "|", Sensor, "|",\
            Lens[i]
        rawimage = np.memmap(Images[i], dtype=np.uint16,
                            shape=(Height[i], Width[i]))  # .byteswap()
        plt.subplot(3, int(np.ceil(len(Images) / 3)), i + 1)
        plt.imshow(rawimage, cmap=plt.cm.gray)
        ImageTitle = Lens[i], '\nFocus',  str(Focus[i]), \
            'Aperture', str(Aperture[i]), 'f\nExp. time', \
            str(ExposureTime[i]), 'ms, Dist.', str(SDD[i]), 'mm'
        plt.title(' '.join(ImageTitle))
    #~ plt.subplot(3,5,15)
    #~ plt.title(Sensor,fontsize=20)
    plt.tight_layout()
    plt.savefig('SensorLensCombination_' + Sensor + '.png')
    #~ plt.savefig('SensorLensCombinationEnhanced_' + Sensor + '.png')
    plt.show()
