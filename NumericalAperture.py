# -*- coding: utf-8 -*-

import matplotlib.pylab as plt
import numpy
from scipy import integrate

lpa = 400.0
hpa = 300.0
pxs = 0.194
maxres = 1.3
epx = 1 / (2 * maxres)

tsl = 1.0
nxp = 1.0
NAc = pxs / (tsl / 2)
NAa = integrate.quad(lambda x: numpy.arctan(pxs / (2 * x)), 0.01, 1)[0]
print 'middle NA:', NAc
print 'average NA:', NAa

pcs = 0.006944
mag = 36 / lpa
b = 50.0
g = b / mag

FStop = 1.4
NAdet = b / (FStop * 2 * g)

mag = numpy.arange(0, 1.01, 0.01)

legend = []
plt.figure()
for FStop in [0.5, 0.8, 1, 1.25, 1.4, 2]:
    plt.plot(mag, mag / (2 * FStop * (1 + mag)))
    legend.append(FStop)
plt.legend(legend)
plt.hlines(NAa, 0, 1)
plt.xlabel('Magnification')
plt.ylabel('NA')
plt.show()
