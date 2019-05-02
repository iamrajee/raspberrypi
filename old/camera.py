import cv2

cv2.namedWindow("preview")
vc = cv2.VideoCapture(1)
vc.set(3,2560) #1920
vc.set(4,1920)#1080

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

cv2.destroyWindow("preview")
vc.release()