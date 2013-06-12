#! /usr/bin/env python
# coding: utf-8

import optparse
import sys
import numpy
from pylab import *
import time

ion()

# Use Pythons Optionparser to define and read the options, and also
# give some help to the user
parser = optparse.OptionParser()
usage = "usage: %prog [options] arg"
parser.add_option('-a', dest='Angle', type='float',
	help='Angular view of the Objective',
	metavar='53')
parser.add_option('-f', dest='FOV', type='float',
	default = 43,
	help='Desired field of view (square for the moment). Default = 43 cm',
	metavar='43')	
(options, args) = parser.parse_args()

# show the help if no parameters are given
if options.Angle==None:
	parser.print_help()
	print ''
	print 'Example:'
	print 'The command below shows the configuration of a detector with '
	print 'an optics with an opening angle of 78° used to get a field'
	print 'of view of 50 cm:'
	print ''
	print 'EssentialMed-Optics.py -a 78 -f 50'
	print ''
	sys.exit(1)
print ''

#~ tan(\alpha/2) = (FOV/2) / Distance
#~ Distance = (FOV/2)/tan(\alpha/2)

FOV = float(options.FOV)
AngleDeg = float(options.Angle)
AngleRad = numpy.deg2rad(AngleDeg)
WorkingDistance = (FOV/2)/numpy.tan(AngleRad/2)

print 'The working distance for'
print 'a desired field of view of ' + str('%.2f' % FOV) + ' cm and '
print 'an opening angle of ' + str('%.2f' % AngleDeg) + '°'
print 'is ' + str('%.2f' % WorkingDistance) + ' cm'

# Camera
CamSize = 5.25
rect = Rectangle((-CamSize, -(float(CamSize)/2)), CamSize, CamSize,
	facecolor="#aaaaaa")
gca().add_patch(rect)

# Angle
from matplotlib.patches import Wedge
wedgecolor = 'r'
Wedge = Wedge((0,0), WorkingDistance*.3, -(AngleDeg/2), (AngleDeg/2),
	fill=False, color=wedgecolor)
plt.gca().add_patch(Wedge)

# Beams
beamcolor = wedgecolor
plt.plot([0,WorkingDistance],[0,FOV/2],beamcolor)
plt.plot([0,WorkingDistance],[0,-FOV/2],beamcolor)

# Screen
screencolor = 'k'
plt.plot(
	[WorkingDistance,WorkingDistance],
	[(options.FOV/2),-(options.FOV/2)],linewidth='5',color=screencolor)
plt.axhline(color=screencolor,linestyle='--')

plt.axis('equal')
plt.title('Angular opening: ' + str(options.Angle) + ', Screen size: ' +\
	str(options.FOV) + 'cm , Working Distance: ' +\
	str('%.2f' % WorkingDistance) + 'cm')
plt.xlabel('Distance [cm]')
plt.text(WorkingDistance*.3*numpy.cos(AngleRad), 
	WorkingDistance*.3*numpy.sin(AngleRad),
	str(options.Angle) + u'°') # http://is.gd/pxodor
plt.axis([-5,85,0,0])
plt.draw()

SaveName = 'EssentialMed-Optics_angle_' +str(options.Angle) + '_wd_' +\
	str('%.2f' % WorkingDistance)
FigureName = ''.join([SaveName,'.png'])
savefig(FigureName)
print 'Figure saved to ' + FigureName

plt.show()
#~ plt.draw()
#~ time.sleep(1)
#~ plt.close()
