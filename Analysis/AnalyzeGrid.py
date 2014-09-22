"""
Script to "analyze" the grid shown in the radiographies from Ivan.

The user manually selects the grid, the histogram of the grid is then shown.

Region selection code based on http://is.gd/GoCP5g
"""

from __future__ import division
import os
import sys
import numpy
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.gridspec import GridSpec
import time
import logging
import linecache
import random
from functions import myLogger
from functions import get_git_hash

# Where shall we start?
if 'linux' in sys.platform:
    # If running at the office, grep AFS
    RootFolder = ('/afs/psi.ch/project/EssentialMed/MasterArbeitBFH/' +
        'XrayImages')
    #~ StartingFolder = os.path.join(RootFolder, '20140721')  # 11
    #~ StartingFolder = os.path.join(RootFolder, '20140722')  # 44
    #~ StartingFolder = os.path.join(RootFolder, '20140724')  # 91
    #~ StartingFolder = os.path.join(RootFolder, '20140730')  # 30
    #~ StartingFolder = os.path.join(RootFolder, '20140731')  # 262
    #~ StartingFolder = os.path.join(RootFolder, '20140818')  # 20
    #~ StartingFolder = os.path.join(RootFolder, '20140819')  # 64
    #~ StartingFolder = os.path.join(RootFolder, '20140820')  # 64
    #~ StartingFolder = os.path.join(RootFolder, '20140822')  # 149
    #~ StartingFolder = os.path.join(RootFolder, '20140823')  # 6
    #~ StartingFolder = os.path.join(RootFolder, '20140825')  # 99
    #~ StartingFolder = os.path.join(RootFolder, '20140829')  # 4
    #~ StartingFolder = os.path.join(RootFolder, '20140831')  # 309
    #~ StartingFolder = os.path.join(RootFolder, '20140901')  # 149
    #~ StartingFolder = os.path.join(RootFolder, '20140903')  # 30
    #~ StartingFolder = os.path.join(RootFolder, '20140907')  # 277
    #~ StartingFolder = os.path.join(RootFolder, '20140914')  # 47
    #~ StartingFolder = os.path.join(RootFolder, '20140916')  # 51
    #~ StartingFolder = os.path.join(RootFolder, '20140920')  # 94
    StartingFolder = os.path.join(RootFolder, '20140921')  # 227
else:
    # If running on Ivans machine, look on the connected harddisk
    StartingFolder = ('/Volumes/WINDOWS/Aptina/Hamamatsu/AR0130/Computar-11A/')
    StartingFolder = ('/Volumes/exFAT')

# Testing
#~ StartingFolder = os.path.join(RootFolder, '20140731', 'Toshiba', 'AR0132',
    #~ 'Lensation-CHR6020')
# Testing


# Setup
# Draw lines in final plot $pad pixels longer than the selection (left & right)
pad = 25
# Draw $steps lines in the final selected ROI
steps = 10
# Draw rectangles and lines with this alpha
overlayalpha = 0.125
linealpha = 3 * overlayalpha


def tellme(blurb):
    print(blurb)
    plt.title(blurb)
    plt.draw()

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
SDD = [float(linecache.getline(i, 13).split(':')[1].split('mm')[0].strip())
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
    plt.ion()
    print str(Counter + 1) + '/' + str(len(Experiment)), '| ID', \
        ExperimentID[SelectedExperiment], '|', \
        Scintillator[SelectedExperiment], '|', Sensor[SelectedExperiment], \
        '|', Lens[SelectedExperiment], '|', SDD[SelectedExperiment], \
        'mm | git version', get_git_hash()
    # See if we've already ran the resolution evaluation, i.e. have a
    # 'ExperimentID.resolution.png' file. If we have, show it and let the user
    # decide to rerun, otherwise skip to next
    # Load image
    ResolutionFileName = os.path.join(
        os.path.dirname(Experiment[SelectedExperiment]),
        ExperimentID[SelectedExperiment] + '.resolution.png')
    if os.path.isfile(ResolutionFileName):
        plt.figure(' '.join([str(Counter + 1) + '/' + str(len(Experiment)),
            '|', ExperimentID[SelectedExperiment], '|',
            Scintillator[SelectedExperiment], '|', Sensor[SelectedExperiment],
            '|', Lens[SelectedExperiment], '| Resolution evaluation']))
        ResolutionFigure = plt.imread(ResolutionFileName)
        plt.imshow(ResolutionFigure)
        currentAxis = plt.gca()
        ok = currentAxis.add_patch(Rectangle((0, 0),
                                   ResolutionFigure.shape[1] / 2,
                                   ResolutionFigure.shape[0],
                                   facecolor='green', alpha=overlayalpha))
        nok = currentAxis.add_patch(Rectangle((ResolutionFigure.shape[1] / 2,
                                    0), ResolutionFigure.shape[1] / 2,
                                    ResolutionFigure.shape[0],
                                    facecolor='red', alpha=overlayalpha))
        if 'linux' in sys.platform:
            plt.tight_layout()
        tellme(' '.join(['click left (green) if you are happy,\nclick right',
            '(red) if you want to redo the evaluation']))
        # If the user clicks in the red, we redo the analysis, if in the green
        # we 'continue' without doing anything
        if plt.ginput(1, timeout=-1)[0][0] < ResolutionFigure.shape[1] / 2:
            print 'We leave',  ExperimentID[SelectedExperiment], 'be'
            plt.close('all')
            continue
        else:
            print 'We redo the evaluation of experiment', \
                ExperimentID[SelectedExperiment]
    logfile = myLogger(os.path.dirname(Experiment[SelectedExperiment]),
        ExperimentID[SelectedExperiment] + '.resolution.log')
    logfile.info(
        'Log file for Experiment ID %s, Resolution analsyis performed on %s',
        ExperimentID[SelectedExperiment],
        time.strftime('%d.%m.%Y at %H:%M:%S'))
    logfile.info('\nMade with "%s" at Revision %s', os.path.basename(__file__),
        get_git_hash())
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

    # Show original images with histograms
    plt.figure(' '.join([str(Counter + 1) + '/' + str(len(Experiment)),
        '| ID', ExperimentID[SelectedExperiment], '|',
        Scintillator[SelectedExperiment], '|', Sensor[SelectedExperiment], '|',
        Lens[SelectedExperiment], '|', str(SDD[SelectedExperiment]),
        'mm | git version', get_git_hash(), '| Originals and Histograms']),
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
    if 'linux' in sys.platform:
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
                                                    alpha=overlayalpha))
        tellme('Done? Press any key for yes, click with mouse for no')
        done = plt.waitforbuttonpress()
        # Redraw image if necessary
        if not done:
            plt.cla()
            plt.subplot(222)
            plt.imshow(StretchedImage, cmap='bone', interpolation='nearest')
    # Give plot a nice title
    BigROISize = [xmax - xmin, ymax - ymin]
    tellme(' '.join(['Selected ROI with a size of', str(BigROISize[0]), 'x',
        str(BigROISize[1]), 'px']))
    logfile.info('Resolution-Phantom x-ROI: %s-%s (%s px)', xmin, xmax,
        xmax - xmin)
    logfile.info('Resolution-Phantom y-ROI: %s-%s (%s px)', ymin, ymax,
        ymax - ymin)
    # Show selected ROI and select sub-ROI to plot the line profiles
    plt.subplot(221)
    plt.title(' '.join([ExperimentID[SelectedExperiment] +
        '.image.corrected.png with', str(BigROISize[0]), 'x',
        str(BigROISize[1]), 'px ROI']))
    currentAxis = plt.gca()
    BigROI = currentAxis.add_patch(Rectangle((xmin, ymin), xmax - xmin,
                                                    ymax - ymin,
                                                    facecolor='red',
                                                    edgecolor='black',
                                                    alpha=overlayalpha))
    plt.subplot(222)
    plt.cla()
    CroppedImage = OriginalImage[ymin:ymax, xmin:xmax]
    CroppedImageStretched = StretchedImage[ymin:ymax, xmin:xmax]
    plt.imshow(CroppedImageStretched, cmap='bone', interpolation='none')
    if 'linux' in sys.platform:
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
                                                    alpha=overlayalpha))
        tellme('Done? Press any key for yes, click with mouse for no')
        done = plt.waitforbuttonpress()
        # Redraw image if necessary
        if not done:
            plt.cla()
            plt.subplot(222)
            plt.imshow(CroppedImageStretched, cmap='bone',
                interpolation='none')
    if ((xxmax + pad) - (xxmin - pad) > numpy.shape(CroppedImage)[0]) or \
        ((xxmin - pad) <= 0):
        print 'Padding the selected ROI would make it bigger than the image'
        waspad = pad
        pad = 0
        print 'Setting padding from', waspad, 'to', pad, 'pixels'
    else:
        waspad = []
    # Give plot a nice title
    LineROISize = [xxmax - xxmin + pad + pad, yymax - yymin]
    tellme(' '.join(['Selected ROI with a size of', str(LineROISize[0]), 'x',
        str(LineROISize[1]), 'px']))
    logfile.info(80 * '-')
    logfile.info('Selected region in Resolution-Phantom x-ROI: %s-%s (%s px)',
        xxmin - pad, xxmax + pad, xxmax - xxmin + pad + pad)
    logfile.info('Selected region in Resolution-Phantom y-ROI: %s-%s (%s px)',
        yymin, yymax, yymax - yymin)
    logfile.info(80 * '-')

    # Final plot
    fig = plt.figure(' '.join([str(Counter + 1) + '/' + str(len(Experiment)),
        '|', ExperimentID[SelectedExperiment], '|',
        Scintillator[SelectedExperiment], '|', Sensor[SelectedExperiment], '|',
        Lens[SelectedExperiment], '| Result']), figsize=[16, 9])
    plt.suptitle(' '.join([Scintillator[SelectedExperiment], '|',
        Sensor[SelectedExperiment], '|', Lens[SelectedExperiment], '|',
        str(SDD[SelectedExperiment]), 'cm | version', get_git_hash()]))
    # Use gridspec for easier positioning
    gs1 = GridSpec(3, 3)
    gs1.update(left=0.05, right=0.95, hspace=-0.2)
    # Show original image on top left
    plt.subplot(gs1[0, 0])
    plt.imshow(OriginalImage, cmap='bone', interpolation='nearest')
    plt.title('Original Image')
    # Stretched image with both ROIs in top middle
    plt.subplot(gs1[0, 1])
    plt.imshow(StretchedImage, cmap='bone', interpolation='nearest')
    plt.title(' '.join(['Contrast stretched Image\nROIs', str(BigROISize[0]),
        'x', str(BigROISize[1]), 'px (red),', str(LineROISize[0]), 'x',
        str(LineROISize[1]), 'px (green).']))
    currentAxis = plt.gca()
    BigROI = currentAxis.add_patch(Rectangle((xmin, ymin), xmax - xmin,
                                                    ymax - ymin,
                                                    facecolor='red',
                                                    edgecolor='black',
                                                    alpha=overlayalpha))
    LineROI = currentAxis.add_patch(Rectangle((xmin + xxmin - pad,
                                               ymin + yymin),
                                               xxmax - xxmin + pad + pad,
                                               yymax - yymin,
                                               facecolor='green',
                                               edgecolor='black',
                                               alpha=overlayalpha))
    # ROI and LineROI on top right
    plt.subplot(gs1[0, 2])
    plt.imshow(CroppedImageStretched, cmap='bone', interpolation='none')
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
        plt.axhline(y=height, xmin=(xxmin - pad) / BigROISize[0],
            xmax=(xxmax + pad) / BigROISize[0], linewidth=2,
            alpha=linealpha, color=clr[c])
    tellme(' '.join([str(BigROISize[0]), 'x', str(BigROISize[1]),
        'px ROI\nLocation of lines from plots below']))

    # Plot values for original image in the middle
    gs2 = GridSpec(4, 1)
    gs2.update(left=0.05, right=0.95, hspace=0)
    plotoriginal = plt.subplot(gs2[2, :])
    for c, line in enumerate(SelectedLines):
        plt.plot(line, linewidth=2, alpha=linealpha, color=clr[c])
    plt.plot(numpy.mean(SelectedLines, axis=0), 'k', linewidth='2',
        label=' '.join(['mean of', str(steps), 'shown lines']))
    plt.xlim([0, LineROISize[0]])
    plt.ylim([0, 1])
    if 'linux' in sys.platform:
        plt.legend(loc='best')
    else:
        plt.legend([' '.join(['mean of', str(steps), 'shown lines'])],
            loc='best')
    # Turn off x-ticks: http://stackoverflow.com/a/12998531/323100
    plt.tick_params(axis='x', which='both', labelbottom='off')
    # remove "0" y-tick label: http://stackoverflow.com/a/13583251/323100
    yticks = plotoriginal.yaxis.get_major_ticks()
    yticks[0].label1.set_visible(False)
    plt.title(' '.join(['Brightness in the green', str(LineROISize[0]), 'x',
        str(LineROISize[1]),
        'px ROI. Top: original image, bottom: contrast stretched image']))

    # Plot values for contrast streched image at the bottom
    plotmean = plt.subplot(gs2[-1, :], sharex=plotoriginal)
    for c, line in enumerate(SelectedLinesStretched):
        plt.plot(line, linewidth=2, alpha=linealpha, color=clr[c])
    plt.plot(numpy.mean(SelectedLinesStretched, axis=0), 'k', linewidth='2',
        label=' '.join(['mean of', str(steps), 'shown lines']))
    plt.xlim([0, LineROISize[0]])
    plt.ylim([0, 1])
    if 'linux' in sys.platform:
        plt.legend(loc='best')
    else:
        plt.legend([' '.join(['mean of', str(steps), 'shown lines'])],
            loc='best')
    # Write mean plot values to log file
    logfile.info('Mean brightness along %s equally spaced lines in ROI', steps)
    for i in numpy.mean(SelectedLines, axis=0):
        logfile.info(i)
    logfile.info(80 * '-')

    SaveName = os.path.join(os.path.dirname(Experiment[SelectedExperiment]),
        ExperimentID[SelectedExperiment] + '.resolution.png')

    plt.draw()
    plt.ioff()

    # If we decreased the padding, 'waspad' is set. In this case reset the
    # padding to the original value
    if waspad:
        print 'Setting padding back from', pad, 'to', waspad, 'pixels'
        pad = waspad

    plt.savefig(SaveName)
    print 'Figure saved as', SaveName
    print 80 * '-'

    time.sleep(1)
    plt.close('all')
