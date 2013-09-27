from pylab import *
import os
import scipy
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
Mean = [np.round(double(open(FileName).readlines()[5].split()[3]),
                 decimals=2) for FileName in Spectra]

for i in range(len(Spectra)):
    plt.plot(Data[i][:, 0], Data[i][:, 1],
             label=str(Energy[i]) + 'kV, Mean=' + str(Mean[i]) + 'keV')

plt.legend(loc='best')
plt.title('X-ray spectra')
plt.xlabel('Energy [kV]')
plt.ylabel('Photons')
plt.savefig('plot.pdf')

WhichOneShallWeIntegrate = 6
plt.figure()
plt.plot(Data[WhichOneShallWeIntegrate][:, 0],
         Data[WhichOneShallWeIntegrate][:, 1])

Integral = scipy.integrate.trapz(Data[WhichOneShallWeIntegrate][:, 1],
                                 Data[WhichOneShallWeIntegrate][:, 0])
print 'The integral for', Energy[WhichOneShallWeIntegrate], 'kV is',\
    str(round(Integral/1e6, 3)) + 'e6 photons'

plt.show()
