#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
from pylab import *
import os
import glob

GOTTHARDArea = 1130 * (50 / 1000) * 2  # mm
Distance = 163  # cm
ScintillatorArea = 430 * 430   # mm
print 'The area of the GOTTHARD sensor we used was', int(GOTTHARDArea), 'mm²'
print 'This is', int(round(ScintillatorArea/GOTTHARDArea)), 'times smaller',\
    'than the scintillator we plan to use (430 x 430 mm²)'

SiliconAttenuation = np.loadtxt('Si_Attenuation.dat')
SiliconTransmission = np.loadtxt('Si_Transmission.dat')

Spectrapath = '/afs/psi.ch/user/h/haberthuer/EssentialMed/Images/12-GOTTHARD_and_TIS/GOTTHARD'
Spectra = sort(glob.glob(os.path.join(Spectrapath, '*.txt')))

FileName = [os.path.basename(item) for item in Spectra]
Data = [np.loadtxt(item) for item in Spectra]
DataName = [open(item).readlines()[0].split()[0][1:-2] for item in Spectra]

# Get Filenames of Spectra and split it up into the desired values like kV, mAs
# and exposure time with some basic string handling.
Modality = [item.split('_')[0] for item in FileName]
Energy = [int(item.split('_')[1][:-2]) for item in FileName]
Current = [int(item.split('_')[2][:-2]) for item in FileName]
mAs = [float(item.split('_')[3][:-3]) for item in FileName]
ExposureTime = [int(item.split('_')[4][:-6]) for item in FileName]

Frames = [open(item).readlines()[0].split()[1] for item in Spectra]
BinCenter = [open(item).readlines()[1].split()[0] for item in Spectra]
Photons = [open(item).readlines()[1].split()[1] for item in Spectra]
PhotonsPerFrame = [open(item).readlines()[1].split()[2] for item in Spectra]

for Sample in range(len(Spectra)):
    print 'For', Modality[Sample]
    print '    * with', Energy[Sample], 'kV and,', mAs[Sample],\
        'mAs we recorded'
    print '    * a total of', '%.3e' % np.sum(Data[Sample][:, 1]),\
        'photons over an area of', int(GOTTHARDArea), 'mm².'
    print '    * which are',\
        '%.3e' % (np.sum(Data[Sample][:, 1]) *
                  (ScintillatorArea/GOTTHARDArea)),\
        'photons over the full scintillator area (43 x 43 cm²)'

exit()

plt.figure()
hold(True)
plt.subplot(1, 2, 1)
plt.semilogy(SiliconAttenuation[:, 0]*1000, SiliconAttenuation[:, 1], 'r')
plt.xlabel('Photon Energy [keV]')
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.ylabel(r'Attenuation coefficient $\frac{\mu}{\rho}$ [cm2/g]')
plt.title('Attenuation')
plt.xlim([0, 120])

plt.subplot(1, 2, 2)
plt.plot(SiliconTransmission[:, 0]/1000, SiliconTransmission[:, 1], 'g')
plt.xlabel('Photon Energy [keV]')
plt.ylabel('Tranmission')
plt.title('Transmission for a thickness of 320 um')
plt.xlim([0, 120])

plt.savefig('Si_Attenuation_Transmission.pdf')
plt.show()
