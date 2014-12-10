#!/usr/bin/python

"""
Script to plot line on TIFF, useful for 'calculating' the best focus of
the EssentialMed Setup. Since the objective doesn't really have the focal
distance Edmund optics stated...
Reads TIFF-Stack with images from focus shifting on the LINOS-rail. Plots
a line (coordinates read from a txt-File, see around line 45) on the
'original' image and generates a lineplot from this line side by side
with the slice. Opens fiji with all images in the end so we can easily
browse through all those slices and find the best focus...
"""

import libtiff
import matplotlib.pylab as plt
import linecache
import os

# Setup
# All Apertures, "mixed media" on the intensifying screen
#~ Series = 2
# Only extreme Apertures, only Siemens-Star
Series = 3

# Leave '0' for 'natural' length of plot axis. Set to a value if scaling is
# desired
ScaleAxis = 600

# Just plot a horizontal line in the middle of the images (or shifted by YSHIFT
# below). If set to zero, Coordinates are read from file.
SimpleHorizontalLine = 0
# Shift this many pixels up from 1024, the middle of the image (Only used if
# plotting SimpleHorizontalLine)
YSHIFT = -50

if Series == 2:
    Apertures = [1.8, 4, 8, 16]
elif Series == 3:
    Apertures = [1.8, 16]

# The trick with the [-X:] loads only the X last entries of the Aperture-List.
for F in Apertures[-4:]:
    # Open tiff file
    tif = libtiff.TIFFfile('/afs/psi.ch/project/EssentialMed/Images/' +
        str(Series) + '-FocusTest/Series_F' + str('%04.1f' % F) + '.tif')
    #~ plt.ion()
    for i in range(0, len(tif.pages)):
        plt.figure(figsize=(16, 8))
        plt.subplots_adjust(left=None, bottom=None, right=None, top=None,
            wspace=None, hspace=None)
        # Add first subplot with Original Image and plot the line where we take
        # the lineprofile
        ax1 = plt.subplot(121)
        ax1.imshow(tif.asarray(key=i), cmap=plt.cm.gray)
        ax1.set_xlim([0, 2048])
        ax1.set_ylim([2048, 0])
        axis('off')
        if SimpleHorizontalLine == 1:
            ax1.plot([0 + 400, 2048 - 400], [1024 - YSHIFT, 1024 - YSHIFT],
                'r')
            # Cheat with 'line', so we have something to write at the end...
            line = 'asdf ' + str(0 + 400) + ' ' + str(1024 - YSHIFT) + ' ' + \
                str(2048 - 400) + ' ' + str(1024 - YSHIFT)
        else:
            # Reads coordinates from a text file which will then be used to
            # plot stuff on images.
            # '+2' since we have two headerlines '+1' since python starts at
            # line 0 :)
            line = linecache.getline('/afs/psi.ch/project/EssentialMed/' +
                'Images/Coordinates_UpInStar.txt', i + 3)
            line = linecache.getline('/afs/psi.ch/project/EssentialMed/' +
                'Images/Coordinates_Arbitrary.txt', i + 3)
            line = linecache.getline('/afs/psi.ch/project/EssentialMed/' +
                'Images/Coordinates_LowerLine.txt', i + 3)
            ax1.plot([line.split()[1], line.split()[3]],
                     [line.split()[2], line.split()[4]], 'r')
        plt.title('Image ' + str(i))
        # Plot Lineprofile
        ax2 = plt.subplot(122)
        if SimpleHorizontalLine == 1:
            ax2.plot(tif.asarray(key=i)[1024 - YSHIFT, 0 + 400:2048 - 400])
        else:
            ax2.plot(tif.asarray(key=i)[str(line.split()[2]),
                int(line.split()[1]):int(line.split()[3])])
        if ScaleAxis == 0:
            # scale x-axis of lineplot to real length
            ax2.set_xlim([0, (int(line.split()[3]) - int(line.split()[1]))])
        else:
            # scale x-axis of lineplot to the same length for all plots
            ax2.set_xlim([0, ScaleAxis])
        # Adapt to Brightness
        if F == 1.8:
            if Series == 2:
                ax2.set_ylim([0, 256])
            else:
                ax2.set_ylim([0, 256])
        # Only for Series 2...
        elif F == 4:
            ax2.set_ylim([0, 180])
        # Only for Series 2...
        elif F == 8:
            ax2.set_ylim([0, 250])
        elif F == 16:
            if Series == 2:
                ax2.set_ylim([0, 75])
            else:
                ax2.set_ylim([0, 256])
        plt.title('Line length: ' +
            str(int(line.split()[3]) - int(line.split()[1])))
        plt.draw()
        SaveName = '/afs/psi.ch/project/EssentialMed/Images/' + \
            str(Series) + '-FocusTest/F' + str('%04.1f' % F) + '/F' + \
            str('%04.1f' % F) + '_Image_' + str('%02d' % i) + \
            '_LineProfile_from_' + str(line.split()[1]) + '_to_' + \
            str(line.split()[3]) + '_on_height_' + str(line.split()[2]) + \
            '.png'
        savefig(SaveName)
        print 'Figure ' + str(i) + ' saved to ' + SaveName
        plt.close()

    # View the figures we just saved as stack in Fiji
    viewcommand = '/scratch/Apps/Fiji.app/fiji-linux ' +\
            '/afs/psi.ch/project/EssentialMed/Images/' + str(Series) + \
            '-FocusTest/F' + str('%04.1f' % F) + '/F* &'
    os.system(viewcommand)
