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
PatternSize = 5
Image = numpy.floor(numpy.random.random((PatternSize, PatternSize)) + .5)
#~ scipy.misc.imsave('_random.png', Image)
ImageGaussianFiltered = ndimage.gaussian_filter(Image, sigma=5)

# Show Image
fig=plt.figure()
plt.subplot(2,2,1)
plt.imshow(Image, cmap='gray', origin='lower', interpolation='nearest')
plt.title('Random image')
plt.subplot(2,2,2)
plt.imshow(ImageGaussianFiltered, cmap='gray', origin='lower',
           interpolation='nearest')
plt.title('Gaussian filtered')

mu, sigma = 100, 15
x = mu + sigma * numpy.random.randn(10000)
ax = fig.add_subplot(223)

# the histogram of the data
n, bins, patches = ax.hist(x, 50, normed=1, facecolor='green', alpha=0.75)
# add a 'best fit' line for the normal PDF
y = mlab.normpdf(bins, mu, sigma)
l = ax.plot(bins, y, 'r--', linewidth=5)

ax.set_xlabel('Smarts')
ax.set_ylabel('Probability')
#ax.set_title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
ax.set_xlim(40, 160)
ax.set_ylim(0, 0.03)
ax.grid(True)

plt.show()
