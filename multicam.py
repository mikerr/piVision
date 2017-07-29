import cv2
import numpy as np

cams = []
for i in range(0,9):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        cams.append(cap)
        print "found camera at index " ,  i

while True:
    name = "Camera "
    for cam in cams:
        name = name + "."
        _,frame = cam.read()
        cv2.imshow(name,frame)

    if cv2.waitKey(1) == ord('q'):
        break
cv2.destroyAllWindow
