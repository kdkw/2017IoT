# coding: UTF-8
# Camera control 
# May 24 2017 T.Kawamoto

import RPi.GPIO as GPIO
import time
import getch as g
from picamera import PiCamera

PAN=20
TILT=21
FREQ=50
NEUTRAL=7.5
DELTA=0.2
WAIT=0.2
MAX=10
MIN=5

cpw_PAN=NEUTRAL
cpw_TILT=NEUTRAL
panflag=0
tiltflag=0

GPIO.setmode(GPIO.BCM)
GPIO.setup(PAN,GPIO.OUT)
GPIO.setup(TILT,GPIO.OUT)

camera=PiCamera()
camera.rotation=180

while True:
	gch = g._Getch()
	x=gch()
	if ord(x) == 3:
		print "CTRL-C"
		ppan.stop()
		ptilt.stop()
		GPIO.cleanup(PAN)
		GPIO.cleanup(TILT)
		exit()
	else:
		if x == 'a':
			print "left turn",
			panflag=1
			if cpw_PAN <= MAX:
				cpw_PAN += DELTA
		elif x == 'd':
			print "right turn",
			panflag=1
			if cpw_PAN >= MIN:
				cpw_PAN -= DELTA
		elif x == 'w':
			print "tilt up"
			tiltflag=1
			if cpw_TILT >= MIN:
				cpw_TILT -= DELTA
		elif x == 's':
			print "tilt down",
			tiltflag=1
			if cpw_TILT <= MAX:
				cpw_TILT += DELTA
		elif x == 'x':
			print "neutral position",
			panflag=1
			tiltflag=1
			cpw_TILT = NEUTRAL
			cpw_PAN = NEUTRAL
		elif x == ' ':
			print "shutter",
			my_file=open('my_image.jpg','wb')
			camera.capture(my_file)
			my_file.close()
			print "image saved"


	if panflag == 1:
		ppan=GPIO.PWM(PAN,FREQ)
		print "cpw_PAN=%.1f cpw_TILT=%.1f" % (cpw_PAN, cpw_TILT)
		ppan.start(cpw_PAN)	
		panflag = 0
		time.sleep(WAIT)
		ppan.stop()

	if tiltflag == 1:
		ptilt=GPIO.PWM(TILT,FREQ)
		print "cpw_PAN=%.1f cpw_TILT=%.1f" % (cpw_PAN, cpw_TILT)
		ptilt.start(cpw_TILT)	
		tiltflag = 0
		time.sleep(WAIT)
		ptilt.stop()
