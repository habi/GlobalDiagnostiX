# -*- coding: utf-8 -*-

"""
Script to undistort camera images, based on checkerboard pattern.
The script is based on [the OpenCV-Python tutorials](http://is.gd/KhTOuX) and
the [OpenCV Python samples](http://git.io/dydjBQ)

The script *needs* the example images left*.jpg found in opencv/samples/cpp or
available for download [here](http://git.io/MDUBRw).
"""

import os
import numpy
import cv2
import glob
import matplotlib.pylab as plt

LoadOmmatidiag = True

if LoadOmmatidiag:
    BaseDir = '/afs/psi.ch/project/EssentialMed/Images' \
              '/DetectorElectronicsTests/EssentialLab/Valerie'
    OriginalsList = glob.glob(os.path.join(BaseDir, '???.???.?.??.png'))
    ImageList = glob.glob(os.path.join(BaseDir, '*_edit.jpg'))
else:
    BaseDir = '/afs/psi.ch/project/EssentialMed/Dev/Demonstrator'
    ImageList = glob.glob(os.path.join(BaseDir, 'left*.jpg'))
    OriginalsList = ImageList

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 0.001)

# We *have* to give the pattern size to look for.
# This is the number of visible chess board "inner edges", i.e. number of
# rows and columns -1.
# For the sample images (LoadOmmatidiag = False) (7,6) is good.
# For the edited checkerboard images, we use (5, 4).
# See http://dasl.mem.drexel.edu/~noahKuntz/openCVTut10.html for counting :)
if LoadOmmatidiag:
    PatternSize = (3, 3)
else:
    PatternSize = (7, 6)
# Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ...., (6,5,0)
ObjectPoints = numpy.zeros((PatternSize[1] * PatternSize[0], 3), numpy.float32)
ObjectPoints[:, :2] = numpy.mgrid[0:PatternSize[0],
                                  0:PatternSize[1]].T.reshape(-1, 2)

# Arrays to store object points and image points from all the images.
# 3d point in real world space
RealWorldPoints = []
# 2d points in image plane.
ImagePoints = []

if not ImageList:
    print 'Download left*.jpg from http://git.io/MDUBRw and save these', \
        'images in the same folder as this script'
    exit('FilesNotFound')

plt.figure('Original images', figsize=[16, 9])
for counter, FileName in enumerate(ImageList):
    print 'processing %s...' % FileName
    Image = cv2.imread(FileName)
    # Image = cv2.GaussianBlur(Image, (11, 11), 0)
    Image_BW = cv2.cvtColor(Image, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners.
    Found, Corners = cv2.findChessboardCorners(Image_BW, PatternSize)

    # If found, refine the image points, add them to their lists and draw
    # the chessboard corners on the images
    if Found:
        print 'Found pattern!'
        # Find more precise corner points. The fist tuple influences the side
        # length of the search window. The second tuple is the dead region in
        # the middle of the search zone, see http://is.gd/xm6SXi
        cv2.cornerSubPix(Image_BW, Corners, (30, 30), (-1, -1), criteria)
        ImagePoints.append(Corners)
        RealWorldPoints.append(ObjectPoints)
        cv2.drawChessboardCorners(Image, PatternSize, Corners, Found)
    plt.subplot(3, 5, counter + 1)
    plt.imshow(Image)
    ImageTitle = os.path.basename(FileName)
    if Found:
        ImageTitle = '\n'.join(('Pattern found on', ImageTitle))
    plt.title(ImageTitle)
    plt.axis('off')

if not ImagePoints:
    print 'I was not able to find a pattern on any image, maybe tray another ' \
          '"PatternSize"...'
    exit('PatternNotFound')

print '\nApplying undistortion parameters found on %s images to %s ' \
      'Orignals\n' % (len(ImagePoints), len(OriginalsList))

# Calibrate camera if points are found
RMS, CameraMatrix, DistortionCoefficients, rvecs, tvecs = \
    cv2.calibrateCamera(RealWorldPoints, ImagePoints, Image_BW.shape, None,
                        None)

# Display images
plt.figure('Undistorted images', figsize=[16, 9])
for counter, FileName in enumerate(OriginalsList):
    print 'undistorting %s...' % FileName
    Image = cv2.imread(FileName)
    NewCameraMatrix, ROI = \
        cv2.getOptimalNewCameraMatrix(CameraMatrix, DistortionCoefficients,
                                      (Image.shape[1], Image.shape[0]), 1,
                                      (Image.shape[1], Image.shape[0]))

    # Undistort images
    UndistortedImage = cv2.undistort(Image, CameraMatrix,
                                     DistortionCoefficients, None,
                                     NewCameraMatrix)
    plt.imsave(FileName[:-4] + '_undistort.png', UndistortedImage)
    plt.subplot(3, 5, counter + 1)
    plt.imshow(UndistortedImage)
    plt.title(os.path.basename(FileName))
    plt.axis('off')

print "RMS:", RMS
print "camera matrix:\n\t", CameraMatrix
print "distortion coefficients: ", DistortionCoefficients.ravel()

print 'Checkerboard pattern found on', len(ImagePoints), 'images'

plt.show()