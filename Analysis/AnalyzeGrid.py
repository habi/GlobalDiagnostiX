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


# Where shall we start?
RootFolder = ('/afs/psi.ch/project/EssentialMed/MasterArbeitBFH/' +
    'XrayImages')
#~ StartingFolder = os.path.join(RootFolder, '20140721')
#~ StartingFolder = os.path.join(RootFolder, '20140722')
#~ StartingFolder = os.path.join(RootFolder, '20140724')
#~ StartingFolder = os.path.join(RootFolder, '20140730')
#~ StartingFolder = os.path.join(RootFolder, '20140731')
#~ StartingFolder = os.path.join(RootFolder, '20140818')
#~ StartingFolder = os.path.join(RootFolder, '20140819')
#~ StartingFolder = os.path.join(RootFolder, '20140820')
#~ StartingFolder = os.path.join(RootFolder, '20140822')
#~ StartingFolder = os.path.join(RootFolder, '20140823')
StartingFolder = os.path.join(RootFolder, '20140825')

#~ # Testing
#~ StartingFolder = os.path.join(RootFolder, '20140724', 'Pingseng', 'MT9M001',
    #~ 'Lensation-CHR6020', 'Lung')
#~ # Testing
#~ StartingFolder = RootFolder


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

# Look for all folders matching the naming convention
Experiment = []
ExperimentID = []
for root, dirs, files in os.walk(StartingFolder):
    #~ print 'Looking for experiment IDs in folder', os.path.basename(root)
    if len(os.path.basename(root)) == 7 and \
        not 'Toshiba' in os.path.basename(root) and \
        not 'MT9' in os.path.basename(root) and \
        not 'AR0' in os.path.basename(root):
        Experiment.append(root)
        ExperimentID.append(os.path.basename(root))

print 'I found', len(Experiment), 'experiment IDs in', StartingFolder
print 80 * '-'

AnalyisList = range(len(Experiment))

# Go through each selected experiment
for Counter, SelectedExperiment in enumerate(AnalyisList):
    print str(Counter + 1) + '/' + str(len(Experiment))
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

    plt.figure(ExperimentID[SelectedExperiment], figsize=[16, 9])
    # Show Images
    plt.subplot(221)
    plt.imshow(OriginalImage, cmap='bone', interpolation='nearest')
    plt.title('Original')
    plt.subplot(222)
    plt.imshow(StretchedImage, cmap='bone', interpolation='nearest')
    plt.title('Contrast stretched')
    # Histograms
    plt.subplot(223)
    plt.hist(OriginalImage.flatten(), 64)
    plt.subplot(224)
    plt.hist(StretchedImage.flatten(), 64)
    #~ plt.xlim([0, 256])
    plt.tight_layout()

    plt.figure(' '.join([str(Counter + 1) + '/' + str(len(Experiment)),
        'Selection']), figsize=[23, 9])
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
        xmin = int(round(min(pts[:, 0])))
        xmax = int(round(max(pts[:, 0])))
        ymin = int(round(min(pts[:, 1])))
        ymax = int(round(max(pts[:, 1])))
        currentAxis = plt.gca()
        rectangle = currentAxis.add_patch(Rectangle((xmin, ymin), xmax - xmin,
                                                    ymax - ymin,
                                                    facecolor='red',
                                                    edgecolor='black',
                                                    alpha=0.25))
        tellme('Done? Press any key for yes, click with mouse for no')
        done = plt.waitforbuttonpress()
        # Redraw image if necessary
        if not done:
            plt.cla()
            plt.subplot(121)
            plt.imshow(StretchedImage, cmap='bone', interpolation='nearest')
    # Give plot a nice title
    ROISize = [xmax - xmin, ymax - ymin]
    tellme(' '.join(['Selected ROI with a size of', str(ROISize[1]), 'x',
        str(ROISize[0]), 'px']))
    logfile.info('Resolution-Phantom x-ROI: %s-%s (%s px)', xmin, xmax,
        xmax - xmin)
    logfile.info('Resolution-Phantom y-ROI: %s-%s (%s px)', ymin, ymax,
        ymax - ymin)
    # Show selected ROI
    plt.subplot(322)
    CroppedImage = StretchedImage[ymin:ymax, xmin:xmax]
    plt.imshow(CroppedImage, cmap='bone', interpolation='none')
    tellme(' '.join(['ROI:', str(xmax - xmin), 'x', str(ymax - ymin), 'px']))
    plt.tight_layout()
    # Select ROI of resolution phantom. Afterwards we draw $steps horizontal
    # lines in a region $pad px bigger than the selected ROI
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
        xmin = int(round(min(pts[:, 0])))
        xmax = int(round(max(pts[:, 0])))
        ymin = int(round(min(pts[:, 1])))
        ymax = int(round(max(pts[:, 1])))
        currentAxis = plt.gca()
        rectangle = currentAxis.add_patch(Rectangle((xmin - pad, ymin),
                                                    xmax - xmin + pad + pad,
                                                    ymax - ymin,
                                                    facecolor='red',
                                                    edgecolor='black',
                                                    alpha=0.25))
        tellme('Done? Press any key for yes, click with mouse for no')
        done = plt.waitforbuttonpress()
        # Redraw image if necessary
        if not done:
            plt.cla()
            plt.subplot(322)
            plt.imshow(CroppedImage, cmap='bone', interpolation='none')
    # Give plot a nice title
    ROISize = [xmax - xmin + pad + pad, ymax - ymin]
    tellme(' '.join(['Selected ROI with a size of', str(ROISize[1]), 'x',
        str(ROISize[0]), 'px and location of lines from plot below']))
    logfile.info('Selected region in Resolution-Phantom x-ROI: %s-%s (%s px)',
        xmin, xmax, xmax - xmin)
    logfile.info('Selected region in Resolution-Phantom y-ROI: %s-%s (%s px)',
        ymin, ymax, ymax - ymin)
    logfile.info(80 * '-')

    # draw $steps horizontal lines $pad px around the selected one
    # IWantHue, dark background, 10 colors, hard
    clr = ["#6B9519", "#9B46C3", "#281B32", "#F29C2F", "#F0418C", "#8DF239",
        "#EBF493", "#4680F0", "#402305", "#9F9BFD"]
    Phantom = numpy.empty(shape=((xmax + pad) - (xmin - pad), steps))
    SelectedHeight = numpy.linspace(ymin, ymax, steps)
    SelectedLines = [line for
        line in [CroppedImage[int(round(height)), xmin - pad:xmax + pad] for
        height in SelectedHeight]]

    plt.subplot(322)
    for c, height in enumerate(SelectedHeight):
        plt.axhline(height, linewidth=4, alpha=0.5, color=clr[c])
    plt.subplot(324)
    for c, line in enumerate(SelectedLines):
        plt.plot(line, alpha=0.5, color=clr[c])
    plt.plot(numpy.mean(SelectedLines, axis=0), 'k', linewidth='2',
        label=' '.join(['mean of', str(steps), 'shown lines']))
    plt.xlim([0, xmax + pad - xmin - pad])
    plt.ylim([0, 256])
    plt.legend(loc='best')
    plt.title('Brightness in the red ROI shown above')
    plt.subplot(326)
    for c, line in enumerate(SelectedLines):
        plt.plot(line, alpha=0.5, color=clr[c])
    plt.plot(numpy.mean(SelectedLines, axis=0), 'k', linewidth='2',
        label=' '.join(['mean of', str(steps), 'shown lines']))
    plt.xlim([0, xmax + pad - xmin - pad])
    plt.legend(loc='best')
    plt.title('Brightness in the red ROI shown above, scaled')
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

    time.sleep(1)
    plt.close('all')
