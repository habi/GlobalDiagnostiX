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
    images = glob.glob(os.path.join(BaseDir, '*.png'))
else:
    BaseDir = '/afs/psi.ch/project/EssentialMed/Dev/Demonstrator'
    images = glob.glob(os.path.join(BaseDir, 'left*.jpg'))

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1)

# We *have* to give the pattern size to look for.
# This is the number of visible chess board "inner edges", i.e. number of
# rows and columns -1.
# For the sample images (LoadOmmatidiag = False) (7,6) is good.
# For LoadOmmatidiag we see something with (4,3)
if LoadOmmatidiag:
    PatternSize = (8, 5)
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

if not len(images):
    print 'Download left*.jpg from http://git.io/MDUBRw and save these', \
        'images in the same folder as this script'
    exit('FilesNotFound')

plt.figure('Original images', figsize=[16, 9])
for counter, FileName in enumerate(images):
    print 'processing %s...' % FileName
    Image = cv2.imread(FileName)
    Image_BW = cv2.cvtColor(Image, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners.
    Found, Corners = cv2.findChessboardCorners(Image_BW, PatternSize)

    # If found, refine the image points, add them to their lists and draw
    # the chessboard corners on the images
    if Found:
        # Find more precise points. The fist tuple influences the side length
        # of the search window. The second tuple is the dead region in the
        # middle of the search zone, see http://is.gd/xm6SXi
        cv2.cornerSubPix(Image_BW, Corners, (10, 10), (-1, -1), criteria)
        ImagePoints.append(Corners)
        RealWorldPoints.append(ObjectPoints)
        cv2.drawChessboardCorners(Image, PatternSize, Corners, Found)
    plt.subplot(3, 5, counter + 1)
    plt.imshow(Image)
    plt.title(os.path.basename(FileName))
    plt.axis('off')

RMS, CameraMatrix, DistortionCoefficients, rvecs, tvecs = \
    cv2.calibrateCamera(RealWorldPoints, ImagePoints, Image_BW.shape, None,
                        None)

plt.figure('Undistorted images', figsize=[16, 9])
for counter, FileName in enumerate(images):
    print 'undistorting %s...' % FileName
    Image = cv2.imread(FileName)
    NewCameraMatrix, ROI = \
        cv2.getOptimalNewCameraMatrix(CameraMatrix, DistortionCoefficients,
                                      (Image.shape[1], Image.shape[0]), 1,
                                      (Image.shape[1], Image.shape[0]))

    # Undistort images
    UndistorImage = cv2.undistort(Image, CameraMatrix, DistortionCoefficients,
                                  None, NewCameraMatrix)

    plt.subplot(3, 5, counter + 1)
    plt.imshow(UndistorImage)
    plt.title(os.path.basename(FileName))
    plt.axis('off')
plt.show()


print "RMS:", RMS
print "camera matrix:\n\t", CameraMatrix
print "distortion coefficients: ", DistortionCoefficients.ravel()

print len(RealWorldPoints), 'real world points and', len(ImagePoints), \
    'image points found.'