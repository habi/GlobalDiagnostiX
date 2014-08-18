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
    Directory = '/afs/psi.ch/user/h/haberthuer/EssentialMed/MasterArbeitBFH/XrayImages/20140731/Toshiba/AR0132/TIS-TBL-6C-3MP/Hand'
    Folder = '5808858'
    File = '5808858_Toshiba_AR0132_1280x964_TIS-TBL-6C-3MP_190mmSDD_Hand_60kV_2mAs_25.0msXray_65.99msCMOS_11.raw'
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
    Directory = '/afs/psi.ch/user/h/haberthuer/EssentialMed/MasterArbeitBFH/XrayImages/20140731/Toshiba/AR0132/TIS-TBL-6C-3MP/Hand'
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

plt.figure('Selection')
plt.subplot(121)
plt.imshow(StretchedImage, cmap='bone', interpolation='nearest')

# Let the user select the ROI of the resolution phantom
tellme('Click with the mouse to start')
plt.waitforbuttonpress()
done = False
while not done:
    pts = []
    while len(pts) < 2:
        tellme('Select 2 diagonal edges of the resolution phantom')
        pts = numpy.asarray( plt.ginput(2,timeout=-1) )
        if len(pts) < 2:
            tellme('Too few points, starting over')
            time.sleep(1) # Wait a second
    # Get region of interest from user input and draw it
    xmin = min(pts[:,0])
    xmax = max(pts[:,0])
    ymin = min(pts[:,1])
    ymax = max(pts[:,1])
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
tellme(' '.join(['ROI:', str(int(round(xmax-xmin))), 'x',
    str(int(round(ymax-ymin))), 'px']))
plt.tight_layout()
# Select horizontal line to plot
done = False
while not done:
    pts = []
    while len(pts) < 1:
        tellme('Select height of grid positions')
        pts = numpy.asarray( plt.ginput(1,timeout=-1) )
        if len(pts) < 1:
            tellme('Try again')
            time.sleep(1) # Wait a second
    # Get region of interest from user input and draw it
    plt.axhline(pts[:,1], linewidth=4, color='k', alpha=0.5)
    tellme('Done? Press any key for yes, click with mouse for no')
    done = plt.waitforbuttonpress()
    # Get rid of fill
    if not done:
        plt.clf()
        plt.subplot(222)
        plt.imshow(CroppedImage, origin='upper', interpolation='none')
tellme('Selected line')

# draw five horizontal lines 20 px around the selected one
# IWantHue, dark background, 5 colors, hard
clr=["#53F5F4", "#3F235B", "#5D8A1A", "#F6B08A", "#BBBBF9"]
Phantom = []
for c, i in enumerate(numpy.linspace(-20,20,5)):
    plt.subplot(222)
    plt.axhline(i + pts[:,1], linewidth=4, alpha = 0.5, color=clr[c])
    plt.subplot(224)
    plt.plot(CroppedImage[i + int(round(pts[:,1])),:], color=clr[c])
    #~ Phantom = Phantom + CroppedImage[i + int(round(pts[:,1])),:]
#~ print Phantom
#~ plt.plot(numpy.mean(Phantom), 'k', linewidth='10', label='mean', alpha=1)
#~ plt.legend(loc='best')


plt.ioff()
plt.show()
exit()




##################################################
# Define a triangle by clicking three points
##################################################
plt.clf()
plt.axis([-1.,1.,-1.,1.])
plt.setp(plt.gca(),autoscale_on=False)



plt.waitforbuttonpress()

happy = False
while not happy:
    pts = []
    while len(pts) < 3:
        tellme('Select 3 corners with mouse')
        pts = np.asarray( plt.ginput(3,timeout=-1) )
        if len(pts) < 3:
            tellme('Too few points, starting over')
            time.sleep(1) # Wait a second

    ph = plt.fill( pts[:,0], pts[:,1], 'r', lw=2 )

    tellme('Happy? Key click for yes, mouse click for no')

    happy = plt.waitforbuttonpress()

    # Get rid of fill
    if not happy:
        for p in ph: p.remove()

##################################################
# Now contour according to distance from triangle
# corners - just an example
##################################################

# Define a nice function of distance from individual pts
def f(x,y,pts):
    z = np.zeros_like(x)
    for p in pts:
        z = z + 1/(np.sqrt((x-p[0])**2+(y-p[1])**2))
    return 1/z

X,Y = np.meshgrid( np.linspace(-1,1,51), np.linspace(-1,1,51) )
Z = f(X,Y,pts)

CS = plt.contour( X, Y, Z, 20 )

tellme( 'Use mouse to select contour label locations, middle button to finish' )
CL = plt.clabel( CS, manual=True )

##################################################
# Now do a zoom
##################################################
tellme( 'Now do a nested zoom, click to begin' )
plt.waitforbuttonpress()

happy = False
while not happy:
    tellme( 'Select two corners of zoom, middle mouse button to finish' )
    pts = np.asarray( plt.ginput(2,timeout=-1) )

    happy = len(pts) < 2
    if happy: break

    pts = np.sort(pts,axis=0)
    plt.axis( pts.T.ravel() )

tellme('All Done!')
plt.show()
