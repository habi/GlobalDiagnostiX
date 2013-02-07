#!/usr/bin/python
# coding=utf8

# Script to work with the Input/Output Pins of the RPi
# Ultimately thought to trigger the Elphel camera
# Based on http://code.google.com/p/raspberry-gpio-python/

import RPi.GPIO as GPIO
import time

def is_even(i):
	return (i % 2) == 0

# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD) # Named sequentially, as seen on the connector. compare http://elinux.org/File:GPIOs.png
# GPIO.setmode(GPIO.BCM) # Named GPIO*, see table http://is.gd/xWDsp7 (e.g. 007 is the last pin)

print 'set up GPIO output channel'
Pin = 26
GPIO.setup(Pin, GPIO.OUT)

# set RPi board pin selected above to high for a certain time, wait, set it low
# lather, rinse, repeat
sleepytime = 0.1
for Iteration in range(10):
	if is_even(Iteration):
		print 'setting high for',sleepytime,'s'
		GPIO.output(Pin, GPIO.HIGH)
		time.sleep(sleepytime)
	else:
		print 'setting low for',sleepytime,'s'
		GPIO.output(Pin, GPIO.LOW)
		time.sleep(sleepytime)
