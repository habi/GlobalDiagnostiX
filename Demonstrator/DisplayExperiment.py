"""
Script to read and display the experiments done with the iAi electronics
prototype
"""

import glob
import os
import numpy
import matplotlib.pylab as plt

# CameraSize
CameraWidth = 1280
CameraHeight = 1024

# Get images
RootPath = '/afs/psi.ch/project/EssentialMed/Images/DetectorElectronicsTests'

# Get Folders
Folder = '*Gain-Se*'
Radiographies = sorted(glob.glob(os.path.join(RootPath, Folder, '*1-44.gray')))
Darks = sorted(glob.glob(os.path.join(RootPath, Folder, '*0-44.gray')))

Mean = numpy.zeros(len(Radiographies))
Max = numpy.zeros(len(Radiographies))
STD = numpy.zeros(len(Radiographies))

CorrectedMean = numpy.zeros(len(Radiographies))
CorrectedMax = numpy.zeros(len(Radiographies))
CorrectedSTD = numpy.zeros(len(Radiographies))

# Display difference
plt.figure(figsize=(16, 9))
for counter in range(len(Radiographies)):
    # Inform user
    print counter, 'of', len(Radiographies), 'Reading Images'

    # Grab data
    ImageData = numpy.fromfile(Radiographies[counter],
                               dtype=numpy.int16).reshape(CameraHeight,
                                                           CameraWidth)
    DarkData = numpy.fromfile(Darks[counter], dtype=numpy.int16).reshape(
        CameraHeight, CameraWidth)
    CorrectedData = ImageData - DarkData
    Mean[counter] = numpy.mean(ImageData)
    Max[counter] = numpy.max(ImageData)
    STD[counter] = numpy.std(ImageData)
    CorrectedMean[counter] = numpy.mean(ImageData)
    CorrectedMax[counter] = numpy.max(ImageData)
    CorrectedSTD[counter] = numpy.std(ImageData)
    ExposureTime = os.path.basename(Radiographies[counter]).split('-e')[
        1].split('-g')[0]
    Gain = os.path.basename(Radiographies[counter]).split('-g')[1].split(
        '-i')[0]

    # Display data
    plt.subplot(4, len(Radiographies), counter + 1)
    plt.imshow(ImageData, cmap='bone', vmin=numpy.mean(ImageData),
        vmax=numpy.max(ImageData))
    plt.axis('off')
    plt.title('\n'.join([ExposureTime + ' ms', 'Gain ' + Gain]))

    plt.subplot(4, len(Radiographies), counter + 1 + len(Radiographies))
    #~ plt.hist(ImageData.flatten(), bins=128, fc='k', ec='k')
    plt.axis('off')

    #~ plt.subplot(5, len(Radiographies), counter + 1 + 2 * len(Radiographies))
    plt.imshow(CorrectedData, cmap='bone', vmin=0, vmax=100)
    plt.axis('off')
    plt.title('Corrected Image')

    plt.subplot(4, len(Radiographies), counter + 1 + 2 * len(Radiographies))
    plt.hist(CorrectedData.flatten(), bins=128, fc='k', ec='k')
    plt.yticks=[1,2]

    plt.subplots_adjust(hspace = 0.5)

# Plot max, mean and standard deviation of images
plt.subplot(414)
plt.plot(Max,'-o',label='Max')
plt.plot(Mean,'-o',label='Mean')
plt.plot(STD,'-o',label='STD')

plt.plot(CorrectedMax,'-o',label='Corrected Max')
plt.plot(CorrectedMean,'-o',label='Corrected Mean')
plt.plot(CorrectedSTD,'-o',label='Corrected STD')

plt.legend(loc='best')
plt.tight_layout()
plt.show()
