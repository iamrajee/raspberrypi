import time as t
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

lm1= 31
lm2 = 33
rm1 = 35
rm2 = 37
b = 7
setpin1 = [b,lm1,lm2,rm1,rm2]
for pin in setpin1:
  GPIO.setup(pin,GPIO.OUT)

#GPIO.output(lm1,True)
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
def dleft():
    GPIO.output(lm1,0)
    GPIO.output(lm2,0)
    GPIO.output(rm1,1)
    GPIO.output(rm2,0)

def dright():
    GPIO.output(lm1,1)
    GPIO.output(lm2,0)
    GPIO.output(rm1,0)
    GPIO.output(rm2,0)


def backward():
    GPIO.output(lm1,0)
    GPIO.output(lm2,1)
    GPIO.output(rm1,0)
    GPIO.output(rm2,1)

def stop():
    GPIO.output(lm1,0)
    GPIO.output(lm2,0)
    GPIO.output(rm1,0)
    GPIO.output(rm2,0)

def buzzon():
    GPIO.output(b,1)
    
def buzzoff():
    GPIO.output(b,0)
    
    
# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
pts = deque(maxlen=args["buffer"])
 
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    vs = VideoStream(src=0).start()
 
# otherwise, grab a reference to the video file
else:
    vs = cv2.VideoCapture(args["video"])
 
# allow the camera or video file to warm up
time.sleep(2.0)

# keep looping
while True:
    # grab the current frame
    frame = vs.read()
 
    # handle the frame from VideoCapture or VideoStream
    frame = frame[1] if args.get("video", False) else frame
    
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
        break

    # resize the frame, blur it, and convert it to the HSV
    # color space
    #frame = imutils.resize(frame, width=600)

    blurred = cv2.GaussianBlur(frame, (11, 11), 0)

    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    


    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
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
        #print(radius)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
        # only proceed if the radius meets a minimum size
        if (radius > 30) and (radius < 100):
            xflag = 1
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
    
    fcx = np.shape(frame)[0]/2
    fcy = np.shape(frame)[1]/2
    cv2.circle(frame,(fcy,fcx),10,(0,255,0),-1)


    # update the points queue
    '''
    pts.appendleft(center)


    # loop over the set of tracked points
    for i in range(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        if pts[i - 1] is None or pts[i] is None:
            continue
 
        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
        '''
    # if the 'q' key is pressed, stop the loop
    
     
 
    

    

    #cv2.circle(frame,(fcx,fcy),10,(0,255,0),-1)
    
    
    # print(radius)
    if xflag == 1:
        delta = radius
        if x < fcy - delta:
            print("left")
            dleft()
        elif x  > fcy + delta:
            print("right")
            dright()
        # if y < fcy - delta:
        #     print("backward")
        #     backward()
        # elif y  > fcy + delta:
        #     print("forward")
        #     forward()
        else:
            print("stop")
            stop()
    else:
            print("stop")
            stop()
            
    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord("q"):
        break
        

 
# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
    vs.stop()
 
# otherwise, release the camera
else:
    vs.release()
 
# close all windows
cv2.destroyAllWindows()
stop()
