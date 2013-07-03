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


def polynomialfit(data,order):
    '''
    calculate the polynomial fit of an input for a defined degree
    '''
    x, y = range(len(data)), data
    coefficients = np.polyfit(x, y, order)
    return np.polyval(coefficients, x)


# Generate edge for N points
N = 500
dirac = np.zeros(N)
dirac[:N / 2] = 1

# Filter edge
sigma_1 = 0.5
gauss_1 = scipy.ndimage.gaussian_filter(dirac, sigma=sigma_1)
sigma_2 = 0.75
gauss_2 = scipy.ndimage.gaussian_filter(dirac, sigma=sigma_2)

Total = 55
SaveFigure = True
for iteration in range(Total):
    print 'Plotting', iteration, 'of', Total
    noise_sigma = 0.001
    gauss_1_noise = gauss_1 + noise_sigma * randn(len(gauss_2))
    gauss_2_noise = gauss_2 + noise_sigma * randn(len(gauss_2))

    '''
    Save the plots in a dictionary, so we can iterate through it afterwards. See
    http://stackoverflow.com/a/2553532/323100 and
    http://docs.python.org/2/tutorial/datastructures.html#looping-techniques for
    reference how it's done.
    '''
    plots = dict((name, eval(name)) for name in ['dirac', 'gauss_1', 'gauss_2',
                                                 'gauss_1_noise', 'gauss_2_noise'])

    plt.figure(figsize=(16, 16))
    counter = 0
    ShowRegion = 50
    for name, data in sorted(plots.iteritems()):
        counter += 1
        plt.subplot(4, len(plots), counter)
        plt.plot(data)
        plt.ylim(-0.1, 1.1)
        plt.xlim(len(dirac)/2-ShowRegion/2, len(dirac)/2+ShowRegion/2)
        plt.title(name)

        plt.subplot(4, len(plots), counter+len(plots))
        plt.plot(LSF(data))
        plt.title('LSF')
        plt.ylim(-0.1, 1.1)

        plt.subplot(4, len(plots), counter+2*len(plots))
        plt.plot(MTF(data))
        plt.plot(np.ones(N)*MTF(data)[len(dirac)/2])
        plt.ylim(-0.1, 1.1)
        plt.xlim(0, len(dirac)/2)
        plt.title(' '.join(['MTF @ Nyquist=', str(np.round(MTF(data)[len(dirac)/2],
                                                           3)*100), '%']))

        plt.subplot(4, len(plots), counter+3*len(plots))
        #~ plt.plot(MTF(data),label='orig')
        for degree in range(4,10):
            plt.plot(polynomialfit(MTF(data),degree),label=str(degree))
        #~ plt.legend()
        plt.ylim(-0.1, 1.1)        
        plt.title('Polynomial fit with degree ' + str(degree))

    if SaveFigure:
        plt.savefig('MTF_' + str(int(time.time()*10)) + '.png')
    else:
        plt.show()
