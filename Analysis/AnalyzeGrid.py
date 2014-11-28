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
import functions

# Where shall we start?
RootFolder = '/afs/psi.ch/project/EssentialMed/MasterArbeitBFH/XrayImages'
# Look for images of only one scintillator
StartingFolder = os.path.join(RootFolder, 'AppScinTech-HE')
StartingFolder = os.path.join(RootFolder, 'Hamamatsu')
StartingFolder = os.path.join(RootFolder, 'Pingseng')
StartingFolder = os.path.join(RootFolder, 'Toshiba')
# Look through all folders
StartingFolder = RootFolder

# Look for a special folder
#~ StartingFolder = os.path.join(RootFolder, 'Hamamatsu', 'MT9M001',
    #~ 'TIS-TBL-6C-3MP')

# Ask user for a special case
Scintillators = ('AppScinTech-HE', 'Pingseng', 'Hamamatsu', 'Toshiba')
Sensors = ('AR0130', 'AR0132', 'MT9M001')

ChosenScintillator = functions.AskUser(
    'Which scintillator do you want to look at?', Scintillators)
ChosenSensor = functions.AskUser('Which sensor do you want to look at?',
    Sensors)
StartingFolder = os.path.join(RootFolder, ChosenScintillator, ChosenSensor)

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
    #~ print(blurb)
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
ExperimentID = [linecache.getline(i, 1).split('ID')[1].split(',')[0].strip()
                for i in LogFiles]
# for c, i in enumerate(LogFiles):
#     print LogFiles[c]
#     print '\t', linecache.getline(i, 1).split('ID')[1].split(',')[0].strip(), \
#         linecache.getline(i, 10).split(':')[1].strip()
Sensor = [linecache.getline(i, 10).split(':')[1].strip() for i in LogFiles]
Scintillator = [linecache.getline(i, 9).split(':')[1].strip() for i in LogFiles]
Lens = [str(linecache.getline(i, 11).split(':')[1].strip()) for i in LogFiles]
SDD = [float(linecache.getline(i, 13).split(':')[1].split('mm')[0].strip())
       for i in LogFiles]
Modality = [linecache.getline(i, 14).split(':')[1].strip() for i in LogFiles]
Exposuretime = [float(linecache.getline(i, 18).split(':')[1].split('ms')[
                          0].strip()) for i in LogFiles]

# DEBUG
debug = False
if debug:
    for i in LogFiles:
        print i, 'max of', \
            float(linecache.getline(i, 25).split(':')[1].strip())
    exit()
# DEBUG

Max = [float(linecache.getline(i, 25).split(':')[1].strip())
    for i in LogFiles]
Mean = [float(linecache.getline(i, 26).split(':')[1].strip())
    for i in LogFiles]
STD = [float(linecache.getline(i, 27).split(':')[1].strip())
    for i in LogFiles]

# Generate folder names
Experiment = [item[:-len('.analysis.log')] for item in LogFiles]

# Get git hash once per session, so it doesn't take so long for Ivan...
git_hash = functions.get_git_hash()
if 'linux' in sys.platform:
    git_hash = git_hash + ' (from Linux)'
else:
    git_hash = git_hash + ' (from OS X)'

# Go through each selected experiment (in the shuffled list)
for Counter, SelectedExperiment in enumerate(range(len(Experiment))):
    plt.ion()
    print str(Counter + 1) + '/' + str(len(Experiment)), '|', \
        Scintillator[SelectedExperiment], '|', Sensor[SelectedExperiment], \
        '|', Lens[SelectedExperiment], '|', \
        ExperimentID[SelectedExperiment], '|', SDD[SelectedExperiment], \
        'mm | git version', git_hash
    # See if we've already ran the resolution evaluation, i.e. have a
    # 'ExperimentID.resolution.png' file. If we have, show it and let the user
    # decide to rerun, otherwise skip to next
    # Load image
    ResolutionFileName = os.path.join(
        os.path.dirname(Experiment[SelectedExperiment]),
        ExperimentID[SelectedExperiment] + '.resolution.png')
    decide = True
    if os.path.isfile(ResolutionFileName):
        decide = False
        plt.figure(' '.join([str(Counter + 1) + '/' + str(len(Experiment)),
            '| Redo evaluation |', Scintillator[SelectedExperiment], '|',
            Sensor[SelectedExperiment], '|', Lens[SelectedExperiment], '|',
            ExperimentID[SelectedExperiment], '|',
            str(SDD[SelectedExperiment]), 'mm | git version', git_hash]),
            figsize=(20, 12))
        ResolutionFigure = plt.imread(ResolutionFileName)
        plt.imshow(ResolutionFigure)
        plt.axis('off')
        currentAxis = plt.gca()
        ok = currentAxis.add_patch(Rectangle((0, 0),
                                   ResolutionFigure.shape[1] / 2,
                                   ResolutionFigure.shape[0],
                                   facecolor='green', alpha=overlayalpha))
        nok = currentAxis.add_patch(Rectangle((ResolutionFigure.shape[1] / 2,
                                    0), ResolutionFigure.shape[1] / 2,
                                    ResolutionFigure.shape[0],
                                    facecolor='red', alpha=overlayalpha))
        tellme(' '.join(['click left (green) if you are happy,\nclick right',
            '(red) if you want to redo the evaluation']))
        # If the user clicks in the red, we redo the analysis, if in the green
        # we 'continue' without doing anything
        if plt.ginput(1, timeout=-1)[0][0] < ResolutionFigure.shape[1] / 2:
            print 'We leave',  ExperimentID[SelectedExperiment], 'be'
            plt.close('all')
            continue
        else:
            print 'We redo the evaluation of', \
                ExperimentID[SelectedExperiment]
    if decide:
        # Load the image and let the user decide if he wants to do the
        # evaluation or directly skip to the next experiment ID
        print 'See if we want to do the evaluation'
        SelectionFileName = os.path.join(
            os.path.dirname(Experiment[SelectedExperiment]),
            ExperimentID[SelectedExperiment] +
            '.image.corrected.stretched.png')
        SelectionImage = plt.imread(SelectionFileName)
        plt.figure(' '.join([str(Counter + 1) + '/' + str(len(Experiment)),
            '| Decision |', Scintillator[SelectedExperiment], '|',
            Sensor[SelectedExperiment], '|', Lens[SelectedExperiment], '|',
            ExperimentID[SelectedExperiment], '|',
            str(SDD[SelectedExperiment]), 'mm | git version', git_hash]),
            figsize=(16, 12))
        plt.imshow(SelectionImage, cmap='bone')
        plt.axis('off')
        currentAxis = plt.gca()
        ok = currentAxis.add_patch(Rectangle((0, 0),
                                   SelectionImage.shape[1] / 2,
                                   SelectionImage.shape[0],
                                   facecolor='green', alpha=overlayalpha))
        nok = currentAxis.add_patch(Rectangle((SelectionImage.shape[1] / 2,
                                    0), SelectionImage.shape[1] / 2,
                                    SelectionImage.shape[0],
                                    facecolor='red', alpha=overlayalpha))
        tellme(' '.join(['click left (green) if you want to do the',
            'evaluation,\nclick right (red) if you want to skip experiment',
            ExperimentID[SelectedExperiment]]))
        # If the user clicks in the red, we do the analysis, if in the green
        # we 'continue' to the next experiment ID
        if plt.ginput(1, timeout=-1)[0][0] > SelectionImage.shape[1] / 2:
            print 'We skip',  ExperimentID[SelectedExperiment]
            plt.close('all')
            continue
        else:
            print 'We evaluate', ExperimentID[SelectedExperiment]
    else:
        wediditalready = False
    logfile = functions.myLogger(
        os.path.dirname(Experiment[SelectedExperiment]),
        ExperimentID[SelectedExperiment] + '.resolution.log')
    logfile.info(
        'Log file for Experiment %s, Resolution analsyis performed on %s',
        ExperimentID[SelectedExperiment],
        time.strftime('%d.%m.%Y at %H:%M:%S'))
    logfile.info('\nMade with "%s" at Revision %s', os.path.basename(__file__),
        git_hash)
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
        '| Originals & Histograms |', Scintillator[SelectedExperiment], '|',
        Sensor[SelectedExperiment], '|', Lens[SelectedExperiment], '|',
        ExperimentID[SelectedExperiment], '|',
        str(SDD[SelectedExperiment]), 'mm | git version', git_hash]),
        figsize=(16, 9))
    plt.subplot(221)
    plt.imshow(OriginalImage, cmap='bone', interpolation='bicubic')
    plt.title(' '.join([ExperimentID[SelectedExperiment] +
        '.image.corrected.png (' + str(OriginalImage.shape[1]), 'x',
        str(OriginalImage.shape[0]), 'px)']))
    plt.axis('off')
    plt.subplot(222)
    plt.imshow(StretchedImage, cmap='bone', interpolation='bicubic')
    plt.title(' '.join([ExperimentID[SelectedExperiment] +
        '.image.corrected.stretched.png (' + str(StretchedImage.shape[1]), 'x',
        str(StretchedImage.shape[0]), 'px)']))
    # Histograms
    bins = 256
    plt.subplot(223)
    plt.hist(OriginalImage.flatten(), bins, histtype='stepfilled',
        normed=True)
    #~ plt.xlim([0, 0.95])
    plt.subplot(224)
    plt.hist(StretchedImage.flatten(), bins, histtype='stepfilled',
        normed=True)
    #~ plt.xlim([0, 0.95])
    if 'linux' in sys.platform:
        plt.tight_layout()
    # Let the user select the ROI of the resolution phantom on the contrast
    # stretched image
    plt.subplot(222)
    plt.imshow(StretchedImage, cmap='bone', interpolation='bicubic')
    done = False
    while not done:
        pts = []
        while len(pts) < 2:
            tellme('Select 2 diagonal edges of the resolution phantom')
            pts = numpy.asarray(plt.ginput(2, timeout=-1))
            if len(pts) < 2:
                tellme('Too few points, starting over')
                time.sleep(0.1)
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
        done = plt.waitforbuttonpress(timeout=-1)
        # Redraw image if necessary
        if not done:
            plt.cla()
            plt.subplot(222)
            plt.imshow(StretchedImage, cmap='bone', interpolation='bicubic')
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
    plt.imshow(CroppedImageStretched, cmap='bone', interpolation='bicubic')
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
                time.sleep(0.1)  # Wait a second
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
        done = plt.waitforbuttonpress(timeout=-1)
        # Redraw image if necessary
        if not done:
            plt.cla()
            plt.subplot(222)
            plt.imshow(CroppedImageStretched, cmap='bone',
                interpolation='bicubic')
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
        '| Result |', Scintillator[SelectedExperiment], '|',
        Sensor[SelectedExperiment], '|', Lens[SelectedExperiment], '|',
        ExperimentID[SelectedExperiment], '|', str(SDD[SelectedExperiment]),
        'mm | git version', git_hash]),
        figsize=(16, 9))
    plt.suptitle(' '.join([Scintillator[SelectedExperiment], '|',
        Sensor[SelectedExperiment], '|', Lens[SelectedExperiment], '|',
        str(SDD[SelectedExperiment]), 'mm | version', git_hash]))
    # Use gridspec for easier positioning
    gs1 = GridSpec(3, 3)
    gs1.update(left=0.05, right=0.95, hspace=-0.2)
    # Show original image on top left
    plt.subplot(gs1[0, 0])
    plt.imshow(OriginalImage, cmap='bone', interpolation='bicubic')
    plt.axis('off')
    plt.title(' '.join(['Original Image with a size of',
        str(OriginalImage.shape[1]), 'x', str(OriginalImage.shape[0]), 'px']))
    # Stretched image with both ROIs in top middle
    plt.subplot(gs1[0, 1])
    plt.imshow(StretchedImage, cmap='bone', interpolation='bicubic')
    plt.axis('off')
    plt.title(' '.join(['Contrast stretched Original\nROIs',
        str(BigROISize[0]), 'x', str(BigROISize[1]), 'px (red),',
        str(LineROISize[0]), 'x', str(LineROISize[1]), 'px (green).']))
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
    plt.imshow(CroppedImageStretched, cmap='bone', interpolation='bicubic')
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
        'px ROI\nLocation of', str(steps), 'lines from plots below']))

    # Plot values for original image in the middle
    gs2 = GridSpec(4, 1)
    gs2.update(left=0.05, right=0.95, hspace=0)
    plotoriginal = plt.subplot(gs2[2, :])
    for c, line in enumerate(SelectedLines):
        plt.plot(line, linewidth=2, alpha=linealpha, color=clr[c])
    plt.plot(numpy.mean(SelectedLines, axis=0), 'k', linewidth='2')
    plt.xlim([0, LineROISize[0]])
    plt.ylim([0, 1])
    # Turn off x-ticks: http://stackoverflow.com/a/12998531/323100
    plt.tick_params(axis='x', which='both', labelbottom='off')
    # remove "0" y-tick label: http://stackoverflow.com/a/13583251/323100
    yticks = plotoriginal.yaxis.get_major_ticks()
    yticks[0].label1.set_visible(False)
    plt.title(' '.join(['Brightness in the green', str(LineROISize[0]), 'x',
        str(LineROISize[1]), 'px ROI.\nTop: original image, bottom: contrast',
        'stretched image. Color: lines from above right, Black: Mean of',
        str(steps), 'lines']))
    # Plot values for contrast streched image at the bottom
    plotmean = plt.subplot(gs2[-1, :], sharex=plotoriginal)
    for c, line in enumerate(SelectedLinesStretched):
        plt.plot(line, linewidth=2, alpha=linealpha, color=clr[c])
    plt.plot(numpy.mean(SelectedLinesStretched, axis=0), 'k', linewidth='2',
        label=' '.join(['mean of', str(steps), 'shown lines']))
    plt.xlim([0, LineROISize[0]])
    plt.ylim([0, 1])
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
    plt.pause(0.001)
    time.sleep(1)
    plt.close('all')
