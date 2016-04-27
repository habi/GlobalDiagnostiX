# -*- coding: utf-8 -*-

"""
Script used to calculate the surface entrance dose of a certain x-ray
measurement. Gives the same results as the 'Diagnostische Referenzwerte'
Excel calculator on the BAG-page, in the right side-bar of http://is.gd/E2qIPA.
The calculation is based on 'Merkblatt R-06-04' from BAG.
The file is an extensiuon of SurfaceEntranceDose.py, which was used to plot
the SED for a talk at an SLS Symposium.
"""

from __future__ import division  # fix integer division
from optparse import OptionParser
import sys


# Use Pythons Optionparser to define and read the options, and also
# give some help to the user
parser = OptionParser()
usage = "usage: %prog [options] arg"
parser.add_option('-v', '--kilovolt', dest='kV',
                  type='float',
                  help='set kV',
                  metavar='90')
parser.add_option('-a', '--milliamperesecond', dest='mAs',
                  type='float',
                  help='set mAs',
                  metavar='125')
parser.add_option('-d', '--distance', dest='FocusDistance',
                  type='float',
                  default=140.,
                  help='Focus distance in cm. Defaults to 140 cm',
                  metavar='120')
(options, args) = parser.parse_args()

# show the help if no parameters are given
if options.kV is None or options.mAs is None:
    parser.print_help()
    print 'Example:'
    print 'The command below calculates the surface entrance dose of a',\
        '"Chest: PA standing", where the WHO manual gives 120 kV and 2 mAs',\
        'as base values. The distance is shortened fromt the default 140 cm',\
        'to 1 meter.'
    print
    print sys.argv[0], '-v 120 -a 2 -d 100'
    print
    sys.exit(1)

# Parameters
# The K-value is based on the machine. The BAG-calculator (see below) list 0.1
K = 0.1
# BSF as found by Arouna2000, cited by BAG2012. *This* BSF gives the same SED
# values as the XLS-calculator from BAG (http://is.gd/oTpniQ) which I copied to
# /afs/psi.ch/project/EssentialMed/PresentationsAndInfo/BAG/R-0 DRWCalc 5.0.xls
BSF = 1.35
# BSF as found in BAG2012. "Der ueber verschiedene Anlagen gemittelte
# Korrekturfaktor betrug 1.15"
# BSF = 1.15

# calculating while converting Focusdistance from m to cm
SED = K * (options.kV / 100) ** 2 * options.mAs *\
    (100 / options.FocusDistance) ** 2 * BSF
print
print 'Calculating the surface entrance dose for an x-ray pulse with'
print '   *', options.kV, 'kV'
print '   *', options.mAs, 'mAs and'
print '   *', options.FocusDistance / 100, 'm focal distance.'
print '   * the characteristic constant K of the setup was set to', K,\
    'mGy/mA.'
print '   * the back-scatter factor was set to', str(BSF) + '.'
print 'The surface entrance dose is thus SED = K*(U/100)^2*Q*(1/FOD)^2*BSF=' +\
    str(round(SED, 3)), 'mGy'
