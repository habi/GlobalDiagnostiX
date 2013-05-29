'''
Script to calculate the Modulation transfer function of a edge target.

Kickstarted from from https://gist.github.com/stefanv/2051954 and additional
info from http://www.normankoren.com/Tutorials/MTF.html which tells us that
"MTF can be defined as the magnitude of the Fourier transform of the point or
line spread function. And some wikipedia lookup.
'''

from __future__ import division

import numpy as np
import scipy
import scipy.ndimage
import scipy.fftpack
from pylab import *
import time


def MTF(edgespreadfunction):
    '''
    Compute the modulation transfer function (MTF).

    The MTF is defined as the FFT of the line spread function.
    The line spread function is defined as the derivative of the edge spread
    function. The edge spread function are the values along an edge, ideally a
    knife-edge test target. See an explanation here: http://is.gd/uSC5Ve
    '''
    linespreadfunction = np.diff(edgespreadfunction)
    return np.fft.fft(linespreadfunction)


def LSF(edgespreadfunction):
    '''
    Compute the modulation transfer function (MTF).

    The MTF is defined as the FFT of the line spread function.
    The line spread function is defined as the derivative of the edge spread
    function. The edge spread function are the values along an edge, ideally a
    knife-edge test target. See an explanation here: http://is.gd/uSC5Ve
    '''
    return np.abs(np.diff(edgespreadfunction))

# Generate edge for N points
N = 50
edge = np.zeros(N)
edge[N // 2:] = 1

# Filter edge
gauss_05 = scipy.ndimage.gaussian_filter(edge, sigma=5)
gauss_10 = scipy.ndimage.gaussian_filter(edge, sigma=10)
#~ uniform = scipy.ndimage.uniform_filter(edge, size=10)

'''
Save the plots in a dictionary, so we can iterate through it afterwards. See
http://stackoverflow.com/a/2553532/323100 and
http://docs.python.org/2/tutorial/datastructures.html#looping-techniques for
reference how it's done.
'''
plots = dict((name, eval(name)) for name in ['edge', 'gauss_05', 'gauss_10'])

# Plot Edge and differently filtered variants
plt.figure()
plt.subplot(131)
for name, values in plots.iteritems():
    plt.plot(values, label=name)
    plt.legend()
#~ plt.ylim(0, 1.1)
plt.legend(loc='best')
plt.title('Edge')

# Plot LSF (absolute values)
plt.subplot(132)
for name, values in plots.iteritems():
    plt.plot(LSF(values), label=name)
plt.legend(loc='best')
plt.ylim(-1.1, 1.1)
plt.title('LSF')

# Plot MTF (absolute values)
plt.subplot(133)
for name, values in plots.iteritems():
    plt.plot(MTF(values), label=name)
plt.legend(loc='best')
plt.ylim(-1.1, 1.1)
plt.title('MTF')
plt.draw()
