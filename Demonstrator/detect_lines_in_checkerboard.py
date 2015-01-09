# -*- coding: utf-8 -*-

"""
Script to detect horizontal and vertical lines on a sliding window along images
The script is based on the answers to
[this Stack Overflow question](http://stackoverflow.com/q/7227074/323100)
"""

import matplotlib
import matplotlib.pylab as plt
import os
import cv2
import math

BasePath = '/afs/psi.ch/project/EssentialMed/Images/DetectorElectronicsTests/' \
           'EssentialLab/Valerie'

tcpIpPool = ['192.168.1.31', '192.168.1.32', '192.168.1.33', '192.168.1.34',
             '192.168.1.35', '192.168.1.36', '192.168.1.37', '192.168.1.38',
             '192.168.1.39', '192.168.1.40', '192.168.1.41', '192.168.1.42']

ImageName = tcpIpPool[0] + '.png'

plt.figure(figsize=[16, 9])

InputImage = cv2.imread(os.path.join(BasePath, ImageName))

RegionSize = 200
for i in range(1, InputImage.shape[1] - RegionSize, 50):
    plt.clf()
    plt.suptitle(' '.join(['Region of size', str(RegionSize),
                           'starting at px.', str(i)]))
    img = InputImage[:, i:i + 200, :]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 80, 120)
    lines = cv2.HoughLinesP(cv2.flip(edges, flipCode=0), 1, math.pi / 2, 2,
                            None, 30, 1)
    for line in lines[0]:
        pt1 = (line[0], line[1])
        pt2 = (line[2], line[3])

    plt.subplot(141)
    plt.imshow(InputImage, interpolation='none')
    window = matplotlib.patches.Rectangle((i, 0), RegionSize,
                                          InputImage.shape[0], color='blue',
                                          alpha=0.25)
    plt.gca().add_patch(window)
    plt.axvline(x=i)
    plt.axvline(x=i + 200)
    plt.title('Sliding window along image')
    plt.subplot(142)
    plt.imshow(gray, interpolation='none', cmap='gray')
    plt.title('Grayscale image')
    plt.subplot(143)
    plt.imshow(edges, interpolation='none', cmap='gray')
    plt.title('Edges')
    plt.subplot(144)
    plt.imshow(cv2.flip(gray, flipCode=0), interpolation='none', cmap='gray')
    for coordinates in lines[0]:
        plt.plot([coordinates[0], coordinates[2]],
                 [coordinates[1], coordinates[3]], color='y', linestyle='-',
                 linewidth='5', alpha=0.5)
        plt.plot([coordinates[0], coordinates[2]],
                 [coordinates[1], coordinates[3]], color='k', linestyle='-')
    plt.xlim([0, img.shape[1]])
    plt.ylim([0, img.shape[0]])
    plt.title('Detected horizontal\nand vertical lines')
    plt.pause(0.001)
plt.show()
