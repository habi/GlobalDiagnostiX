#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
from pylab import *
import os
import glob
from scipy import interpolate
import time

FigureSize = [8,9]
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
# Generate Labels which we can use later-on
Label = [Modality[i] + ': ' + str(Energy[i]) + 'kV, ' + str(mAs[i]) + 'mAs, ' + str(ExposureTime[i]) + 'ms' for i in range(len(Spectra))]

Frames = [open(item).readlines()[0].split()[1] for item in Spectra]
BinCenter = [open(item).readlines()[1].split()[0] for item in Spectra]
Photons = [open(item).readlines()[1].split()[1] for item in Spectra]
PhotonsPerFrame = [open(item).readlines()[1].split()[2] for item in Spectra]

# Calculate attenuation in 320 um of Silicon
SiliconAttenuation = np.loadtxt('Si_Attenuation.dat')
SiliconDensity = 2.329  # g/cm³
SiliconThickness = 320  # um

# Plot transmission
plt.figure(figsize=FigureSize)
plt.plot(SiliconAttenuation[:, 0]*1000,
         (np.exp(- (SiliconAttenuation[:, 1] * SiliconDensity * SiliconThickness / 10000 ))),
         'ro', label='Si Transmission')
plt.xlabel('Photon Energy [keV]')
plt.ylabel('Tranmission')
plt.ylim([0,1])
plt.savefig('1_Si_Transmission.pdf', transparent=True)

# Plot transmission
plt.figure(figsize=FigureSize)
plt.loglog(SiliconAttenuation[:, 0], SiliconAttenuation[:, 1],
         'r', label='Si Transmission')
plt.xlabel('Photon Energy [keV]')
plt.ylabel('Tranmission')
plt.savefig('1_Si_Transmission.pdf', transparent=True)

plt.show()
sys.exit()

# Plot transmission-zoom
plt.figure(figsize=FigureSize)
for i in reversed(range(5000,20250,500)):
    plt.plot(SiliconAttenuation[:, 0]*1000,
            (np.exp(- (SiliconAttenuation[:, 1] * SiliconDensity * SiliconThickness / 10000 ))),
            'ro', label='Si Transmission')
    plt.xlabel('Photon Energy [keV]')
    plt.ylabel('Tranmission')
    plt.ylim([0,1])
    plt.xlim(xmin=0)
    plt.xlim(xmax=i)
    print '%05i' % i
    plt.draw()
    plt.savefig('anim' + str('%05i' % (20000 - i)) + '.png', transparent=True)

for i in reversed(range(1000,5000,200)):
    plt.plot(SiliconAttenuation[:, 0]*1000,
            (np.exp(- (SiliconAttenuation[:, 1] * SiliconDensity * SiliconThickness / 10000 ))),
            'ro', label='Si Transmission')
    plt.xlabel('Photon Energy [keV]')
    plt.ylabel('Tranmission')
    plt.ylim([0,1])
    plt.xlim(xmin=0)
    plt.xlim(xmax=i)
    print '%05i' % i
    plt.draw()
    plt.savefig('anim' + str('%05i' % (20000 - i)) + '.png', transparent=True)

for i in reversed(range(120,1000,50)):
    plt.plot(SiliconAttenuation[:, 0]*1000,
            (np.exp(- (SiliconAttenuation[:, 1] * SiliconDensity * SiliconThickness / 10000 ))),
            'ro', label='Si Transmission')
    plt.xlabel('Photon Energy [keV]')
    plt.ylabel('Tranmission')
    plt.ylim([0,1])
    plt.xlim(xmin=0)
    plt.xlim(xmax=i)
    print '%05i' % i
    plt.draw()
    plt.savefig('anim' + str('%05i' % (20000 - i)) + '.png', transparent=True)

# Plot transmission with the limits that are interesting for us
plt.figure(figsize=FigureSize)
plt.plot(SiliconAttenuation[:, 0]*1000,
         (np.exp(- (SiliconAttenuation[:, 1] * SiliconDensity * SiliconThickness / 10000 ))),
         'ro', label='Si Transmission')
plt.xlabel('Photon Energy [keV]')
plt.ylabel('Tranmission')
plt.xlim([0,120])
plt.ylim([0,1])
plt.savefig('2_Si_Transmission_limits.pdf', transparent=True)
#~ plt.show()

# Plot interpolated transmission
x = SiliconAttenuation[:, 0] * 1000
y = (np.exp(- (SiliconAttenuation[:, 1] * SiliconDensity * SiliconThickness / 10000 )))
interpolated = interpolate.interp1d(x, y, kind='cubic')
xnew = np.linspace(1,120,1000)  # get 1000 steps from 1 to 120

plt.figure(figsize=FigureSize)
plt.plot(SiliconAttenuation[:, 0]*1000,
         (np.exp(- (SiliconAttenuation[:, 1] * SiliconDensity * SiliconThickness / 10000 ))),
         'ro', label='Si Transmission')
plt.plot(xnew,interpolated(xnew),'r',label='Interpolated values')         
plt.xlabel('Photon Energy [keV]')
plt.ylabel('Tranmission')
plt.xlim([0,120])
plt.ylim([0,1])
plt.savefig('3_Si_Transmission_limits_interpolated.pdf', transparent=True)

print 'Plotting uncorrected spectra'
for i in range(int(len(Spectra)/2)):
    plt.figure(figsize=FigureSize)
    k = i + int(len(Spectra)/2)
    plt.plot(Data[i][:, 0], Data[i][:, 1], label=Label[i], color='k')
    plt.plot(Data[k][:, 0], Data[k][:, 1], label=Label[k], color='g')
    plt.legend(loc=1)
    plt.xlim([0,5000])
    plt.ylim(ymin=0)
    plt.savefig('4_' + DataName[i] + '.pdf', transparent=True)

print 'Plotting corrected spectra'
for i in range(int(len(Spectra)/2)):
    plt.figure(figsize=FigureSize)
    k = i + int(len(Spectra)/2)
    plt.plot(Data[i][:, 0], Data[i][:, 1], color='k', alpha=0.125)
    plt.plot(Data[k][:, 0], Data[k][:, 1], color='g', alpha=0.125)
    plt.plot(xnew * 5000 / 120, interpolated(xnew) * Data[i][:, 1], color='k',
             label=Label[i])
    plt.plot(xnew * 5000 / 120, interpolated(xnew) * Data[k][:, 1], color='g',
             label=Label[k])
    plt.legend(loc=1)
    plt.xlim([0,5000])
    plt.ylim(ymin=0)
    plt.savefig('5_' + DataName[i] + 'corrected.pdf', transparent=True)

print 'Plotting corrected log-spectra'
for i in range(int(len(Spectra)/2)):
    plt.figure(figsize=FigureSize)
    k = i + int(len(Spectra)/2)
    plt.semilogy(Data[i][:, 0], Data[i][:, 1], color='k', alpha=0.125)
    plt.semilogy(Data[k][:, 0], Data[k][:, 1], color='g', alpha=0.125)
    plt.semilogy(xnew * 5000 / 120, interpolated(xnew) * Data[i][:, 1], color='k',
             label=Label[i])
    plt.semilogy(xnew * 5000 / 120, interpolated(xnew) * Data[k][:, 1], color='g',
             label=Label[k])
    plt.legend(loc=1)
    plt.xlim([0,5000])
    plt.ylim(ymin=1)
    plt.savefig('6_' + DataName[i] + 'log.pdf', transparent=True)

sys.exit()














print 'Plotting Spectra, Logplot and Difference for'
for i in range(int(len(Spectra)/2)):
    plt.figure(figsize=FigureSize)
    k = i + int(len(Spectra)/2)
    print '    * ' + DataName[i], 'vs.', DataName[k]
    print '        * for', DataName[i], 'we recorded',\
        '%.3e' % int(np.sum(Data[i][:, 1])), 'photons.'
    print '        * for', DataName[k], 'we recorded',\
        '%.3e' % int(np.sum(Data[k][:, 1])), 'photons.'
    print '        * the difference is',\
        '%.3e' % int(np.sum(Data[i][:, 1]) - np.sum(Data[k][:, 1])), 'photons'
    plt.subplot(1, 3, 1)
    plt.plot(Data[i][:, 0], Data[i][:, 1], label=DataName[i], color='k')
    plt.plot(Data[k][:, 0], Data[k][:, 1], label=DataName[k], color='g')
    plt.xlabel('BinCenter [adc]')
    plt.ylabel('Photons [count]')
    plt.xlim(xmin=0)
    # Plotting left, right and then middle, so we have the legend on top
    plt.subplot(1, 3, 3)
    plt.plot(Data[i][:, 0], Data[i][:, 1], color='k',
             label=' '.join([Modality[i] + ',', str(Energy[i]) + 'kV,',
                             str(mAs[i]) + 'mAs']))
    plt.plot(Data[k][:, 0], Data[k][:, 1], color='g',
             label=' '.join([Modality[k][:2] + ' ' + Modality[k][13:] + ',',
             str(Energy[k]) + 'kV,', str(mAs[k]) + 'mAs']))
    plt.plot(Data[i][:, 0], (Data[i] - Data[k])[:, 1],
             label='Difference', color='r')
    plt.legend(loc='center', bbox_to_anchor=(0.5, 0.1))
    plt.xlabel('BinCenter [adc]')
    plt.ylabel('Photons [count]')
    plt.title('Difference')
    plt.xlim(xmin=0)
    plt.subplot(1, 3, 2)
    plt.semilogy(Data[i][:, 0], Data[i][:, 1], label=DataName[i], color='k')
    plt.semilogy(Data[k][:, 0], Data[k][:, 1], label=DataName[k], color='g')
    plt.xlabel('BinCenter [adc]')
    plt.ylabel('Photons [log count]')
    plt.legend(loc='center', bbox_to_anchor=(0.5, 0.9))
    plt.xlim(xmin=0)
    plt.savefig(os.path.join('img', 'Full_' + DataName[i] + '.png'),
                transparent=True)
    plt.savefig(os.path.join('img', 'Full_' + DataName[i] + '.pdf'),
                transparent=True)
    plt.show()


exit()

print
print 'Plotting'
for i in range(int(len(Spectra)/2)):
    plt.figure(figsize=FigureSize)
    k = i + int(len(Spectra)/2)
    print '    * ' + DataName[i] + '/' + DataName[k]
    plt.plot(Data[i][:, 0], Data[i][:, 1], color='k',
                 label=' '.join([Modality[i] + ',',
                                 str(Energy[i]) + 'kV,',
                                 str(mAs[i]) + 'mAs,',
                                 str(ExposureTime[i]) + 'ms']))
    plt.plot(Data[k][:, 0], Data[k][:, 1], color='g',
                 label=' '.join([Modality[k] + ',',
                                 str(Energy[k]) + 'kV,',
                                 str(mAs[k]) + 'mAs,',
                                 str(ExposureTime[k]) + 'ms']))
    plt.plot(Data[i][:, 0], (Data[i] - Data[k])[:, 1],
             label='Difference', color='r')                                 
    plt.legend(loc='best')
    plt.xlabel('BinCenter [adc]')
    plt.xlim(xmin=0)
    plt.savefig(os.path.join('img', 'Photons_' + DataName[i] + '.png'),
                transparent=True)
    plt.savefig(os.path.join('img', 'Photons_' + DataName[i] + '.pdf'),
                transparent=True)
    #~ plt.show()

print
print 'Plotting Logplot for every modality'
for i in range(int(len(Spectra)/2)):
    plt.figure(figsize=FigureSize)
    k = i + int(len(Spectra)/2)
    print '    * ' + DataName[i] + '/' + DataName[k]    
    plt.semilogy(Data[i][:, 0], Data[i][:, 1], color='k',
                 label=' '.join([Modality[i] + ',',
                                 str(Energy[i]) + 'kV,',
                                 str(mAs[i]) + 'mAs,',
                                 str(ExposureTime[i]) + 'ms']))
    plt.semilogy(Data[k][:, 0], Data[k][:, 1], color='g',
                 label=' '.join([Modality[k] + ',',
                                 str(Energy[k]) + 'kV,',
                                 str(mAs[k]) + 'mAs,',
                                 str(ExposureTime[k]) + 'ms']))
    plt.semilogy(Data[i][:, 0], (Data[i] - Data[k])[:, 1],
                 label='Difference', color='r')                                 
    plt.legend(loc='best')
    plt.xlabel('BinCenter [adc]')
    plt.xlim(xmin=0)
    plt.savefig(os.path.join('img', 'Log_Photons_' + DataName[i] + '.png'),
                transparent=True)
    plt.savefig(os.path.join('img', 'Log_Photons_' + DataName[i] + '.pdf'),
                transparent=True)
    #~ plt.show()
