import numpy as np
import cv2
import imutils

video_capture = cv2.VideoCapture(-1)
fx = 640
fy = 480
video_capture.set(3, fx)
video_capture.set(4, fy)

delta = 50
tl= fx/2 - delta
tr= fx/2 + delta

while(True):
	# Capture the frames
	ret, frame = video_capture.read()

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

			print("Turn Left!")

 

		if cx < tr and cx > tl:

			print("On Track!")

 

		if cx <= tl:
			print("Turn Right")
	else:
		print("I don't see the line")

	#Display the resulting frame
	# cv2.imshow('frame1',blur)

	cv2.imshow('frame2',thresh)
	cv2.imshow('frame',crop_img)
	if cv2.waitKey(1) & 0xFF == ord('q'):

		break
