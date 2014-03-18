'''
Script to calculate the Modulation transfer function of some input images

It's based on the idea that once can use a random pattern to calculate the MTF,
as specified by Daniels et al. in http://dx.doi.org/10.1117/12.190433, which
was found through http://stackoverflow.com/q/18823968.

Imaging a random test pattern with a known (white) power spectral density and
equal power in all spatial frequencies and transforming this image into the
frequency domain gives the MTF. Since the input PSD is uniform, the square root
of the output PSD is equivalent to the MTF of the optical system, as defined by
http://is.gd/FFRB8b

The script reads images which were generated with GDX.ini in DevWare. It looks
for the best focused one via the mean (exposure) and standard deviation of each
image in a given (user-selected) folder. This image is then used for
calculating the MTF, giving us some "hard facts" on the quality of the images.
MTF.
'''

from __future__ import division
import os
import glob
import numpy
import matplotlib.pyplot as plt

print "Hey ho, let's go"

Root = '/scratch/tmp/DevWareX/'
# colors according to http://tools.medialab.sciences-po.fr/iwanthue/
Hues = ["#C56447", "#A2C747", "#AB5CB2", "#96A8BF", "#543E3F", "#80B17D"]
Hues = ["#9D6188", "#97A761"]

# Look for sensor folders (saved in DevWare with GDX.ini -> [Python: Acquire X
# images over a given rail distance])
print 'Looking for sensor-folders in', Root, 'and disregarding other folders'
SensorList = [os.path.basename(i) for
    i in sorted(glob.glob(os.path.join(Root, '*')))]
if len(SensorList) > 1:
    print 'Please select the sensor you want to look at'
    for i, item in enumerate(SensorList):
        # Only look for AR130, AR132 and MT9M001 folders
        if item.startswith('AR') or item.startswith('MT9'):
            print i, '-', item
    Sensor = []
    while Sensor not in range(len(SensorList)):
        Sensor = int(input('Please enter a number: '))
else:
    Sensor = 0

# In this folder, look for lenses (saved as above)
print 'Looking for lens folders in', os.path.join(Root, SensorList[Sensor])
LensList = [os.path.basename(i) for
    i in sorted(glob.glob(os.path.join(Root, SensorList[Sensor], '*')))]
if len(LensList) > 1:
    # Only let the user select if we found more than one lens folder
    print 'Please select the lens you want to look at'
    for i, item in enumerate(LensList):
        print i, '-', item
    Lens = []
    while Lens not in range(len(LensList)):
        Lens = int(input('Please enter a number: '))
else:
    Lens = 0

# And finally, look for folders in which we saved the images
print 'Looking for image folders in', os.path.join(Root, SensorList[Sensor],
                                                    LensList[Lens])
FolderList = [i for i in sorted(glob.glob(os.path.join(Root,
                                                        SensorList[Sensor],
                                                        LensList[Lens], '*')))]
if len(FolderList) > 1:
    # Only let the user select if we found more than one image folder
    print 'Please select the folder of the images you want to look at'
    for i, item in enumerate(FolderList):
        print i, '-', os.path.basename(item)
    Folder = []
    while Folder not in range(len(FolderList)):
        Folder = int(input('Please enter a number: '))
else:
    Folder = 0

# Now we---finally---gan get a list of images to work with, yay!
Images = [i for i in sorted(glob.glob(os.path.join(FolderList[Folder],
                                                      '*.raw')))]
print 'I will work with the', len(Images), '.raw files found in',\
    FolderList[Folder]
print

# Get necessary parameters from the file names
ImageHeight = int(os.path.basename(Images[1]).split('_')[1].split('x')[1])
ImageWidth = int(os.path.basename(Images[1]).split('_')[1].split('x')[0])
#~ Probably get some more parameters, but for now it's enough...

# Iterate through the files, calculate the mean (exposure) and standard
# deviation of each image and plot these values.
print 'Calculating Mean for each of the', len(Images), 'images'
MeanExposure = [numpy.mean(numpy.memmap(x, dtype=numpy.uint16,
                                        shape=(ImageHeight, ImageWidth)))
                for x in Images]

print 'Calculating standard deviation for each of the', len(Images), 'images'
STD = [numpy.std(numpy.memmap(x, dtype=numpy.uint16,
                              shape=(ImageHeight, ImageWidth)))
       for x in Images]

normalize = True
if normalize:
    # Normalize the values around the mean and convert the now array back to a
    # list. This gives more comparable numbers for both the mean and STD.
    MeanExposure = MeanExposure - numpy.mean(MeanExposure)
    MeanExposure = MeanExposure.tolist()
    STD = STD - numpy.mean(STD)
    STD = STD.tolist()

plt.figure('Focus', figsize=(16, 9))
# Plot mean and STD
plt.subplot(311)
plt.title(' '.join([str(len(Images)), 'Images from', SensorList[Sensor],
                    'with', LensList[Lens]]))
plt.plot(MeanExposure, color='r', alpha=0.5,
    label='Exposure with Max @ Img. ' + \
    str(MeanExposure.index(max(MeanExposure))))
plt.plot(STD, color='b', alpha=0.5,
    label='STD with Max @ Img. ' + str(STD.index(max(STD))))

# Print details and plot positions of 'Details' chosen images
Details = 7
DetailImages = [i for i in range(1, len(Images),
                                   int(round(len(Images) / Details)))]
for i in DetailImages:
    print str(i).zfill(2), '|',
    if normalize:
        print 'normalized',
    print 'Exp', round(MeanExposure[i], 4), '|',
    if normalize:
        print 'normalized',
    print 'STD of', round(STD[i], 4)
    plt.plot(i, MeanExposure[i], color='r', marker='.')
    plt.plot(i, STD[i], color='b', marker='.')
    plt.annotate(i, xy=(i, STD[i]), xytext=(0, 15), textcoords='offset points',
                 ha='center', va='top')
# Plot and mark worst and best image: http://stackoverflow.com/a/5147430/323100
plt.plot(STD.index(min(STD)), min(STD), color='b', marker='v')
plt.annotate(os.path.basename(
    Images[STD.index(min(STD))]).split('_')[-1].split('.')[0],
    xy=(STD.index(min(STD)), min(STD)), xytext=(0, 30),
    textcoords='offset points', ha='center', va='bottom',
    bbox=dict(boxstyle='round,pad=0.5', fc='b', alpha=0.125),
    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.79'))
plt.plot(STD.index(max(STD)), max(STD), color='b', marker='^')
plt.annotate(os.path.basename(
    Images[STD.index(max(STD))]).split('_')[-1].split('.')[0],
    xy=(STD.index(max(STD)), max(STD)), xytext=(0, 30),
    textcoords='offset points', ha='center', va='bottom',
    bbox=dict(boxstyle='round,pad=0.5', fc='b', alpha=0.125),
    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.79'))
plt.xlim([0, len(Images) - 1])
plt.legend(loc='best')

DisplayImages = [Images[i] for i in DetailImages]
# Display selection of images below the plot
for i, item in enumerate(DisplayImages):
    plt.subplot(3, Details, i + 1 + Details)
    plt.imshow(numpy.memmap(item, dtype=numpy.uint16,
                            shape=(ImageHeight, ImageWidth)), cmap='gray',
                            interpolation='nearest')
    plt.title('Img ' + str(DetailImages[i]) + '@' + \
        os.path.basename(item.split('_')[-1].split('.')[0]))
    # Display without ticks:
    plt.axis('off')

# Display worst and best image
plt.subplot(3, 2, 5)
plt.imshow(numpy.memmap(Images[STD.index(min(STD))], dtype=numpy.uint16,
           shape=(ImageHeight, ImageWidth)), cmap='gray',
           interpolation='nearest')
plt.title('worst STD@' +
    os.path.basename(Images[STD.index(min(STD))]).split('_')[-1].split('.')[0])
#~ plt.axis('off')
plt.subplot(3, 2, 6)
plt.imshow(numpy.memmap(Images[STD.index(max(STD))], dtype=numpy.uint16,
           shape=(ImageHeight, ImageWidth)), cmap='gray',
           interpolation='nearest')
plt.title('best STD@' +
    os.path.basename(Images[STD.index(max(STD))]).split('_')[-1].split('.')[0])
#~ plt.axis('off')

# Save this figure
plt.savefig('MTF_Focus_' + SensorList[Sensor] + '_' + LensList[Lens] + '.png')

print 'Image', str(MeanExposure.index(max(MeanExposure))), '(' + \
    os.path.basename(Images[MeanExposure.index(max(MeanExposure))]) +\
    ') is the brightest.'
print 'Image', str(STD.index(max(STD))), '(' + \
    os.path.basename(Images[STD.index(max(STD))]) + ') has the largest STD.'

# Done with focussing stuff. And now for something completely different!
# Get an "original" random image which we can use for calculating the
# "original" PSD
RandomImage = numpy.random.randint(2,
                                   size=[ImageHeight, ImageWidth]) * (2 ** 16)

# Load the image with best focus
CameraImage = numpy.fromfile(Images[STD.index(max(STD))],
                             dtype=numpy.uint16).reshape(ImageHeight,
                                                         ImageWidth)


def FFT2D(Image, Exponent=2):
    return numpy.abs(numpy.fft.fft2(Image)) ** Exponent


def PSD(Image):
    # PSD according to Daniels1995
    return numpy.mean(Image, axis=0)

plt.figure('MTF', figsize=(16, 9))
plt.subplot(241)
plt.imshow(RandomImage, interpolation='none', cmap='gray')
plt.title('Random image')
plt.subplot(242)
plt.imshow(FFT2D(RandomImage, 0.1), interpolation='none', cmap='gray')
plt.title('2D FFT')

plt.subplot(245)
plt.imshow(CameraImage, interpolation='none', cmap='gray')
plt.title('best focus')
plt.subplot(246)
plt.imshow(FFT2D(CameraImage, 0.1), interpolation='none', cmap='gray')
plt.title('2D FFT')

plt.subplot(143)
plt.plot(PSD(RandomImage), label='random PSD')
plt.plot(PSD(CameraImage), label='camera PSD')
plt.xlim([0, ImageWidth / 2])
plt.legend(loc='best')
plt.title('PSD')


def MTF(ImageBeforeTransformation, ImageAfterTransformation):
    # remove DC component of images
    MeanA = ImageBeforeTransformation - numpy.mean(ImageBeforeTransformation)
    MeanB = ImageAfterTransformation - numpy.mean(ImageAfterTransformation)
    # calculate power spectral density of both images, according to Daniels1995
    PSD_A = numpy.abs(numpy.fft.fft2(MeanA)) ** 2
    PSD_A = numpy.mean(PSD_A, axis=0)
    PSD_B = numpy.abs(numpy.fft.fft2(MeanB)) ** 2
    PSD_B = numpy.mean(PSD_B, axis=0)
    ImgWidth = ImageBeforeTransformation.shape[1]
    return numpy.sqrt(PSD_B / PSD_A)[:ImgWidth / 2]

plt.subplot(144)
plt.plot(MTF(RandomImage, CameraImage))
#~ plt.ylim([0, 1])
#~ plt.xlim([0, ImageWidth / 2])
plt.title('MTF')

# Save this figure
plt.savefig('MTF_MTF_' + SensorList[Sensor] + '_' + LensList[Lens] + '.png')

plt.show()
