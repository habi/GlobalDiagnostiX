"""
Script to "analyze" the grid shown in the radiographies from Ivan.

The user manually selects the grid, the histogram of the grid is then shown.

Region selection code based on http://is.gd/GoCP5g
"""

from __future__ import division
import os
import numpy
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import time


def tellme(blurb):
    print(blurb)
    plt.title(blurb)
    plt.draw()


def normalize(image, depth=256):
    """Normalize image to chosen bit depth"""
    #~ print 'Normalizing image from [' + str(numpy.min(image)) + ':' + \
        #~ str(numpy.max(image)) + '] to',
    normalizedimage = ((image - numpy.min(image)) *
        ((depth) / (numpy.max(image) - numpy.min(image))))
    #~ print '[' + str(numpy.min(normalizedimage)) + ':' + \
        #~ str(numpy.max(normalizedimage)) + ']'
    return normalizedimage


def contrast_stretch(image):
    #~ print 'Clipping image from [' + str(numpy.min(image)) + ':' + \
        #~ str(numpy.max(image)) + '] to',
    clippedimage = numpy.clip(image, numpy.mean(image) - 2 * numpy.std(image),
                              numpy.mean(image) + 2 * numpy.std(image))
    #~ print '[' + str(numpy.min(clippedimage)) + ':' + \
        #~ str(numpy.max(clippedimage)) + ']'
    return clippedimage


ReadRaw = True
if ReadRaw:
    Directory = '/afs/psi.ch/user/h/haberthuer/EssentialMed/' + \
        'MasterArbeitBFH/XrayImages/20140731/Toshiba/AR0132/' + \
        'TIS-TBL-6C-3MP/Hand'
    Folder = '5808858'
    File = '5808858_Toshiba_AR0132_1280x964_TIS-TBL-6C-3MP_190mmSDD_Hand_' + \
        '60kV_2mAs_25.0msXray_65.99msCMOS_11.raw'
    Size = [int(File.split('_')[3].split('x')[1]),
        int(File.split('_')[3].split('x')[0])]
    # Load Image
    FileToLoad = os.path.join(Directory, Folder, File)
    Image = numpy.fromfile(FileToLoad, dtype=numpy.uint16).reshape(Size)
    # Pad outer edges of image (DevWare setup data (?)
    padwidth = 3
    # left
    Image[:, :padwidth] = 0
    # right
    Image[:, -padwidth:] = 0
    # top
    Image[:padwidth, :] = 0
    # bottom
    Image[-padwidth:, :] = 0
else:
    Directory = '/afs/psi.ch/user/h/haberthuer/EssentialMed/' + \
        'MasterArbeitBFH/XrayImages/20140731/Toshiba/AR0132/' + \
        'TIS-TBL-6C-3MP/Hand'
    Folder = ''
    File = 'Analysis_5808858_Corrected.png'
    FileToLoad = os.path.join(Directory, Folder, File)
    Image = plt.imread(FileToLoad)

NormalizedImage = normalize(Image)
StretchedImage = normalize(contrast_stretch(Image))

plt.ion()

plt.figure(File, figsize=[23, 9])
# Images
plt.subplot(231)
plt.imshow(Image, cmap='bone', interpolation='nearest')
plt.title('Original')
plt.subplot(232)
plt.imshow(NormalizedImage, cmap='bone', interpolation='nearest')
plt.title('Normalized')
plt.subplot(233)
plt.imshow(StretchedImage, cmap='bone', interpolation='nearest')
#~ plt.colorbar()
plt.title('Contrast stretched')
# Histograms
plt.subplot(234)
plt.hist(Image.flatten(), 64)
plt.subplot(235)
plt.hist(NormalizedImage.flatten(), 64)
plt.subplot(236)
plt.hist(StretchedImage.flatten(), 64)
plt.xlim([0, 256])
plt.tight_layout()

plt.figure('Selection', figsize=[23, 9])
plt.subplot(121)
plt.imshow(StretchedImage, cmap='bone', interpolation='nearest')

# Let the user select the ROI of the resolution phantom
done = False
while not done:
    pts = []
    while len(pts) < 2:
        tellme('Select 2 diagonal edges of the resolution phantom')
        pts = numpy.asarray(plt.ginput(2, timeout=-1))
        if len(pts) < 2:
            tellme('Too few points, starting over')
            time.sleep(1)  # Wait a second
    # Get region of interest from user input and draw it
    xmin = min(pts[:, 0])
    xmax = max(pts[:, 0])
    ymin = min(pts[:, 1])
    ymax = max(pts[:, 1])
    currentAxis = plt.gca()
    rectangle = currentAxis.add_patch(Rectangle((xmin, ymin), xmax - xmin,
                                                ymax - ymin, facecolor='red',
                                                alpha=0.25))
    tellme('Done? Press any key for yes, click with mouse for no')
    done = plt.waitforbuttonpress()
    # Redraw image if necessary
    if not done:
        plt.clf()
        plt.subplot(121)
        plt.imshow(StretchedImage, cmap='bone', interpolation='nearest')
# Draw selected ROI
tellme('Selected ROI')
plt.subplot(222)
CroppedImage = contrast_stretch(Image[ymin:ymax, xmin:xmax])
plt.imshow(CroppedImage, cmap='bone', interpolation='none')
tellme(' '.join(['ROI:', str(int(round(xmax - xmin))), 'x',
    str(int(round(ymax - ymin))), 'px']))
plt.tight_layout()
# Select ROI of resolution phantom. Afterwards we draw $steps horizontal lines
# in a region $pad px bigger than the selected ROI
pad = 25
steps = 5
done = False
while not done:
    pts = []
    while len(pts) < 2:
        tellme('Select opposite edges of resolution phantom region')
        pts = numpy.asarray(plt.ginput(2, timeout=-1))
        if len(pts) < 2:
            tellme('Too few points, starting over')
            time.sleep(1)  # Wait a second
    # Get region of interest from user input and draw it
    xmin = min(pts[:, 0])
    xmax = max(pts[:, 0])
    ymin = min(pts[:, 1])
    ymax = max(pts[:, 1])
    currentAxis = plt.gca()
    rectangle = currentAxis.add_patch(Rectangle((xmin - pad, ymin),
                                                xmax - xmin + pad + pad,
                                                ymax - ymin, facecolor='red',
                                                alpha=0.25))
    tellme('Done? Press any key for yes, click with mouse for no')
    done = plt.waitforbuttonpress()
    # Redraw image if necessary
    if not done:
        plt.clf()
        plt.subplot(222)
        plt.imshow(CroppedImage, cmap='bone', interpolation='none')
tellme('Selected ROI and lines of plot below')

# draw $steps horizontal lines $pad px around the selected one
# IWantHue, dark background, 10 colors, hard
clr = ["#6B9519", "#9B46C3", "#281B32", "#F29C2F", "#F0418C", "#8DF239",
    "#EBF493", "#4680F0", "#402305", "#9F9BFD"]
Phantom = numpy.empty(shape=(int(round((xmax + pad) - (xmin - pad))),
                             steps))
SelectedHeight = numpy.linspace(ymin, ymax, steps)
SelectedLines = [line for
    line in [CroppedImage[int(round(height)), xmin - pad:xmax + pad] for
    height in SelectedHeight]]

plt.subplot(222)
for c, height in enumerate(SelectedHeight):
    plt.axhline(height, linewidth=4, alpha=0.5, color=clr[c])
plt.subplot(224)
for c, line in enumerate(SelectedLines):
    plt.plot(line, alpha=0.5, color=clr[c])
plt.plot(numpy.mean(SelectedLines, axis=0), 'k', linewidth='4',
    label=' '.join(['mean of', str(steps), 'shown lines']))
plt.legend(loc='best')
plt.title('Brightness in the red ROI shown above')
plt.tight_layout()

plt.ioff()
plt.show()
