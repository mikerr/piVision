#!/usr/bin/python

import os,subprocess,glob,time
import cv2.cv as cv
from optparse import OptionParser

cv.NamedWindow("result", 1)

command = "raspistill -tl 65 -n -rot 180 -o /run/shm/image%d.jpg -w 640 -h 480 -e jpg"
p=subprocess.Popen(command,shell = True)

# wait until we have at least 2 image files

while True:
	    files = filter(os.path.isfile, glob.glob('/run/shm/' + "image*jpg"))
	    if len(files) > 1:
		break
	    print "waiting for images"
	    time.sleep(0.5)
	
if True:
	detected = 0
        frame = None
        while True:
        
	    t = cv.GetTickCount() 

	    if p.poll() is not None:
			print "restarting raspistill"
    			p=subprocess.Popen(command,shell=True)

	    files = filter(os.path.isfile, glob.glob('/run/shm/' + "image*jpg"))
	    files.sort(key=lambda x: os.path.getmtime(x))
	    imagefile = (files[-2])
		 
	    frame=cv.LoadImage(imagefile,cv.CV_LOAD_IMAGE_COLOR)
	    # uncomment for spare cpu (reduce frame rate)
	    time.sleep (0.05)
	    t = cv.GetTickCount()  - t
    	    cv.ShowImage("result", frame)
            print "capture = %gfps" % (1000 / (t/(cv.GetTickFrequency()*1000.)))
            if cv.WaitKey(1) >= 0:
                break
p.kill()
cv.DestroyWindow("result")
