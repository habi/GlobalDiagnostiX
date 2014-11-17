# -*- coding: utf-8 -*-

"""
Script to load the set of images acquired in the x-ray lab.
Since we acquire images before, during and after exposure it is really annoying
to manually sift through all the images in all the directories and to look for
the 'best' exposure.
This script loads each image in each directory, computes the mean of the images
and gives out the maximum of the this mean. This should be the 'best' exposed
image(s) of all the exposures.
"""

from __future__ import division
import glob
import os
import matplotlib
import matplotlib.pyplot as plt
import numpy
import sys
import time
import scipy.misc  # for saving png or tif at the end

import functions


# Setup
# If Manual selection is true, the user is asked to select one of the
# experiment IDs manually, otherwise the script just goes through all the IDs
# it finds in the starting folder
ManualSelection = False
SaveOutputImages = True

# Where shall we start?
if 'linux' in sys.platform:
    # Where shall we start?
    RootFolder = ('/afs/psi.ch/project/EssentialMed/MasterArbeitBFH/' +
        'XrayImages')
    case = 3
    if case == 1:
        # Look for images of only one scintillator
        StartingFolder = os.path.join(RootFolder, 'AppScinTech-HE')
        #~ StartingFolder = os.path.join(RootFolder, 'Hamamatsu')
        #~ StartingFolder = os.path.join(RootFolder, 'Pingseng')
        #~ StartingFolder = os.path.join(RootFolder, 'Toshiba')
    elif case == 2:
        # Look through all folders
        StartingFolder = RootFolder
    elif case == 3:
        # Ask for what to do
        Scintillators = ('AppScinTech-HE', 'Pingseng', 'Hamamatsu', 'Toshiba')
        Sensors = ('AR0130', 'AR0132', 'MT9M001')
        Lenses = ('Computar-11A', 'Framos-DSL219D-650-F2.0',
            'Framos-DSL224D-650-F2.0', 'Framos-DSL311A-NIR-F2.8',
            'Framos-DSL949A-NIR-F2.0', 'Lensation-CHR4020',
            'Lensation-CHR6020', 'Lensation-CM6014N3', 'Lensation-CY0614',
            'TIS-TBL-6C-3MP', '')
        ChosenScintillator = functions.AskUser(
            'Which scintillator do you want to look at?', Scintillators)
        ChosenSensor = functions.AskUser(
            'Which sensor do you want to look at?', Sensors)
        ChosenLens = functions.AskUser(
            'Which lens do you want to look at? ("empty" = "all")',
            Lenses)
        StartingFolder = os.path.join(RootFolder, ChosenScintillator,
            ChosenSensor, ChosenLens)
else:
    # If running on Ivans machine, look on the connected harddisk
    StartingFolder = ('/Volumes/WINDOWS/Aptina/Hamamatsu/AR0130/Computar-11A/')
    StartingFolder = ('/Volumes/exFAT')

# Testing
# StartingFolder = os.path.join(RootFolder, '20140731', 'Toshiba', 'AR0132',
    # 'Lensation-CHR6020')
# Testing


def normalizeImage(image, depth=256, verbose=False):
    """Normalize image to chosen bit depth"""
    if verbose:
        print 'Normalizing image from [' + str(numpy.min(image)) + ':' + \
            str(numpy.max(image)) + '] to',
    normalizedimage = ((image - numpy.min(image)) *
        ((depth) / (numpy.max(image) - numpy.min(image))))
    if verbose:
        print '[' + str(numpy.min(normalizedimage)) + ':' + \
            str(numpy.max(normalizedimage)) + ']'
    return normalizedimage


def contrast_stretch(image, verbose=False):
    """
    Clip image histogram to the mean \pm two standard deviation, according to
    http://is.gd/IBV4Gw "The (few) values falling outside 1 or 2 standard
    deviations may usually be discarded (histogram trimming) without serious
    loss of prime data.
    I looked at the images, and 1/2 seems too harsh. I'm using 3 STD to clip
    the images
    """
    if verbose:
        print 'Clipping image from [' + str(numpy.min(image)) + ':' + \
            str(numpy.max(image)) + '] to',
    clippedimage = numpy.clip(image,
                              numpy.mean(image) - (3 * numpy.std(image)),
                              numpy.mean(image) + (3 * numpy.std(image)))
    if verbose:
        print '[' + str(numpy.min(clippedimage)) + ':' + \
            str(numpy.max(clippedimage)) + ']'
    return normalizeImage(clippedimage)

# Look for all folders matching the naming convention
Experiment, ExperimentID = functions.get_experiment_list(StartingFolder)
print 'I found', len(Experiment), 'experiment IDs in', StartingFolder

# Get list of files in each folder, these are all the radiographies we acquired
# The length of this list is then obviously the number of radiographies
Radiographies = [sorted(glob.glob(os.path.join(Folder, '*.raw')))
                 for Folder in Experiment]
NumberOfRadiographies = [len(Radiographies[i])
                         for i in range(len(Experiment))]

# Warn if a directory is empty, i.e. contains 0 NumberOfRadiographies
# This most probably happened if DevWare crashed
EmptyOnes = [item == 0 for item in NumberOfRadiographies]
for counter, i in enumerate(Experiment):
    if EmptyOnes[counter]:
        print
        print 'Empty directory', i, 'found!'
        os.rmdir(i)
        exit(' '.join(['I deleted this folder, just start again. I will',
            'proceed or delete the next empty folder...']))

AnalyisList = []
if ManualSelection:
    # Ask the user which experimentID to show
    ## Concatenate the list for display purposes:
    ## http://stackoverflow.com/a/22642307/323100
    Choices = ['{} with {} images'.format(x, y)
               for x, y in zip(ExperimentID, NumberOfRadiographies)]
    Choice = functions.AskUser('Which one do you want to look at?', Choices)
    AnalyisList.append(Choices.index(Choice))
    print
    plt.ion()
else:
    AnalyisList = range(len(Experiment))

# Go through each selected experiment
for Counter, SelectedExperiment in enumerate(AnalyisList):
    # Inform the user and start logging
    print 80 * '-'
    print str(Counter + 1) + '/' + str(len(AnalyisList)) + \
        ': Looking at experiment', ExperimentID[SelectedExperiment]
    # See if DarkDeleter.py was already run on this experiment
    DarkDeleterLog = os.path.join(
        os.path.dirname(Experiment[SelectedExperiment]),
        ExperimentID[SelectedExperiment] + '.deletion.log')
    if os.path.isfile(DarkDeleterLog):
        DoAnalyze = False
        # Did we really delete them? If not, we can repeat the analysis
        for line in open(DarkDeleterLog, 'r'):
            # The last line of the log file tells us if we did it or not...
            if 'Set "ReallyRemove"' in line:
                print 'We have a deletion log file, but did not actually', \
                    'delete the files. Proceeding...'
                DoAnalyze = True
    else:
        DoAnalyze = True
    if not DoAnalyze:
        # If we removed some files it doesn't make sense to redo the analysis
        print
        print '\tWe already ran DarkDeleter.py on experiment', \
            ExperimentID[SelectedExperiment]
        print '\tWe thus do not analyze it again.'
        print '\tTake a look at', os.path.join(
            os.path.dirname(Experiment[SelectedExperiment])
                [len(StartingFolder) + 1:],
            ExperimentID[SelectedExperiment] + '.analysis.log'), \
                'for more info'
        print
    else:
        # Otherwise do all the work now!
        logfile = functions.myLogger(os.path.dirname(
            Experiment[SelectedExperiment]),
            ExperimentID[SelectedExperiment] + '.analysis.log')
        logfile.info('Log file for Experiment ID %s, Analsyis performed on %s',
            ExperimentID[SelectedExperiment],
            time.strftime('%d.%m.%Y at %H:%M:%S'))
        logfile.info('\nMade with "%s" at Revision %s\n',
            os.path.basename(__file__), functions.get_git_hash())
        logfile.info(80 * '-')
        logfile.info('All image files are to be found in %s', StartingFolder)
        logfile.info('This experiment ID can be found in the subfolder %s',
            Experiment[SelectedExperiment][len(StartingFolder):])
        logfile.info(80 * '-')

        # Grab the information from the filenames
        Scintillator = Radiographies[SelectedExperiment][0].split('_')[1]
        Sensor = Radiographies[SelectedExperiment][0].split('_')[2]
        Size = [int(Radiographies[SelectedExperiment][0].split('_')[3].
            split('x')[1]),
                int(Radiographies[SelectedExperiment][0].split('_')[3].
            split('x')[0])]
        Lens = Radiographies[SelectedExperiment][0].split('_')[4]
        SCD = int(Radiographies[SelectedExperiment][0].split('_')[5][:-5])
        Modality = Radiographies[SelectedExperiment][0].split('_')[6]
        Voltage = \
            float(Radiographies[SelectedExperiment][0].split('_')[7][:-2])
        mAs = float(Radiographies[SelectedExperiment][0].split('_')[8][:-3])
        SourceExposuretime = \
            float(Radiographies[SelectedExperiment][0].split('_')[9][:-6])
        CMOSExposuretime = \
            float(Radiographies[SelectedExperiment][0].split('_')[10][:-6])

        # Inform the user some more and log some more
        print '    * with', NumberOfRadiographies[SelectedExperiment], \
            'images'
        print '    * in the folder', \
            os.path.dirname(Experiment[SelectedExperiment])
        print '    * conducted with the', Scintillator, 'scintillator,'
        print '    *', Sensor, 'CMOS with an exposure time of', \
            CMOSExposuretime, 'ms'
        print '    * source exposure time of', SourceExposuretime, 'ms'
        print '    *', Lens, 'lens for the'
        print '    *', Modality, 'and calculating their mean'

        logfile.info('Scintillator: %s', Scintillator)
        logfile.info('Sensor: %s', Sensor)
        logfile.info('Lens: %s', Lens)
        logfile.info('Image size: %s x %s px', Size[1], Size[0])
        logfile.info('Scintillator-Sensor distance: %s mm', SCD)
        logfile.info('Modality: %s', Modality)
        logfile.info('Source kV: %s', Voltage)
        logfile.info('Source mAs: %s', mAs)
        logfile.info('Source exposure time: %s ms', SourceExposuretime)
        logfile.info('CMOS exposure time: %s ms', CMOSExposuretime)
        logfile.info(80 * '-')

        # Read images and calculate max, mean, STD and dark/img-threshold
        print 'Reading images,',
        Images = [numpy.fromfile(Image, dtype=numpy.uint16).reshape(Size)
                     for Image in Radiographies[SelectedExperiment]]
        # Zero out a small outer region of each image, since we have some
        # DevWare information in this region. These values change the max and
        # mean.
        padwidth = 3
        for counter in range(len(Images)):
            # left
            Images[counter][:, :padwidth] = 0
            # right
            Images[counter][:, -padwidth:] = 0
            # top
            Images[counter][:padwidth, :] = 0
            # bottom
            Images[counter][-padwidth:, :] = 0
        print 'calculating max,',
        ImageMax = [numpy.max(i) for i in Images]
        print 'calculating mean',
        ImageMean = [numpy.mean(i) for i in Images]
        print 'and standard deviation'
        ImageSTD = [numpy.std(i) for i in Images]
        Threshold = numpy.min(ImageMax) * 1.618

        # Split images in "real" and dark images
        print 'Selecting dark frames and image frames'
        RealImages = [i for i in Images if i.max() > Threshold]
        DarkImages = [i for i in Images if i.max() <= Threshold]
        logfile.info('We have')
        logfile.info(
            '\t* %s dark images (Max below or equal to Threshold of %s)',
            len(DarkImages), round(Threshold, 2))
        logfile.info('\t* %s images (Max above Threshold of %s)',
            len(RealImages), round(Threshold, 2))
        for c, Image in enumerate(Images):
            if ImageMean[c] == max(ImageMean):
                logfile.info('With image %s being the brightest one', c + 1)
                logfile.info('\t* Filename: %s',
                    os.path.basename(Radiographies[SelectedExperiment][c]))
                logfile.info('\t* Max: %s', round(ImageMax[c], 3))
                logfile.info('\t* Mean: %s', round(ImageMean[c], 3))
                logfile.info('\t* STD: %s', round(ImageSTD[c], 3))
        logfile.info(80 * '-')
        print 'From', NumberOfRadiographies[SelectedExperiment], \
            'images we selected', len(RealImages), 'above and', \
            len(DarkImages), 'images below the threshold'
        # Calculate final images
        MeanDarkImage = numpy.mean(DarkImages, axis=0)
        if len(RealImages) == 0:
            # If no image is above the selection threshold, use brightest
            print
            print '\tImage', ImageMean.index(max(ImageMean)), \
                'is the brightest image of experiment', \
                ExperimentID[SelectedExperiment]
            print '\tIts max of',  round(max(ImageMean), 2), \
                'is below the selection threshold of', round(Threshold, 2)
            print '\tIt is probably safe to delete the whole directory...'
            print '\tI am using this *single* image as "result"'
            print
            SummedImage = Images[ImageMean.index(max(ImageMean))]
            logfile.info('Using image %s with a max of %s as final image',
                ImageMean.index(max(ImageMean)) + 1,
                round(ImageMean[ImageMean.index(max(ImageMean))], 2))

        else:
            SummedImage = numpy.sum(RealImages, axis=0)
            logfile.info('Using %s images for summed final image',
                len(RealImages))
        logfile.info(80 * '-')

        # Subtract mean dark image from the summed projections, use as
        # corrected image
        CorrectedImage = SummedImage - MeanDarkImage

        # Show images to the user if desired
        logfile.info('Details of the %s images for experiment ID %s',
            NumberOfRadiographies[SelectedExperiment],
            ExperimentID[SelectedExperiment])
        plt.figure(num=1,
            figsize=(NumberOfRadiographies[SelectedExperiment], 5))
        for c, Image in enumerate(Images):
            if Image.max() > Threshold or Image.max() == max(ImageMean):
                if SaveOutputImages:
                    plt.subplot(3, len(Images), c + 1)
                logfile.info('%s/%s: Mean: %s,\tMax: %s,\tSTD: %s\t--> Image',
                    str(c + 1).rjust(2), len(Radiographies[Counter]),
                    ("%.2f" % round(ImageMean[c], 2)).rjust(6),
                    str(ImageMax[c]).rjust(4),
                    ("%.2f" % round(ImageSTD[c], 2)).rjust(6))
            else:
                plt.subplot(3, len(Images), len(Images) + c + 1)
                logfile.info('%s/%s: Mean: %s,\tMax: %s,\tSTD: %s\t--> Dark',
                    str(c + 1).rjust(2), len(Radiographies[Counter]),
                    ("%.2f" % round(ImageMean[c], 2)).rjust(6),
                    str(ImageMax[c]).rjust(4),
                    ("%.2f" % round(ImageSTD[c], 2)).rjust(6))
            plt.imshow(Image, cmap='bone', interpolation='none')
            plt.axis('off')
            plt.title(' '.join(['img', str(c), '\nmx',
                                str(round(ImageMax[c], 1)), '\nmn',
                                str(round(ImageMean[c], 1))]))
        print
        logfile.info(80 * '-')
        plt.subplot(313)
        plt.plot(ImageMax, marker='o', label='max', color='r')
        plt.plot(ImageMean, marker='o', label='mean', color='g')
        plt.plot(ImageSTD, marker='o', label='STD', color='b')
        plt.title(' '.join(['Image characteristics for an exposure time of',
            ("%.2f" % CMOSExposuretime).zfill(6), 'ms']))
        plt.axhline(Threshold, label='selection threshold', color='r',
            linestyle='--')
        plt.xlim([-0.5, NumberOfRadiographies[SelectedExperiment] - 0.5])
        plt.legend(loc='best')
        if 'linux' in sys.platform:
            plt.tight_layout()
        plt.subplots_adjust(hspace=.05)
        plt.subplots_adjust(wspace=.05)
        plt.draw()
        if SaveOutputImages:
            SaveFigName = os.path.join(os.path.dirname(
                Experiment[SelectedExperiment]),
                ExperimentID[SelectedExperiment] + '.overview.all.png')
            plt.savefig(SaveFigName)
            logfile.info('Overview plot saved as %s',
                         os.path.basename(SaveFigName))
        plt.figure(num=2, figsize=(16, 9))
        # Show average darks
        plt.subplot(231)
        plt.imshow(MeanDarkImage, cmap='bone', interpolation='none')
        plt.title(' '.join(['Average of', str(len(DarkImages)),
                            'dark images']))
        plt.subplot(234)
        plt.imshow(contrast_stretch(MeanDarkImage), cmap='bone',
            interpolation='none')
        plt.title('Contrast stretched average')
        # Show summed projections
        plt.subplot(232)
        plt.imshow(SummedImage, cmap='bone', interpolation='none')
        plt.title(' '.join([str(len(RealImages)), 'summed projections']))
        plt.subplot(235)
        plt.imshow(contrast_stretch(SummedImage), cmap='bone',
            interpolation='none')
        plt.title('Contrast stretched projections sum')
        plt.subplot(233)
        plt.imshow(CorrectedImage, cmap='bone', interpolation='none')
        plt.title(' '.join([str(len(RealImages)), 'projections -',
            str(len(DarkImages)), 'darks']))
        plt.subplot(236)
        plt.imshow(contrast_stretch(CorrectedImage), cmap='bone',
        interpolation='none')
        plt.title('Contrast stretched corrected image')
        plt.draw()
        if SaveOutputImages:
            SaveFigName = os.path.join(os.path.dirname(
                Experiment[SelectedExperiment]),
                ExperimentID[SelectedExperiment] +
                '.overview.darkflatscorrected.png')
            plt.savefig(SaveFigName)
            logfile.info('Dark/Flats/Corrected plot saved as %s',
                os.path.basename(SaveFigName))
            logfile.info(80 * '-')

        # Save final output images (dark, images, corrected)
        if SaveOutputImages:
            print 'Saving mean dark frame'
            DarkName = os.path.join(os.path.dirname(
                Experiment[SelectedExperiment]),
                ExperimentID[SelectedExperiment] + '.image.dark')
            scipy.misc.imsave(DarkName + '.png', normalizeImage(MeanDarkImage))
            scipy.misc.imsave(DarkName + '.stretched.png',
                contrast_stretch(MeanDarkImage))
            logfile.info('Average of %s dark frames saved as %s.png',
                len(DarkImages), DarkName)
            print 'Saving summed images'
            SummedName = os.path.join(os.path.dirname(
                Experiment[SelectedExperiment]),
                ExperimentID[SelectedExperiment] + '.image.sum')
            scipy.misc.imsave(SummedName + '.png', normalizeImage(SummedImage))
            scipy.misc.imsave(SummedName + '.stretched.png',
                contrast_stretch(SummedImage))
            logfile.info('Sum of %s image frames saved as %s.png',
                len(RealImages), SummedName)
            print 'Saving corrected image'
            CorrName = os.path.join(os.path.dirname(
                Experiment[SelectedExperiment]),
                ExperimentID[SelectedExperiment] + '.image.corrected')
            scipy.misc.imsave(CorrName + '.png',
                normalizeImage(CorrectedImage))
            scipy.misc.imsave(CorrName + '.stretched.png',
                contrast_stretch(CorrectedImage))
            logfile.info('Sum of %s images subtracted with the mean of %s ' +
                'dark frames saved as %s.png', len(RealImages),
                len(DarkImages), CorrName)
            logfile.info(' '.join(['\nAlso saved each image as',
                ' *.stretched.png, which is the contrast-stretched version',
                '(clipped to 3 STD around the mean of the image.']))
        if ManualSelection:
            plt.ioff()
            plt.show()
        else:
            plt.close('all')

print
print 'Analysis of', StartingFolder, 'finished'
