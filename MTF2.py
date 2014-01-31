'''
Script to calculate the Modulation transfer function of a lens-detector system

It's based on the idea that once can use a random pattern to calculate the MTF,
as specified by Daniels et al. in http://dx.doi.org/10.1117/12.190433, which
was found through http://stackoverflow.com/q/18823968
'''

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy
import scipy
from scipy import ndimage
import sys

print "Let's go"

# Setup
# Image size for the random and comb-pattern
PatternSize = [111, 333]

# 6 colors according to http://tools.medialab.sciences-po.fr/iwanthue/
Hues = ["#C56447", "#A2C747", "#AB5CB2", "#96A8BF", "#543E3F", "#80B17D"]
Hues = ['r', 'g', 'b', 'c', 'm', 'y']


def rgb2gray(rgb):
    '''
    convert an image from rgb to grayscale
    http://stackoverflow.com/a/12201744/323100
    '''
    return numpy.dot(rgb[..., :3], [0.299, 0.587, 0.144])


def padImage(InputImage, width=5, paditwith=256):
    '''
    Pad the input image with 'width' voxels of white (default), to minimize
    edge-effects
    '''
    InputImage[:width, :] = paditwith
    InputImage[-width:, :] = paditwith
    InputImage[:, :width] = paditwith
    InputImage[:, -width:] = paditwith
    return InputImage


def gaussfilter(InputImage, sigma=0.8):
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
    According to Peter it's good if we first get rid of the DC-component of the
    image, which means to delete the mean of the image from itself
    '''
    #~ InputImage -= numpy.mean(InputImage)
    FFTImg = numpy.fft.fft2(InputImage)
    FFTShift = numpy.fft.fftshift(FFTImg)
    return numpy.abs(FFTShift) ** Exponent


def showImage(InputImage, height=0.618, color=Hues[0]):
    '''
    Display the image given as input in gray-scale, plot a 'color' line on
    it at a given 'height'
    '''
    plt.imshow(InputImage, cmap='gray', interpolation='none')
    plt.hlines(InputImage.shape[0] * height, 0, InputImage.shape[1],
               linewidth=5, color=color, alpha=0.5)


def showFFT(InputImage, colorh=Hues[2], colorv=Hues[3]):
    '''
    Show the FFT of the image and overlay a horizontal and vertical line from
    the middle of the image to the border (with colors 'colorh' and 'colorv'
    '''
    plt.imshow(psd(InputImage), cmap='gray', interpolation='none')
    plt.hlines(InputImage.shape[0] / 2, InputImage.shape[1] / 2,
               InputImage.shape[1], linewidth=5, color=colorh, alpha=0.5)
    plt.vlines(InputImage.shape[1] / 2, InputImage.shape[0] / 2,
               InputImage.shape[0], linewidth=5, color=colorv, alpha=0.5)


def plotFFT(InputImage, colorh=Hues[2], colorv=Hues[3], colorgaussh=Hues[4],
            colorgaussv=Hues[5]):
    '''
    Plot first the horizontal line from the middle of the image (shape[1] / 2)
    to the border (shape[1]:) at half the vertical height (shape[0]/2). Then
    plot the vertical line from the middle of the image (shape[0]/2) to the
    border (shape[0]/2:) in the middle of the horizontal length (shape[1] / 2))
    '''
    plt.plot(psd(InputImage)[InputImage.shape[0] / 2,
                             InputImage.shape[1] / 2:], linestyle='-',
             linewidth=5, color=colorh, alpha=0.5)
    plt.plot(psd(gaussfilter(InputImage))[InputImage.shape[0] / 2,
                                          InputImage.shape[1] / 2:],
             linestyle='-', linewidth=5, color=colorgaussh, alpha=0.5)
    plt.plot(psd(InputImage)[InputImage.shape[0] / 2:,
                             InputImage.shape[1] / 2], linestyle='-',
             linewidth=5, color=colorv, alpha=0.5)
    plt.plot(psd(gaussfilter(InputImage))[InputImage.shape[0] / 2:,
                                          InputImage.shape[1] / 2],
             linestyle='-', linewidth=5, color=colorgaussv, alpha=0.5)

if PatternSize[0] < 11:
    PatternSize[0] = 11
    print 'We cannot work with a length of images smaller than 11. Thus', \
        'setting it to that...'
if PatternSize[0] % 2 == 0:
    print 'The synthetic images (random/comb) need to have an odd width,', \
        'increasing', PatternSize[0], 'to',
    PatternSize[0] += 1
    print PatternSize[0]
if PatternSize[1] % 2 == 0:
    print 'The synthetic images (random/comb) need to have an odd width,', \
        'increasing', PatternSize[1], 'to',
    PatternSize[1] += 1
    print PatternSize[1]

# Generate random image
#~ ImageRandom = numpy.floor(numpy.random.random(PatternSize) + .5) * 256
ImageRandom = numpy.random.randint(2, size=PatternSize) * 256
ImageRandom = padImage(ImageRandom)
scipy.misc.imsave('MTF_random.png', ImageRandom)

# Generate image with comb structure
# Make empty image
ImageComb = numpy.zeros(PatternSize)
# Go through all the colums, and set them to one so that we have 10 line-pairs
for i in range(PatternSize[1]):
    if numpy.floor(i / (PatternSize[1] / 20)) % 2:
        ImageComb[:, i] = 256
ImageComb = padImage(ImageComb)
scipy.misc.imsave('MTF_comb.png', ImageComb)

# Generate image with knife edge
# Make empty image
ImageEdge = numpy.zeros(PatternSize)
ImageEdge[:, PatternSize[0] / 2:] = 256
ImageEdge = padImage(ImageEdge)
scipy.misc.imsave('MTF_edge.png', ImageEdge)

# Load "real" image and reverse it instantly, so we don't have to use
# origin=lower all over the place :)
ImageReal = rgb2gray(plt.imread('aptina_test.jpg')[::-1])
#~ ImageReal = padImage(ImageReal,5,-1)
scipy.misc.imsave('MTF_real.png', ImageComb)

# Set up figure using gridspec (http://matplotlib.org/users/gridspec.html)
gs = gridspec.GridSpec(8, 12)
plt.figure('Images', figsize=(16, 9))

# Show the original images
plt.subplot(gs[0:2, 0:2])
plt.title('Original')
showImage(ImageRandom)
plt.subplot(gs[2:4, 0:2])
showImage(ImageComb)
plt.subplot(gs[4:6, 0:2])
showImage(ImageEdge)
plt.subplot(gs[6:8, 0:2])
showImage(ImageReal)

#~ # Show them gaussfiltered
plt.subplot(gs[0:2, 2:4])
plt.title('Gaussfiltered\nsigma=0.8')
showImage(gaussfilter(ImageRandom), color=Hues[1])
plt.subplot(gs[2:4, 2:4])
showImage(gaussfilter(ImageComb), color=Hues[1])
plt.subplot(gs[4:6, 2:4])
showImage(gaussfilter(ImageEdge), color=Hues[1])
plt.subplot(gs[6:8, 2:4])
showImage(gaussfilter(ImageReal), color=Hues[1])

HistogramBins = PatternSize[1] / 10
# Show the line-plots and histograms
plt.subplot(gs[0, 4:6])
plt.title('Lineplot & Histograms')
plt.plot(ImageRandom[PatternSize[0] * 0.618, :], color=Hues[0])
plt.plot(gaussfilter(ImageRandom)[PatternSize[0] * 0.618, :], color=Hues[1])
plt.xlim([0, PatternSize[1]])
plt.subplot(gs[1, 4])
plt.hist(ImageRandom.flatten(), HistogramBins)
plt.subplot(gs[1, 5])
plt.hist(gaussfilter(ImageRandom).flatten(), HistogramBins)
plt.subplot(gs[2, 4:6])
plt.plot(ImageComb[PatternSize[0] * 0.618, :], color=Hues[0])
plt.plot(gaussfilter(ImageComb)[PatternSize[0] * 0.618, :], color=Hues[1])
plt.xlim([0, PatternSize[1]])
plt.subplot(gs[3, 4])
plt.hist(ImageComb.flatten(), HistogramBins)
plt.subplot(gs[3, 5])
plt.hist(gaussfilter(ImageComb).flatten(), HistogramBins)
plt.subplot(gs[4, 4:6])
plt.plot(ImageEdge[ImageEdge.shape[0] * 0.618, :], color=Hues[0])
plt.plot(gaussfilter(ImageEdge)[ImageEdge.shape[0] * 0.618, :], color=Hues[1])
plt.xlim([0, ImageEdge.shape[1]])
plt.subplot(gs[5, 4])
plt.hist(ImageEdge.flatten(), HistogramBins)
plt.subplot(gs[5, 5])
plt.hist(gaussfilter(ImageEdge.flatten()), HistogramBins)
plt.subplot(gs[6, 4:6])
plt.plot(ImageRandom[PatternSize[0] * 0.618, :], color=Hues[0])
plt.plot(gaussfilter(ImageRandom)[PatternSize[0] * 0.618, :], color=Hues[1])
plt.xlim([0, PatternSize[1]])
plt.subplot(gs[7, 4])
plt.hist(ImageRandom.flatten(), HistogramBins)
plt.subplot(gs[7, 5])
plt.hist(gaussfilter(ImageRandom).flatten(), HistogramBins)

# Show the 2D FFT of the original image
plt.subplot(gs[0:2, 6:8])
plt.title('2D FFT')
showFFT(ImageRandom)
plt.subplot(gs[2:4, 6:8])
showFFT(ImageComb)
plt.subplot(gs[4:6, 6:8])
showFFT(ImageEdge)
plt.subplot(gs[6:8, 6:8])
showFFT(ImageReal)

# Show the 2D FFT of the gauss-filtered image
plt.subplot(gs[0:2, 8:10])
plt.title('2D FFT of gauss-\nfiltered image')
showFFT(gaussfilter(ImageRandom), colorh=Hues[4], colorv=Hues[5])
plt.subplot(gs[2:4, 8:10])
showFFT(gaussfilter(ImageComb), colorh=Hues[4], colorv=Hues[5])
plt.subplot(gs[4:6, 8:10])
showFFT(gaussfilter(ImageEdge), colorh=Hues[4], colorv=Hues[5])
plt.subplot(gs[6:8, 8:10])
showFFT(gaussfilter(ImageReal), colorh=Hues[4], colorv=Hues[5])

# Show the horizontal and vertical plot from the middle of the 2D FFT. From
# this we can assess the MTF
plt.subplot(gs[0:2, 10:12])
plt.title('MTF')
plotFFT(ImageRandom)
plt.subplot(gs[2:4, 10:12])
plotFFT(ImageComb)
plt.subplot(gs[4:6, 10:12])
plotFFT(ImageEdge)
plt.subplot(gs[6:8, 10:12])
plotFFT(ImageReal)

plt.show()
sys.exit('done')

"""
"Notes" after discussing it with Peter M.:
- Idea with random noise image is nice (from Daniels1995)
- To be able to compare cameras, we need to take magnification and physical
  pixel size into account, hence we *need* a scale-bar in the images, to be
  able to calculate that.
- We should take lots of images, i.e. 10 photos from 10 different random images
  and then calculate the standard deviation of the noise in the fourier space
  (1) and the mean of the 100 MTFs (2). This should make it possible to
  calculate not only the optical properties (2), but also get out the noise
  properties of the electrical system (1) (smaller STDEV = better).
"""
