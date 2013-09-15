#!/usr/bin/python

import os,subprocess,glob,time
import cv2.cv as cv
from optparse import OptionParser

cv.NamedWindow("result", 1)

raspicam=0
if raspicam:
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
else:
	capture=cv.CaptureFromCAM(0)
	cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 320 );
	cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 240 );
	
oldimage = None
if True:
	detected = 0
        frame = None
        while True:
        
	    t = cv.GetTickCount() 

	    if raspicam:
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
	    		oldimage = imagefile
	    else:
		frame=cv.QueryFrame(capture)
    	    cv.ShowImage("result", frame)
            if cv.WaitKey(10) >= 0:
                break
	    t = cv.GetTickCount()  - t
            print "capture = %gfps" % (1000 / (t/(cv.GetTickFrequency()*1000.)))
p.kill()
cv.DestroyWindow("result")

oldtime=0
for filename in files:
	mtime = os.path.getmtime(filename)
	print mtime - oldtime
	oldtime = mtime
