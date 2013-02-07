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
print 'use Raspberry Pi board pin numbers'
GPIO.setmode(GPIO.BOARD)

# set up GPIO output channel
print 'set up GPIO output channel'
Pin = 11
GPIO.setup(Pin, GPIO.OUT)

# set RPi board pin selected above to high for a certain time, wait, set it low
# lather, rinse, repeat
sleepytime = 1
for Iteration in range(10):
	if is_even(Iteration):
		print 'setting high'
		GPIO.output(Pin, GPIO.HIGH)
		time.sleep(sleepytime)
	else:
		print 'setting low'
		GPIO.output(Pin, GPIO.LOW)
		time.sleep(sleepytime)
