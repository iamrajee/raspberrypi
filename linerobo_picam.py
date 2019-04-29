#========================== IMPORTS ========================#
import numpy as np
import cv2
import time
import imutils

from picamera import PiCamera          #PICAMERA
from picamera.array import PiRGBArray

import RPi.GPIO as GPIO                #GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#========================== MOTOR PINS  AND FUNCTIONS (Only run on Raspi)========================#
lm1= 31
lm2 = 33
rm1 = 35
rm2 = 37

setpin1 = [lm1,lm2,rm1,rm2]
for pin in setpin1:
  GPIO.setup(pin,GPIO.OUT)

def forward():
    GPIO.output(lm1,1)
    GPIO.output(lm2,0)
    GPIO.output(rm1,1)
    GPIO.output(rm2,0)

def left():
    GPIO.output(lm1,0)
    GPIO.output(lm2,1)
    GPIO.output(rm1,1)
    GPIO.output(rm2,0)

def right():
    GPIO.output(lm1,1)
    GPIO.output(lm2,0)
    GPIO.output(rm1,0)
    GPIO.output(rm2,1)

def sleft():
    GPIO.output(lm1,0)
    GPIO.output(lm2,0)
    GPIO.output(rm1,1)
    GPIO.output(rm2,0)

def sright():
    GPIO.output(lm1,1)
    GPIO.output(lm2,0)
    GPIO.output(rm1,0)
    GPIO.output(rm2,0)

def backward():
    GPIO.output(lm1,0)
    GPIO.output(lm2,1)
    GPIO.output(rm1,0)
    GPIO.output(rm2,1)

def Stop():
    GPIO.output(lm1,0)
    GPIO.output(lm2,0)
    GPIO.output(rm1,0)
    GPIO.output(rm2,0)

#========================== VARIABLE ========================#
fx = 640
fy = 480
delta = 60
tl= fx/2 - delta
tr= fx/2 + delta

fright=0 #FLAG
fleft=0

'''
#******************* USING WEB CAM====================#
vc = cv2.VideoCapture(-1)
vc.set(3, fx)
vc.set(4, fy)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False
while rval:
        rval, frame = vc.read()
        #******************************#
        '''

#********************* USING PICAM ******************#
camera = PiCamera() # initialize the camera and grab a reference to the raw camera capture
camera.resolution = (fx, fy)
camera.framerate = 64
rawCapture = PiRGBArray(camera, size=(fx, fy))
 
time.sleep(0.1)# allow the camera to warmup

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):# grab the raw NumPy array representing the image, then initialize the timestamp and occupied/unoccupied text
	frame = frame.array
	#********************************************#
	#'''
	#cv2.imshow('Actual_frame',frame)                           #<<--
	
	# Crop the image
	crop_img = frame[fy/2:fy, 0:fx]
	#cv2.imshow('crop_img',crop_img)                            #<<--

	# Convert to grayscale
	gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
	#cv2.imshow('gray',gray)                                    #<<--

	# Gaussian blur
	blur = cv2.GaussianBlur(gray,(5,5),0)
	#cv2.imshow('blur',blur)                                    #<<--

	# Color thresholding
	ret,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)
	#cv2.imshow('thresh',thresh)                                #<<--

	# Find the contours of the frame
	contours = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)
	contours = imutils.grab_contours(contours)
	
	if len(contours) > 0:           
                fright=0
                fleft=0
                
		c = max(contours, key=cv2.contourArea) #CONTOUR WITH MAX AREA

		M = cv2.moments(c)

 

		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00'])

 
                # DISPLAYING CX AND CY
		cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
		cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)

                # DISPLAYING LEFT, RIGHT, FORWARD
		cv2.line(crop_img,(tl,0),(tl,fy/2),(0,0,255),2)
		cv2.line(crop_img,(tr,0),(tr,fy/2),(0,0,255),2)
 
                # DRAWING OUTLING AROUND CONTOUR
		cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)

 
		if cx >= tr:
                    sright()
                    fright =1
		    print("Turn Right")
		elif cx < tr and cx > tl:
                    forward()
                    print("On Track!")
		elif cx <= tl:
                    sleft()
                    fleft =1
		    print("Turn Left!")
	else: #IF no countor
                '''
                if fright==1:
                    sleft()
                elif fleft==1:
                    sright()
                else:'''
                Stop()
		print("I don't see the line")

        
        #==== Show Image ======#
	cv2.imshow('final_frame',crop_img)                                #<<--
	
	
	rawCapture.truncate(0)# picamera only # clear the stream in preparation for the next frame
	
	#Breaking condition
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
            Stop()
	    break


# close all windows
cv2.destroyAllWindows()
Stop()

