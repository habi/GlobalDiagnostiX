# -*- coding: utf-8 -*-

"""
Plot ball lenses
"""

import matplotlib.pylab as plt
import numpy

Dia = numpy.arange(0, 15, 0.2)
NA = (0.918919 * (-1.0 + Dia)) / Dia
FNo = (0.544118 * Dia) / (-1.0 + Dia)

plt.plot(Dia, NA, 'r', label='NA')
plt.plot(Dia, FNo, 'g', label='FNo')
plt.legend(loc='best')
plt.xlim([1.5, 10])
plt.ylim([0.3, 1.2])

for i in (2, 8):
    plt.axvline(i, color='k')
    if i > 3:
        plt.axhline(NA[numpy.where(Dia == i)], color='k')
        plt.axhline(FNo[numpy.where(Dia == i)], color='k')

plt.show()
