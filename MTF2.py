'''
Script to calculate the Modulation transfer function of a lens-detector system

It's based on the idea that once can use a random pattern to calculate the MTF,
as specified by Daniels et al. in http://dx.doi.org/10.1117/12.190433, which
was found through http://stackoverflow.com/q/18823968
'''

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy
import scipy
from scipy import ndimage
import sys

print "Let's go"


def rgb2gray(rgb):
    '''
    convert an image from rgb to grayscale
    http://stackoverflow.com/a/12201744/323100
    '''
    return numpy.dot(rgb[..., :3], [0.299, 0.587, 0.144])


def gaussfilter(InputImage, sigma=5):
    '''
    Apply gauss filter to input image, with a default sigma of 0.8, or an
    user-supplied sigma
    '''
    return ndimage.gaussian_filter(InputImage, sigma)


def psd(InputImage, Exponent=0.1):
    '''
    According to http://stackoverflow.com/a/15541995 we calculate the FFT,
    shift it so that the low spatial freqencies are in the center. The power
    spectral density is the square of the absolute of the FFT.
    Power spectral density according to MATLAB: http://is.gd/YSUOeG
    "imagesc( log10(abs(fftshift(fft2(Picture))).^2 ))"
    '''
    FFTImg = numpy.fft.fft2(InputImage)
    FFTShift = numpy.fft.fftshift(FFTImg)
    return numpy.abs(FFTShift) ** Exponent

# Generate image with random black/white pixels
PatternSize = 260
# Random int(0:1)
ImageRandom = numpy.floor(numpy.random.random((PatternSize, PatternSize)) + .5)
# Random 0:1
#~ ImageRandom = (numpy.random.random((PatternSize, PatternSize)) *
               #~ 256).astype('uint8')
scipy.misc.imsave('MTF_random.png', ImageRandom)

# Generate image with comb structure
ImageComb = numpy.zeros([PatternSize, PatternSize])
for i in range(PatternSize / 10 / 2):
    ImageComb[:, 20 * i:20 * i + 10] = 1
scipy.misc.imsave('MTF_comb.png', ImageComb)

# Load "real" image
ImageReal = rgb2gray(plt.imread('Dose1.png'))
scipy.misc.imsave('MTF_real.png', ImageComb)

plt.figure('Images', figsize=(10, 10))
# Show the original images
plt.subplot(3, 4, 1)
plt.title('Original')
plt.imshow(ImageRandom, cmap='gray', interpolation='none')
plt.hlines(PatternSize / 2, 0, PatternSize, 'b')
plt.subplot(3, 4, 5)
plt.imshow(ImageComb, cmap='gray', interpolation='none')
plt.hlines(PatternSize / 2, 0, PatternSize, 'b')
plt.subplot(3, 4, 9)
plt.imshow(ImageReal, cmap='gray', interpolation='none')
plt.hlines(ImageReal.shape[0] / 2, 0, ImageReal.shape[1], 'b')

# Show them gaussfiltered
plt.subplot(3, 4, 1 + 1)
plt.title('Gaussfiltered\nsigma=0.8')
plt.imshow(gaussfilter(ImageRandom), cmap='gray', interpolation='none')
plt.hlines(PatternSize / 2, 0, PatternSize, 'r')
plt.subplot(3, 4, 5 + 1)
plt.imshow(gaussfilter(ImageComb), cmap='gray', interpolation='none')
plt.hlines(PatternSize / 2, 0, PatternSize, 'r')
plt.subplot(3, 4, 9 + 1)
plt.imshow(gaussfilter(ImageReal), cmap='gray', interpolation='none')
plt.hlines(ImageReal.shape[0] / 2, 0, ImageReal.shape[1], 'r')

HistogramBins = 10
# Show the line-plots and histograms
plt.subplot(6, 4, 1 + 2)
plt.title('Lineplot & Histograms')
plt.plot(ImageRandom[PatternSize / 2, :], 'b', label='Original')
plt.plot(gaussfilter(ImageRandom)[PatternSize / 2, :], 'r', label='Original')
plt.xlim([0, PatternSize])
plt.subplot(6, 8, 1 + 12)
plt.hist(ImageRandom.flatten(), HistogramBins)
plt.subplot(6, 8, 1 + 13)
plt.hist(gaussfilter(ImageRandom).flatten(), HistogramBins)

plt.subplot(6, 4, 1 + 10)
plt.plot(ImageRandom[PatternSize / 2, :], 'b', label='Original')
plt.plot(gaussfilter(ImageRandom)[PatternSize / 2, :], 'r', label='Original')
plt.xlim([0, PatternSize])
plt.subplot(6, 8, 1 + 28)
plt.hist(ImageComb.flatten(), HistogramBins)
plt.subplot(6, 8, 1 + 29)
plt.hist(gaussfilter(ImageComb).flatten(), HistogramBins)

plt.subplot(6, 4, 1 + 18)
plt.plot(ImageReal[ImageReal.shape[0] / 2, :], 'b', label='Original')
plt.plot(gaussfilter(ImageReal)[ImageReal.shape[0] / 2, :], 'r',
    label='Original')
plt.xlim([0, ImageReal.shape[1]])
plt.subplot(6, 8, 1 + 44)
plt.hist(ImageReal.flatten(), HistogramBins)
plt.subplot(6, 8, 1 + 45)
plt.hist(gaussfilter(ImageReal).flatten(), HistogramBins)

# Show the 2D FFT and/or Power spectral density
plt.subplot(3, 4, 1 + 3)
plt.title('Power spectral density')
plt.imshow(psd(ImageRandom), cmap='gray', interpolation='none')
plt.subplot(3, 4, 5 + 3)
plt.imshow(psd(ImageComb), cmap='gray', interpolation='none')
plt.subplot(3, 4, 9 + 3)
plt.imshow(psd(ImageReal), cmap='gray', interpolation='none')

plt.show()
sys.exit('done')
