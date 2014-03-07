"""
Script to show some of the images from the Focus/FOV test.
Images in the given folder were saved with the
"[Python: Capture Multiple Exposures]" part of GDX.ini in DevWare of Aptina
"""

import os
import glob
import numpy as np
import matplotlib.pyplot as plt

Root = "/afs/psi.ch/project/EssentialMed/Images/13-Aptina_Focus_Test/FocusFOV"
Sensor = "AR0130"
Sensor = "AR0132"
Sensor = "MT9M001"

Images = sorted(glob.glob(os.path.join(Root, Sensor, '*.raw')))
Height = [int(os.path.basename(i).split('_')[1].split('x')[1]) for i in Images]
Width = [int(os.path.basename(i).split('_')[1].split('x')[0]) for i in Images]
Lens = [os.path.basename(i).split('_')[2] for i in Images]
SDD = [float(os.path.basename(i).split('_')[3].split('mm')[0]) for i in Images]
Focus = [float(os.path.basename(i).split('_')[4]) for i in Images]
Aperture = [float(os.path.basename(i).split('_')[5][:-1]) for i in Images]
ExposureTime = [os.path.basename(i).split('_')[6].split('ms')[0]
    for i in Images]

print Height[1]
print Width[1]
print Lens[1]
print SDD[1]
print Focus[1]
print Aperture[1]
print ExposureTime[1]

#~ Open the RAW files in Fiji as "16-bit Unsigned" with the "Width" and
#~ "Height" given in the DevWare-window and with "Little-Endian byte order"

for i, item in enumerate(Images):
    rawimage = np.memmap(Images[i], dtype=np.uint16,
                         shape=(Height[i], Width[i]))
    plt.imshow(rawimage, cmap=plt.cm.gray)
    ImageTitle = Sensor, 'with the lens', Lens[i], 'focused to', \
        str(Focus[i]), 'and aperture set to', str(Aperture[i]), \
        'f\nExposure time of', str(ExposureTime[i]), \
        'ms, giving a scintillator-headboard distance of', str(SDD[i]), 'mm'
    plt.title(' '.join(ImageTitle))
    plt.show()
