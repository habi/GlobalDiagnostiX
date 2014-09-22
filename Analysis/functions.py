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
