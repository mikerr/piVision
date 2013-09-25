#!/usr/bin/python
"""
colortrack.py - track object by it's colour

first double click on selected colour,
then track any blobs with that colour
"""

import os,subprocess,glob,time
#import cv2.cv as cv
import cv

posx=0
posy=0
global h,s,v,i,im,evente
h,s,v,i,r,g,b,j,evente=0,0,0,0,0,0,0,0,0

#	Mouse callback function	
def my_mouse_callback(event,x,y,flags,param):
	global evente,h,s,v,i,r,g,b,j
	evente=event
	if event==cv.CV_EVENT_LBUTTONDBLCLK:		# Here event is left mouse button double-clicked
		hsv=cv.CreateImage(cv.GetSize(frame),8,3)
		cv.CvtColor(frame,hsv,cv.CV_BGR2HSV)
		(h,s,v,i)=cv.Get2D(hsv,y,x)
		(r,g,b,j)=cv.Get2D(frame,y,x)
		print "x,y =",x,y
		print "hsv= ",cv.Get2D(hsv,y,x)		# Gives you HSV at clicked point
		print "im= ",cv.Get2D(frame,y,x) 	# Gives you RGB at clicked point

#	Thresholding function	
def getthresholdedimg(im):
	'''This function take RGB image.Then convert it into HSV for easy colour detection and threshold it with the given part as white and all other regions as black.Then return that image'''
	imghsv=cv.CreateImage(cv.GetSize(im),8,3)
	cv.CvtColor(im,imghsv,cv.CV_BGR2HSV)
	imgthreshold=cv.CreateImage(cv.GetSize(im),8,1)
	cv.InRangeS(imghsv,cv.Scalar(h,100,10),cv.Scalar(h+20,255,255),imgthreshold)
	return imgthreshold

def getpositions(im):
	''' this function returns leftmost,rightmost,topmost and bottommost values of the white blob in the thresholded image'''
	leftmost=0
	rightmost=0
	topmost=0
	bottommost=0
	temp=0
	for i in range(im.width):
		col=cv.GetCol(im,i)
		if cv.Sum(col)[0]!=0.0:
			rightmost=i
			if temp==0:
				leftmost=i
				temp=1		
	for i in range(im.height):
		row=cv.GetRow(im,i)
		if cv.Sum(row)[0]!=0.0:
			bottommost=i
			if temp==1:
				topmost=i
				temp=2	
	return (leftmost,rightmost,topmost,bottommost)

raspicam = 1 
if raspicam:
	
	command = "raspistill -tl 65 -n -rot 180 -hf -o /run/shm/image%d.jpg -w 320 -h 240 -e bmp >/dev/null"
	p=subprocess.Popen(command,shell = True)

	# wait until we have at least 2 image files

	for timeout in range (5):
	    files = filter(os.path.isfile, glob.glob('/run/shm/' + "image*.jpg"))
	    if len(files) > 1:
		break
	    print "waiting for images"
	    time.sleep(5)
	if ( not len (files) > 1):
	    print "No images"
	    exit (1)

	# get (last-1) recent image
	files.sort(key=lambda x: os.path.getmtime(x))
	imagefile = (files[-2])

	frame=cv.LoadImage(imagefile,cv.CV_LOAD_IMAGE_COLOR)

else:
	#usb cam

	capture=cv.CaptureFromCAM(0)
	cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 320 );
	cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 240 );

	frame=cv.QueryFrame(capture)

test=cv.CreateImage(cv.GetSize(frame),8,3)	
imdraw=cv.CreateImage(cv.GetSize(frame),8,3)	# We make all drawings on imdraw.

cv.NamedWindow("pick")
cv.SetMouseCallback("pick",my_mouse_callback)

cv.NamedWindow("output")
cv.NamedWindow("threshold")	

h = 8; # orange
pan = 100
pandir = 0

while(1):

	if raspicam:
		if p.poll() is not None:
			#exit (0)
			print "restarting raspistill"
    			p=subprocess.Popen(command,shell=True)
		files = filter(os.path.isfile, glob.glob('/run/shm/' + "image*jpg"))
		files.sort(key=lambda x: os.path.getmtime(x))
		imagefile = (files[-2])

		frame=cv.LoadImage(imagefile,cv.CV_LOAD_IMAGE_COLOR)
	else:
		#usb cam
		frame=cv.QueryFrame(capture)

	thresh_img=getthresholdedimg(frame)		# We get coordinates from thresh_img
	
	cv.Erode(thresh_img,thresh_img,None,1)		# Eroding removes small noises
	cv.Dilate(thresh_img,thresh_img,None,1)		# Dilate

	cv.ShowImage("threshold",thresh_img)
	storage = cv.CreateMemStorage(0)
	contour = cv.FindContours(thresh_img, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_NONE)
	points = []	

	while contour:
		# Draw bounding rectangles
		bound_rect = cv.BoundingRect(list(contour))

		
		if (cv.ContourArea(contour) > 200):
			pt1 = (bound_rect[0], bound_rect[1])
			pt2 = (bound_rect[0] + bound_rect[2], bound_rect[1] + bound_rect[3])
			points.append(pt1)
			points.append(pt2)
			cv.Rectangle(frame, pt1, pt2, cv.CV_RGB(255,0,0), 1)

			obj_mid = bound_rect[0] + ( bound_rect[2] /2 )
			frame_mid = frame.width / 2
			mid =  frame_mid - obj_mid

			# only move if not near middle

			offset = abs(mid)
			if  offset > 20:
				pandir= (mid / offset)
			else: 
				pandir=0
		contour = contour.h_next()

	(leftmost,rightmost,topmost,bottommost)=getpositions(thresh_img)
	if (leftmost-rightmost!=0) or (topmost-bottommost!=0):
		lastx=posx
		lasty=posy
		posx=cv.Round((rightmost+leftmost)/2)
		posy=cv.Round((bottommost+topmost)/2)
		if lastx!=0 and lasty!=0:
			cv.Line(imdraw,(posx,posy),(lastx,lasty),(b,g,r))
			cv.Circle(imdraw,(posx,posy),5,(b,g,r),-1)

	cv.Add(test,imdraw,test)	# Adding imdraw on test keeps all lines there on the test frame. If not, we don't get full drawing, instead we get only that fraction of line at the moment.

    	cv.ShowImage("pick", frame)
	cv.ShowImage("output",test)

	pan = int (pan + pandir)
	if pan > 180: 
		pan = 180
	if pan < 0: 
		pan = 0

	os.system('echo "0="' + str(pan) + ' >/dev/servoblaster')

	if cv.WaitKey(1)>= 0:
		break
	if evente == cv.CV_EVENT_LBUTTONDBLCLK:
		print "double click"
		cv.Set(test, cv.CV_RGB(0,0,0));

