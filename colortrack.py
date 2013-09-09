#!/usr/bin/python
"""
colortrack.py - track object by its colour

ifirst double lcik on selected colour,
then track any blobs with that colour
"""

import os,subprocess,glob,time
import cv2.cv as cv

posx=0
posy=0
global h,s,v,i,im,evente
h,s,v,i,r,g,b,j,evente=0,0,0,0,0,0,0,0,0

#	Mouse callback function	(from earlier mouse_callback.py with little modification)
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

#	Thresholding function	(from earlier mouse_callback.py)	
def getthresholdedimg(im):
	'''This function take RGB image.Then convert it into HSV for easy colour detection and threshold it with the given part as white and all other regions as black.Then return that image'''
	imghsv=cv.CreateImage(cv.GetSize(im),8,3)
	cv.CvtColor(im,imghsv,cv.CV_BGR2HSV)
	imgthreshold=cv.CreateImage(cv.GetSize(im),8,1)
	cv.InRangeS(imghsv,cv.Scalar(h,100,10),cv.Scalar(h+10,255,255),imgthreshold)
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

# get a frame

command = "raspistill -tl 65 -n -rot 180 -hf -o /run/shm/image%d.jpg -w 320 -h 240 -e bmp"
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

# get (last-1) recent image
files.sort(key=lambda x: os.path.getmtime(x))
imagefile = (files[-2])

frame=cv.LoadImage(imagefile,cv.CV_LOAD_IMAGE_COLOR)

cv.NamedWindow("pick")
cv.SetMouseCallback("pick",my_mouse_callback)
while(1):
	cv.ShowImage("pick",frame)
	cv.WaitKey(33)
	if evente==7:	# When double-clicked(i.e. event=7), this window closes and opens next window
		break


cv.NamedWindow("output")
cv.NamedWindow("threshold")	

print "opened windows"
time.sleep(1)
while(1):
	if p.poll() is not None:
			print "restarting raspistill"
    			p=subprocess.Popen(command,shell=True)
	files = filter(os.path.isfile, glob.glob('/run/shm/' + "image*jpg"))
	files.sort(key=lambda x: os.path.getmtime(x))
	imagefile = (files[-2])

	frame=cv.LoadImage(imagefile,cv.CV_LOAD_IMAGE_COLOR)

	test=cv.CreateImage(cv.GetSize(frame),8,1)	# We make all drawings on imdraw.
	imdraw=cv.CreateImage(cv.GetSize(frame),8,1)	# We make all drawings on imdraw.

	#cv.Flip(frame,frame,1)				# Horizontal flipping for synchronization, comment it to see difference.
	thresh_img=getthresholdedimg(frame)		# We get coordinates from thresh_img
	cv.Erode(thresh_img,thresh_img,None,1)		# Eroding removes small noises
	(leftmost,rightmost,topmost,bottommost)=getpositions(thresh_img)
	if (leftmost-rightmost!=0) or (topmost-bottommost!=0):
		lastx=posx
		lasty=posy
		posx=cv.Round((rightmost+leftmost)/2)
		posy=cv.Round((bottommost+topmost)/2)
		if lastx!=0 and lasty!=0:
			cv.Line(imdraw,(posx,posy),(lastx,lasty),(b,g,r))
		cv.Circle(imdraw,(posx,posy),5,(b,g,r),-1)

	#cv.Add(test,imdraw,test)			# Adding imdraw on test keeps all lines there on the test frame. If not, we don't get full drawing, instead we get only that fraction of line at the moment.

    	cv.ShowImage("pick", frame)
	cv.ShowImage("output",imdraw)
	cv.ShowImage("threshold",thresh_img)

	if cv.WaitKey(100)>= 0:
		break
p.kill()

