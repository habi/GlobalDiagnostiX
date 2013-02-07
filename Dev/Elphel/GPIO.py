#!/usr/bin/python
# coding=utf8

# Script to work with the Input/Output Pins of the RPi
# Ultimately thought to trigger the Elphel camera
# Based on http://code.google.com/p/raspberry-gpio-python/

import sys
import time
# Try to import the GPIO library
try:
	import RPi.GPIO as GPIO
except:
	print 'I cannot import RPI.GPIO, you have to run the script as root'
	print 'try running it again with'
	print 'sudo',' '.join(sys.argv) # joining the sys.argv list to a string so we can print it
	sys.exit(1)

try:
	sleepytime = float(sys.argv[1])
	steps = int(sys.argv[2])
except:	
	print 'Start the script with two parameters'
	print sys.argv[0],'Sleeptime Repeats'
	sys.exit(1)

def is_even(i):
	return (i % 2) == 0

# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD) # Named sequentially, as seen on the connector. compare http://elinux.org/File:GPIOs.png
# GPIO.setmode(GPIO.BCM) # Named GPIO*, see table http://is.gd/xWDsp7 (e.g. 007 is the last pin)

print 'set up GPIO output channel'
Pin = 26 # BOARD
#~ Pin = 007 # BMC
GPIO.setup(Pin, GPIO.OUT)

# set RPi board pin selected above to high for a certain time, wait, set it low
# lather, rinse, repeat for 'steps' steps
for Iteration in range(steps):
	if is_even(Iteration):
		print str(Iteration +1) + '/' + str(steps),'| Pin',Pin,'high for',sleepytime,'s'
		GPIO.output(Pin, GPIO.HIGH)
		time.sleep(sleepytime)
	else:
		print str(Iteration +1) + '/' + str(steps),'| Pin',Pin,'low for',sleepytime,'s'
		GPIO.output(Pin, GPIO.LOW)
		time.sleep(sleepytime)

# Reset every channel that has been set up by this program to INPUT with no pullup/pulldown and no event detection.
GPIO.cleanup()
