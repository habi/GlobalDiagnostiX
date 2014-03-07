"""
Script to show some of the images from the Focus/FOV test.
Images in the given folder were saved with the
"[Python: Capture Multiple Exposures]" part of GDX.ini in DevWare of Aptina
"""

import os
import numpy as np
import matplotlib.pyplot as plt

Root = "/afs/psi.ch/project/EssentialMed/Images/13-Aptina_Focus_Test/FocusFOV"
Sensor = "AR0130"
Image = "AR0130_1280x964_DSL315B_93.0mm_0.0_0.0f_166ms.raw"

ImageFile = os.path.join(Root, Sensor, Image)

print ImageFile


#~ Open the RAW files in Fiji as "16-bit Unsigned" with the "Width" and
#~ "Height" given in the DevWare-window and with "Little-Endian byte order"

rawimage = np.memmap(ImageFile, dtype=np.uint16, shape=(960, 1280))

plt.imshow(rawimage, cmap=plt.cm.gray)
plt.show()
