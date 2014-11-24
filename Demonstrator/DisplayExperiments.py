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

# Grab names
RadiographyName = [glob.glob(os.path.join(RootPath, i, '*1-44.gray'))[0] for
    i in FolderList]
DarkName = [glob.glob(os.path.join(RootPath, i, '*0-44.gray'))[0] for
    i in FolderList]

# Read files
print 'Reading all radiographies'
Radiography = [numpy.fromfile(i, dtype=numpy.int16).reshape(CameraHeight,
    CameraWidth) for i in RadiographyName]
print 'Reading all darks'
Dark = [numpy.fromfile(i, dtype=numpy.int16).reshape(CameraHeight, CameraWidth)
    for i in DarkName]
print 'Calculating corrected images'
CorrectedData = [Radiography[i] - Dark[i] for i in range(len(FolderList))]
CorrectedAdat = [Dark[i] - Radiography[i] for i in range(len(FolderList))]

# Grab parameters from filename
kV = [os.path.basename(i).split('kV_')[0].split('_')[-1] for i in FolderList]
mAs = [os.path.basename(i).split('mAs_')[0].split('kV_')[-1] for
    i in FolderList]
SourceExposureTime = [os.path.basename(i).split('ms_')[0].split('mAs_')[-1]
    for i in FolderList]
CMOSExposureTime = [os.path.basename(i).split('-e')[1].split('-g')[0]
    for i in RadiographyName]
Gain = [os.path.basename(i).split('-g')[1].split('-i')[0]
    for i in RadiographyName]

# Grab information from files
ValuesImage = [[numpy.min(i), numpy.mean(i), numpy.max(i), numpy.std(i)]
    for i in Radiography]
ValuesDark = [[numpy.min(i), numpy.mean(i), numpy.max(i), numpy.std(i)]
    for i in Dark]
ValuesCorrectedData = [[numpy.min(i), numpy.mean(i), numpy.max(i),
    numpy.std(i)] for i in CorrectedData]
ValuesCorrectedAdat = [[numpy.min(i), numpy.mean(i), numpy.max(i),
    numpy.std(i)] for i in CorrectedAdat]

for counter, Folder in enumerate(FolderList):
    print 80 * '-'
    print str(counter + 1) + '/' + str(len(FolderList)), '|', \
        os.path.basename(Folder)

    # Inform the user
    print '\nFor the experiment with', kV[counter], 'kV,', mAs[counter], \
        'mAs we have the following image properties'
    print '\tMin\tMean\tMax\tSTD'
    print 'Image\t',    round(ValuesImage[counter][0], 1), '\t', \
        round(ValuesImage[counter][1], 1), '\t', \
        round(ValuesImage[counter][2], 1), '\t', \
        round(ValuesImage[counter][3], 1)
    print 'Dark\t',    round(ValuesDark[counter][0], 1), '\t', \
        round(ValuesDark[counter][1], 1), '\t', \
        round(ValuesDark[counter][2], 1), '\t', \
        round(ValuesDark[counter][3], 1)
    print 'Img-Drk\t',    round(ValuesCorrectedData[counter][0], 1), '\t', \
        round(ValuesCorrectedData[counter][1], 1), '\t', \
        round(ValuesCorrectedData[counter][2], 1), '\t', \
        round(ValuesCorrectedData[counter][3], 1)
    print 'Drk-Imgk\t',    round(ValuesCorrectedAdat[counter][0], 1), '\t', \
        round(ValuesCorrectedAdat[counter][1], 1), '\t', \
        round(ValuesCorrectedAdat[counter][2], 1), '\t', \
        round(ValuesCorrectedAdat[counter][3], 1)

    plt.figure(figsize=(16, 9))
    FigureTitle = str(counter + 1) + '/' + str(len(FolderList)), '|', \
        os.path.basename(Folder), '\nXray shot with', kV[counter], 'kV and',\
        mAs[counter], 'mAs (' + SourceExposureTime[counter] + \
        'ms source exposure time).\nCaptured with', \
        CMOSExposureTime[counter], 'ms CMOS exposure time and Gain', \
        Gain[counter]
    plt.suptitle(' '.join(FigureTitle))
    plt.subplot(221)
    plt.imshow(Radiography[counter], cmap='bone', interpolation='nearest')
    plt.title('Image')
    plt.subplot(222)
    plt.imshow(Dark[counter], cmap='bone', interpolation='nearest')
    plt.title('Dark')
    plt.subplot(223)
    plt.imshow(CorrectedData[counter], cmap='bone', interpolation='nearest',
        vmin=ValuesCorrectedData[counter][0],
        vmax=(ValuesCorrectedData[counter][1] + 3 *
            ValuesCorrectedData[counter][3]))
    plt.title('Img-Drk')
    plt.subplot(224)
    plt.imshow(CorrectedAdat[counter], cmap='bone', interpolation='nearest',
        vmin=ValuesCorrectedAdat[counter][0],
        vmax=(ValuesCorrectedAdat[counter][1] + 3 *
            ValuesCorrectedAdat[counter][3]))
    plt.title('Drk-Img')
    plt.show()
