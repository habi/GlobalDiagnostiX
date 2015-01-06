# -*- coding: utf-8 -*-

"""
Script to "calculate" the detector.
The script estimates the number of photons landing on the scintillator
from the source and the number of photons reaching the detector.
Also it displays the geometrical situation depending no the chosen parameters.

You can run this script to produce several frames of output as so:
(or use the command at the end of the script to also start Fiji and do some
more stuff)

for f in {10..15..1};
    do for o in {45..50..1};
        do for s in {5..10..1};
            do ./CalculateDetector.py -f $f -o $o -s $s -p;
        done;
    done;
done
"""

import numpy
from scipy import constants
from scipy import integrate
import matplotlib.pylab as plt
from matplotlib.patches import Wedge, Rectangle
from optparse import OptionParser
import sys
import os

# ##################### SETUP ######################

# Use Pythons Optionparser to define and read the options, and also
# give some help to the user
parser = OptionParser()
usage = "usage: %prog [options] arg"
parser.add_option('-s', '--ScreenSize', dest='FOV', type='float', default=4.5,
                  help='Field of view in centimeters, i.e. desired screen '
                       'size (default=43 cm)', metavar='43')
parser.add_option('-o', '--OpeningAngle', dest='OpeningAngle', default=90.0,
                  type='float',
                  help='Opening angle of the lens in degrees (default=90)',
                  metavar='45')
parser.add_option('-n', '--NumericalAperture', dest='NA', default=0.4,
                  type='float',
                  help='Numerical Aperture of the lens',
                  metavar='0.6')
parser.add_option('-f', '--FStop', dest='FStop', default=1.2, type='float',
                  help='F-Stop of the lens',
                  metavar='0.8')
parser.add_option('-c', '--CCDSize', dest='SensorSize', default=3.0,
                  type='float',
                  help='Size of the CCD/CMOS sensor (in millimeters!), '
                       'Default=7 mm/0.7 cm', metavar='7')
parser.add_option('-e', '--Energy', dest='InputEnergy', default=50.4,
                  type='float',
                  help='Energy of the x-ray photons in kV (default=50 kV)',
                  metavar='120')
parser.add_option('-l', '--LinePairs', dest='LinePairs', default=5.0,
                  type='float',
                  help='Desired resolution in lp/mm (default=2.5 lp/mm)',
                  metavar='4')
parser.add_option('-p', '--print', dest='Output', default=False,
                  action='store_true',
                  help='Save/Print output files to disk', metavar=1)
(options, args) = parser.parse_args()
options.SensorSize /= 10
options.InputEnergy *= 1000

# show the help if some important parameters are not given
if options.FOV is None \
        or options.OpeningAngle is None \
        or options.SensorSize is None \
        or options.InputEnergy is None \
        or options.LinePairs is None:
    parser.print_help()
    print 'Example:'
    print 'The command below shows you the configuration for a setup with a ' \
          'screen size of 20.5 cm (half the required size), a lens with an ' \
          'opening angle of 45 deg, a small sensor of 7 mm and an x-ray ' \
          'energy of 50 kV:'
    print ''
    print sys.argv[0], '-s 20.5 -o 45 -c 7 -e 50'
    print ''
    sys.exit(1)

print 80 * '_'

# CALCULATE
# Intensifying screen
# http://www.sprawls.org/ppmi2/FILMSCR/:
# > Although the total energy of the light emitted by a screen is much less
# than the total x-ray energy the screen receives, the light energy is much
# more efficient in exposing film because it is "repackaged" into a much larger
# number of photons. If we assume a 5% energy conversion efficiency, then one
# 50-keV x-ray photon can produce 1,000 blue-green light photons with an energy
# of 2.5 eV each.
ScreenAbsorption = 0.1
ScreenConversion = 0.5
ScreenEmission = 1

ScreenOutput = ScreenAbsorption * ScreenConversion * ScreenEmission

# nm (green according to http://is.gd/AWmNpp)
Wavelength = 500e-9
# E = h * nu, nu = c / lambda
PhotonEnergyJ = constants.h * constants.c / Wavelength
PhotonEnergyeV = PhotonEnergyJ / constants.eV
# print 'Visible light photons with a wavelength of',int(Wavelength*1e9),\
# 'nm have an energy of',round(PhotonEnergyJ,22),'J or',\
# round(PhotonEnergyeV,3),'eV.'

PhotonsAfterScintillator = options.InputEnergy / PhotonEnergyeV * ScreenOutput
print 'For each', options.InputEnergy / 1000, 'kV x-ray photon'
print '    * we have', int(round(PhotonsAfterScintillator)), 'visible light', \
    'photons after the scintillator (with a'
print '      conversion efficiency of', ScreenOutput * 100, '%).'

# Lens
LensReflectance = 0.02
LensAbsorption = 0.02
# Assume a set of double plano-convex lenses, with 4% loss per lens
LensTransmission = 1 - (2 * LensReflectance) - (2 * LensAbsorption)
PhotonsAfterLens = PhotonsAfterScintillator * LensTransmission
# ~ tan(\alpha/2) = (FOV/2) / Distance
# ~ Distance = (FOV/2)/tan(\alpha/2)
WorkingDistance = (options.FOV / 2) / numpy.tan(
    numpy.deg2rad(options.OpeningAngle) / 2)

print '    * we have', int(round(PhotonsAfterLens)), 'visible light photons', \
    'after the lens couple (with a'
print '      transmission of', LensTransmission * 100, '%).'

# Sensor
QESensor = 0.4
ProducedElectrons = PhotonsAfterLens * QESensor
Demagnification = options.FOV / options.SensorSize
SensorPosition = WorkingDistance / Demagnification

print '    * we get', int(round(ProducedElectrons)), 'electrons on the', \
    'detector (with a QE of', str(QESensor) + ').'

# LinePairs
LinePairsScintillator = options.FOV * 10 * options.LinePairs
PixelsNeeded = LinePairsScintillator * 2
SensorPixelSize = options.SensorSize / PixelsNeeded

# Comparison with Flatpanel detectors
FlatPanelPixelSize = 0.194  # mm
ScintillatorThickness = 1.0  # mm
ConversionEfficiency = 1.0
NumericalApertureCalculated = FlatPanelPixelSize / (ScintillatorThickness / 2)
NumericalApertureAverage = \
    integrate.quad(lambda x: numpy.arctan(FlatPanelPixelSize / (2 * x)),
                   0.01, 1)[0]
NumericalApertureDetermined = (SensorPosition * 10) / (
    options.FStop * 2 * SensorPosition * 10 / (1 / Demagnification))
FStopJBAG = 0.8
NumericalApertureJBAG = 1 / (2 * FStopJBAG)

# PLOT
# Plot optical configuration
# Draw the stuff we calculated above
fig = plt.figure(1, figsize=(32, 18))
Thickness = 1.0
SupportThickness = 0.5
XRaySourcePosition = 25

# Optical Configuration
plt.subplot(211)
plt.axis('equal')
# axes = plt.gca()
# axes.axes.get_yaxis().set_ticks([])
plt.title('Angular opening: ' + str('%.2f' % options.OpeningAngle) +
          ', Screen size: ' + str('%.2f' % options.FOV) +
          'cm, Working Distance: ' + str('%.2f' % round(WorkingDistance, 2)) +
          'cm\nScintillator Efficiency: ' + str(round(ScreenOutput, 2) * 100)
          + '%, Lens transmission: ' + str(round(LensTransmission, 2) * 100)
          + '%, QE sensor: ' + str(QESensor))
plt.xlabel('Distance [cm]')
plt.ylabel('Distance [cm]')

# Optical Axis
plt.axhline(color='k', linestyle='--')

# X-rays
x = numpy.arange(0, XRaySourcePosition - Thickness - SupportThickness, 0.1)
for yshift in numpy.arange(-options.FOV / 2, options.FOV / 2,
                            options.FOV / 10.0):
    plt.plot(-x - Thickness - SupportThickness, numpy.sin(x) + yshift, 'k')

# Scintillator
ScintillatorSupport = Rectangle(
    (-Thickness - SupportThickness, (options.FOV / 2) + SupportThickness),
    Thickness + SupportThickness, -options.FOV - SupportThickness * 2,
    facecolor="black")
plt.gca().add_patch(ScintillatorSupport)
Scintillator = Rectangle((-Thickness, options.FOV / 2), Thickness,
                         -options.FOV, facecolor="lightgreen")
plt.gca().add_patch(Scintillator)

# Light-Cone
# Opening angle
wedgecolor = 'r'
Wedge = Wedge((WorkingDistance, 0), -WorkingDistance * .25,
              -(options.OpeningAngle / 2), (options.OpeningAngle / 2),
              fill=False, color=wedgecolor)
plt.gca().add_patch(Wedge)

# Light Beams
beamcolor = wedgecolor
# Scintillator - Lens
plt.plot([0, WorkingDistance], [options.FOV / 2, 0], beamcolor)
plt.plot([0, WorkingDistance], [-options.FOV / 2, 0], beamcolor)
# Lens - Sensor
plt.plot([WorkingDistance, WorkingDistance + SensorPosition],
         [0, options.FOV / 2 / Demagnification], beamcolor)
plt.plot([WorkingDistance, WorkingDistance + SensorPosition],
         [0, -options.FOV / 2 / Demagnification], beamcolor)

# Camera
Sensor = Rectangle((WorkingDistance + SensorPosition, options.SensorSize / 2),
                   Thickness / 4, -options.SensorSize, facecolor="black")
plt.gca().add_patch(Sensor)
Housing = Rectangle((WorkingDistance + SensorPosition + Thickness / 4,
                     options.SensorSize / 2 / .618), Thickness / 4 / .618,
                    -options.SensorSize / .618, facecolor="black")
plt.gca().add_patch(Housing)

# Text
step = options.FOV / 8.0
plt.text(1.618 * WorkingDistance, options.FOV / 2,
         '- 1 ' + str(options.InputEnergy / 1000) + ' kV x-ray photon')
plt.text(1.618 * WorkingDistance, options.FOV / 2 - step,
         '- ' + str(int(PhotonsAfterScintillator)) + ' ' + str(
             Wavelength * 1e9) + ' nm photons after scintillator')
plt.text(1.618 * WorkingDistance, options.FOV / 2 - 2 * step,
         '- ' + str(int(PhotonsAfterLens)) + ' ' + str(
             Wavelength * 1e9) + ' nm photons after lens')
plt.text(1.618 * WorkingDistance, options.FOV / 2 - 3 * step,
         '- ' + str(int(ProducedElectrons)) + ' electrons on sensor')
plt.text(1.618 * WorkingDistance, options.FOV / 2 - 4 * step,
         '- Opening Angle: ' + str(
             options.OpeningAngle) + ' deg')  # http://is.gd/pxodor
plt.text(1.618 * WorkingDistance, options.FOV / 2 - 5 * step,
         '- Sensorsize: ' + str(options.SensorSize) + ' cm')
plt.text(1.618 * WorkingDistance, options.FOV / 2 - 6 * step,
         '- Demagnification: ' + str('%.2f' % Demagnification) + 'x')
plt.text(1.618 * WorkingDistance, options.FOV / 2 - 7 * step,
         '- To achieve ' + str('%.2f' % options.LinePairs) + ' lp/mm, we need')
plt.text(1.618 * WorkingDistance, options.FOV / 2 - 8 * step,
         '   a sensor with ' + str(
             round(PixelsNeeded ** 2 / 1e6, 2)) + ' Mpx (' + str(
             int(PixelsNeeded)) + 'x' + str(int(PixelsNeeded)) + ' px)')
plt.text(1.618 * WorkingDistance, options.FOV / 2 - 9 * step,
         '   resulting in a pixelsize of ' + str(
             '%.2f' % (SensorPixelSize * 1000)) + ' um.')

# Plot NA
plt.subplot(234)
plt.axis('equal')
Magnification = numpy.arange(0, 1.01, 0.01)
for FStop in [0.5, 0.8, 1, 1.2, 1.4, 2]:
    plt.plot(Magnification, Magnification / (2 * FStop * (1 + Magnification)),
             label='f/' + str('%0.2f' % FStop))
plt.plot(Magnification,
         Magnification / (2 * options.FStop * (1 + Magnification)), 'g--',
         linewidth=5, label='f/' + str('%0.2f' % options.FStop))
plt.legend(loc='upper left')
plt.hlines(NumericalApertureAverage, 0, 1)
plt.text(0.618, NumericalApertureAverage, 'NA flat panel')
plt.hlines(NumericalApertureDetermined, 0, 1)
plt.text(0.618, NumericalApertureDetermined, 'simulated NA of our lens')
plt.hlines(NumericalApertureJBAG, 0, 1)
plt.text(0.618, NumericalApertureJBAG, 'NA JBAG (?)')
plt.vlines(1 / Demagnification, 0, 1, 'g', '--')
plt.text(1 / Demagnification + 0.25, 0.8, 'Our calculated\nDemagnification: ' +
         str(Demagnification) + 'x=' + str(round(1 / Demagnification, 3)))

plt.title('NA')
plt.xlabel('Magnification')
plt.ylabel('NA')
plt.xlim([0, 1])

# Plot X-ray spectra
plt.subplot(235)
# http://stackoverflow.com/a/11249430/323100
Spectra = [
    (os.path.join(os.getcwd(), 'Spectra/Xray-Spectrum_040kV.txt')),
    (os.path.join(os.getcwd(), 'Spectra/Xray-Spectrum_046kV.txt')),
    (os.path.join(os.getcwd(), 'Spectra/Xray-Spectrum_053kV.txt')),
    (os.path.join(os.getcwd(), 'Spectra/Xray-Spectrum_060kV.txt')),
    (os.path.join(os.getcwd(), 'Spectra/Xray-Spectrum_070kV.txt')),
    (os.path.join(os.getcwd(), 'Spectra/Xray-Spectrum_080kV.txt')),
    (os.path.join(os.getcwd(), 'Spectra/Xray-Spectrum_090kV.txt')),
    (os.path.join(os.getcwd(), 'Spectra/Xray-Spectrum_100kV.txt')),
    (os.path.join(os.getcwd(), 'Spectra/Xray-Spectrum_120kV.txt'))
]

AnodeMaterial = [str(open(FileName).readlines()[1].split()[3]) for FileName in
                 Spectra]
Energy = [int(open(FileName).readlines()[2].split()[4]) for FileName in
          Spectra]
Ripple = [float(open(FileName).readlines()[3].split()[4]) for FileName in
          Spectra]
AirKerma = [float(open(FileName).readlines()[4].split()[3]) for FileName in
            Spectra]
MeanEnergy = [float(open(FileName).readlines()[5].split()[3]) for FileName in
              Spectra]
FilterMaterial = [str(open(FileName).readlines()[9].split()[1]) for FileName in
                  Spectra]
FilterThickness = [int(open(FileName).readlines()[9].split()[2]) for FileName
                   in Spectra]
Data = [(numpy.loadtxt(FileName)) for FileName in Spectra]

for i in range(len(Spectra)):
    plt.plot(Data[i][:, 0], Data[i][:, 1],
             label=str(Energy[i]) + 'kV, Mean=' + str(
                 round(MeanEnergy[i], 2)) + 'keV')
    # plt.plot( Data[i][:,0], Data[i][:,1], label=str(Energy[i]) +'kV')

plt.legend(loc='best')
plt.title(
    'X-ray spectra for ' + AnodeMaterial[0] + ' Anode,\n' + FilterMaterial[
        0] + ' Filter with ' + str(FilterThickness[0]) + ' mm Thickness')
plt.xlabel('Energy [kV]')
plt.ylabel('Photons')

# Plot of Ball Lenses
plt.subplot(236)
Dia = numpy.arange(0, 15, 0.2)
NA = (0.918919 * (-1.0 + Dia)) / Dia
FNo = (0.544118 * Dia) / (-1.0 + Dia)

plt.plot(Dia, NA, 'r', label='NA')
plt.plot(Dia, FNo, 'g', label='FNo')
plt.legend(loc='best')
plt.xlim([1.5, 10])
plt.ylim([0.3, 1.2])

for i in (2, 8):
    plt.axvline(i, color='k')
    if i > 3:
        plt.axhline(NA[numpy.where(Dia == i)], color='k')
        plt.axhline(FNo[numpy.where(Dia == i)], color='k')

plt.savefig('CalculateDetector.png')

# OUTPUT
if options.Output:
    Prefix = 'Config'
    try:
        os.mkdir(os.path.join(os.getcwd(), Prefix))
    except OSError:
        print 'Directory', os.path.join(os.getcwd(),
                                        Prefix), 'already exists, did not ' \
                                                 'create it...'
    print

    # We should probably do something more clever with "print "%10.4f" %
    # options" than the stuff below
    SaveName = Prefix + str(options).replace('{', '_').replace('}', ''). \
        replace("'", '').replace(': ', '_').replace(', ', '-'). \
        replace('-Output_True', '').replace('9999999999999', '')
    # getting the output of 'options' and doing some string-replacement to get
    # a nice filename for the output.

    # FIGURE
    plt.savefig(os.path.join(Prefix, ''.join([SaveName, '.png'])),
                dpi=fig.dpi)
    print 'Figure saved to ' + os.path.join(Prefix,
                                            ''.join([SaveName, '.png']))
    print
    # LOGFILE
    # Redirect console-output to a file according to
    # http://stackoverflow.com/a/4829801/323100
    # open the result file in write mode
    logfile = open(os.path.join(Prefix, ''.join([SaveName, '.txt'])), 'w')
    # store the default system handler to be able to restore it
    old_stdout = sys.stdout
    # Now your file is used by print as destination
    sys.stdout = logfile

    print 'Call the script with the commandline below to get the same result.'
    print ' '.join(sys.argv)
    print 80 * '-'
    print 'If we define the intensifying screen:'
    print '\t- to have an absorption of', 100 * ScreenAbsorption, '%'
    print '\t- to convert', 100 * ScreenConversion, \
        '% of the incoming x-rays to visible light'
    print '\t- and to have an emmittance of', 100 * ScreenAbsorption, \
        '% of all converted photons'
    print 'we have a total efficiency of the screen of ', 100 * ScreenOutput, \
        '%.'

    print
    print 'One incoming', options.InputEnergy / 1000, \
        'keV x-ray photon will thus produce:'
    print '\t-', int(round(PhotonsAfterScintillator)), \
        'photons with a wavelength of', \
        int(Wavelength * 1e9), 'nm (or', round(PhotonEnergyeV, 3), 'eV).'
    print '\t-', int(round(PhotonsAfterLens)), 'of these photons (' + \
                                               str(
                                                   LensTransmission * 100) + \
                                               ' %) will arrive at the sensor'
    print '\t- which will produce', int(round(ProducedElectrons)), \
        'electrons on a sensor with a QE of', QESensor

    print 'To achieve', options.LinePairs, 'lp/mm on a', options.FOV, \
        'cm scintillator, we need a sensor with', \
        round(int(PixelsNeeded) ** 2 / 1e6, 1), 'Mpx (' + \
        str(int(PixelsNeeded)) + 'x' + str(int(PixelsNeeded)), \
        'px), which results in pixels with a physical size of', \
        round(SensorPixelSize * 1000, 2), 'um on a', options.SensorSize, \
        'cm sensor.'

    print 'For the chosen optical configuration of:'
    print '\t- FOV =', '%.2f' % options.FOV, 'cm and'
    print '\t- Opening angle =', '%.2f' % options.OpeningAngle + 'deg we get a'
    print '\t- Working distance of', '%.2f' % WorkingDistance, 'cm'

    print
    print 'Numerical Aperture:'
    print '\t- calculated NA:', NumericalApertureCalculated, \
        '(central element in scintillator layer of FPD)'
    print '\t- average NA:', NumericalApertureAverage, \
        '(average NA on optical axis assuming 10 um distance between ' \
        'scintillator and detector)'
    print '\t- NA JBAG lenses:', NumericalApertureJBAG, \
        '(assuming F=1/2NA -> NA = 1/2F, with F =', FStopJBAG, ')'
    print '\t- NA for our sensor:', NumericalApertureDetermined, \
        '(according to Rene = SensorDistance / (FStop * 2 * SensorDistance/' \
        'Magnification)'

    sys.stdout = old_stdout  # here we restore the default behavior
    logfile.close()  # do not forget to close your file

    print 'Logfile saved to ' + os.path.join(Prefix,
                                             ''.join([SaveName, '.txt']))
    print
else:
    plt.show()

print 'The options were:'
# getting the output of 'options' and doing some string-replacement to get a
# nice filename for the output.
print str(options).replace('{', '').replace('}', '').replace("'", '').replace(
    ', ', '\n')

print 80 * '_'
print 'Call the script with the commandline below to get the same result...'
print ' '.join(sys.argv)

if options.Output:
    print
    print 'use the command below to open all the generated .png iamges with ' \
          'Fiji.'
    viewcommand = '/home/scratch/Apps/Fiji.app/fiji-linux -eval' + \
            'run("Image Sequence...", "open=' + os.getcwd() + \
            ' starting=1 increment=1 scale=100 file=png or=[] sort");\' &'
    print viewcommand
    print 80 * '_'

# # kill all runnig fiji jobs
# killall fiji-linux;
# # remove all calculated images
# rm *.png;
# # calculate some stuff
# for f in {10..43..15}; # Field of View
# do echo FOV $f;
# for o in {10..150..15}; # Opening Angle
# do echo OpeningAngle $o;
# for s in {5..25..15}; # Sensor Size
# do echo SensorSize $s;
# ./CalculateDetector.py -f $f -o $o -s $s -p;
# done;
# done;
# done
# # open fiji
# /home/scratch/Apps/Fiji.app/fiji-linux -eval 'run("Image Sequence...",
# "open=/afs/psi.ch/project/EssentialMed/Dev starting=1 increment=1 scale=100
# file=png or=[] sort");' & # start fiji
