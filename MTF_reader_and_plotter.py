'''
Script to calculate the MTF from a real image.

Based on /afs/EssentialMed/Dev/MTF.py
'''
from pylab import *
import numpy as np
import scipy
import os

ion()

# SETUP
SelectStartPointManually = False
SelectEdgeManually = False
EdgeRange = 100

# Images
ImagePath = '/afs/psi.ch/project/EssentialMed/Images'
ImageDir = '11-MTF'
#~ ImageFile = 'iPhone_with_xray_film.jpg'
#~ ImageFile = 'iPhone_with_xray_film_hdr.jpg'
#~ ImageFile = 'iPhone_with_xray_film_window.jpg'
ImageFile = 'iPhone_with_xray_film_window_hdr.jpg'


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


def rgb2gray(rgb):
    '''
    convert an image from rgb to grayscale
    http://stackoverflow.com/a/12201744/323100
    '''
    return np.dot(rgb[..., :3], [0.299, 0.587, 0.144])


def polynomialfit(data, order):
    '''
    calculate the polynomial fit of an input for a defined degree
    '''
    x, y = range(len(data)), data
    coefficients = np.polyfit(x, y, order)
    return np.polyval(coefficients, x)

ImageToLoad = os.path.join(ImagePath, ImageDir, ImageFile)

# Read the image and convert it to grayscale rightaway
ImageRGB = plt.imread(ImageToLoad)
Image = rgb2gray(ImageRGB)

ImageWidth = Image.shape[0]
ImageHeight = Image.shape[1]
print 'The image we loaded is', ImageWidth, 'by', ImageHeight, \
    'pixels big. That is', round(ImageWidth * ImageHeight/1e6, 3), 'MPx.'

plt.subplot(221)
plt.imshow(ImageRGB, origin='lower')
plt.title('Pick point for drawing\n horizontal and vertical profile')
if SelectStartPointManually:
    PickPoint = ginput(1)
else:
    PickPoint = [[1500, 1000]]
plt.title('Original image')
Horizon = int(PickPoint[0][1])
Vertigo = int(PickPoint[0][0])
if SelectStartPointManually:
    print 'You selected horizontal line', Horizon, 'and vertical line', Vertigo
else:
    print 'I selected horizontal line', Horizon, 'and vertical line', Vertigo
plt.hlines(Horizon, 0, ImageHeight, 'r')
plt.vlines(Vertigo, 0, ImageWidth, 'b')
plt.draw()
plt.subplot(223)
HorizontalProfile = Image[Horizon, :]
plt.plot(HorizontalProfile, 'r')
plt.title('Horizontal Profile')
#~ plt.xlim(0, ImageHeight)
#~ plt.ylim(0, 256)
plt.subplot(222)
VerticalProfile = Image[:, Vertigo]
plt.plot(VerticalProfile, range(ImageWidth), 'b')
#~ plt.xlim(0, 256)
#~ plt.ylim(0, ImageWidth)
plt.title('Vertical Profile')
plt.draw()

print 'The horizontal profile (red) goes from', min(HorizontalProfile), 'to',\
    max(HorizontalProfile)
print 'The vertical profile (blue) goes from', min(VerticalProfile), 'to',\
    max(VerticalProfile)

plt.figure(figsize=(16, 9))
plt.subplot(311)
plt.plot(VerticalProfile)
if SelectEdgeManually:
    plt.title('Select approximate middle of knife edge')
    EdgePosition = ginput(1)
    plt.title('Vertical Profile')
else:
    EdgePosition = [[LSF(VerticalProfile).argmax(), np.nan]]
    plt.title('Vertical Profile\n(selected automatically)')
plt.axvspan(EdgePosition[0][0]-EdgeRange, EdgePosition[0][0]+EdgeRange,
            facecolor='r', alpha=0.5)

plt.subplot(312)
plt.plot(LSF(VerticalProfile))
plt.axvspan(EdgePosition[0][0]-EdgeRange, EdgePosition[0][0]+EdgeRange,
            facecolor='r', alpha=0.5)
plt.title('LSF')

#~ plt.subplot(413)
#~ plt.plot(MTF(VerticalProfile))
#~ plt.title('MTF')

plt.subplot(3, 3, 7)
plt.plot(VerticalProfile)
plt.xlim(EdgePosition[0][0]-EdgeRange, EdgePosition[0][0]+EdgeRange)
plt.title('Zoomed Edge')

plt.subplot(3, 3, 8)
plt.plot(LSF(VerticalProfile))
plt.xlim(EdgePosition[0][0]-EdgeRange, EdgePosition[0][0]+EdgeRange)
plt.title('Zoomed LSF')

plt.subplot(3, 3, 9)
plt.plot(MTF(VerticalProfile), alpha=0.5)
order = 20
plt.plot(polynomialfit(MTF(VerticalProfile), order), linewidth=5)
plt.xlim(0, len(MTF(VerticalProfile))/2)
plt.title('MTF with polyfit of order' + str(order))

ioff()
plt.show()
