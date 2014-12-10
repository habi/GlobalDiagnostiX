"""
Generate test-image for calculating the MTF
"""
from __future__ import division
import numpy
import scipy
import itertools
import matplotlib.pyplot as plt


def draw_fansegment(startradius, length, angle):
    plt.arrow(Size[1] / 2 + (startradius * numpy.cos(numpy.deg2rad(angle))),
              Size[0] / 2 + (startradius * numpy.sin(numpy.deg2rad(angle))),
              length * numpy.cos(numpy.deg2rad(angle)),
              length * numpy.sin(numpy.deg2rad(angle)))

Size = [768, 1024]
Size = [1024, 1024]

print 'Generating random image with a size of', Size[0], 'x', Size[1], 'px'
# Generate random image
ImageRandom = numpy.random.randint(2, size=Size) * 256
scipy.misc.imsave('Target_random.png', ImageRandom)
print 'Saved random image'
# Write grid onto image
GridSize = 100
for x, y in itertools.izip_longest(range(0, Size[0], GridSize),
                                   range(0, Size[1], GridSize)):
    if x:
        ImageRandom[x, :] = 1
    if y:
        ImageRandom[:, y] = 1

scipy.misc.imsave('Target_random_grid.png', ImageRandom)
print 'Saved random image with grid'

print 'Generating star pattern with a size of', Size[0], 'x', Size[1], 'px'
# Draw star-pattern with defined length


saveDPI = 150
fig = plt.figure(figsize=(Size[1] / saveDPI, Size[0] / saveDPI))
Length = 100
angles = numpy.linspace(0, 360, 3600)
for radius in range(0, max(Size), 2 * Length):
    for angle in angles:
        if round(angle / 10) % 2 == 0:
            draw_fansegment(radius, Length, angle)
            draw_fansegment(radius + Length, Length, angle + 10)
    plt.plot(Size[1] / 2 + radius * numpy.cos(numpy.deg2rad(angles)),
             Size[0] / 2 + radius * numpy.sin(numpy.deg2rad(angles)),
             color='k', linewidth=2)
    plt.plot(Size[1] / 2 + radius / 2 * numpy.cos(numpy.deg2rad(angles)),
             Size[0] / 2 + radius / 2 * numpy.sin(numpy.deg2rad(angles)),
             color='k', linewidth=2)
plt.axis([0, Size[1], 0, Size[0]])
plt.gca().axes.get_xaxis().set_visible(False)
plt.gca().axes.get_yaxis().set_visible(False)
fig.savefig('Target_star.png', dpi=saveDPI)
print 'Saved star pattern'

# Show what we've done
plt.figure('Result', figsize=(16, 9))
plt.subplot(131)
plt.imshow(plt.imread('Target_random.png'), cmap='gray', interpolation='none')
plt.subplot(132)
plt.imshow(plt.imread('Target_random_grid.png'), cmap='gray',
           interpolation='none')
plt.subplot(133)
plt.imshow(plt.imread('Target_star.png'), cmap='gray', interpolation='none')
plt.show()
