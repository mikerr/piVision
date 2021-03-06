import cv2
import numpy as np

cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)

while True:
    _,cam1 = cap1.read()
    _,cam2 = cap2.read()
    sidebyside = np.hstack((cam1,cam2))
    cv2.imshow("Multicam",sidebyside)

    if cv2.waitKey(1) == ord('q'):
        break
cap1.release()
cap2.release()
cv2.destroyAllWindow
