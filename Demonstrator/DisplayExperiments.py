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
    print str(counter) + '/' + str(len(FolderList)), '|', os.path.basename(
        Folder)
    RadiographyName = glob.glob(os.path.join(RootPath, Folder, '*1-44.gray'))[0]
    DarkName = glob.glob(os.path.join(RootPath, Folder, '*0-44.gray'))[0]

    # Read images
    print 'Reading', RadiographyName
    Radiography = numpy.fromfile(RadiographyName, dtype=numpy.int16).reshape(
        CameraHeight, CameraWidth)
    print 'Reading', DarkName
    Dark = numpy.fromfile(DarkName, dtype=numpy.int16).reshape(
        CameraHeight, CameraWidth)
    CorrectedData = Radiography - Dark

    # Grab parameters from filename
    kV = os.path.basename(Folder).split('kV_')[0].split('_')[-1]
    mAs = os.path.basename(Folder).split('mas_')[0].split('kV_')[-1]
    SourceExposureTime = os.path.basename(Folder).split('ms_')[0].split(
        'mas_')[-1]
    CMOSExposureTime = os.path.basename(RadiographyName).split('-e')[
        1].split('-g')[0]
    Gain = os.path.basename(RadiographyName).split('-g')[1].split('-i')[0]

    plt.figure()
    FigureTitle = str(counter) + '/' + str(len(FolderList)), '| Xray shot ', \
        'with', kV, 'kV and', mAs, 'mAs (' + SourceExposureTime + \
        'ms source exposure time).\nCaptured with', CMOSExposureTime, \
        'ms CMOS exposure time and Gain', Gain
    plt.suptitle(' '.join(FigureTitle))
    plt.subplot(131)
    plt.imshow(Radiography, cmap='bone', interpolation='nearest')
    plt.title('Radiography')
    plt.subplot(132)
    plt.imshow(Dark, cmap='bone', interpolation='nearest')
    plt.title('Dark Image')
    plt.subplot(133)
    plt.imshow(CorrectedData, cmap='bone', interpolation='nearest')
    plt.title('corrected Image')
    plt.show()