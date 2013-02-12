#!/usr/bin/python

'''
Script to switch Network interfaces between DHCP and Elphel
First version based on reading the values from their respective outputs
New version simply sets to Elphel as default when called without a flag.
Options -p or -p switch to the *P*SI *D*HCP server
'''

import os
from optparse import OptionParser

# Setup the Options
Parser = OptionParser()
Usage = 'Usage: % prog [Options] arg'

Parser.add_option('-e', '--Elphel', dest='Elphel',
                  help='Switch the network interface to work with the '
                  'Elphel camera (default)s',
                  default=True,
                  action='store_true')
Parser.add_option('-d', '--DHCP', dest='DHCP',
                  help='Switch the network interface to *D*HCP, to '
                  'work with PSI ethernet',
                  action='store_true')
Parser.add_option('-p', '--PSI', dest='PSI',
                  help='Switch the network interface to DHCP, to work '
                  'with *P*SI ethernet',
                  action='store_true')
(Options, Arguments) = Parser.parse_args()

if Options.DHCP or Options.PSI:
    print ('Setting network interface to "PSI" with '
           '"sudo dhclient eth0 > /dev/null"')
    os.system('sudo dhclient eth0 > /dev/null')
    print
    print ('Unplug the Ethernet cable from the Camera, plug in the PSI '
           'Ethernet cable and interweb')
elif Options.Elphel:
    print ('Setting network interface to "Elphel" with '
           '"sudo ifconfig eth0 192.168.0.1 > /dev/null"')
    os.system('sudo ifconfig eth0 192.168.0.1 > /dev/null')
    print
    print ('Uplug the PSI Ethernet cable, plug in the Elphel cable and '
           'wait a while for the camera to boot')

if not Options.Elphel:
    print 'If you just switched from Elphel to to PSI,'
    print ' then it is probably a good idea to run'
    print 'cd;bash SyncToAFS.cmd'
    print ('to rsync all changes in the home directory to '
           '/afs/EssentialMed/Dev/RPI')
    print 'and maybe also do a "git commit -a" and a "git push"'
