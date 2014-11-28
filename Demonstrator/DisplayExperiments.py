# -*- coding: utf-8 -*-

"""
Script to read and display the experiments done with the iAi electronics
prototype in the x-ray lab
"""

import os
import glob
import numpy
import matplotlib.pylab as plt
import platform
import random

import lineprofiler


def my_display_image(image):
    """
    Display an image with the 'bone' color map, bicubic interpolation and with
    the gray values from the minimum of the image to the mean plus three times
    the standard deviation of the image
    """
    plt.imshow(image, cmap='bone', interpolation='bicubic',
               vmin=numpy.min(image),
               vmax=numpy.mean(image) + 3 * numpy.std(image))
    plt.axis('off')


def my_display_histogram(image, howmanybins=64, histogramcolor='k',
                         rangecolor='r'):
    """
    Display the histogram of an input image, including the ranges we have set
    in the MyDisplayImage function above as dashed lines
    """
    plt.hist(image.flatten(), bins=howmanybins, histtype='stepfilled',
             fc=histogramcolor, alpha=0.309)
    plt.axvline(x=numpy.min(image), color=rangecolor, linestyle='--')
    plt.axvline(x=numpy.mean(image), color='k', linestyle='--')
    plt.axvline(x=numpy.mean(image) + 3 * numpy.std(image), color=rangecolor,
                linestyle='--')
    # turn off y-ticks: http://stackoverflow.com/a/2176591/323100
    plt.gca().axes.get_yaxis().set_ticks([])
    plt.title('Histogram. Black = mean, Red = Display range')

# Setup
CameraWidth = 1280
CameraHeight = 1024

# Get images
if platform.node() == 'anomalocaris':
    RootPath = '/Volumes/slslc/EssentialMed/Images/DetectorElectronicsTests'
else:
    RootPath = '/afs/psi.ch/project/EssentialMed/Images' \
               '/DetectorElectronicsTests'

# Get all subfolders: http://stackoverflow.com/a/973488/323100
FolderList = os.walk(RootPath).next()[1]

# Shuffle the Folderlist to make clicking less boring...
random.shuffle(FolderList)

# Get images from the module with IP 44, since that was the one that was focus
# and aligned properly for this test
RadiographyName = [glob.glob(os.path.join(RootPath, i, '*1-44.gray'))[0] for
                   i in FolderList]
DarkName = [glob.glob(os.path.join(RootPath, i, '*0-44.gray'))[0] for i in
            FolderList]

# Read files
print 'Reading all radiographies'
Radiography = [numpy.fromfile(i, dtype=numpy.int16).reshape(CameraHeight,
                                                            CameraWidth) for
               i in RadiographyName]
print 'Reading all darks'
Dark = [numpy.fromfile(i, dtype=numpy.int16).reshape(CameraHeight,
                                                     CameraWidth) for i in
        DarkName]
print 'Calculating all corrected images'
CorrectedData = [Radiography[i] - Dark[i] for i in range(len(FolderList))]
# Shift gray values of corrected data to min=0
# CorrectedData = [ i - numpy.min(i) for i in CorrectedData]

# Grab parameters from filename
kV = [os.path.basename(i).split('kV_')[0].split('_')[-1] for i in FolderList]
mAs = [os.path.basename(i).split('mAs_')[0].split('kV_')[-1] for i in
       FolderList]
SourceExposureTime = [os.path.basename(i).split('ms_')[0].split('mAs_')[-1]
                      for i in FolderList]
CMOSExposureTime = [os.path.basename(i).split('-e')[1].split('-g')[0] for i
                    in RadiographyName]
Gain = [os.path.basename(i).split('-g')[1].split('-i')[0] for i in
        RadiographyName]

# Grab information from files
ValuesImage = [[numpy.min(i), numpy.mean(i), numpy.max(i), numpy.std(i)] for
               i in Radiography]
ValuesDark = [[numpy.min(i), numpy.mean(i), numpy.max(i), numpy.std(i)] for i
              in Dark]
ValuesCorrectedData = [[numpy.min(i), numpy.mean(i), numpy.max(i), numpy.std(
    i)] for i in CorrectedData]

for counter, Folder in enumerate(FolderList):
    print 80 * '-'
    print str(counter + 1) + '/' + str(len(FolderList)), '|', \
        os.path.basename(Folder)

    # Inform the user
    print '\nFor the experiment with', kV[counter], 'kV,', mAs[counter], \
        'mAs we have the following image properties'
    print '\tMin\tMean\tMax\tSTD'
    print 'Image\t', round(ValuesImage[counter][0], 1), '\t', \
        round(ValuesImage[counter][1], 1), '\t', \
        round(ValuesImage[counter][2], 1), '\t', \
        round(ValuesImage[counter][3], 1)
    print 'Dark\t', round(ValuesDark[counter][0], 1), '\t', \
        round(ValuesDark[counter][1], 1), '\t', \
        round(ValuesDark[counter][2], 1), '\t', \
        round(ValuesDark[counter][3], 1)
    print 'Img-Drk\t', round(ValuesCorrectedData[counter][0], 1), '\t', \
        round(ValuesCorrectedData[counter][1], 1), '\t', \
        round(ValuesCorrectedData[counter][2], 1), '\t', \
        round(ValuesCorrectedData[counter][3], 1)

    # Select line profile on corrected image
    selectedpoints, profile = lineprofiler.lineprofile(CorrectedData[counter])

    # Display all the important things
    plt.figure(counter + 1, figsize=(16, 9))
    FigureTitle = str(counter + 1) + '/' + str(len(FolderList)), \
        '| Xray shot with', kV[counter], 'kV and', mAs[counter], \
        'mAs (' + SourceExposureTime[counter] + \
        'ms source exposure time). Captured with', CMOSExposureTime[counter], \
        'ms CMOS exposure time and Gain', Gain[counter]
    plt.suptitle(' '.join(FigureTitle))

    plt.subplot(441)
    my_display_image(Radiography[counter])
    plt.title('Image')

    plt.subplot(442)
    my_display_histogram(Radiography[counter])

    plt.subplot(445)
    my_display_image(Dark[counter])
    plt.title('Dark')

    plt.subplot(446)
    my_display_histogram(Dark[counter])
    plt.title('')

    plt.subplot(243)
    my_display_image(CorrectedData[counter])
    plt.title('Image - Dark')

    plt.subplot(244)
    my_display_histogram(CorrectedData[counter])

    # Draw selection on corrected image
    plt.figure(counter + 1, figsize=(16, 9))
    plt.subplot(243)
    my_display_image(CorrectedData[counter])
    plt.plot((selectedpoints[1, 0], selectedpoints[0, 0]),
             (selectedpoints[1, 1], selectedpoints[0, 1]), color='red',
             marker='o')
    plt.plot(selectedpoints[1, 0], selectedpoints[1, 1], color='yellow',
             marker='o')
    plt.plot(selectedpoints[0, 0], selectedpoints[0, 1], color='black',
             marker='o')
    plt.title('Image - Dark')

    # Draw line profile
    plt.subplot(212)
    plt.plot(profile, color='red', label='Line profile')
    plt.plot(0, profile[0], color='yellow', marker='o', markersize=25,
             alpha=0.309)
    plt.plot(len(profile)-1, profile[-1], color='black', marker='o',
             markersize=25, alpha=0.309)
    plt.axhline(numpy.mean(CorrectedData[counter]), color='k',
                label=u'Image mean ± STD')
    plt.fill_between(range(len(profile)),
                     numpy.mean(CorrectedData[counter]) + numpy.std(
                         CorrectedData[counter]),
                     numpy.mean(CorrectedData[counter]) - numpy.std(
                         CorrectedData[counter]),
                     alpha=0.309, color='k')
    plt.figure(counter + 1, figsize=(16, 9))

    plt.legend(loc='best')
    plt.xlim([0, len(profile) - 1])
    plt.ylim([numpy.mean(CorrectedData[counter]) - 3 * numpy.std(
        CorrectedData[counter]),
        numpy.mean(CorrectedData[counter]) + 3 * numpy.std(CorrectedData[
            counter])])
    plt.title('Line profile along selection')

    plt.savefig(os.path.join(RootPath, Folder + '.png'))
    plt.show()
