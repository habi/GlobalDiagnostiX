"""
Script to read and display the experiments done with the iAi electronics
prototype in the x-ray lab
"""

import os
import glob
import numpy
import matplotlib.pylab as plt
import platform

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
CorrectedAdat = [Dark[i] - Radiography[i] for i in range(len(FolderList))]

# # Shift gray values of corrected data to min=0
# CorrectedData = [ i - numpy.min(i) for i in CorrectedData]
# CorrectedAdat = [ i - numpy.min(i) for i in CorrectedAdat]

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
ValuesCorrectedAdat = [[numpy.min(i), numpy.mean(i), numpy.max(i), numpy.std(
    i)] for i in CorrectedAdat]

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
    print 'Drk-Img\t', round(ValuesCorrectedAdat[counter][0], 1), '\t', \
        round(ValuesCorrectedAdat[counter][1], 1), '\t', \
        round(ValuesCorrectedAdat[counter][2], 1), '\t', \
        round(ValuesCorrectedAdat[counter][3], 1)

    plt.figure(figsize=(20, 10))
    FigureTitle = str(counter + 1) + '/' + str(len(FolderList)), '|', \
        os.path.basename(Folder), ' Xray shot with', kV[counter], 'kV and',\
        mAs[counter], 'mAs (' + SourceExposureTime[counter] + \
        'ms source exposure time). Captured with', \
        CMOSExposureTime[counter], 'ms CMOS exposure time and Gain', \
        Gain[counter]
    plt.suptitle(' '.join(FigureTitle))

    plt.subplot(241)
    plt.imshow(Radiography[counter], cmap='bone', interpolation='bicubic',
               vmin=ValuesImage[counter][0],
               vmax=ValuesImage[counter][1] + 3 * ValuesImage[counter][3])
    plt.title('Image')
    plt.axis('off')

    plt.subplot(242)
    plt.hist(Radiography[counter].flatten(), bins=128, fc='k', ec='k')
    plt.axvline(x=ValuesImage[counter][0], color='r', linestyle='--')
    plt.axvline(x=ValuesImage[counter][1] + 3 * ValuesImage[counter][3],
                color='r', linestyle='--')
    plt.title('Image Histogram (red=display range)')

    plt.subplot(243)
    plt.imshow(Dark[counter], cmap='bone', interpolation='bicubic',
               vmin=ValuesDark[counter][0],
               vmax=ValuesDark[counter][1] + 3 * ValuesDark[counter][3])
    plt.title('Dark')
    plt.axis('off')

    plt.subplot(244)
    plt.hist(Dark[counter].flatten(), bins=128, fc='k', ec='k')
    plt.axvline(x=ValuesDark[counter][0], color='r', linestyle='--')
    plt.axvline(x=ValuesDark[counter][1] + 3 * ValuesDark[counter][3],
                color='r', linestyle='--')
    plt.title('Dark Histogram (red=display range)')

    plt.subplot(245)
    plt.imshow(CorrectedData[counter], cmap='bone', interpolation='bicubic',
               vmin=ValuesCorrectedData[counter][0],
               vmax=(ValuesCorrectedData[counter][1] + 3 *
                     ValuesCorrectedData[counter][3]))
    plt.title('Img-Drk')
    plt.axis('off')

    plt.subplot(246)
    plt.hist(CorrectedData[counter].flatten(), bins=128, fc='k', ec='k')
    plt.axvline(x=ValuesCorrectedData[counter][0], color='r', linestyle='--')
    plt.axvline(x=ValuesCorrectedData[counter][1] + 3 * ValuesCorrectedData[
        counter][3], color='r', linestyle='--')
    plt.title('Corrected Histogram (red=display range)')

    plt.subplot(247)
    plt.imshow(CorrectedAdat[counter], cmap='bone', interpolation='bicubic',
               vmin=ValuesCorrectedAdat[counter][0],
               vmax=(ValuesCorrectedAdat[counter][1] + 3 *
                     ValuesCorrectedAdat[counter][3]))
    plt.title('Drk-Img')
    plt.axis('off')

    plt.subplot(248)
    plt.hist(CorrectedAdat[counter].flatten(), bins=128, fc='k', ec='k')
    plt.axvline(x=ValuesCorrectedAdat[counter][0], color='r', linestyle='--')
    plt.axvline(x=ValuesCorrectedAdat[counter][1] + 3 * ValuesCorrectedAdat[
        counter][3], color='r', linestyle='--')
    plt.title('Corrected Histogram (red=display range)')

    plt.savefig(os.path.join(RootPath, Folder + '.png'))

    plt.show()
