# coding: utf-8

"""
based on code from http://www.frantzmarti$che.com/blog/?p=84
"""

from __future__ import division
import optparse
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import colorsys

os.system('clear')
plt.ion()
Savepath = '/afs/psi.ch/project/EssentialMed/Dev/Images/CMOSDistance'

# Use Pythons Optionparser to define and read the options, and also
# give some help to the user
parser = optparse.OptionParser()
usage = "usage: %prog [options] arg"
# 17.526 is the standard lenght of the mounting surface to sensor length,
# according to Mr. Guarino from Lensation and
# books.google.ch/books?id=DaQY8CrmqFcC&pg=PA140&lpg=PA140&dq=17.526+mm
parser.add_option('-d', dest='CMOSDistance', type='float',
                  help='CMOS-Lens-Distance [mm]. Default=%default',
                  default=17.526, metavar='13')
parser.add_option('-s', dest='UseSensor', type='int',
                  help='Sensor to use. 1=AR0130 , 2= AR0132, 3= MT9M0010. '
                       'Default=%default', default=2, metavar='2')
(options, args) = parser.parse_args()

'''
for i in {100..150};
do for s in {1,2,3};
do python lens_simulation.py -d $i -s $s;
done;
done
'''
print 'TEMPORARY'
print
print 'CMOSDistance converted from', options.CMOSDistance, 'mm to',
options.CMOSDistance = options.CMOSDistance / 10
print options.CMOSDistance, 'mm'
print
print 'TEMPORARY'


def plotcolors(NumberOfColors):
    # After http://stackoverflow.com/a/9701141/323100
    colors = []
    for i in np.arange(0., 360., 360. / NumberOfColors):
        hue = i / 360.
        lightness = (50 + np.random.rand() * 10) / 100.
        saturation = (90 + np.random.rand() * 10) / 100.
        colors.append(colorsys.hls_to_rgb(hue, lightness, saturation))
    return colors


def add_lens(z, f, diam, lbl):
    # simply draws a thin-lens at the provided location parameters:
    # - z:    location along the optical axis (in mm)
    # - f:    focal length (in mm, can be negative if div. lens)
    # - diam: lens diameter in mm
    # - lbl:  label to identify the lens on the drawing
    ww, tw, rad = diam / 10.0, diam / 3.0, diam / 2.0
    plt.plot([z, z],    [-rad, rad],                'k', linewidth=2)
    #~ plt.plot([z, z + tw], [-rad, -rad + np.sign(f) * ww], 'y', linewidth=2)
    #~ plt.plot([z, z - tw], [-rad, -rad + np.sign(f) * ww], 'y', linewidth=2)
    #~ plt.plot([z, z + tw],  [rad,  rad - np.sign(f) * ww], 'y', linewidth=2)
    #~ plt.plot([z, z - tw],  [rad,  rad - np.sign(f) * ww], 'y', linewidth=2)
    plt.plot([z + f, z + f], [-ww, ww], 'y', linewidth=2)
    plt.plot([z - f, z - f], [-ww, ww], 'y', linewidth=2)
    lens = patches.Ellipse((z, 0), width=2 * f, height=diam,
                           facecolor='y', linewidth=2, alpha=0.125)
    plt.gcf().gca().add_patch(lens)
    plt.text(z, rad + 2.0, lbl + '\nf=' + str(round(f, 2)),
             horizontalalignment='center')


def propagate_beam(p0, NA, nr, zl, ff, raycolor='b'):
    # geometrical propagation of light rays from given source parameters:
    # - p0: location of the source (z0, x0) along and off axis (in mm)
    # - NA: numerical aperture of the beam (in degrees)
    # - nr: number of rays to trace
    # - zl: array with the location of the lenses
    # - ff: array with the focal length of lenses
    # - raycolor: color of the rays on plot
    apa = NA * np.pi / 180.0
    z0 = p0[0]
    if (np.size(p0) == 2):
        x0 = p0[1]
    else:
        x0 = 0.0

    zl1, ff1 = zl[(z0 < zl)], ff[(z0 < zl)]
    nl = np.size(zl1)  # number of lenses

    zz, xx, tani = np.zeros(nl + 2), np.zeros(nl + 2), np.zeros(nl + 2)
    tan0 = np.tan(apa / 2.0) - np.tan(apa) * np.arange(nr) / (nr - 1)

    for i in range(nr):
        tani[0] = tan0[i]  # initial incidence angle
        zz[0], xx[0] = z0, x0
        for j in range(nl):
            zz[j + 1] = zl1[j]
            xx[j + 1] = xx[j] + (zz[j + 1] - zz[j]) * tani[j]
            tani[j + 1] = tani[j] - xx[j + 1] / ff1[j]

        zz[nl + 1] = zmax
        xx[nl + 1] = xx[nl] + (zz[nl + 1] - zz[nl]) * tani[nl]
        plt.plot(zz, xx, color=raycolor)

FOVSize = np.array([430 / 3., 430 / 4.])
FOVDiagonal = np.sqrt(FOVSize[0] ** 2 + FOVSize[1] ** 2)

if options.UseSensor == 1:
    Sensor = 'AR0130'
    # Full Resolution: 1280H x 960V (1.2Mp)
    # Pixel Size: 3.75um x 3.75um
    pixelsize = 3.75 / 1000
    CMOSSize = np.array([1280 * pixelsize, 960 * pixelsize])
elif options.UseSensor == 2:
    Sensor = 'AR0132'
    # Full Resolution: 1280H x 960V (1.2Mp)
    # Pixel Size: 3.75um x 3.75um
    pixelsize = 3.75 / 1000
    CMOSSize = np.array([1280 * pixelsize, 960 * pixelsize])
elif options.UseSensor == 3:
    Sensor = 'MT9M0010'
    # Active pixels: 1,280H x 1,024V
    # Pixel size: 5.2um x 5.2um
    pixelsize = 5.2 / 1000
    CMOSSize = np.array([1280 * pixelsize, 1024 * pixelsize])

# Make output directory
try:
    os.makedirs(os.path.join(Savepath, Sensor))
except:
    # Don't do anything if the folder already exists
    pass

CMOSDiagonal = np.sqrt(CMOSSize[0] ** 2 + CMOSSize[1] ** 2)

print 'We are calcuating with the', Sensor, 'sensor, which has a size of', \
    round(CMOSSize[0], 2), 'x', round(CMOSSize[1], 2), \
    'mm, a diagonal of', round(CMOSDiagonal, 2), 'mm (or', \
    round(CMOSDiagonal * 0.0393701, 2), 'inch).'
print 'The FOV we want to look at is', round(FOVSize[0], 2), 'x', \
    round(FOVSize[1], 2), 'mm (430 x 430mm @ 4:3), a diagonal of', \
    round(FOVDiagonal, 2), 'mm'

Magnification = FOVDiagonal / CMOSDiagonal
print 'We thus have a (de)magnification of', round(Magnification, 2), 'x'

# Draw the different sizes.
figure1 = plt.figure(figsize=(9, 9))
plt.title("Sizes, head on")
plt.show()

Scintillator = patches.Rectangle((0, 0), 430, 430, facecolor='g', linewidth=2)
figure1.gca().add_patch(Scintillator)
for x in range(3):
    for y in range(4):
        # Draw rectangles: http://is.gd/rmDuV1
        FOV = patches.Rectangle((x * FOVSize[0], y * FOVSize[1]),
                                width=FOVSize[0], height=FOVSize[1],
                                facecolor='g', linewidth=2)
        figure1.gca().add_patch(FOV)
        Ellipse = patches.Ellipse((FOVSize[0] / 2 - CMOSSize[0] / 2 + x *
                                  FOVSize[0], FOVSize[1] / 2 -
                                  CMOSSize[1] / 2 + y * FOVSize[1]),
                                  width=FOVSize[0] / 0.618,
                                  height=FOVSize[1] / 0.618, color='k',
                                  alpha=0.125)
        figure1.gca().add_patch(Ellipse)
        CMOS = patches.Rectangle((FOVSize[0] / 2 - CMOSSize[0] / 2 + x *
                                  FOVSize[0], FOVSize[1] / 2 -
                                  CMOSSize[1] / 2 + y * FOVSize[1]),
                                 width=CMOSSize[0], height=CMOSSize[1],
                                 facecolor='b', linewidth=2)
        figure1.gca().add_patch(CMOS)
# Draw one more so we can get labels
FOV = patches.Rectangle((0, 0), FOVSize[0], FOVSize[1], facecolor='g',
                        linewidth=2, label='FOV')
figure1.gca().add_patch(FOV)
Ellipse = patches.Ellipse((FOVSize[0] / 2 - CMOSSize[0] / 2,
                           FOVSize[1] / 2 - CMOSSize[1] / 2),
                          width=FOVSize[0] / 0.618, height=FOVSize[1] / 0.618,
                          color='k', alpha=0.125, label='Opt. Circle')
figure1.gca().add_patch(Ellipse)
CMOS = patches.Rectangle((FOVSize[0] / 2 - CMOSSize[0] / 2,
                          FOVSize[1] / 2 - CMOSSize[1] / 2), CMOSSize[0],
                         CMOSSize[1], facecolor='b', linewidth=2,
                         label=Sensor)
figure1.gca().add_patch(CMOS)
plt.legend()
plt.axis('scaled')
plt.xlabel('Length [mm]')
plt.ylabel('Length [mm]')
plt.savefig(os.path.join(Savepath, Sensor,
                         'lens_simulation_sizecomparison.png'),
            transparent=True)

print 80 * '-'

# www.physicsclassroom.com/class/refrn/Lesson-5/The-Mathematics-of-Lenses
# The magnification equation relates the ratio of the image distance and
# object distance to the ratio of the image height (hi) and object height
# (ho). The magnification equation is stated as follows:
# 1/f = 1/do + 1/di
# M = hi/ho = - di/do
# --> M * ho = hi or M * -do = di

# options.CMOSDistance comes from the options.CMOSDistance option, which is set
# to a default of 17.526 mm
FOVPosition = Magnification * options.CMOSDistance
FocalLength = 1 / ((1 / options.CMOSDistance) + (1 / FOVPosition))

print 'If the CMOS is set to be', options.CMOSDistance, 'mm away from the', \
    'lens, the Scintillator has to be', round(FOVPosition, 2), \
    'mm away from the lens.'
print 'This means that the total optical length is', \
    round(options.CMOSDistance + FOVPosition, 2), 'mm'
print 'Since the CMOS is', round(options.CMOSDistance, 2), 'mm away from', \
    'the lens we thus need a lens with a focal length of approximately', \
    int(round(FocalLength))

print 'You can set the distance between the CMOS and the lens with the', \
    '"-d" option.'
print sys.argv[0], '-d', options.CMOSDistance
print 'was used to generate this plot'

print 80 * '-'

#~ Lens
# Draw the lens at the origin, to simplify things
LensPosition = np.array([0])
# Since we only draw *one* lens for the moment, we convert the focal length
# calculated above to a NumPy array, so we can use the drawing code
FocalLength = np.array([FocalLength])

#~ FNumber = FocalLength / LensDiameter
#~ FNumber = 1 / ( 2 * NumericalAperture)
#~ -> 1 / ( 2 * FNumber) = NumericalAperture
FNumber = 1.4
NumericalAperture = 1 / (2 * FNumber)
SzintillatorWidth = 5

figure2 = plt.figure(figsize=(16, 9))
plt.show()
# Draw top view
plt.subplot(121)
plt.title(' '.join([Sensor, '| Top view | CMOS-Lens-distance',
                    str(options.CMOSDistance), 'mm']))
# Draw CMOS and Scintillator
plt.plot((-options.CMOSDistance, -options.CMOSDistance),
         (-CMOSSize[0] / 2, CMOSSize[0] / 2), color='b', linewidth=2)
plt.plot((FOVPosition, FOVPosition), (-FOVSize[0] / 2, FOVSize[0] / 2),
         color='g', linewidth=SzintillatorWidth)
plt.xlabel('Distance [mm]')
plt.ylabel('Distance [mm]')
# Draw Lens(es)
LensDiameter = 12.0
for i in range(np.size(LensPosition)):
    add_lens(LensPosition[i], FocalLength[i], LensDiameter, "L" + str(i))
zmin, zmax = -options.CMOSDistance, FOVPosition
# Draw beam paths
c = plotcolors(5)
c = ['blue', 'blue', 'blue', 'blue', 'blue', 'blue']
NumberOfRays = 5
BeamNA = 10
propagate_beam((-options.CMOSDistance, 0), BeamNA, NumberOfRays, LensPosition,
               FocalLength, raycolor=c[0])
propagate_beam((-options.CMOSDistance, CMOSSize[0] / 4), BeamNA, NumberOfRays,
               LensPosition, FocalLength, raycolor=c[1])
propagate_beam((-options.CMOSDistance, CMOSSize[0] / 2), BeamNA, NumberOfRays,
               LensPosition, FocalLength, raycolor=c[2])
propagate_beam((-options.CMOSDistance, -CMOSSize[0] / 4), BeamNA, NumberOfRays,
               LensPosition, FocalLength, raycolor=c[3])
propagate_beam((-options.CMOSDistance, -CMOSSize[0] / 2), BeamNA, NumberOfRays,
               LensPosition, FocalLength, raycolor=c[4])
plt.xlim([-30, 250])
plt.ylim([-FOVSize[0] / 2 * 1.1, FOVSize[0] / 2 * 1.1])

# Draw side view
plt.subplot(122)
plt.title(' '.join([Sensor, '| Side view | CMOS-Lens-distance',
                    str(options.CMOSDistance), 'mm']))
# Draw CMOS and Scintillator
plt.plot((-options.CMOSDistance, -options.CMOSDistance),
         (-CMOSSize[1] / 2, CMOSSize[1] / 2), color='b', linewidth=2)
plt.plot((FOVPosition, FOVPosition), (-FOVSize[1] / 2, FOVSize[1] / 2),
         color='g', linewidth=SzintillatorWidth)
# Draw Lens(es)
for i in range(np.size(LensPosition)):
    add_lens(LensPosition[i], FocalLength[i], LensDiameter, "L" + str(i))
# Draw beam paths
propagate_beam((-options.CMOSDistance, 0), BeamNA, NumberOfRays, LensPosition,
               FocalLength, raycolor=c[0])
propagate_beam((-options.CMOSDistance, CMOSSize[1] / 4), BeamNA, NumberOfRays,
               LensPosition, FocalLength, raycolor=c[1])
propagate_beam((-options.CMOSDistance, CMOSSize[1] / 2), BeamNA, NumberOfRays,
               LensPosition, FocalLength, raycolor=c[2])
propagate_beam((-options.CMOSDistance, -CMOSSize[1] / 4), BeamNA, NumberOfRays,
               LensPosition, FocalLength, raycolor=c[3])
propagate_beam((-options.CMOSDistance, -CMOSSize[1] / 2), BeamNA, NumberOfRays,
               LensPosition, FocalLength, raycolor=c[4])
plt.xlabel('Distance [mm]')
plt.ylabel('Distance [mm]')
plt.xlim([-30, 250])
plt.ylim([-FOVSize[0] / 2 * 1.1, FOVSize[0] / 2 * 1.1])
plt.draw()

plt.savefig(os.path.join(Savepath, Sensor, 'lens_simulation_view_' +
            str(round(options.CMOSDistance, 1)).zfill(5) + 'mm.png'),
            transparent=True)
plt.savefig(os.path.join(Savepath, Sensor, 'movie_lens_simulation_view_' +
            str(int(round(options.CMOSDistance, 1) * 10)).zfill(7) + 'mm.png'),
            transparent=True)
plt.ioff()
# plt.show()
