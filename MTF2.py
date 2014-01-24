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

print "Let's go"

# http://stackoverflow.com/a/12201744

# Generate random image
PatternSize = 256
#~ Image = numpy.floor(numpy.random.random((PatternSize, PatternSize)) + .5)
#~ Image = (numpy.random.random((PatternSize, PatternSize)) * 256).astype('uint8')
Image = plt.imread('Dose1.png')[:,:,2]
#~ scipy.misc.imsave('_random.png', Image)
ImageGaussianFiltered = ndimage.gaussian_filter(Image, sigma=1)

# Power spectral density according to MATLAB: http://is.gd/YSUOeG
# imagesc( log10(abs(fftshift(fft2(Picture))).^2 ))

# According to http://stackoverflow.com/a/15541995 we calculate the FFT, shift
# it so that the low spatial freqencies are in the center. The power spectral
# density is the square of the absolute of the FFT
ImagePSD = numpy.abs(numpy.fft.fftshift(numpy.fft.fft2(Image))) ** 2
ImageGaussPSD = numpy.abs(numpy.fft.fftshift(numpy.fft.fft2(ImageGaussianFiltered))) ** 2

# Show Image
plt.subplot(3, 2, 1)
plt.imshow(Image, cmap='gray', interpolation='nearest')
plt.title('Random image')
plt.grid(True, ls="-", color='r')

plt.subplot(3, 2, 2)
plt.imshow(ImageGaussianFiltered, cmap='gray', interpolation='nearest')
plt.title('Gaussian filtered')

# Plot the histogram of the images, with PatternSize bins
plt.subplot(3, 2, 3)
histogram = plt.hist(Image.flatten(),PatternSize)
plt.title('Histogram of\nRandom image')
plt.xlim([0,256])

plt.subplot(3, 2, 4)
plt.hist(ImageGaussianFiltered.flatten(),PatternSize)
plt.title('Histogram of\nGaussian filtered image')
plt.xlim([0,256])

# Power spectral density
plt.subplot(3, 3, 7)
plt.imshow(ImagePSD, cmap='gray', interpolation='nearest')
plt.title('PSD of image')

plt.subplot(3, 3, 8)
plt.imshow(ImagePSD - ImageGaussPSD, cmap='gray', interpolation='nearest')
plt.title('PSD difference')

plt.subplot(3, 3, 9)
plt.imshow(ImageGaussPSD, cmap='gray', interpolation='nearest')
plt.title('PSD of gaussian filtered image')

plt.show()
sys.exit('done')



# add a 'best fit' line for the normal PDF
#~ y = mlab.normpdf(bins, mu, sigma)
#~ plt.plot(bins, y, 'r--', linewidth=5)
plt.grid(True)

plt.xlabel('Smarts')
plt.ylabel('Probability')
#ax.set_title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')

#~ ax.grid(True)

plt.show()
