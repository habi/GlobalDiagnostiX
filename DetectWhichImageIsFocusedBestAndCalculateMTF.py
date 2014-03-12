'''
Script to calculate the Modulation transfer function of some input images

It's based on the idea that once can use a random pattern to calculate the MTF,
as specified by Daniels et al. in http://dx.doi.org/10.1117/12.190433, which
was found through http://stackoverflow.com/q/18823968

The script reads some images from the test system which were found to be
focused best (with DetectWhichImageIsFocusedBest.py) and plots their respective
MTF
'''

from __future__ import division
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy
import scipy
from scipy import ndimage
import sys
import os
import glob

print "Let's go"

# 6 colors according to http://tools.medialab.sciences-po.fr/iwanthue/
Hues = ["#C56447", "#A2C747", "#AB5CB2", "#96A8BF", "#543E3F", "#80B17D"]
#~ Hues = ["#A35540", "#95BD56", "#9F5EAB", "#7E9A99"]
#~ Hues = ["#97A861", "#9D6188"]


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
    According to Peter Modregger it's good if we first get rid of the
    DC-component of the image, which means to delete the mean of the image from
    itself
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
             linewidth=5, color=colorh, alpha=1)
    plt.plot(psd(gaussfilter(InputImage))[InputImage.shape[0] / 2,
                                          InputImage.shape[1] / 2:],
             linestyle='-', linewidth=5, color=colorgaussh, alpha=0.5)
    plt.plot(psd(InputImage)[InputImage.shape[0] / 2:,
                             InputImage.shape[1] / 2], linestyle='-',
             linewidth=5, color=colorv, alpha=1)
    plt.plot(psd(gaussfilter(InputImage))[InputImage.shape[0] / 2:,
                                          InputImage.shape[1] / 2],
             linestyle='-', linewidth=5, color=colorgaussv, alpha=0.5)

# Read in Images
Root = '/scratch/tmp/DevWareX/'


SensorList = [os.path.basename(i) for
    i in sorted(glob.glob(os.path.join(Root, '*')))]


print 'Which sensor-images do you want to look at?'

for i,item in enumerate(SensorList):
    print i, '-', item

Sensor = []
while Sensor not in range(len(SensorList)):
    Sensor = int(input('Please enter a number: '))

print 'Ok, I will work with the files in', os.path.join(Root,SensorList[Sensor])
exit()


#~ ImageReal = plt.imread(os.path.join(Root, Directory, File))

FileList = ['AR0130/1392901972_AR0130_004ms_from100mm_to200mm_in25steps/AR0130_004ms_from100mm_to200mm_in25steps_132mm.png',
    'AR0130/1393342195_AR0130_0.12_2.0f_029ms_0mm_to150mm/AR0130_0.12_2.0f_029ms_0mm_to150mm_049mm.png',
    'AR0130/1393342395_AR0130_0.12_2.0f_044ms_0mm_to1500mm/AR0130_0.12_2.0f_044ms_0mm_to1500mm_600mm.png',
    'AR0130/1393346142_AR0130_0.16_2.0f_030ms_0mm_to200mm/AR0130_0.16_2.0f_030ms_0mm_to200mm_036mm.png',
    'AR0130/1393346212_AR0130_0.16_2.0f_030ms_0mm_to200mm/AR0130_0.16_2.0f_030ms_0mm_to200mm_118mm.png',
    'AR0130/1393346258_AR0130_0.16_2.0f_019ms_0mm_to200mm/AR0130_0.16_2.0f_019ms_0mm_to200mm_088mm.png',
    'AR0130/1393346400_AR0130_0.16_2.0f_019ms_0mm_to200mm/AR0130_0.16_2.0f_019ms_0mm_to200mm_084mm.png',
    'A-1300/1393606205_A-1300_0.0_2.0f_022ms_150mm_to400mm/A-1300_0.0_2.0f_022ms_150mm_to400mm_354mm.png',
    'A-1300/1393606263_A-1300_0.0_2.0f_022ms_150mm_to400mm/A-1300_0.0_2.0f_022ms_150mm_to400mm_210mm.png']
for i, image in enumerate(FileList):
    print 10 * '-', i + 1, '/', len(FileList) - 1, 30 * '-'
    plt.subplot(4, len(FileList), i + 1)
    print 'Reading', image
    plt.imshow(plt.imread(os.path.join(Root, image)), cmap='gray')
    plt.title(i)
    plt.subplot(4, len(FileList), i + 1 + len(FileList))
    print 'Calculating & plotting FFT'
    showFFT(plt.imread(os.path.join(Root, image)))
    plt.subplot(4, len(FileList), i + 1 + 2 * len(FileList))
    print 'Calculating & plotting MTF'
    plotFFT(plt.imread(os.path.join(Root, image)))
plt.subplot(414)
for i, image in enumerate(FileList):
    plotFFT(plt.imread(os.path.join(Root, image)))
plt.legend()

plt.show()
