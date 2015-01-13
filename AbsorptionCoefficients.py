# -*- coding: utf8 -*-

"""
Script to plot some absorption coefficients from NIST.
The absorption coefficient data was downloaded as ASCII format table from
http://physics.nist.gov/PhysRefData/XrayMassCoef/tab4.html as "material.dat"
for some materials.
"""

import os
import glob
import matplotlib.pylab as plt
import numpy as np

BaseDir = os.path.join(os.getcwd(), 'nist', '*')
print 'Found', len(glob.glob(BaseDir)), 'files with data from NIST'
for item in glob.glob(BaseDir):
    print 'loading', os.path.basename(item)
    # Skip lines in which there's more than the info we need (K, L, M, etc)
    # http://stackoverflow.com/a/17151323
    with open(item) as f:
        lines = (line for line in f if len(line.split()) < 4)
        Data = np.loadtxt(lines)
        plt.loglog(Data[:, 0], Data[:, 1],
                   label=os.path.splitext(os.path.basename(item))[0])

plt.rc('text', usetex=True)
plt.title(r"$\mu/\rho$ [$\textrm{cm}^{2}$/g]")
plt.legend()
plt.show()
