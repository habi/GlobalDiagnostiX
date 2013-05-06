#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Calculate photons and radiation dose per second
'''

from pylab import *
import math
import os

# Setup parameters
FOV = 5  # cm
Area = FOV ** 2  # cm²
r = 120  # cm
Voltage = 40e3  # kV
Current = 25e-3  # mA
AverageEnergy = 28e3  # keV
eta = 1e-9  # *ZV
Z = 74  # Tungsten
eV = 1.602e-19  # J
AttenuationCoefficient = 0.418   # cm^-1
Thickness = 1  # cm
Weight = 0.0255
QFactor = 1  # http://en.wikipedia.org/wiki/Dosimetry#Equivalent_Dose
WeightingFactor = 0.12  # http://en.wikipedia.org/wiki/Dosimetry#Effective_dose
ExposureTime = 112  # s

# Calculate the number of photons from the tube to the sample
#~ N0 = (VI/E)*eta*(A/4Pir²)
N0 = (Voltage * Current) / (Voltage * eV) * \
    eta * Z * Voltage * \
    Area / (4 * math.pi * r ** 2)

print '%.4e' % N0, 'photons/s are emitted by the tube at', Voltage / 1000,\
    'kV and', Current * 1000, 'mA'

# Number of absorbed photons
#~ N = N0(1-e^-uT)
N = N0 * (1 - math.e ** (-AttenuationCoefficient * Thickness))

print '%.4e' % N, 'photons/s are absorbed in the sample.'

# Absorbed radiation dose per second
#~ Da = Eneregy / Weight  # J/kg per second
Da = N * AverageEnergy * eV / Weight

print round(Da, 4), 'Gy/s are absorbed by a', Weight, 'kg sample'

# Effective dose per second
#~ De = Da * Wr, WR = Q * N
De = Da * QFactor * WeightingFactor

print round(De*1000, 4), 'mSv/s is the effective dose'

# Total effective dose on the sample
D = De * ExposureTime

print round(D*1000, 4), 'Sv is the effective dose on the sample, (Exposure',\
    'time =',ExposureTime, 's)'


exit()

# http://stackoverflow.com/a/11249430/323100
Spectrapath = '/afs/psi.ch/project/EssentialMed/Dev/Spectra'
Spectra = [
    #(os.path.join(Spectrapath, 'Xray-Spectrum_040kV.txt')),
    (os.path.join(Spectrapath, 'Xray-Spectrum_046kV.txt')),
    #(os.path.join(Spectrapath, 'Xray-Spectrum_053kV.txt')),
    #(os.path.join(Spectrapath, 'Xray-Spectrum_060kV.txt')),
    (os.path.join(Spectrapath, 'Xray-Spectrum_070kV.txt')),
    #(os.path.join(Spectrapath, 'Xray-Spectrum_080kV.txt')),
    #(os.path.join(Spectrapath, 'Xray-Spectrum_090kV.txt')),
    #(os.path.join(Spectrapath, 'Xray-Spectrum_100kV.txt')),
    #(os.path.join(Spectrapath, 'Xray-Spectrum_100kV.txt')),
    #(os.path.join(Spectrapath, 'Xray-Spectrum_120kV.txt'))
]

Data = [(np.loadtxt(FileName)) for FileName in Spectra]
Energy = [int(open(FileName).readlines()[3].split()[7])
          for FileName in Spectra]
Mean = [double(open(FileName).readlines()[6].split()[3])
        for FileName in Spectra]

# Give out values
for i in range(len(Spectra)):
    print Energy[i], 'kVP =>', Mean[i], 'keV'
