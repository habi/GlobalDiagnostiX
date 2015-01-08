# -*- coding: utf-8 -*-

"""
Script to undistort camera images, based on checkerboard pattern.
The script is based on [the OpenCV-Python tutorials](http://is.gd/KhTOuX) and
the [OpenCV Python samples](http://git.io/dydjBQ)

The script *needs* the example images left*.jpg found in opencv/samples/cpp or
available for download [here](http://git.io/MDUBRw).
"""

import numpy as np
import cv2
import glob
import matplotlib.pylab as plt

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1)

# Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
# 3d point in real world space
objpoints = []
# 2d points in image plane.
imgpoints = []

images = glob.glob('left*.jpg')

if not len(images):
    print 'Download left*.jpg from http://git.io/MDUBRw and save these', \
        'images in the same folder as this script'

plt.figure(figsize=[16,9])
for counter, fname in enumerate(images):
    print 'processing %s...' % fname
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners. We *have* to give the pattern size to look
    # for.
    patternsize = (7,6)
    found, corners = cv2.findChessboardCorners(gray, patternsize)

    # If found, add object points, image points (after refining them)
    if found:
        # find more precise points
        cv2.cornerSubPix(gray,corners,(5,5),(-1,-1),criteria)

        imgpoints.append(corners.reshape(-1,2))
        objpoints.append(objp)

        # Draw and display the corners
        cv2.drawChessboardCorners(img, (7,6), corners, found)
    plt.subplot(3,5,counter+1)
    plt.imshow(img)
    plt.title(fname)
    plt.axis('off')
plt.show()

rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape, None, None)
print "RMS:", rms
print "camera matrix:\n", camera_matrix
print "distortion coefficients: ", dist_coefs.ravel()

plt.figure(figsize=[16,9])
for counter, fname in enumerate(images):
    print 'undistorting %s...' % fname
    img = cv2.imread(fname)
    h,  w = img.shape[:2]
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(camera_matrix,dist_coefs,(w,h),1,(w,h))

    # undistort
    dst = cv2.undistort(img, camera_matrix, dist_coefs, None, newcameramtx)

    plt.subplot(3,5,counter+1)
    plt.imshow(dst)
    plt.title(fname)
    plt.axis('off')
plt.show()
