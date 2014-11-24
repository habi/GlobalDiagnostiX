"""
Script to read and display the experiments done with the iAi electronics
prototype in the x-ray lab
"""

import glob
import os
import numpy
import matplotlib.pylab as plt
import platform

# CameraSize
CameraWidth = 1280
CameraHeight = 1024

# Get images
if platform.node() == 'anomalocaris':
    RootPath = '/Volumes/slslc/EssentialMed/Images/DetectorElectronicsTests'
else:
    RootPath = '/afs/psi.ch/project/EssentialMed/Images' \
               '/DetectorElectronicsTests'

# Get Images from all folders in RootPath. But only get the ones from IP 44,
# since that was the one that was focus and aligned properly for this test.
FolderList = sorted(glob.glob(os.path.join(RootPath, '*')))

for counter, Folder in enumerate(FolderList):
    print 80 * '-'
    print str(counter + 1) + '/' + str(len(FolderList)), '|', os.path.basename(
        Folder)
    RadiographyName = glob.glob(os.path.join(RootPath,
                                             Folder, '*1-44.gray'))[0]
    DarkName = glob.glob(os.path.join(RootPath, Folder, '*0-44.gray'))[0]

    # Read images
    print 'Reading', RadiographyName
    Radiography = numpy.fromfile(RadiographyName, dtype=numpy.int16).reshape(
        CameraHeight, CameraWidth)
    print 'Reading', DarkName
    Dark = numpy.fromfile(DarkName, dtype=numpy.int16).reshape(CameraHeight,
                                                               CameraWidth)
    CorrectedData = Radiography - Dark
    CorrectedAdat = Dark - Radiography

    # Grab information from files
    MaxImage = numpy.max(Radiography)
    MinImage = numpy.min(Radiography)
    MeanImage = numpy.mean(Radiography)
    STDImage = numpy.std(Radiography)

    MaxDark = numpy.max(Dark)
    MinDark = numpy.min(Dark)
    MeanDark = numpy.mean(Dark)
    STDDark = numpy.std(Dark)

    MaxCorrectedData = numpy.max(CorrectedData)
    MinCorrectedData = numpy.min(CorrectedData)
    MeanCorrectedData = numpy.mean(CorrectedData)
    STDCorrectedData = numpy.std(CorrectedData)

    MaxCorrectedAdat = numpy.max(CorrectedAdat)
    MinCorrectedAdat = numpy.min(CorrectedAdat)
    MeanCorrectedAdat = numpy.mean(CorrectedAdat)
    STDCorrectedAdat = numpy.std(CorrectedAdat)

    # Grab parameters from filename
    kV = os.path.basename(Folder).split('kV_')[0].split('_')[-1]
    mAs = os.path.basename(Folder).split('mAs_')[0].split('kV_')[-1]
    SourceExposureTime = os.path.basename(Folder).split('ms_')[0].split(
        'mAs_')[-1]
    CMOSExposureTime = os.path.basename(RadiographyName).split('-e')[
        1].split('-g')[0]
    Gain = os.path.basename(RadiographyName).split('-g')[1].split('-i')[0]

    # Inform the user
    print '\nFor the experiment with', kV, 'kV,', mAs, \
        'mAs we have the following image properties'
    print '\tMin\tMean\tMax\tSTD'
    print 'Image\t',    round(MinImage, 1), '\t', \
        round(MeanImage, 1), '\t', round(MaxImage, 1), '\t', \
        round(STDImage, 1)
    print 'Dark\t',     round(MinDark, 1), '\t', \
        round(MeanDark, 1), '\t', round(MaxDark, 1), '\t', round(STDDark, 1)
    print 'Img-Drk\t',  round(MinCorrectedData, 1), '\t', \
        round(MeanCorrectedData, 1), '\t', round(MaxCorrectedData, 1), '\t', \
        round(STDCorrectedData, 1)
    print 'Drk-Img\t',  round(MinCorrectedAdat, 1), '\t', \
        round(MeanCorrectedAdat, 1), '\t', round(MaxCorrectedAdat, 1), '\t', \
        round(STDCorrectedAdat, 1)

    plt.figure(figsize=(16, 9))
    FigureTitle = str(counter + 1) + '/' + str(len(FolderList)), '|', \
                  os.path.basename(Folder), '\nXray shot with', kV, 'kV and',\
                  mAs, 'mAs (' + SourceExposureTime + \
                  'ms source exposure time).\nCaptured with', \
                  CMOSExposureTime, 'ms CMOS exposure time and Gain', Gain
    plt.suptitle(' '.join(FigureTitle))
    plt.subplot(221)
    plt.imshow(Radiography, cmap='bone', interpolation='nearest')
    plt.title('Image')
    plt.subplot(222)
    plt.imshow(Dark, cmap='bone', interpolation='nearest')
    plt.title('Dark')
    plt.subplot(223)
    plt.imshow(CorrectedData, cmap='bone', interpolation='nearest',
               vmin=numpy.amin(CorrectedData),
               vmax=MeanCorrectedData + 3 * STDCorrectedData)
    plt.title('Img-Drk')
    plt.subplot(224)
    plt.imshow(CorrectedAdat, cmap='bone', interpolation='nearest',
               vmin=numpy.amin(CorrectedAdat),
               vmax=MeanCorrectedAdat + 3 * STDCorrectedAdat)
    plt.title('Drk-Img')
    plt.show()
