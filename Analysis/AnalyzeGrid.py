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
import logging
import linecache
import random

# Where shall we start?
RootFolder = ('/afs/psi.ch/project/EssentialMed/MasterArbeitBFH/' +
    'XrayImages')
#~ StartingFolder = os.path.join(RootFolder, '20140721')
#~ StartingFolder = os.path.join(RootFolder, '20140722')
#~ StartingFolder = os.path.join(RootFolder, '20140724')
#~ StartingFolder = os.path.join(RootFolder, '20140730')
#~ StartingFolder = os.path.join(RootFolder, '20140731')
#~ StartingFolder = os.path.join(RootFolder, '20140818')
StartingFolder = os.path.join(RootFolder, '20140819')
StartingFolder = os.path.join(RootFolder, '20140820')
StartingFolder = os.path.join(RootFolder, '20140822')
StartingFolder = os.path.join(RootFolder, '20140823')
#~ StartingFolder = os.path.join(RootFolder, '20140825')
#~ StartingFolder = os.path.join(RootFolder, '20140829')
#~ StartingFolder = os.path.join(RootFolder, '20140831')
#~ StartingFolder = os.path.join(RootFolder, '20140901')


# Testing
#~ StartingFolder = os.path.join(RootFolder, '20140731', 'Toshiba', 'AR0132',
    #~ 'Lensation-CHR6020')
# Testing
#~ StartingFolder = RootFolder

# Setup
# Draw lines in final plot $pad pixels longer than the selection (left & right)
pad = 25
# Draw $steps lines in the final selected ROI
steps = 6


def get_git_revision_short_hash():
    import subprocess
    hashit = subprocess.Popen(['git', 'rev-parse', '--short', 'HEAD'],
        stdout=subprocess.PIPE)
    output, error = hashit.communicate()
    return output


def tellme(blurb):
    print(blurb)
    plt.title(blurb)
    plt.draw()


def myLogger(Folder, LogFileName):
    """
    Since logging in a loop does always write to the first instaniated file,
    we make a little wrapper around the logger function to have one log file
    per experient ID. Based on http://stackoverflow.com/a/2754216/323100
    """
    logger = logging.getLogger(LogFileName)
    # either set INFO or DEBUG
    #~ logger.setLevel(logging.DEBUG)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(os.path.join(Folder, LogFileName), 'w')
    logger.addHandler(handler)
    return logger

# Generate a list of log files, based on http://stackoverflow.com/a/14798263
LogFiles = [os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(StartingFolder)
    for f in files if f.endswith('analysis.log')]

print 'I found', len(LogFiles), 'log files in', StartingFolder

# Shuffle the logfiles, to make clicking less boring...
random.shuffle(LogFiles)

# Grab all the necessary parameters from the log files
ExperimentID = \
    [linecache.getline(i, 1).split('ID')[1].split(',')[0].strip() for i in
    LogFiles]
Sensor = [linecache.getline(i, 10).split(':')[1].strip() for i in LogFiles]
Scintillator = [linecache.getline(i, 9).split(':')[1].strip()
    for i in LogFiles]
Lens = [str(linecache.getline(i, 11).split(':')[1].strip()) for i in LogFiles]
SSD = [float(linecache.getline(i, 13).split(':')[1].split('mm')[0].strip())
    for i in LogFiles]
Modality = [linecache.getline(i, 14).split(':')[1].strip()
    for i in LogFiles]
Exposuretime = [float(linecache.getline(i, 18)
    .split(':')[1].split('ms')[0].strip()) for i in LogFiles]
Max = [float(linecache.getline(i, 25).split(':')[1].strip())
    for i in LogFiles]
Mean = [float(linecache.getline(i, 26).split(':')[1].strip())
    for i in LogFiles]
STD = [float(linecache.getline(i, 27).split(':')[1].strip())
    for i in LogFiles]

# Generate folder names
Experiment = [item[:-len('.analysis.log')] for item in LogFiles]

# Go through each selected experiment (in the shuffled list)
for Counter, SelectedExperiment in enumerate(range(len(Experiment))):
    print str(Counter + 1) + '/' + str(len(Experiment)), '|', \
        ExperimentID[SelectedExperiment], '|', \
        Scintillator[SelectedExperiment], '|', Sensor[SelectedExperiment], \
        '|', Lens[SelectedExperiment]
    logfile = myLogger(os.path.dirname(Experiment[SelectedExperiment]),
        ExperimentID[SelectedExperiment] + '.resolution.log')
    logfile.info(
        'Log file for Experiment ID %s, Resolution analsyis performed on %s',
        ExperimentID[SelectedExperiment],
        time.strftime('%d.%m.%Y at %H:%M:%S'))
    logfile.info('\nMade with "%s" at Revision %s', os.path.basename(__file__),
        get_git_revision_short_hash())
    logfile.info(80 * '-')
    # either read original or contrast-stretched corrected image
    OriginalImage = plt.imread(os.path.join(
        os.path.dirname(Experiment[SelectedExperiment]),
        ExperimentID[SelectedExperiment] + '.image.corrected.png'))
    StretchedImage = plt.imread(os.path.join(
        os.path.dirname(Experiment[SelectedExperiment]),
        ExperimentID[SelectedExperiment] + '.image.corrected.stretched.png'))
    logfile.info('Loading corrected and contrast stretched corrected image')
    logfile.info(os.path.join(os.path.dirname(Experiment[SelectedExperiment]),
        ExperimentID[SelectedExperiment] + '.image.corrected.png'))
    logfile.info(os.path.join(os.path.dirname(Experiment[SelectedExperiment]),
        ExperimentID[SelectedExperiment] + '.image.corrected.stretched.png'))
    logfile.info(80 * '-')

    plt.ion()

    # Show original images with histograms
    plt.figure(' '.join([str(Counter + 1) + '/' + str(len(Experiment)), '|',
        ExperimentID[SelectedExperiment], '|',
        Scintillator[SelectedExperiment], '|', Sensor[SelectedExperiment], '|',
        Lens[SelectedExperiment], '| Originals and Histograms']),
        figsize=[16, 9])
    plt.subplot(221)
    plt.imshow(OriginalImage, cmap='bone', interpolation='nearest')
    plt.title(ExperimentID[SelectedExperiment] + '.image.corrected.png')
    plt.subplot(222)
    plt.imshow(StretchedImage, cmap='bone', interpolation='nearest')
    plt.title(ExperimentID[SelectedExperiment] +
        '.image.corrected.stretched.png')
    # Histograms
    bins = 256
    plt.subplot(223)
    plt.hist(OriginalImage.flatten(), bins, fc='k', ec='k')
    plt.subplot(224)
    plt.hist(StretchedImage.flatten(), bins, fc='k', ec='k')
    plt.tight_layout()

    # Let the user select the ROI of the resolution phantom on the contrast
    # stretched image
    plt.subplot(222)
    plt.imshow(StretchedImage, cmap='bone', interpolation='nearest')
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
        xmin = int(round(min(pts[:, 0])))
        xmax = int(round(max(pts[:, 0])))
        ymin = int(round(min(pts[:, 1])))
        ymax = int(round(max(pts[:, 1])))
        currentAxis = plt.gca()
        BigROI = currentAxis.add_patch(Rectangle((xmin, ymin), xmax - xmin,
                                                    ymax - ymin,
                                                    facecolor='red',
                                                    edgecolor='black',
                                                    alpha=0.25))
        tellme('Done? Press any key for yes, click with mouse for no')
        done = plt.waitforbuttonpress()
        # Redraw image if necessary
        if not done:
            plt.cla()
            plt.subplot(222)
            plt.imshow(StretchedImage, cmap='bone', interpolation='nearest')
    # Give plot a nice title
    BigROISize = [xmax - xmin, ymax - ymin]
    tellme(' '.join(['Selected ROI with a size of', str(BigROISize[1]), 'x',
        str(BigROISize[0]), 'px']))
    logfile.info('Resolution-Phantom x-ROI: %s-%s (%s px)', xmin, xmax,
        xmax - xmin)
    logfile.info('Resolution-Phantom y-ROI: %s-%s (%s px)', ymin, ymax,
        ymax - ymin)
    # Show selected ROI and select sub-ROI to plot the line profiles
    plt.subplot(221)
    plt.title(' '.join([ExperimentID[SelectedExperiment] +
        '.image.corrected.png with', str(BigROISize[1]), 'x',
        str(BigROISize[0]), 'px ROI']))
    currentAxis = plt.gca()
    BigROI = currentAxis.add_patch(Rectangle((xmin, ymin), xmax - xmin,
                                                    ymax - ymin,
                                                    facecolor='red',
                                                    edgecolor='black',
                                                    alpha=0.25))
    plt.subplot(222)
    CroppedImage = OriginalImage[ymin:ymax, xmin:xmax]
    CroppedImageStretched = StretchedImage[ymin:ymax, xmin:xmax]
    plt.imshow(CroppedImageStretched, cmap='bone', interpolation='none')
    plt.tight_layout()
    # Select ROI of resolution phantom.
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
        xxmin = int(round(min(pts[:, 0])))
        xxmax = int(round(max(pts[:, 0])))
        yymin = int(round(min(pts[:, 1])))
        yymax = int(round(max(pts[:, 1])))
        currentAxis = plt.gca()
        LineROI = currentAxis.add_patch(Rectangle((xxmin - pad, yymin),
                                                    xxmax - xxmin + pad + pad,
                                                    yymax - yymin,
                                                    facecolor='green',
                                                    edgecolor='black',
                                                    alpha=0.25))
        tellme('Done? Press any key for yes, click with mouse for no')
        done = plt.waitforbuttonpress()
        # Redraw image if necessary
        if not done:
            plt.cla()
            plt.subplot(222)
            plt.imshow(CroppedImageStretched, cmap='bone',
                interpolation='none')
    # Give plot a nice title
    LineROISize = [xxmax - xxmin + pad + pad, yymax - yymin]
    tellme(' '.join(['Selected ROI with a size of', str(LineROISize[1]), 'x',
        str(LineROISize[0]), 'px']))
    logfile.info(80 * '-')
    logfile.info('Selected region in Resolution-Phantom x-ROI: %s-%s (%s px)',
        xxmin, xxmax, xxmax - xxmin)
    logfile.info('Selected region in Resolution-Phantom y-ROI: %s-%s (%s px)',
        yymin, yymax, yymax - yymin)
    logfile.info(80 * '-')

    # Final plot
    plt.figure(' '.join([str(Counter + 1) + '/' + str(len(Experiment)), '|',
        ExperimentID[SelectedExperiment], '|',
        Scintillator[SelectedExperiment], '|', Sensor[SelectedExperiment], '|',
        Lens[SelectedExperiment], '| Result']), figsize=[16, 9])
    ## Original image
    plt.subplot(331)
    plt.imshow(OriginalImage, cmap='bone', interpolation='nearest')
    plt.title(' '.join([Scintillator[SelectedExperiment], '|',
        Sensor[SelectedExperiment], '|', Lens[SelectedExperiment]]))
    # Stretched image with both ROIs
    plt.subplot(332)
    plt.imshow(StretchedImage, cmap='bone', interpolation='nearest')
    plt.title(' '.join(['Selected ROIs', str(BigROISize[1]), 'x',
        str(BigROISize[0]), 'px (red) and', str(LineROISize[1]), 'x',
        str(LineROISize[0]), 'px (green).']))
    currentAxis = plt.gca()
    BigROI = currentAxis.add_patch(Rectangle((xmin, ymin), xmax - xmin,
                                                    ymax - ymin,
                                                    facecolor='red',
                                                    edgecolor='black',
                                                    alpha=0.5))
    LineROI = currentAxis.add_patch(Rectangle((xmin + xxmin - pad,
                                               ymin + yymin),
                                               xxmax - xxmin + pad + pad,
                                               yymax - yymin,
                                               facecolor='green',
                                               edgecolor='black', alpha=0.5))
    # ROI and LineROI
    plt.subplot(333)
    plt.imshow(CroppedImageStretched, cmap='bone', interpolation='none')
    currentAxis = plt.gca()
    LineROI = currentAxis.add_patch(Rectangle((xxmin - pad, yymin),
                                                xxmax - xxmin + pad + pad,
                                                yymax - yymin,
                                                facecolor='green',
                                                edgecolor='black',
                                                alpha=0.5))
    tellme(' '.join([str(BigROISize[1]), 'x', str(BigROISize[0]),
        'px ROI\nLocation of lines from plots below']))
    # Draw $steps horizontal lines in the LineROI
    # IWantHue, dark background, 10 colors, hard
    clr = ["#6B9519", "#9B46C3", "#281B32", "#F29C2F", "#F0418C", "#8DF239",
        "#EBF493", "#4680F0", "#402305", "#9F9BFD"]
    SelectedHeight = numpy.linspace(yymin, yymax, steps)
    SelectedLines = [line for line in
        [CroppedImage[int(round(height)), xxmin - pad:xxmax + pad] for height
        in SelectedHeight]]
    SelectedLinesStretched = [line for line in
        [CroppedImageStretched[int(round(height)), xxmin - pad:xxmax + pad]
        for height in SelectedHeight]]
    for c, height in enumerate(SelectedHeight):
        plt.axhline(height, linewidth=2, alpha=1, color=clr[c])
    # Plot values
    plt.subplot(312)
    for c, line in enumerate(SelectedLines):
        plt.plot(line, alpha=0.5, color=clr[c])
    plt.plot(numpy.mean(SelectedLines, axis=0), 'k', linewidth='2',
        label=' '.join(['mean of', str(steps), 'shown lines']))
    plt.xlim([0, LineROISize[0]])
    plt.ylim([0, 1])
    plt.legend(loc='best')
    plt.title(' '.join(['Brightness in the green', str(LineROISize[1]), 'x',
        str(LineROISize[0]),
        'px ROI.\nTop: original image, bottom: contrast stretched image']))
    plt.subplot(313)
    for c, line in enumerate(SelectedLinesStretched):
        plt.plot(line, alpha=0.5, color=clr[c])
    plt.plot(numpy.mean(SelectedLinesStretched, axis=0), 'k', linewidth='2',
        label=' '.join(['mean of', str(steps), 'shown lines']))
    plt.xlim([0, LineROISize[0]])
    plt.ylim([0, 1])
    plt.legend(loc='best')
    plt.tight_layout()
    logfile.info('Mean brightness along %s equally spaced lines in ROI', steps)
    for i in numpy.mean(SelectedLines, axis=0):
        logfile.info(i)
    logfile.info(80 * '-')

    SaveName = os.path.join(os.path.dirname(Experiment[SelectedExperiment]),
        ExperimentID[SelectedExperiment] + '.resolution.png')

    plt.draw()
    plt.ioff()
    plt.savefig(SaveName)
    print 'Figure saved as', SaveName
    print 80 * '-'

    #~ time.sleep(1)
    plt.close('all')
