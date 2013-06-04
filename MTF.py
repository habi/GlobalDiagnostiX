'''
Script to calculate the Modulation transfer function of a edge target.

Kickstarted from from https://gist.github.com/stefanv/2051954 and additional
info from http://www.normankoren.com/Tutorials/MTF.html which tells us that
"MTF can be defined as the magnitude of the Fourier transform of the point or
line spread function. And some wikipedia lookup.
'''

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
    return np.abs(np.fft.fft(linespreadfunction))
    

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
N = 500
edge = np.zeros(N)
edge[:N / 2] = 1

#~ edge=np.arange(-50,50,0.1)

# Filter edge
sigma_1 = 0.5
gauss_1 = scipy.ndimage.gaussian_filter(edge, sigma=sigma_1)
sigma_2 = 0.75
gauss_2 = scipy.ndimage.gaussian_filter(edge, sigma=sigma_2)

'''
Save the plots in a dictionary, so we can iterate through it afterwards. See
http://stackoverflow.com/a/2553532/323100 and
http://docs.python.org/2/tutorial/datastructures.html#looping-techniques for
reference how it's done.
'''
plots = dict((name, eval(name)) for name in ['edge', 'gauss_1', 'gauss_2'])

plt.figure(figsize=(16,12))
plt.subplot(331)
plt.plot(edge,label='edge')
plt.ylim(-0.1,1.1)
plt.xlim(len(edge)/2-25,len(edge)/2+25)
plt.title('Ideal Edge')

plt.subplot(334)
plt.plot(LSF(edge),label='lsf')
plt.title('LSF')
plt.ylim(-0.1,1.1)
plt.xlim(len(edge)/2-25,len(edge)/2+25)
plt.ylim(-0.1,1.1)

plt.subplot(337)
plt.plot(MTF(edge),label='MTF')
plt.ylim(-0.1,1.1)
plt.xlim(0,len(edge)/2)
plt.title(' '.join(['MTF @ Nyquist=',str(np.round(MTF(edge)[len(edge)/2],3)*100),'%']))
         
plt.subplot(332)
plt.plot(gauss_1,label='edge')
plt.ylim(-0.1,1.1)
plt.xlim(len(edge)/2-25,len(edge)/2+25)
plt.title(' '.join(['Gauss with Sigma',str(sigma_1)]))

plt.subplot(335)
plt.plot(LSF(gauss_1),label='lsf')
plt.ylim(-0.1,1.1)
plt.xlim(len(edge)/2-25,len(edge)/2+25)
plt.title(' '.join(['LSF @ Sigma',str(sigma_1)]))

plt.subplot(338)
plt.plot(MTF(gauss_1),label='MTF')
plt.plot(np.ones(N)*MTF(gauss_1)[len(edge)/2])
plt.ylim(-0.1,1.1)
plt.xlim(0,len(edge)/2)
plt.title(' '.join(['MTF @ Nyquist=',str(np.round(MTF(gauss_1)[len(edge)/2],3)*100),'%']))

plt.subplot(333)
plt.plot(gauss_2,label='edge')
plt.ylim(-0.1,1.1)
plt.xlim(len(edge)/2-25,len(edge)/2+25)
plt.title(' '.join(['Gauss with Sigma',str(sigma_2)]))

plt.subplot(336)
plt.plot(LSF(gauss_2),label='lsf')
plt.ylim(-0.1,1.1)
plt.xlim(len(edge)/2-25,len(edge)/2+25)
plt.title(' '.join(['LSF @ Sigma',str(sigma_2)]))

plt.subplot(339)
plt.plot(MTF(gauss_2),label='MTF')
plt.plot(np.ones(N)*MTF(gauss_2)[len(edge)/2])
plt.ylim(-0.1,1.1)
plt.xlim(0,len(edge)/2)
plt.title(' '.join(['MTF @ Nyquist=',str(np.round(MTF(gauss_2)[len(edge)/2],3)*100),'%']))

plt.show()
