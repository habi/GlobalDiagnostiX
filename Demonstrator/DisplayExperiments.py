"""
Script to read and display the experiments done with the iAi electronics
prototype in the x-ray lab
"""

import os
import glob
import numpy
import matplotlib.pylab as plt
import platform

def MyDisplayImage(Image):
    """
    Display an image with the 'bone' color map, bicubic interpolation and with
    the gray values from the minimum of the image to the mean plus three times
    the standard deviation of the image
    """
    plt.imshow(Image, cmap='bone', interpolation='bicubic',
               vmin=numpy.min(Image),
               vmax=numpy.mean(Image) + 3 * numpy.std(Image))
    plt.axis('off')

def MyDisplayHistogram(Image, HowManyBins=64, HistogramColor='b',
                        RangeColor='r'):
    """
    Display the histogram of an input image, including the ranges we have set
    in the MyDisplayImage function above as dashed lines
    """
    plt.hist(Image.flatten(), bins=HowManyBins, histtype='stepfilled',
             fc=HistogramColor)
    plt.axvline(x=numpy.min(Image), color=RangeColor, linestyle='--')
    plt.axvline(x=numpy.mean(Image), color='k', linestyle='--')
    plt.axvline(x=numpy.mean(Image) + 3 * numpy.std(Image), color=RangeColor,
                linestyle='--')
    plt.title('Histogram with display range')

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
print 'Calculating corrected images'
CorrectedData = [Radiography[i] - Dark[i] for i in range(len(FolderList))]
# Shift gray values of corrected data to min=0
#~ CorrectedData = [ i - numpy.min(i) for i in CorrectedData]

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

    plt.figure(figsize=(20, 4))
    FigureTitle = str(counter + 1) + '/' + str(len(FolderList)), '|', \
        os.path.basename(Folder), ' Xray shot with', kV[counter], 'kV and',\
        mAs[counter], 'mAs (' + SourceExposureTime[counter] + \
        'ms source exposure time). Captured with', \
        CMOSExposureTime[counter], 'ms CMOS exposure time and Gain', \
        Gain[counter]
    plt.suptitle(' '.join(FigureTitle))

    plt.subplot(161)
    MyDisplayImage(Radiography[counter])
    plt.title('Image')

    plt.subplot(162)
    MyDisplayHistogram(Radiography[counter])

    plt.subplot(163)
    MyDisplayImage(Dark[counter])
    plt.title('Dark')

    plt.subplot(164)
    MyDisplayHistogram(Dark[counter])

    plt.subplot(165)
    MyDisplayImage(CorrectedData[counter])
    plt.title('Image - Dark')

    plt.subplot(166)
    MyDisplayHistogram(CorrectedData[counter])

    plt.tight_layout()
    plt.savefig(os.path.join(RootPath, Folder + '.png'))

    plt.show()
