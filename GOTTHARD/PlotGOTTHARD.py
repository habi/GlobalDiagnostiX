#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
from pylab import *
import os
import glob

# http://stackoverflow.com/a/11249430/323100
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

#~ for Sample in range(len(Spectra)):
    #~ print 'For', Modality[Sample], '(' + str(Energy[Sample]), 'kV,',\
        #~ mAs[Sample], 'mAs) we recorded a total of',\
        #~ int(np.sum(Data[Sample][:, 1])), 'photons.'

print 'Plotting Spectra, Logplot and Difference for'
for i in range(int(len(Spectra)/2)):
    plt.figure(figsize=(16, 9))
    k = i + int(len(Spectra)/2)
    print '    * ' + DataName[i] + '/' + DataName[k]    
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
    #~ plt.show()


print
print 'Plotting'
for i in range(int(len(Spectra)/2)):
    plt.figure(figsize=(16, 9))
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
    plt.figure(figsize=(16, 9))
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
    

exit()
for WhichOneShallWeIntegrate in range(len(Spectra)):
    #~ plt.figure()
    #~ plt.plot(Data[WhichOneShallWeIntegrate][:, 0],
            #~ Data[WhichOneShallWeIntegrate][:, 1])

    Integral = scipy.integrate.trapz(Data[WhichOneShallWeIntegrate][:, 1],
                                     Data[WhichOneShallWeIntegrate][:, 0])
    print 'The integral for', Energy[WhichOneShallWeIntegrate], 'kV is',\
        str(round(Integral/1e6, 3)) + 'e6 photons'
        
    #~ plt.show()
