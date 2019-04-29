#========================== IMPORTS ========================#
from collections import deque
import numpy as np
import cv2
import imutils
import time

from picamera import PiCamera          #PICAMERA
from picamera.array import PiRGBArray

import RPi.GPIO as GPIO #GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#========================== MOTOR PINS  AND FUNCTIONS (Only run on Raspi)========================#
lm1= 31
lm2 = 33
rm1 = 35
rm2 = 37
b = 7

setpin1 = [b,lm1,lm2,rm1,rm2]
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

def buzzon():
    GPIO.output(b,1)
    
def buzzoff():
    GPIO.output(b,0)
#-------------------------------------------------------------#

#========================== VARIABLE ========================#
fx = 640
fy = 480
delta = 60
tl= fx/2 - delta
tr= fx/2 + delta

# define the lower and upper boundaries of the "green"
#ball in the HSV color space, then initialize the
#list of tracked points
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
#-------------------------------------------------------------#



'''
#******************* USING WEB CAM====================#
vc = cv2.VideoCapture(-1)
time.sleep(2.0)# allow the camera or video file to warm up
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
        
    #cv2.imshow("Actual_Frame", frame)      #<<--

    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    #cv2.imshow("blurred", blurred)      #<<--
    
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    #cv2.imshow("hsv", hsv)      #<<--
    
    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    #cv2.imshow("mask", mask)      #<<--
    mask = cv2.erode(mask, None, iterations=2)
    #cv2.imshow("erode", mask)      #<<--
    mask = cv2.dilate(mask, None, iterations=2)
    #cv2.imshow("dilate", mask)      #<<--
    

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None
    
    xflag = 0
    # only proceed if at least one contour was found
    if len(cnts) > 0:
        
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)

        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
        # only proceed if the radius meets the constrains
        if (radius > 30) and (radius < 100):
            xflag = 1
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
    
    fcx = np.shape(frame)[0]/2
    fcy = np.shape(frame)[1]/2
    cv2.circle(frame,(fcy,fcx),10,(0,255,0),-1)

    if xflag == 1:
        delta = radius
        if x < fcy - delta:
            print("left")
            sleft()
        elif x  > fcy + delta:
            print("right")
            sright()
        else:
            print("stop")
            Stop()
    else:
        print("stop")
        Stop()
            
    # show the frame to our screen
    cv2.imshow("Final_Frame", frame) #<<---
    key = cv2.waitKey(1) & 0xFF
    
    rawCapture.truncate(0)# picamera only # clear the stream in preparation for the next frame
	    
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# close all windows
cv2.destroyAllWindows()
Stop()


