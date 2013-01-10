#!/usr/bin/python

# Script to switch Network interfaces between DHCP and Elphel
# First version based on reading the values from their respective outputs
# New version simply sets to Elphel as default, other options as options

import os
import commands
from optparse import OptionParser

# Setup the Options
parser = OptionParser()
usage = 'usage: % prog [options] arg'

parser.add_option('-e','--Elphel',dest='Elphel',
	help='Switch the network interface to work with the Elphel camera (default)',
	default=True,action='store_true')
parser.add_option('-d','--DHCP',dest='DHCP',
	help='Switch the network interface to DHCP, to work with PSI',
	action='store_true')
parser.add_option('-p','--PSI',dest='PSI',
	help='Switch the network interface to DHCP, to work with PSI',
	action='store_true')
(options,args) = parser.parse_args()

if options.DHCP or options.PSI:
	print 'Setting network interface to "PSI" with "sudo dhclient eth0 > /dev/null"'
	os.system('sudo dhclient eth0 > /dev/null')
	print
	print 'Unplug the Ethernet cable from the Camera, plug in the PSI Ethernet cable and interweb'
elif options.Elphel:
	print 'Setting network interface to "Elphel" with "sudo ifconfig eth0 192.168.0.1 > /dev/null"'
	os.system('sudo ifconfig eth0 192.168.0.1 > /dev/null')
	print 
	print 'Uplug the PSI Ethernet cable, plug in the Elphel cable and wait a while for the camera to boot'

if options.DHCP or options.PSI:
	print
	print 'If you just switched from Elphel to to PSI,'
	print ' then it is probably a good idea to run'
	print 'cd;bash SyncToAFS.cmd'
	print 'to rsync all changes in the home directory to /afs/EssentialMed/Dev/RPI'
	print
	print 'and maybe also do a "git commit;git push"...'
