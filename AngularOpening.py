# -*- coding: utf-8 -*-

"""
Calculate the angular opening of the lens, including the shades that we have
to build in between.
"""
from __future__ import division
import optparse
import sys
import os
import numpy
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from matplotlib.patches import Rectangle

os.system('clear')

# Use Pythons Optionparser to define and read the options, and also
# give some help to the user
parser = optparse.OptionParser()
usage = "usage: %prog [options] arg"
parser.add_option('-d', dest='Distance', type='float', default=134,
                  metavar='123', help='Scintillator-CMOS distance [mm]. '
                                      'Default = %default mm')
parser.add_option('-f', dest='FOV', type='float', default=450 / 3,
                  metavar='430', help='Desired field of view [mm]. Default = '
                                      '%default mm')
parser.add_option('-o', dest='Overlap', type='float', default=2,
                  metavar='16', help='Overlap between the images [%]. Default '
                                     '= %default %')
parser.add_option('-p', dest='ParaventLength', type='float', default=100,
                  metavar='123', help='Length of the paravents. Default = '
                                      '%default mm')
parser.add_option('-l', dest='LensLength', type='float', default=16.8,
                  metavar='11.3', help='Length of the lens. Default = '
                                       '%default mm')
parser.add_option('-b', dest='BackFocalLength', type='float', default=6.5,
                  metavar='9.0', help='Back focal length of the lens. Default '
                                      '= %default mm')
parser.add_option('-s', dest='SaveImage', default=True, action='store_true',
                  help='Write output, (Default: %default)')
(options, args) = parser.parse_args()

# TBL 6 C 3MP specifications, as from TIS and copied here: http://cl.ly/YQ4Z
# FOV = 145 mm without overlap
# LensLengtht = 10 mm
# BackFocalLength = 6.5 mm
# Measured FOV at a distance of 13 cm is 135 x 105 mm

# show the help if the needed parameters (distance and FOV) are not given
if options.Distance is None or options.FOV is None:
    parser.print_help()
    print ''
    print 'Example:'
    print 'The command below shows the configuration of a detector with '
    print 'an optics with an opening angle of 78° used to get a field'
    print 'of view of 50 cm:'
    print ''
    print sys.argv[0], '-a 78 -f 50'
    print ''
    sys.exit(1)
print ''

#~ tan(\alpha/2) = (FOV/2) / Distance
#~ Distance = (FOV/2)/tan(\alpha/2)

print 'We calculate with a CMOS-Scintillator distance of', options.Distance, \
    'mm.'
print 'With a back focal length of', options.BackFocalLength, \
    'mm and a lens length of', options.LensLength, 'mm we have a distance of',\
    options.Distance - options.BackFocalLength - options.LensLength, \
    'mm from the front of the lens to the scintillator.'

print 'The FOV is corrected with an overlap of', options.Overlap, '% from',  \
    options.FOV, 'mm to',
options.FOV = options.FOV * (1 + (options.Overlap / 100))
print options.FOV, 'mm.'

print 'For a visible FOV of', options.FOV, 'mm at a distance of',  \
    options.Distance, 'mm we get a calculated opening angle of the lens of',
OpeningAngle = numpy.rad2deg(numpy.arctan((options.FOV / 2) /
                                          options.Distance)) * 2
print round(OpeningAngle, 1), 'degrees'

plt.figure(figsize=(5, 15))
for Displacement in (0, - options.FOV / (1 + options.Overlap / 100),
                     options.FOV / (1 + options.Overlap / 100)):
    # Central axis
    plt.axhline(Displacement, color='k', linestyle='--')

    # CMOS
    cmoscolor = 'b'
    plt.plot((0, 0), (Displacement + 3, Displacement - 3), linewidth='5',
             color=cmoscolor)

    # Lens
    rect = Rectangle((options.BackFocalLength, Displacement - 14 / 2),
                     options.LensLength, 14, facecolor="#aaaaaa")
    plt.gca().add_patch(rect)

    # Opening angle, based on CMOS
    wedge = Wedge((0, Displacement), options.Distance * 0.309,
        -OpeningAngle / 2, OpeningAngle / 2, fill=True, color='r', alpha=0.125)
    plt.gca().add_patch(wedge)
    plt.plot((0, options.Distance), (Displacement, Displacement + options.FOV
                                     / 2), color='k', linestyle='--',
             alpha=0.25)
    plt.plot((0, options.Distance), (Displacement, Displacement - options.FOV
                                     / 2), color='k', linestyle='--',
             alpha=0.25)

    # Scintillator FOV
    screencolor = 'k'
    plt.plot([options.Distance, options.Distance], [Displacement + (
        options.FOV / 2), Displacement - (options.FOV / 2)],  linewidth='6',
             color=screencolor)
    screencolor = 'g'
    plt.plot([options.Distance, options.Distance], [Displacement + (
        options.FOV / 2), Displacement - (options.FOV / 2)], linewidth='4',
             color=screencolor)

    # FOV drawn from center of lens
    beamcolor = 'r'
    plt.plot([options.BackFocalLength + options.LensLength,
              options.Distance], [Displacement, Displacement + options.FOV /
                                  2], beamcolor)
    plt.plot([options.BackFocalLength + options.LensLength,
              options.Distance], [Displacement, Displacement - options.FOV /
                                  2], beamcolor)

    # Paravents. Position calculated back from overlap
    paraventcolor = 'k'
    plt.plot(
        [0, options.ParaventLength],
        [Displacement - (options.FOV / (1 + options.Overlap / 100) / 2),
        Displacement - (options.FOV / (1 + options.Overlap / 100) / 2)],
        linewidth='5', color=paraventcolor)

    # Paravent blocking,
    beamcolor = 'g'
    plt.plot([options.BackFocalLength + options.LensLength, options.Distance],
        [Displacement, Displacement + options.FOV / 2], beamcolor)
    plt.plot([options.BackFocalLength + options.LensLength, options.Distance],
        [Displacement, Displacement - options.FOV / 2], beamcolor)

# Nice plotting

plt.title('Angular opening: ' + str(round(OpeningAngle, 2)) + '\nFOV size: ' +
          str(options.FOV) + ' mm (including overlap of ' +
          str(options.Overlap) + ' %)\nWorking Distance: ' +
          str('%.2f' %options.Distance) + ' mm\nParavent length: ' +
          str('%.2f' % options.ParaventLength) + ' mm')
plt.xlabel('Distance [mm]')
plt.axis('equal')

if options.SaveImage:
    SaveName = 'Paravents_' + str(str('%.2f' % OpeningAngle)) + '_wd_' + \
               str('%.2f' % options.Distance) + 'mm_FOV_' + \
               str('%.2f' % options.FOV) + 'mm'
    FigureName = ''.join([SaveName, '.png'])
    plt.savefig(FigureName)
    print 'Figure saved to ' + FigureName

plt.show()
