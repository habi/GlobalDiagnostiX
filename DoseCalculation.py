#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
We'd like to know a bit more about the dose we inflict on the patient.
This script is used to calculate said dose based on the x-ray spectra that we
will be able to set (see Source-Specifications).
"""

from optparse import OptionParser
import sys
import os
import numpy as np
from scipy import constants

# Use Pythons Optionparser to define and read the options, and also
# give some help to the user
parser = OptionParser()
usage = "usage: %prog [options] arg"
parser.add_option('-v', '--kv', dest='kV',
                  type='int',
                  metavar='53',
                  default=53,
                  help='Tube peak voltage [kV] you would like to calcuate the '
                       'dose for. The script only accepts voltages that are '
                       'in the specs (and tells you if you set others). '
                       'Defaults to 90 kV.')
parser.add_option('-m', '--mas', dest='mAs',
                  type='float',
                  metavar='1.6',
                  default=125,
                  help='mAs settings. Defaults to 125 mAs, which with the '
                       'default 90 kV is the setting for lumbar spine.')
parser.add_option('-e', '--exposuretime', dest='Exposuretime',
                  type='float',
                  metavar='100',
                  default=1000,
                  help='Exposure time [ms]. Defaults to 1 second, because we '
                       'assume that "-m" (mAs) is used as input. If the user '
                       'insists, an exposure time can be set.')
parser.add_option('-d', '--distance', dest='Distance',
                  type='int',
                  metavar='100',
                  default=140,
                  help='Source-Detector distance [cm]. Defaults to 1.4 m')
parser.add_option('-l', '--length', dest='Length',
                  type='float',
                  metavar='15',
                  default=20,
                  help='Length of the (square) FOV [cm]. Defaults to 20 cm.')
parser.add_option('-t', '--thickness', dest='Thickness',
                  type='int',
                  metavar='13',
                  default=20,
                  help='Thickness of the patient [cm]. Used to calculate '
                       'attenuation. Defaults to 20 cm.')
parser.add_option('-c', '--chatty', dest='chatty',
                  default=False, action='store_true',
                  help='Be chatty. Default: Tell us only the relevant stuff.',
                  metavar=1)
(options, args) = parser.parse_args()

# show the help if no parameters are given
if options.kV is None:
    parser.print_help()
    print 'Example:'
    print 'The command below calculates the dose for a peak tube voltage of',\
        '60 kV.'
    print
    print sys.argv[0], '-v 60'
    exit(1)

# Inform the user that we only have certain values to work with
Voltage = [46, 53, 60, 70, 80, 90, 100, 120]
if not options.kV in Voltage:
    print 'You can only enter one of these voltages:',\
        str(Voltage).strip('[]'), 'kV'
    print
    print 'Try again with the nearest allowed value:'
    # http://stackoverflow.com/a/9706105/323100
    print sys.argv[0], '-v', Voltage[min(range(len(Voltage)),
                                     key=lambda i:abs(Voltage[i] -
                                                      options.kV))]
    exit(1)

ChosenVoltage = Voltage.index(options.kV)
# Load spectra
SpectraPath = os.path.join(os.getcwd(), 'Spectra')
# Construct file names, then load the data with the filenames (we could do this
# in one step, but like this it's easier to debug. 'SpectrumData' is the data
# without comments, thus we read the mean energy on line 7 in a second step
SpectrumLocation = [os.path.join(SpectraPath, 'Xray-Spectrum_' +
                                              str("%03d" % kV) + 'kV.txt')
                    for kV in Voltage]
SpectrumData = [(np.loadtxt(FileName)) for FileName in SpectrumLocation]
MeanEnergy = [float(open(FileName).readlines()[5].split()[3]) for FileName in
              [os.path.join(SpectraPath, 'Xray-Spectrum_' + str("%03d" % kV) +
                            'kV.txt') for kV in Voltage]]
if options.chatty:
    for v, e in zip(Voltage, MeanEnergy):
        print 'Peak tube voltage', v, 'kV = mean energy', int(round(e)), 'keV'


print 'For a peak tube voltage of', options.kV, 'kV and a current of',\
    int(round(options.mAs / (options.Exposuretime / 1000.))), 'mAs (exposure',\
    'time', options.Exposuretime, 'ms) we get a mean energy of',\
    round(MeanEnergy[ChosenVoltage], 3), 'keV'

# Calculate the numbers of photons emitted from the tube.
PhotonEnergy = ( MeanEnergy[ChosenVoltage] / 1000 ) * constants.e  # Joules
print 'At this mean energy, a single photon has an energy of',\
    '%.3e' % PhotonEnergy, 'J'
eta = 1e-9  # *ZV
Z = 74  # Tungsten

# Calculate the number of photons from the tube to the sample
#~ N0 = (UI/E)*eta*(Area/4*Pi*r²)
    # Energie / PhotonEnergie = Nr. of Photons produced
    # Nr. of Photons produced * Conversion Efficiency = Photons emitted
    # Photons emitted reaching target area
# Calculate the current from the mAs
Current = (options.mAs / (options.Exposuretime / 1000.)) / 1000.  # Ampere
N0 = ((options.kV * Current)/PhotonEnergy)
 
print '    - the tube emitts %.3e' % N0, 'photons'

print 'done'
exit()










# Setup parameters
FOV = 10  # cm. Approximation of a wrist (10 * 10 * 5cm)
Area = FOV ** 2  # cm²
Thickness = 5  # cm
Volume = Area * Thickness
Density = 1.02  # g/cm³
Weight = float(Volume) * Density / 1000  # kg

# @40kV, half bone, half muscle
AttenuationCoefficient = []
AttenuationCoefficient.append(np.mean((2.685e-1, 6.655-1)))
# @70kV (0.5*60+0.5*80), both half bone, half muscle
AttenuationCoefficient.append(np.mean((np.mean((2.048e-01, 3.148e-01)),
                                       np.mean((1.823e-01, 2.229e-01)))))

'''
Skeletal muscle (http://is.gd/D88OFv)
    Energy         μ/ρ       μen/ρ
    (MeV)       (cm2/g)    (cm2/g)
    1.00000E-02  5.356E+00  4.964E+00
    1.50000E-02  1.693E+00  1.396E+00
    2.00000E-02  8.205E-01  5.638E-01
    3.00000E-02  3.783E-01  1.610E-01
    4.00000E-02  *2.685E-01*  7.192E-02
    5.00000E-02  2.262E-01  4.349E-02
    6.00000E-02  *2.048E-01*  3.258E-02
    8.00000E-02  *1.823E-01*  2.615E-02
Cortical bone (http://is.gd/2176eQ)
    Energy         μ/ρ       μen/ρ
    (MeV)       (cm2/g)    (cm2/g)
    1.00000E-02  2.851E+01  2.680E+01
    1.50000E-02  9.032E+00  8.388E+00
    2.00000E-02  4.001E+00  3.601E+00
    3.00000E-02  1.331E+00  1.070E+00
    4.00000E-02  *6.655E-01*  4.507E-01
    5.00000E-02  4.242E-01  2.336E-01
    6.00000E-02  *3.148E-01* 1.400E-01
    8.00000E-02  *2.229E-01*  6.896E-02
'''

r = 140  # cm, Distance from source to sample
eta = 1e-9  # *ZV
Z = 74  # Tungsten
eV = 1.602e-19  # J

QFactor = 1  # http://en.wikipedia.org/wiki/Dosimetry#Equivalent_Dose
WeightingFactor = 0.12  # http://en.wikipedia.org/wiki/Dosimetry#Effective_dose
ExposureTime = 1000e-3  # s

# Read xray spectra
Spectrapath = os.path.join(os.getcwd(), 'Spectra')
#~ Spectra = [(os.path.join(Spectrapath, 'Xray-Spectrum_046kV.txt')),
           #~ (os.path.join(Spectrapath, 'Xray-Spectrum_070kV.txt'))]
Spectra = [(os.path.join(Spectrapath, 'Xray-Spectrum_046kV.txt')),
           (os.path.join(Spectrapath, 'Xray-Spectrum_090kV.txt'))]

Data = [(np.loadtxt(FileName)) for FileName in Spectra]

SourceVoltage = [int(open(FileName).readlines()[2].split()[4])
                 for FileName in Spectra]
AverageEnergy = [float(open(FileName).readlines()[5].split()[3])
                 for FileName in Spectra]

# Give out values
#~ for Voltage, Current, case in zip((SourceVoltage[0], SourceVoltage[1]),
                                  #~ (50, 1.6), range(len(Spectra))):
for Voltage, Current, case in zip((SourceVoltage[0], SourceVoltage[1]),
                                  (8, 125), range(len(Spectra))):
    print 80 * '-'
    print 'For a voltage of', Voltage, 'kV and a current of',\
        Current * ExposureTime, 'mAs (exposure time', ExposureTime, 's)'
    print '    - we get a mean energy of', round(AverageEnergy[case], 4), 'keV'

    # Calculate the number of photons from the tube to the sample
    #~ N0 = (VI/E)*eta*(A/4Pir²)
    N0 = (Voltage * Current) / (Voltage * eV) * \
        eta * Z * Voltage * \
        Area / (4 * np.pi * r ** 2)
    print '    - the tube emitts %.4e' % N0, 'photons per second'

    # Number of absorbed photons
    #~ N = N0(1-e^-uT)
    N = N0 * (1 - math.e ** (-AttenuationCoefficient[case] * Thickness))
    print '    - %.4e' % N, 'photons/s are absorbed in the sample, if we',\
        'assume the sample to have an attenuation coefficient of',\
        AttenuationCoefficient[case], 'cm^-1 (@' + str(Voltage), 'kV)'

    # Absorbed radiation dose per second
    #~ Da = Eneregy / Weight  # J/kg per second
    Da = N * AverageEnergy[case] * 1000 * eV / Weight

    print '    -', round(Da * 1000, 4), 'mGy/s are absorbed by the sample,',\
        ' if we assume it is', Weight, 'kg'

    # Effective dose per second
    #~ De = Da * Wr, WR = Q * N
    De = Da * QFactor * WeightingFactor

    print '    -', round(De*1000, 4), 'mSv/s is the effective dose'

    # Total effective dose on the sample
    D = De * ExposureTime

    print '    -', round(D*1000, 4), 'mSv is the effective dose on the',\
        'sample for an exposure time of =', ExposureTime, 's)'
