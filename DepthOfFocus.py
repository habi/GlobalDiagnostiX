# -*- coding: utf-8 -*-

"""
Script to calculate the depth of focus of the GDX setup.
Formulas from \cite{Greenleaf1950} found via
http://www.dofmaster.com/equations.html
"""

# H is the hyperfocal distance, mm
# f is the lens focal length, mm
# s is the focus distance
# Dn is the near distance for acceptable sharpness
# Df is the far distance for acceptable sharpness
# N is the f-number
# c is the circle of confusion, mm

f = 3
N = 1.4
c = 0.08
s = 200

H = f ** 2 / (N * c + f)
NearDistance = (s * (H - f)) / (H + s)
FarDistance = (s * (H - f)) / (H - s)

print 'The hyperfocal distance is %s' % H
print 'The near distance for acceptable sharpness Dn is %s' % NearDistance
print 'The far distance for acceptable sharpness Df is %s' % FarDistance


print 'Also check image at', \
    'http://www.cambridgeincolour.com/tutorials/dof-calculator.htm'

# Testing some stuff
import matplotlib.pyplot as plt
import os
import numpy

Experiment = '/afs/psi.ch/project/EssentialMed/MasterArbeitBFH/XrayImages/' +\
    'Toshiba/AR0132/TIS-TBL-6C-3MP/Hand/'
ExperimentID = '5808439'
OriginalImage = plt.imread(os.path.join(Experiment, ExperimentID +
                                        '.image.corrected.png'))
StretchedImage = plt.imread(os.path.join(Experiment, ExperimentID +
                                         '.image.corrected.stretched.png'))

print 'The minimum of the original image is %s, the maximum is %s' % (
    numpy.min(OriginalImage), numpy.max(OriginalImage))
print 'The minimum of the stretched image is %s, the maximum is %s' % (
    numpy.min(StretchedImage), numpy.max(StretchedImage))

plt.figure()
plt.subplot(121)
plt.imshow(OriginalImage, cmap='bone')
plt.subplot(122)
plt.hist(OriginalImage.flatten(), 64)

plt.figure()
plt.subplot(121)
plt.imshow(StretchedImage, cmap='bone')
plt.subplot(122)
plt.hist(StretchedImage.flatten(), 64)
plt.show()
