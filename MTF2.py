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


def rgb2gray(rgb):
    '''
    convert an image from rgb to grayscale
    http://stackoverflow.com/a/12201744/323100
    '''
    return numpy.dot(rgb[..., :3], [0.299, 0.587, 0.144])


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
    '''
    FFTImg = numpy.fft.fft2(InputImage)
    FFTShift = numpy.fft.fftshift(FFTImg)
    return numpy.abs(FFTShift) ** Exponent


def averagerows(Image):
    '''
    Average over the rows of the '''
    Average = []
    # Average rows and collapse them into an averaged column
    for row in range(Image.shape[0]):
        Average.append(numpy.mean(Image[row, :]))
    return Average


# Generate image with random black/white pixels
PatternSize = 100
if PatternSize < 11:
    PatternSize = 11
    print 'We cannot work with a length of images smaller than 11. Thus', \
        'setting it to that...'
if PatternSize % 2 ==0:
    print 'The synthetic images (random/comb) need to have an odd length,', \
        'increasing sidelength of', PatternSize, 'by one'
    PatternSize += 1
    
# Random int(0:1)
ImageRandom = numpy.floor(numpy.random.random((PatternSize, PatternSize)) + .5) * 256
# Get rid of DC-component, i.e. subtract the mean of the image
# Random 0:1
#~ ImageRandom = (numpy.random.random((PatternSize, PatternSize)) *
               #~ 256).astype('uint8')
scipy.misc.imsave('MTF_random.png', ImageRandom)

# Generate image with comb structure
# Make empty image
ImageComb = numpy.zeros([PatternSize, PatternSize])
# Go through all the colums, and set them to one so that we have a 10-comb
# structure at the end
for i in range(PatternSize):
    if numpy.floor(i / (PatternSize / 10.0)) % 2:
        ImageComb[:, i] = 256
scipy.misc.imsave('MTF_comb.png', ImageComb)

# Load "real" image
ImageReal = rgb2gray(plt.imread('Dose1.png'))
scipy.misc.imsave('MTF_real.png', ImageComb)

# Set up figure using gridspec (http://matplotlib.org/users/gridspec.html)
gs = gridspec.GridSpec(6, 12)
plt.figure('Images', figsize=(16, 9))

# Show the original images
plt.subplot(gs[0:2,0:2])
plt.title('Original')
plt.imshow(ImageRandom, cmap='gray', interpolation='none')
plt.hlines(PatternSize * 0.618, 0, PatternSize, linewidth=2, color='b', alpha=0.5)
plt.subplot(gs[2:4,0:2])
plt.imshow(ImageComb, cmap='gray', interpolation='none')
plt.hlines(PatternSize * 0.618, 0, PatternSize, linewidth=2, color='b', alpha=0.5)
plt.subplot(gs[4:6,0:2])
plt.imshow(ImageReal, cmap='gray', interpolation='none')
plt.hlines(ImageReal.shape[0] * 0.618, 0, ImageReal.shape[1], linewidth=2, color='b', alpha=0.5)

# Show them gaussfiltered
plt.subplot(gs[0:2,2:4])
plt.title('Gaussfiltered\nsigma=0.8')
plt.imshow(gaussfilter(ImageRandom), cmap='gray', interpolation='none')
plt.hlines(PatternSize * 0.618, 0, PatternSize, linewidth=2, color='r', alpha=0.5)
plt.subplot(gs[2:4,2:4])
plt.imshow(gaussfilter(ImageComb), cmap='gray', interpolation='none')
plt.hlines(PatternSize * 0.618, 0, PatternSize, linewidth=2, color='r', alpha=0.5)
plt.subplot(gs[4:6,2:4])
plt.imshow(gaussfilter(ImageReal), cmap='gray', interpolation='none')
plt.hlines(ImageReal.shape[0] * 0.618, 0, ImageReal.shape[1], linewidth=2, color='r', alpha=0.5)

HistogramBins = PatternSize / 10
# Show the line-plots and histograms
plt.subplot(gs[0,4:6])
plt.title('Lineplot & Histograms')
plt.plot(ImageRandom[PatternSize * 0.618, :], 'b', label='Original')
plt.plot(gaussfilter(ImageRandom)[PatternSize * 0.618, :], 'r', label='Original')
plt.xlim([0, PatternSize])
plt.subplot(gs[1,4])
plt.hist(ImageRandom.flatten(), HistogramBins)
plt.subplot(gs[1,5])
plt.hist(gaussfilter(ImageRandom).flatten(), HistogramBins)

plt.subplot(gs[2,4:6])
plt.plot(ImageComb[PatternSize * 0.618, :], 'b', label='Original')
plt.plot(gaussfilter(ImageComb)[PatternSize * 0.618, :], 'r', label='Original')
plt.xlim([0, PatternSize])
plt.subplot(gs[3,4])
plt.hist(ImageComb.flatten(), HistogramBins)
plt.subplot(gs[3,5])
plt.hist(gaussfilter(ImageComb).flatten(), HistogramBins)

plt.subplot(gs[4,4:6])
plt.plot(ImageReal[ImageReal.shape[0] * 0.618, :], 'b', label='Original')
plt.plot(gaussfilter(ImageReal)[ImageReal.shape[0] * 0.618, :], 'r',
    label='Original')
plt.xlim([0, ImageReal.shape[1]])
plt.subplot(gs[5,4])
plt.hist(ImageReal.flatten(), HistogramBins)
#~ plt.gca().yaxis.set_ticks([])
plt.subplot(gs[5,5])
plt.hist(gaussfilter(ImageReal).flatten(), HistogramBins)
#~ plt.gca().yaxis.set_ticks([])

# Show the 2D FFT of the original image
plt.subplot(gs[0:2,6:8])
plt.title('2D FFT')
plt.imshow(psd(ImageRandom), cmap='gray', interpolation='none')
plt.hlines(PatternSize/2, PatternSize/2, PatternSize, linewidth=2, color='y', alpha=0.5)
plt.vlines(PatternSize/2, PatternSize/2, PatternSize, linewidth=2, color='g', alpha=0.5)
plt.subplot(gs[2:4,6:8])
plt.imshow(psd(ImageComb), cmap='gray', interpolation='none')
plt.hlines(PatternSize/2, PatternSize/2, PatternSize, linewidth=2, color='y', alpha=0.5)
plt.vlines(PatternSize/2, PatternSize/2, PatternSize, linewidth=2, color='g', alpha=0.5)
plt.subplot(gs[4:6,6:8])
plt.imshow(psd(ImageReal), cmap='gray', interpolation='none')
plt.hlines(ImageReal.shape[0]/2, ImageReal.shape[1]/2, ImageReal.shape[1], linewidth=2, color='y', alpha=0.5)
plt.vlines(ImageReal.shape[1]/2, ImageReal.shape[0]/2, ImageReal.shape[0], linewidth=2, color='g', alpha=0.5)

# Show the 2D FFT of the gauss-filtered image
plt.subplot(gs[0:2,8:10])
plt.title('2D FFT of gauss-\nfiltered image')
plt.imshow(psd(gaussfilter(ImageRandom)), cmap='gray', interpolation='none')
plt.hlines(PatternSize/2, PatternSize/2, PatternSize, linewidth=2, color='c', alpha=0.5)
plt.vlines(PatternSize/2, PatternSize/2, PatternSize, linewidth=2, color='m', alpha=0.5)
plt.subplot(gs[2:4,8:10])
plt.imshow(psd(gaussfilter(ImageComb)), cmap='gray', interpolation='none')
plt.hlines(PatternSize/2, PatternSize/2, PatternSize, linewidth=2, color='c', alpha=0.5)
plt.vlines(PatternSize/2, PatternSize/2, PatternSize, linewidth=2, color='m', alpha=0.5)
plt.subplot(gs[4:6,8:10])
plt.imshow(psd(gaussfilter(ImageReal)), cmap='gray', interpolation='none')
plt.hlines(ImageReal.shape[0]/2, ImageReal.shape[1]/2, ImageReal.shape[1], linewidth=2, color='c', alpha=0.5)
plt.vlines(ImageReal.shape[1]/2, ImageReal.shape[0]/2, ImageReal.shape[0], linewidth=2, color='m', alpha=0.5)

# PSD as plots of average over rows of image 
# See \cite{Daniels1995}: The output image data are then captured by a frame
# grabber and processed to yield the output PSD as the abs(FFT)^2 of the output
# image data, averaged over the rows of the image

plt.subplot(gs[0:2,10:12])
plt.title('MTF')
plt.plot(psd(ImageRandom)[PatternSize/2,PatternSize/2:], linewidth=2, color='y',alpha=0.5)
plt.plot(psd(ImageRandom)[PatternSize/2:PatternSize,PatternSize/2], linewidth=2, color='g',alpha=0.5)
plt.plot(psd(gaussfilter(ImageRandom))[PatternSize/2,PatternSize/2:], linewidth=2, color='c',alpha=0.5)
plt.plot(psd(gaussfilter(ImageRandom))[PatternSize/2:PatternSize,PatternSize/2], linewidth=2, color='m',alpha=0.5)
plt.subplot(gs[2:4,10:12])
plt.plot(psd(ImageComb)[PatternSize/2,PatternSize/2:], linewidth=2, color='y',alpha=0.5)
plt.plot(psd(ImageComb)[PatternSize/2:PatternSize,PatternSize/2], linewidth=2, color='g',alpha=0.5)
plt.plot(psd(gaussfilter(ImageComb))[PatternSize/2,PatternSize/2:], linewidth=2, color='c',alpha=0.5)
plt.plot(psd(gaussfilter(ImageComb))[PatternSize/2:PatternSize,PatternSize/2], linewidth=2, color='m',alpha=0.5)
plt.subplot(gs[4:6,10:12])
plt.plot(psd(ImageReal)[ImageReal.shape[0]/2,ImageReal.shape[0]/2:], linewidth=2, color='y')
plt.plot(psd(ImageReal)[ImageReal.shape[1]/2:ImageReal.shape[1],ImageReal.shape[1]/2], linewidth=2, color='g')
plt.plot(psd(gaussfilter(ImageReal))[ImageReal.shape[0]/2,ImageReal.shape[0]/2:], linewidth=2, color='c')
plt.plot(psd(gaussfilter(ImageReal))[ImageReal.shape[1]/2:ImageReal.shape[1],ImageReal.shape[1]/2], linewidth=2, color='m')

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
