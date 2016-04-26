# -*- coding: utf-8 -*-

"""
Calculate the modulation transfer function of a random image.
Testing the idea described in Daniels1995, http://dx.doi.org/10.1117/12.190433
"""

from scipy import ndimage
import numpy
import matplotlib.pyplot as plt


def MTF(ImageBeforeTransformation, ImageAfterTransformation):
    # calculate power spectral density of both images, according to Daniels1995
    PSD_A = numpy.abs(numpy.fft.fft2(ImageBeforeTransformation)) ** 2
    PSD_A = numpy.mean(PSD_A, axis=0)
    PSD_B = numpy.abs(numpy.fft.fft2(ImageAfterTransformation)) ** 2
    PSD_B = numpy.mean(PSD_B, axis=0)
    ImgWidth = ImageBeforeTransformation.shape[1]
    aemmteeaeff = numpy.sqrt(PSD_B / PSD_A)[:ImgWidth / 2]
    return aemmteeaeff

length = 1116
RandomImage = numpy.random.randint(2, size=[length, length]) * (2 ** 16)
# Get rid of DC component
RandomImage -= numpy.mean(RandomImage)
RandomImageGauss = ndimage.gaussian_filter(RandomImage, 0.8)

# PSD according to Daniels1995
PSDImage = numpy.abs(numpy.fft.fft2(RandomImage)) ** 2
PSD = numpy.mean(PSDImage, axis=0)

PSDImageGauss = numpy.abs(numpy.fft.fft2(RandomImageGauss)) ** 2
PSDGauss = numpy.mean(PSDImageGauss, axis=0)

plt.subplot(231)
plt.imshow(RandomImage, interpolation='none', cmap='gray')
plt.title('Random image')
plt.subplot(232)
plt.imshow(numpy.fft.fftshift(PSDImage), interpolation='none', cmap='gray')
plt.title('2D FFT')

plt.subplot(234)
plt.imshow(RandomImageGauss, interpolation='none', cmap='gray')
plt.subplot(235)
plt.imshow(numpy.fft.fftshift(PSDImageGauss), interpolation='none',
           cmap='gray')


plt.subplot(133)
plt.plot(PSD, label='PSD')
plt.plot(PSDGauss, label='PSD gauss')
plt.xlim([0, length])
plt.legend(loc='best')
plt.title('PSD')

plt.figure()
plt.plot(MTF(RandomImage, RandomImageGauss))
plt.ylim([0, 1])
plt.title('MTF')

plt.show()
