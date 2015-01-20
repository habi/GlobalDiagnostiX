# -*- coding: utf-8 -*-

"""
Script to analyze the "dark" images from the experiments in the EssentialLab
"""

import glob
import os
import numpy
import matplotlib.pylab as plt
import matplotlib.patches as patches


def processimage(inputimage, clip=3):
    """
    Clip image brightness to "mean +- 3 STD" (by default). Another value can
    be given. This is applied to the input images if the -c commandline
    parameter is given.
    """
    return numpy.clip(inputimage,
                      numpy.mean(inputimage) - (clip * numpy.std(inputimage)),
                      numpy.mean(inputimage) + (clip * numpy.std(inputimage)))


def my_display_histogram(img, howmanybins=128, histogramcolor='k',
                         rangecolor='r', clip=3):
    """
    Display the histogram of an input image, including the ranges we clip
    the gray values to
    """
    plt.hist(img.flatten(), bins=howmanybins, histtype='stepfilled',
             fc=histogramcolor, alpha=0.309)
    plt.axvline(x=numpy.mean(img) - clip * numpy.std(img), color=rangecolor,
                linestyle='--')
    plt.axvline(x=numpy.mean(img), color='k', linestyle='--')
    plt.axvline(x=numpy.mean(img) + clip * numpy.std(img),
                color=rangecolor, linestyle='--')
    # turn off y-ticks: http://stackoverflow.com/a/2176591/323100
    plt.gca().axes.get_yaxis().set_ticks([])
    plt.title('Histogram. Black = mean\nRed = Display range')

BasePath = '/afs/psi.ch/user/h/haberthuer/EssentialMed/Images/' \
           'DetectorElectronicsTests/EssentialLab/'

FileNames = sorted([item for item in glob.glob(os.path.join(BasePath, '*',
                                                            '*36.gray'))])

# Select only dark images
DarkFolderList = ['1421327978_noxray',
                  '1421327947_noxray',
                  '1421156423_output',
                  '1421155907_output']
DarkFileNames = []
for i in FileNames:
    if os.path.split(os.path.dirname(i))[1] in DarkFolderList:
        DarkFileNames.append(i)

print 'Reading all %s images' % len(FileNames)
Images = [numpy.fromfile(item, dtype=numpy.uint16, count=-1,
                         sep='').reshape(1024, 1280) for item in FileNames]
print 'Reading only %s dark images' % len(DarkFileNames)
DarkImages = [numpy.fromfile(item, dtype=numpy.uint16, count=-1,
                             sep='').reshape(1024, 1280) for item in
              DarkFileNames]

plt.figure('dark images', figsize=[16, 9])
for counter, image in enumerate(DarkImages):
    plt.subplot(3, len(DarkImages), counter + 1)
    plt.imshow(processimage(image), interpolation='bicubic', cmap='gray_r')
    Zoom = patches.Rectangle((333, 456), width=100, height=50, color='g',
                             alpha=0.618)
    plt.gcf().gca().add_patch(Zoom)

    FigureTitle = os.path.basename(os.path.split(FileNames[counter])[0]), \
        '\n', os.path.basename(FileNames[counter]), '\nmean',\
        str(round(numpy.mean(processimage(image)))), '\nSTD', \
        str(round(numpy.std(processimage(image))))
    plt.title(' '.join(FigureTitle))
    plt.axis('off')
    plt.subplot(3, len(DarkImages), counter + len(DarkImages) + 1)
    plt.imshow(processimage(image)[333:333 + 50, 456:456 + 100],
               interpolation='nearest', cmap='gray_r')
    plt.title('Zoomed region')
    plt.axis('off')
    plt.subplot(3, len(DarkImages), counter + 2 * len(DarkImages) + 1)
    my_display_histogram(image)
    plt.xlim([0, 256])

plt.show()