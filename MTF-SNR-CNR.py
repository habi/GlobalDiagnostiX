# -*- coding: utf-8 -*-

"""
Script to calculate MTF, SNR, CNR, etc.
Uses an input image, user selects region, script calculates.
"""

import sys
import os
from optparse import OptionParser
import matplotlib.pylab as plt
import scipy

# clear the commandline
os.system('clear')

# setup interactive plotting
plt.ion()

# Use Pythons Optionparser to define and read the options, and also
# give some help to the user
parser = OptionParser()
usage = "usage: %prog [options] arg"
parser.add_option('-f', '--Filename', dest='Filename',
                  help='Imagefile to open', metavar='path/somefile.jpg')
parser.add_option('-m', '--MTF', dest='MTF', default=False,
                  action='store_true',
                  help='Calculate Modulation transfer function')
parser.add_option('-s', '--SNR', dest='SNR', default=True,
                  action='store_true', help='Calculate Signal-to-noise ratio')
parser.add_option('-c', '--CNR', dest='CNR', default=False,
                  action='store_true',
                  help='Calculate Contrast-to-noise ratio')
parser.add_option('-r', '--roi', dest='ROI',
                  help='ROI to calculate the SNR from '
                       '[Upperleft X,Y,Lowerright X,Y]. If no ROI is given, '
                       'the user has to define a ROI on the image.',
                  metavar='10,100,400,550')
parser.add_option('-t', '--test', dest='Test', default=False,
                  action='store_true', help='Only do a test-run', metavar=1)

(options, args) = parser.parse_args()

print
print 'Temporarily setting filename'
options.Filename = '/afs/psi.ch/project/EssentialMed/Images/' \
                   '06-Elphel-800erScreen/1347623915.00_200ms.jpg'

# print
# print 'Temporarily setting ROI'
# options.ROI = '1946,108,2358,728'

# Show the help if no parameters are given. Or actually if no filename.
if options.Filename is None:
    parser.print_help()
    print 'Example:'
    print ' '.join(sys.argv)
    sys.exit(1)

# Read File
print 'Reading', options.Filename
try:
    Image = plt.imread(options.Filename)
    Image = sum(Image, axis=2)  # sum RGB channels, i.e. convert to grayscale
    # Flip the image upsidedown, since Matplotlib has the origin at a different
    # place. If not, we'd have to use "origin='lower'" in every imshow and
    # calculate too much with all the coordinates...
    Image = flipud(Image)
except:
    print 'I was not able to read the file, did you specify the correct ' \
          'path with "-f"?'
    exit(1)
print 'The image', os.path.basename(options.Filename), 'is', Image.shape[1],\
    'x', Image.shape[0], 'pixels big.'


# Do ROI if desired
plt.figure(1)
plt.imshow(Image, cmap=cm.gray, interpolation='nearest')
plt.title('Original')
if options.ROI:
    # make the ROI-Coordinates into a double tuple, so we can use less code
    # afterwards
    options.ROI = ((int(options.ROI.split(',')[0]),
                    int(options.ROI.split(',')[1])),
                   (int(options.ROI.split(',')[2]),
                    int(options.ROI.split(',')[3])))
else:
    plt.title('Please select two corners of the ROI. Top left, bottom right')
    options.ROI = ginput(2)
    # swap ROI coordinates if necessary (if user clicked right/left instead of
    # left/right)
    if options.ROI[0][0] > options.ROI[1][0]:
        plt.title('Select top left, then bottom right!')
        options.ROI = ginput(2)
        if options.ROI[0][0] > options.ROI[1][0]:
            plt.title('TOP LEFT, BOTTOM RIGHT!')
            options.ROI = ginput(2)

if options.ROI[0][0] > 0:
    plt.subplot(211)
    plt.imshow(Image, cmap=cm.gray, interpolation='nearest')
    plt.title('Original')
    plt.hlines(options.ROI[0][1], options.ROI[0][0], options.ROI[1][0], 'r',
               linewidth=3)
    plt.hlines(options.ROI[1][1], options.ROI[0][0], options.ROI[1][0], 'r',
               linewidth=3)
    plt.vlines(options.ROI[0][0], options.ROI[0][1], options.ROI[1][1], 'r',
               linewidth=3)
    plt.vlines(options.ROI[1][0], options.ROI[0][1], options.ROI[1][1], 'r',
               linewidth=3)
    Image = Image[options.ROI[0][1]:options.ROI[1][1],
            options.ROI[0][0]:options.ROI[1][0]]
    plt.subplot(212)
    plt.imshow(Image, cmap=cm.gray, interpolation='nearest')
    plt.title('ROI: ' +
              str(int(np.round(options.ROI[0][0]))) + ':' +
              str(int(np.round(options.ROI[0][1]))) + ' to ' +
              str(int(np.round(options.ROI[1][0]))) + ':' +
              str(int(np.round(options.ROI[1][1]))))
plt.draw()

# Plot horizontal line
SmoothingStep = 50
plt.figure(2)
plt.imshow(Image, cmap=cm.gray, interpolation='nearest')
plt.title('Select line to plot')
HorizontalLine = int(round(ginput(1)[0][1]))
plt.hlines(HorizontalLine, 0, Image.shape[1], 'r', linewidth=3)

plt.subplot(211)
plt.imshow(Image, cmap=cm.gray, interpolation='nearest')
plt.hlines(HorizontalLine, 0, Image.shape[1], 'r', linewidth=3)
plt.title('Original')
plt.subplot(212)
plt.plot(Image[HorizontalLine, :], label='Line ' + str(HorizontalLine))
window = np.blackman(SmoothingStep)
smoothed = np.convolve(window / window.sum(), Image[HorizontalLine, :],
                       mode='same')
plt.plot(range(SmoothingStep, len(smoothed) - SmoothingStep),
         smoothed[SmoothingStep:-SmoothingStep], 'r--', linewidth=5,
         label='smoothed (by ' + str(SmoothingStep) + ')')
plt.xlim((0, Image.shape[1]))
plt.legend(loc='best')
plt.draw()

if options.MTF:
    print 'calculating MTF of', os.path.basename(options.Filename)
    # http://is.gd/V3XClS
    # Modulation (contrast) = (Imax - Imin) / (Imax + Imin)

if options.SNR:
    print 'calculating SNR of', os.path.basename(options.Filename)
    # http://is.gd/5CMtiI
    # SNR = Psignal / Pnoise = (Asignal / Anoise)^2

    # ~ signaltonoise(instack, axis = 0)
    # ~ Calculates signal-to-noise. Axis can equal None (ravel array first), an
    # integer (the axis over which to operate). Returns: array containing the
    #  value of (mean/stdev) along axis, or 0 when stdev=0

    # Output
    # scipy.stats.signaltonoise(i) = np.mean(i) / np.std(i)
    SNR = scipy.stats.signaltonoise(Image[HorizontalLine, :])
    print 'The SNR is', round(SNR, 3), 'or', round(10 * np.log10(SNR), 3), 'dB'

if options.CNR:
    print 'pick two points on the upper image:'
    options.CNRCoordinates = ginput(2)
    options.CNRRegionWidth = 50
    plt.subplot(211)  # plot on first plot

    # draw CNR ROI around them
    ## Point 1
    plt.hlines(options.CNRCoordinates[0][1] - options.CNRRegionWidth,
               options.CNRCoordinates[0][0] - options.CNRRegionWidth,
               options.CNRCoordinates[0][0] + options.CNRRegionWidth, 'y',
               linewidth=3)
    plt.hlines(options.CNRCoordinates[0][1] + options.CNRRegionWidth,
               options.CNRCoordinates[0][0] - options.CNRRegionWidth,
               options.CNRCoordinates[0][0] + options.CNRRegionWidth, 'y',
               linewidth=3)
    plt.vlines(options.CNRCoordinates[0][0] - options.CNRRegionWidth,
               options.CNRCoordinates[0][1] - options.CNRRegionWidth,
               options.CNRCoordinates[0][1] + options.CNRRegionWidth, 'y',
               linewidth=3)
    plt.vlines(options.CNRCoordinates[0][0] + options.CNRRegionWidth,
               options.CNRCoordinates[0][1] - options.CNRRegionWidth,
               options.CNRCoordinates[0][1] + options.CNRRegionWidth, 'y',
               linewidth=3)
    ## Point 2
    plt.hlines(options.CNRCoordinates[1][1] - options.CNRRegionWidth,
               options.CNRCoordinates[1][0] - options.CNRRegionWidth,
               options.CNRCoordinates[1][0] + options.CNRRegionWidth, 'y',
               linewidth=3)
    plt.hlines(options.CNRCoordinates[1][1] + options.CNRRegionWidth,
               options.CNRCoordinates[1][0] - options.CNRRegionWidth,
               options.CNRCoordinates[1][0] + options.CNRRegionWidth, 'y',
               linewidth=3)
    plt.vlines(options.CNRCoordinates[1][0] - options.CNRRegionWidth,
               options.CNRCoordinates[1][1] - options.CNRRegionWidth,
               options.CNRCoordinates[1][1] + options.CNRRegionWidth, 'y',
               linewidth=3)
    plt.vlines(options.CNRCoordinates[1][0] + options.CNRRegionWidth,
               options.CNRCoordinates[1][1] - options.CNRRegionWidth,
               options.CNRCoordinates[1][1] + options.CNRRegionWidth, 'y',
               linewidth=3)

    print 'calculating CNR of', os.path.basename(options.Filename)
    S1 = np.mean(Image[options.CNRCoordinates[0][1] -
                       options.CNRRegionWidth:options.CNRCoordinates[0][1] +
                                              options.CNRRegionWidth,
                 options.CNRCoordinates[0][0] -
                 options.CNRRegionWidth:options.CNRCoordinates[0][0] +
                                        options.CNRRegionWidth])
    S2 = np.mean(Image[options.CNRCoordinates[1][1] -
                       options.CNRRegionWidth:options.CNRCoordinates[1][1] +
                                              options.CNRRegionWidth,
                 options.CNRCoordinates[1][0] -
                 options.CNRRegionWidth:options.CNRCoordinates[1][0] +
                                        options.CNRRegionWidth])
    Sigma1 = np.std(Image[options.CNRCoordinates[0][1] -
                          options.CNRRegionWidth:options.CNRCoordinates[0][1] +
                                                 options.CNRRegionWidth,
                    options.CNRCoordinates[0][0] -
                    options.CNRRegionWidth:options.CNRCoordinates[0][0] +
                                           options.CNRRegionWidth])
    Sigma2 = np.std(Image[options.CNRCoordinates[1][1] -
                          options.CNRRegionWidth:options.CNRCoordinates[1][1] +
                                                 options.CNRRegionWidth,
                    options.CNRCoordinates[1][0] -
                    options.CNRRegionWidth:options.CNRCoordinates[1][0] +
                                           options.CNRRegionWidth])

    # Output
    print 'CNR between the two selected points:'
    print 'with a ROI area around them of',\
        (2 * options.CNRRegionWidth) ** 2, 'pixels (±width of', \
        options.CNRRegionWidth, 'pixels).'

    CNR = np.abs(S1 - S2) / (Sigma1 + Sigma2)
    print 'The CNR between the two points is:', CNR
    title = 'CNR: ' + str(round(CNR, 4))
    plt.title(title)
    plt.draw()

print
print 'The script was called with this command:', ' '.join(sys.argv)
plt.ioff()
plt.show()
