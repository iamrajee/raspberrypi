import numpy as np
import cv2

from picamera.array import PiRGBArray
from picamera import PiCamera
import time

import imutils
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


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



fx = 640
fy = 480

delta = 60
tl= fx/2 - delta
tr= fx/2 + delta

fright=0
fleft=0

#video_capture = cv2.VideoCapture(-1)
#video_capture.set(3, fx)
#video_capture.set(4, fy)

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (fx, fy)
camera.framerate = 64
rawCapture = PiRGBArray(camera, size=(fx, fy))
 
# allow the camera to warmup
time.sleep(0.1)

#while(True):
	# Capture the frames
#	ret, frame = video_capture.read()
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	frame = frame.array
	# Crop the image
	crop_img = frame[fy/2:fy, 0:fx]

	# Convert to grayscale
	gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

	# Gaussian blur
	blur = cv2.GaussianBlur(gray,(5,5),0)

	# Color thresholding
	ret,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)

	# Find the contours of the frame
	contours = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)
	
	contours = imutils.grab_contours(contours)
	#contours,hierarchy
	# print(type(temp),len(temp),temp)
	# print(np.shape(_))
	# Find the biggest contour (if detected)
	
	if len(contours) > 0:
                fright=0
                fleft=0
		c = max(contours, key=cv2.contourArea)

		M = cv2.moments(c)

 

		cx = int(M['m10']/M['m00'])

		cy = int(M['m01']/M['m00'])

 

		cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)

		cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)


		cv2.line(crop_img,(tl,0),(tl,fy/2),(0,0,255),2)
		cv2.line(crop_img,(tr,0),(tr,fy/2),(0,0,255),2)
 
		cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)

 

		if cx >= tr:
                    sright()
                    fright =1
##		    print("Turn Right")

		elif cx < tr and cx > tl:
                    forward()
                    #Stop()
##                    print("On Track!")

		elif cx <= tl:
                    sleft()
                    fleft =1
##		    print("Turn Left!")
                else:
                    Stop()

	else:
                '''
                if fright==1:
                    sleft()
                elif fleft==1:
                    sright()
                else:'''
                Stop()
		print("I don't see the line")


	cv2.imshow('frame',crop_img)
        key = cv2.waitKey(1) & 0xFF
	rawCapture.truncate(0)# clear the stream in preparation for the next frame
	if key == ord("q"):
            Stop()
	    break


