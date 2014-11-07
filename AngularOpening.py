# -*- coding: utf-8 -*-

"""
Calculate the angular opening of the lens, including the shades that we have
to build in between.
"""
import optparse
import sys
import numpy
from pylab import *

# Use Pythons Optionparser to define and read the options, and also
# give some help to the user
parser = optparse.OptionParser()
usage = "usage: %prog [options] arg"
parser.add_option('-a', dest='Angle', type='float',
    default = 45, metavar=53,
    help='Opening angle of the the Objective. Default = %default degrees')
parser.add_option('-f', dest='FOV', type='float',
    default = 150, metavar='430',
    help='Desired field of view (square for the moment). Default = %default'
    ' mm')
parser.add_option('-d', dest='Distance', type='float',
    default = 130, metavar='123',
    help='Scintillator-CMOS distance. Default = %default mm')
parser.add_option('-l', dest='LensLength', type='float',
    default = 16.8, metavar='11.3',
    help='Length of the lens. Default = %default mm')
parser.add_option('-b', dest='BackFocalLength', type='float',
    default = 6.5, metavar='9.0',
    help='Back focal length of the lens. Default = %default mm')
parser.add_option('-o', dest='Output',
    default=False, action='store_true',
    help='Be really chatty, (Default: %default)')
(options, args) = parser.parse_args()

#~ TBL 6 C 3MP specifications, as from TIS and copied here: http://cl.ly/YQ4Z
#~ FOV = 145 mm without overlap
#~ LensLengtht = 10 mm
#~ BackFocalLength = 6.5 mm

# show the help if needed parameters are not given
if options.Angle==None:
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

FOV = float(options.FOV)
AngleDeg = float(options.Angle)
AngleRad = numpy.deg2rad(AngleDeg)
WorkingDistance = (FOV/2)/numpy.tan(AngleRad/2)

print 'We calculate with a CMOS-Scintillator distance of', options.Distance, \
    'mm.'
print 'With a back focal length of', options.BackFocalLength, \
    'mm and a lens length of', options.LensLength, 'mm we have a distance of',\
    options.Distance - options.BackFocalLength - options.LensLength, \
    'mm from the front of the lens to the scintillator.'

print 'The working distance for'
print 'a desired field of view of ' + str('%.2f' % FOV) + ' cm and '
print 'an opening angle of ' + str('%.2f' % AngleDeg) + '°'
print 'is ' + str('%.2f' % WorkingDistance) + ' mm'

# central axis

plt.axhline(color='k',linestyle='--')
# CMOS
cmoscolor = 'b'
plt.plot( (0,0), (3,-3),linewidth='5',color=cmoscolor)

# Lens
CamSize = 5.25
rect = Rectangle((options.BackFocalLength, -14/2), options.LensLength, 14,
    facecolor="#aaaaaa")
gca().add_patch(rect)

# Angle
from matplotlib.patches import Wedge
wedgecolor = 'r'
#~ Wedge = Wedge((options.BackFocalLength+options.LensLength,0), WorkingDistance * 0.3 , -(AngleDeg/2), (AngleDeg/2),
    #~ fill=False, color=wedgecolor)
#~ plt.gca().add_patch(Wedge)

# Beams
beamcolor = wedgecolor
plt.plot([options.BackFocalLength+options.LensLength,options.Distance],[0,FOV/2],beamcolor)
plt.plot([options.BackFocalLength+options.LensLength,options.Distance],[0,-FOV/2],beamcolor)

# Screen
screencolor = 'k'
plt.plot(
    [options.Distance,options.Distance],
    [(options.FOV/2),-(options.FOV/2)],linewidth='5',color=screencolor)
#~ #~
plt.axis('equal')
#~ plt.title('Angular opening: ' + str(options.Angle) + ', Screen size: ' +\
    #~ str(options.FOV) + 'mm , Working Distance: ' +\
    #~ str('%.2f' % WorkingDistance) + 'mm')
plt.xlabel('Distance [mm]')
#~ plt.text(WorkingDistance*.3*numpy.cos(AngleRad),
    #~ WorkingDistance*.3*numpy.sin(AngleRad),
    #~ str(options.Angle) + u'°') # http://is.gd/pxodor

if options.Output:
    SaveName = 'EssentialMed-Optics_angle_' +str(options.Angle) + '_wd_' +\
        str('%.2f' % options.Distance)
    FigureName = ''.join([SaveName,'.png'])
    savefig(FigureName)
    print 'Figure saved to ' + FigureName

plt.show()
