# import the necessary packages
# from pyimagesearch.shapedetector import ShapeDetector
from ColorLabeler import ColorLabeler
import argparse
import imutils
import cv2
import time
from collections import deque
from imutils.video import VideoStream

# # construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True,
# 	help="path to the input image")
# args = vars(ap.parse_args())

# # load the image and resize it to a smaller factor so that
# # the shapes can be approximated better
# image = cv2.imread(args["image"])

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
#     countor(frame)
# def countor(image):
	image = frame
	# image = cv2.imread("color_test.png")
	resized = imutils.resize(image, width=300)
	ratio = image.shape[0] / float(resized.shape[0])
	
	# blur the resized image slightly, then convert it to both
	# grayscale and the L*a*b* color spaces
	blurred = cv2.GaussianBlur(resized, (5, 5), 0)
	gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
	lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
	thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]
	cv2.imshow("Thresh", thresh)
	
	# find contours in the thresholded image
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	
	# initialize the shape detector and color labeler
	# sd = ShapeDetector()
	cl = ColorLabeler()
	
	# loop over the contours
	for c in cnts:
		# compute the center of the contour
		M = cv2.moments(c)
		if M["m00"] == 0:
			continue
		cX = int((M["m10"] / M["m00"]) * ratio)
		cY = int((M["m01"] / M["m00"]) * ratio)
	
		# detect the shape of the contour and label the color
		# shape = sd.detect(c)
		color = cl.label(lab, c)
	
		# multiply the contour (x, y)-coordinates by the resize ratio,
		# then draw the contours and the name of the shape and labeled
		# color on the image
		c = c.astype("float")
		c *= ratio
		c = c.astype("int")
		# text = "{} {}".format(color, shape)
		# text = "{}".format(color)
		text = color
		cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
		cv2.putText(image, text, (cX, cY),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
	
		# show the output image
		cv2.imshow("Image", image)
		# cv2.waitKey(0)
		key = cv2.waitKey(1) & 0xFF
    
    	if key == ord("q"):
        	break