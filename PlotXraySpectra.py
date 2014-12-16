import matplotlib.pylab as plt
import os
import scipy
import numpy as np
from scipy.integrate import trapz

# http://stackoverflow.com/a/11249430/323100
Spectrapath = '/afs/psi.ch/project/EssentialMed/Dev/Spectra'
Spectra = [
    (os.path.join(Spectrapath, 'Xray-Spectrum_040kV.txt')),
    (os.path.join(Spectrapath, 'Xray-Spectrum_046kV.txt')),
    (os.path.join(Spectrapath, 'Xray-Spectrum_053kV.txt')),
    (os.path.join(Spectrapath, 'Xray-Spectrum_060kV.txt')),
    (os.path.join(Spectrapath, 'Xray-Spectrum_070kV.txt')),
    (os.path.join(Spectrapath, 'Xray-Spectrum_080kV.txt')),
    (os.path.join(Spectrapath, 'Xray-Spectrum_090kV.txt')),
    (os.path.join(Spectrapath, 'Xray-Spectrum_100kV.txt')),
    (os.path.join(Spectrapath, 'Xray-Spectrum_100kV.txt')),
    (os.path.join(Spectrapath, 'Xray-Spectrum_120kV.txt'))]

Data = [(np.loadtxt(FileName)) for FileName in Spectra]
Energy = [int(open(FileName).readlines()[2].split()[4])
          for FileName in Spectra]
Mean = [float(open(FileName).readlines()[5].split()[3])
        for FileName in Spectra]

for i in range(len(Spectra)):
    plt.plot(Data[i][:, 0], Data[i][:, 1],
             label=str(Energy[i]) + 'kV, Mean=' +
                   str(round(Mean[i], 3)) + 'keV')

plt.legend(loc='best')
plt.title('X-ray spectra')
plt.xlabel('Energy [kV]')
plt.ylabel('Photons')
plt.savefig('plot.pdf')

plt.figure(figsize=[22, 5])
for counter, spectra in enumerate(Spectra):
    plt.subplot(1, len(Spectra), counter + 1)
    plt.plot(Data[counter][:, 0], Data[counter][:, 1])
    Integral = scipy.integrate.trapz(Data[counter][:, 1], Data[counter][:, 0])
    print 'The integral for', Energy[counter], 'kV is', \
        str(round(Integral / 1e6, 3)) + 'e6 photons'
    plt.title(str(Energy[counter]) + 'kV\n' +
              str(round(Integral / 1e6, 3)) + 'e6 photons')
    plt.xlim([0, 150])
    plt.ylim([0, 3e6])
    # Turn off y-ticks for subplots 2-end (counter >0)
    if counter:
        plt.setp(plt.gca().get_yticklabels(), visible=False)
plt.tight_layout()
plt.show()
