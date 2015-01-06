# -*- coding: utf-8 -*-

"""
Script to work with the Input/Output Pins of the RPi, ltimately thought to
trigger the Elphel camera.
Based on http://code.google.com/p/raspberry-gpio-python/
"""

import sys
import time
# Try to import the GPIO library
try:
    import RPi.GPIO as GPIO
except:
    print 'I cannot import RPI.GPIO, you have to run the script as root'
    print 'try running it again with'
    print '---'
    print 'sudo', ' '.join(sys.argv)
    print '---'
    sys.exit(1)


def is_even(i):
    return (i % 2) == 0

# to use Raspberry Pi board pin numbers
# Named sequentially, as seen on the connector. compare
# http://elinux.org/File:GPIOs.png
GPIO.setmode(GPIO.BOARD)
# Named GPIO*, see table http://is.gd/xWDsp7 (e.g. 007 is the last pin)
# GPIO.setmode(GPIO.BCM)

print 'set up GPIO input channel'
Pin = 26  # BOARD
#~ Pin = 007  # BMC
GPIO.setup(Pin, GPIO.IN)

print
print 'I am waiting for you to connect pin', Pin, 'and ground'
print

# Wait for Input, then print something and wait for a short while
# Code according to http://is.gd/G88UyN
counter = 1
Previous_Reading = 0
while True:
    if GPIO.input(Pin):
        print "Pin", Pin, "and Ground are connected (" + str(counter),\
            "times)."
        counter += 1
        time.sleep(0.05)

Counter = 1
Previous_Input = 0
while Counter < 100:
    Input = GPIO.input(Pin)
    if not Previous_Input and Input:
        print "Pin", Pin, "and Ground are connected (" + str(Counter),\
            "times)."
        Counter += 1
    Previous_Input = Input
    time.sleep(0.1)

# Reset every channel that has been set up by this program to INPUT with no
# pullup/pulldown and no event detection.
GPIO.cleanup()
