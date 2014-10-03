# -*- coding: utf-8 -*-

"""
Functions that we use for each and every script in the folder
/afs/psi.ch/project/EssentialMed/Dev/Analysis
"""


def AskUser(Blurb, Choices):
    """
    Ask for user input.
    Based on function in MasterThesisIvan.ini
    """
    print(Blurb)
    for Counter, Item in enumerate(sorted(Choices)):
        print '    * [' + str(Counter) + ']:', Item
    Selection = []
    while Selection not in range(len(Choices)):
        try:
            Selection = int(input(' '.join(['Please enter the choice you',
                                            'want [0-' +
                                            str(len(Choices) - 1) +
                                            ']:'])))
        except:
            print 'You actually have to select *something*'
        if Selection not in range(len(Choices)):
            print 'Try again with a valid choice'
    print 'You selected', sorted(Choices)[Selection]
    return sorted(Choices)[Selection]


def get_git_hash():
    """
    Get the current git hash from the repository.
    Good for saving this information into the log files of process.
    Based on http://stackoverflow.com/a/949391/323100 and
    http://stackoverflow.com/a/18283905/323100
    """
    from subprocess import Popen, PIPE
    gitprocess = Popen(['git', '--git-dir',
        '/afs/psi.ch/user/h/haberthuer/EssentialMed/Dev/.git', 'rev-parse',
        '--short', '--verify', 'HEAD'], stdout=PIPE)
    (output, _) = gitprocess.communicate()
    return output.strip()


def myLogger(Folder, LogFileName):
    """
    Since logging in a loop does always write to the first instaniated file,
    we make a little wrapper around the logger function to write to a defined
    log file.
    Based on http://stackoverflow.com/a/2754216/323100
    """
    import logging
    import os
    logger = logging.getLogger(LogFileName)
    # either set INFO or DEBUG
    #~ logger.setLevel(logging.DEBUG)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(os.path.join(Folder, LogFileName), 'w')
    logger.addHandler(handler)
    return logger


def get_experiment_list(StartingFolder):
    """
    Get all folders (Experiment) and ExperimentIDs inside StartingFolder
    """
    import os
    from progressbar import ProgressBar, Percentage, Bar, ETA
    widgets = ['Reading: ', Percentage(), ' ', Bar(), ' ', ETA()]
    pbar = ProgressBar(widgets=widgets, maxval=2222).start()
    Experiment = []
    ExperimentID = []
    for root, dirs, files in os.walk(StartingFolder):
        #~ print 'Looking for experiment IDs in folder', os.path.basename(root)
        if (len(os.path.basename(root)) == 7
            or len(os.path.basename(root)) == 8) \
            and not os.path.basename(root).startswith('2014') \
            and not 'RECYCLE' in os.path.basename(root) \
            and not 'Pingseng' in os.path.basename(root) \
            and not 'Toshiba' in os.path.basename(root) \
            and not 'MT9' in os.path.basename(root) \
            and not 'AR0' in os.path.basename(root):
            Experiment.append(root)
            ExperimentID.append(os.path.basename(root))
            pbar.update(len(ExperimentID))
    pbar.finish()
    return Experiment, ExperimentID


def distance(Folder, chatty=False):
    import os
    import glob
    RawFileName = glob.glob(os.path.join(Folder, '*.raw'))[0]
    ScintillatorCMOSDistance = int(RawFileName.split('_')[5][:-5])
    if chatty:
        print 'Experiment', os.path.basename(Folder), \
            'was performed with a scintillator-CMOS-distance of', \
            ScintillatorCMOSDistance, 'mm'
    return ScintillatorCMOSDistance


def estimate_image_noise(image):
    '''
    # Noise estimation according to http://stackoverflow.com/a/25436112/323100
    # based on Immerkær1996
    '''
    height, width = image.shape
    M = [[1, -2, 1],
        [-2, 4, -2],
        [1, -2, 1]]
    from scipy.signal import convolve2d
    import numpy as np
    sigma = np.sum(np.sum(np.absolute(convolve2d(image, M))))
    sigma = sigma * np.sqrt(0.5 * np.pi) / (6 * (width - 2) * (height - 2))
    return sigma
