"""
Script to read and display the experiments done with the iAi electronics
prototype
"""

import glob
import os
import numpy
import matplotlib.pylab as plt
import matplotlib.gridspec as gridspec
import platform

import lineprofiler

# CameraSize
CameraWidth = 1280
CameraHeight = 1024


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

# Get images
if platform.node() == 'anomalocaris':
    RootPath = '/Volumes/slslc/EssentialMed/Images/DetectorElectronicsTests'
else:
    RootPath = '/afs/psi.ch/project/EssentialMed/Images' \
               '/DetectorElectronicsTests'

MyColors = ['#95C5B5', '#BF55C4', '#BC4E35', '#7FCE56', '#51364A', '#CDB151',
            '#7D81C2', '#576239', '#CA6787']

# Get Folders
Folder = '*Gain-Se*'

RadiographyNames = sorted(glob.glob(os.path.join(RootPath, Folder,
                                                 '*1-44.gray')))
DarkNames = sorted(glob.glob(os.path.join(RootPath, Folder, '*0-44.gray')))

print 'Reading images'
Radiography = [numpy.fromfile(i, dtype=numpy.int16).reshape(CameraHeight,
                                                            CameraWidth)
               for i in RadiographyNames]
Dark = [numpy.fromfile(i, dtype=numpy.int16).reshape(CameraHeight, CameraWidth)
        for i in DarkNames]

print 'Correcting images with darks'
CorrectedImages = [i - k for i, k in zip(Radiography, Dark)]

print 'Crop zoomed region'
ZoomedImages = [i[445:775, 510:615] for i in CorrectedImages]

print 'Get line profiles in zoomed region'
LineProfileCoordinates = [(30, 310), (35, 10)]
# The lineprofiler gives back a tuple with coordinates and line profile based
# on these cordinates. To plot the profile, we can access it with
# LineProfile[i][1].
LineProfile = [lineprofiler.lineprofile(i, LineProfileCoordinates) for i in
               ZoomedImages]

print 'Get min, mean, max and STD for each set of images (original, corrected' \
      ' and zoomed).'

MinImage = [numpy.min(i) for i in Radiography]
MeanImage = [numpy.mean(i) for i in Radiography]
MaxImage = [numpy.max(i) for i in Radiography]
STDImage = [numpy.std(i) for i in Radiography]

MinCorrected = [numpy.min(i) for i in CorrectedImages]
MeanCorrected = [numpy.mean(i) for i in CorrectedImages]
MaxCorrected = [numpy.max(i) for i in CorrectedImages]
STDCorrected = [numpy.std(i) for i in CorrectedImages]

MinZoomed = [numpy.min(i) for i in ZoomedImages]
MeanZoomed = [numpy.mean(i) for i in ZoomedImages]
MaxZoomed = [numpy.max(i) for i in ZoomedImages]
STDZoomed = [numpy.std(i) for i in ZoomedImages]

print 'Get exposure time and gain from image names'

ExposureTime = [os.path.basename(i).split('-e')[1].split('-g')[0] for i in
                RadiographyNames]
Gain = [os.path.basename(i).split('-g')[1].split('-i')[0] for i in
        RadiographyNames]

print 'Displaying information'
# Display
plt.figure(1, figsize=(18, 12))
Grid = gridspec.GridSpec(5, len(RadiographyNames))

# Plot global stuff
plt.rc('lines', linewidth=2, marker='o')

plt.subplot(Grid[2, 0:3])
plt.gca().set_color_cycle(['c', 'm', 'y', 'k'])
plt.plot(MeanCorrected, label='Original')
plt.plot(MeanImage, label='Corrected')
plt.plot(MeanZoomed, label='Zoomed')
plt.title('Mean pixel value')
plt.legend(loc='best')

plt.subplot(Grid[2, 3:6])
plt.gca().set_color_cycle(['c', 'm', 'y', 'k'])
plt.plot(MaxCorrected, label='Original')
plt.plot(MaxImage, label='Corrected')
plt.plot(MaxZoomed, label='Zoomed')
plt.title('Maximum pixel value')
plt.legend(loc='best')

plt.subplot(Grid[2, 6:9])
plt.gca().set_color_cycle(['c', 'm', 'y', 'k'])
plt.plot(STDCorrected, label='Original')
plt.plot(STDImage, label='Corrected')
plt.plot(STDZoomed, label='Zoomed')
plt.title('Standard deviation')
plt.legend(loc='best')

plt.subplot(Grid[4, :])
plt.rc('lines', linewidth=2, marker='')
for c, i in enumerate(LineProfile):
    plt.plot(i[:][1] + 25 * c, color=MyColors[c], label=Gain[c])
plt.title('Line Profiles')
plt.ylabel('[a. u.]')
plt.gca().yaxis.set_major_locator(plt.NullLocator())
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

# Show single images
for counter in range(len(RadiographyNames)):
    plt.subplot(Grid[0, counter])
    plt.imshow(Radiography[counter], cmap='bone', interpolation='bicubic')
    plt.title(str(counter) + ': Gain ' + Gain[counter])
    plt.axis('off')

    plt.subplot(Grid[1, counter])
    my_display_image(CorrectedImages[counter])
    plt.title('Mean+3xSTD')

    plt.subplot(Grid[3, counter])
    my_display_image(ZoomedImages[counter])
    plt.plot((LineProfileCoordinates[0][0], LineProfileCoordinates[1][0]),
             (LineProfileCoordinates[0][1], LineProfileCoordinates[1][1]),
             color=MyColors[counter])
    plt.plot(LineProfileCoordinates[0][0], LineProfileCoordinates[0][1],
             color='yellow', marker='o')
    plt.plot(LineProfileCoordinates[1][0], LineProfileCoordinates[1][1],
             color='black', marker='o')

plt.savefig('Gainseries.png', bbox_inches='tight')
plt.show()
