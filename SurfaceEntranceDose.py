#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Tiny tool to calculate the surface entrance dose of a certain x-ray measurement
Gives the same results as the 'Diagnostische Referenzwerte' Excel calculator on
the BAG-page, in the right side-bar of http://is.gd/E2qIPA.
The calculation is based on 'Merkblatt R-06-04' from BAG
"""

from pylab import *
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

ion()

# Parameters

# The K-value is based on the machine. The BAG-calculator (see below) list 0.1
K = 0.1
FocusDistance = 1.4
# RSF as found by Arouna2000, cited by BAG2012. *This* RSF gives the same SED
# values as the XLS-calculator from BAG (http://is.gd/oTpniQ) which I copied to
# /afs/psi.ch/project/EssentialMed/PresentationsAndInfo/BAG/R-0 DRWCalc 5.0.xls
RSF = 1.35
# RSF as found in BAG2012. "Der über verschiedene Anlagen gemittelte
# Korrekturfaktor betrug 1.15"
#RSF = 1.15

Range_kV = range(30, 130)
Range_mAs = range(0, 60)

# Using *bloody* list comprehension in Python as specified by
# http://stackoverflow.com/a/2397150/323100 Why do I always forget this?
Dose = np.asarray([[K *
                  (float(kV) / 100) ** 2
                  * mAs *
                  (1 / FocusDistance) ** 2
                  * RSF
                  for kV in Range_kV] for mAs in Range_mAs])

# Give out fixed data
print '---'
print 'The characteristic constant of the x-ray setup is', K, 'mGy/mA, the'
print 'focus-surface-distance is', FocusDistance, 'm, the "Rückstreufaktor"'
print 'RSF was set to', str(RSF) + '.'
print
print 'If we calculate the surface entrance dose'
print 'SED = K*(U/100)^2*Q*(1/FOD)^2*RSF'

# Give out plot and varying data
# Surfaceplot based on http://stackoverflow.com/a/3812324/323100, since we only
# have matplotlib 0.99.1.1 installed here at PSI. Check the installed version
# with "python -c 'import matplotlib; print matplotlib.__version__'" in your
# terminal.
fig = plt.figure()
ax = Axes3D(fig)
X, Y = np.meshgrid(Range_kV, Range_mAs)
ax.plot_surface(X, Y, Dose,
                cmap=cm.jet,
                cstride=1,
                rstride=1,
                linewidth=0)

showCase = 1
if showCase == 1:
    # Multiple Values, including Zhentians Breast scan
    showkV = (46., 70., 120., 125., 40.)
    showmAs = (50., 2, 50., 2., 25.)
    what = ('Wrist 1', 'Wrist 2', 'LWS ap', 'Thorax', 'Zhentian')
elif showCase == 2:
    # General values for radiology (from Heinz and R-06-04). Used in
    # movie in presentation
    showkV = (46., 70., 120., 125.)
    showmAs = (50., 2, 50., 2.)
    what = ('Wrist 1', 'Wrist 2', 'LWS ap', 'Thorax')
elif showCase == 3:
    # The two wrist images in the talk, 70 kV with much too high mAs, but
    # otherwise we wouldn't have reached the exposure time needed to sync the
    # camera.
    showkV = (46., 70., 70.)
    showmAs = (50., 50, 2.)
    what = ('Wrist 1', 'Wrist 2 (Experiment)', 'Wrist 2 (Theory)')

for kV, mAs, method in zip(showkV, showmAs, what):
    CurrentDose = Dose[Range_mAs.index(mAs)][Range_kV.index(kV)]
    ax.plot([kV], [mAs], CurrentDose, 'o', c='r', ms=20)
    label = '%d kV & %d mAs\nSE-Dose %0.3f mGy\n%s' % (kV, mAs, CurrentDose,
                                                       method)
    if not showCase == 3:
        ax.text(kV, mAs, CurrentDose, label)
    print
    print 'For a radiography of a', method
    print 'with a source voltage of', kV, 'kV and a charge of', mAs, 'mAs, '
    print 'we get a SED of', round(CurrentDose, 3), 'mGy.'

ax.set_xlabel('kV')
ax.set_ylabel('mAs')
ax.set_zlabel('Dose [mGy]')

savemovie = False
if savemovie:
    # Save output as movie: http://stackoverflow.com/a/12905458/323100
    angles = range(225-44, 225+44)  # 150:270 good values for presentation
    counter = 1
    for angle in angles:
        ax.view_init(elev=34.4, azim=angle)
        print 'saving angle', str(angle + 1) + '° of 360° as movie' + \
            str("%03d" % angle) + '.png - [' + str(counter) + '/' +\
            str(len(angles)) + ']'
        plt.savefig('Dose_movie' + str("%03d" % angle) + '.png',
                    transparent=False)
        plt.draw()
        counter += 1
else:
    ax.view_init(elev=34.4, azim=225)
    plt.savefig('Dose' + str(showCase) + '.png', transparent=True)

ioff()
print
print 'done'
plt.show()
