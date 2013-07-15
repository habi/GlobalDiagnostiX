#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Calculate photons and radiation dose per second
'''

from pylab import *
import numpy as np
import os

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
ExposureTime = 100e-3  # s

# Read xray spectra
Spectrapath = os.path.join(os.getcwd(), 'Spectra')
Spectra = [(os.path.join(Spectrapath, 'Xray-Spectrum_046kV.txt')),
           (os.path.join(Spectrapath, 'Xray-Spectrum_070kV.txt'))]

Data = [(np.loadtxt(FileName)) for FileName in Spectra]
SourceVoltage = [int(open(FileName).readlines()[3].split()[7])
                 for FileName in Spectra]
AverageEnergy = [float(open(FileName).readlines()[6].split()[3])
                 for FileName in Spectra]

# Give out values
for Voltage, Current, case in zip((SourceVoltage[0], SourceVoltage[1]),
                                  (50, 1.6), range(len(Spectra))):
    print 80 * '-'
    print 'For a voltage of', Voltage, 'kV and a current of', Current, 'mAs'
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
        ' sample for an exposure time of =', ExposureTime, 's)'
