#!/usr/bin/python

import os,subprocess,glob,time
import cv2.cv as cv
from optparse import OptionParser

cv.NamedWindow("result", 1)

command = "raspistill -tl 65 -n -rot 180 -hf -o /run/shm/image%d.jpg -w 640 -h 480 -e jpg"
p=subprocess.Popen(command,shell = True)

# wait until we have at least 2 image files

for timeout in range (5):
	    files = filter(os.path.isfile, glob.glob('/run/shm/' + "image*.jpg"))
	    if len(files) > 1:
		break
	    print "waiting for images"
	    time.sleep(1)
if ( not len (files) > 1):
	    print "No images"
	    exit (1)
	
oldimage = None
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

	    #delete old files
	    for filename in files:
		if (filename == imagefile):
			break
		# os.remove(filename)
		 
	    if (imagefile == oldimage):
		#no new image from raspistill
	    	time.sleep (0.1)
	    else:
	    	# uncomment for spare cpu (reduce frame rate)
	    	# time.sleep (0.1)
	    	frame=cv.LoadImage(imagefile,cv.CV_LOAD_IMAGE_COLOR)
    	    	cv.ShowImage("result", frame)
		oldimage = imagefile
	    	t = cv.GetTickCount()  - t
            	print "capture = %gfps" % (1000 / (t/(cv.GetTickFrequency()*1000.)))
            if cv.WaitKey(1) >= 0:
                break
p.kill()
cv.DestroyWindow("result")

oldtime=0
for filename in files:
	mtime = os.path.getmtime(filename)
	print mtime - oldtime
	oldtime = mtime
