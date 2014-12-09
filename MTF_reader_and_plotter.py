'''
Script to calculate the MTF from a real image.

Based on /afs/EssentialMed/Dev/MTF.py
'''

import matplotlib.pylab as plt
import numpy as np
import os

ion()

# SETUP
SelectStartPointManually = False
SelectEdgeManually = False
PolynomialOrder = 5

# Images
ImagePath = '/afs/psi.ch/project/EssentialMed/Images'
ImageDir = '11-MTF'

Camera = 'iPhone'
# Camera = 'tiscam'
# Camera = 'Elphel'

if Camera == 'iPhone':
    # use iPhone images
    ImageFile = 'iPhone_with_xray_film.jpg'
    ImageFile = 'iPhone_with_xray_film_hdr.jpg'
    ImageFile = 'iPhone_with_xray_film_window.jpg'
    ImageFile = 'iPhone_with_xray_film_window_hdr.jpg'
elif Camera == 'tiscam':
    # 'The imaging source' camera images from different objectives
    Objective = 9  # 3,6 or 9
    if Objective == 3:
        ObjectiveDir = 3.6
        ImageFile = 'shot0099.png'  # visually the best one
    elif Objective == 6:
        ObjectiveDir = 6.0
        ImageFile = 'shot0364.png'  # visually the best one
    elif Objective == 9:
        ObjectiveDir = 9.6
        ImageFile = 'shot0072.png'  # visually the best one
    Camera = Camera + '_' + str(ObjectiveDir)
elif Camera == 'Elphel':
    # Elphel images
    ImageFile = 'image.jpg'
else:
    print 'I do not know what to do, exiting'
    exit()


def rgb2gray(rgb):
    '''
    convert an image from rgb to grayscale
    http://stackoverflow.com/a/12201744/323100
    '''
    return np.dot(rgb[..., :3], [0.299, 0.587, 0.144])

ImageToLoad = os.path.join(ImagePath, ImageDir, Camera, ImageFile)

ImageRGB = plt.imread(ImageToLoad)
Image = rgb2gray(ImageRGB)


plt.imshow(np.fft.fft2(Image))
#~ plt.imshow(Image)
ioff()
plt.show()

exit()


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


def polynomialfit(data, order):
    '''
    calculate the polynomial fit of an input for a defined degree
    '''
    x, y = range(len(data)), data
    coefficients = np.polyfit(x, y, order)
    return np.polyval(coefficients, x)

ImageToLoad = os.path.join(ImagePath, ImageDir, Camera, ImageFile)
print 'reading', ImageToLoad

# Read the image and convert it to grayscale rightaway
ImageRGB = plt.imread(ImageToLoad)
Image = rgb2gray(ImageRGB)

ImageWidth = Image.shape[0]
ImageHeight = Image.shape[1]
print 'The image we loaded is', ImageWidth, 'by', ImageHeight, \
    'pixels big. That is', round(ImageWidth * ImageHeight / 1e6, 3), 'MPx.'

plt.subplot(221)
plt.imshow(ImageRGB, origin='lower')
plt.title('Pick point for drawing\n horizontal and vertical profile')
if SelectStartPointManually:
    PickPoint = ginput(1)
else:
    if Camera == 'iPhone':
        PickPoint = [[1500, 1000]]
    elif Camera[:6] == 'tiscam':
        # Select middle of image...
        PickPoint = [[ImageHeight / 2, ImageWidth / 2]]
    elif Camera == 'Elphel':
        PickPoint = [[ImageHeight / 2, ImageWidth / 2]]
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
# plt.xlim(0, ImageHeight)
# plt.ylim(0, 256)
plt.subplot(222)
VerticalProfile = Image[:, Vertigo]
plt.plot(VerticalProfile, range(ImageWidth), 'b')
# plt.xlim(0, 256)
# plt.ylim(0, ImageWidth)
plt.title('Vertical Profile')
plt.draw()

print 'The horizontal profile (red) goes from', min(HorizontalProfile), 'to',\
    max(HorizontalProfile)
print 'The vertical profile (blue) goes from', min(VerticalProfile), 'to',\
    max(VerticalProfile)

# Set range of the region we want to look at to 'Edgerange', about 10% of Image
# width
EdgeRange = int(round(Image.shape[0] * .05 / 10) * 10)

plt.figure(figsize=(16, 9))
plt.subplot(311)
plt.plot(VerticalProfile)
if SelectEdgeManually:
    plt.title('Select approximate middle of knife edge')
    EdgePosition = ginput(1)
    plt.title('Vertical Profile\n(zoom reguion selected manually, width = ' +
              str(EdgeRange) + ' px, approx. 5% of image)')
else:
    EdgePosition = [[LSF(VerticalProfile).argmax(), np.nan]]
    plt.title('Vertical Profile\n(zoom region selected automatically, width ' +
              '= ' + str(EdgeRange) + ' px, approx. 5% of image)')
plt.axvspan(EdgePosition[0][0] - EdgeRange, EdgePosition[0][0] + EdgeRange,
            facecolor='r', alpha=0.5)

plt.subplot(312)
plt.plot(LSF(VerticalProfile))
plt.axvspan(EdgePosition[0][0] - EdgeRange, EdgePosition[0][0] + EdgeRange,
            facecolor='r', alpha=0.5)
plt.title('LSF')

# plt.subplot(413)
# plt.plot(MTF(VerticalProfile))
# plt.title('MTF')

plt.subplot(3, 3, 7)
plt.plot(VerticalProfile)
plt.xlim(EdgePosition[0][0] - EdgeRange, EdgePosition[0][0] + EdgeRange)
plt.title('Zoomed Edge')

plt.subplot(3, 3, 8)
plt.plot(LSF(VerticalProfile))
plt.xlim(EdgePosition[0][0] - EdgeRange, EdgePosition[0][0] + EdgeRange)
plt.title('Zoomed LSF')

plt.subplot(3, 3, 9)
plt.plot(MTF(VerticalProfile), alpha=0.5)
plt.plot(polynomialfit(MTF(VerticalProfile), PolynomialOrder), linewidth=5)
plt.xlim(0, len(MTF(VerticalProfile)) / 2)
plt.title('MTF with polynomial fit of order ' + str(PolynomialOrder) +
          '\nwith a minimum at :' +
          str(round(min(polynomialfit(MTF(VerticalProfile), PolynomialOrder)),
                    3)))

ioff()
plt.show()
