#!/usr/bin/python
"""
Face and object detection using haar-like features.
Finds faces in a camera image or video stream and displays a red box around them.

Based on a python implementation by: Roman Stanchak, James Bowman
"""
import os,subprocess,glob,time
import cv2.cv as cv
from optparse import OptionParser

# Parameters for haar detection
# From the API:
# The default parameters (scale_factor=2, min_neighbors=3, flags=0) are tuned 
# for accurate yet slow object detection. For a faster operation on real video 
# images the settings are: 
# scale_factor=1.2, min_neighbors=2, flags=CV_HAAR_DO_CANNY_PRUNING, 
# min_size=<minimum possible face size

min_size = (5,5)
haar_scale = 1.2
min_neighbors = 2
haar_flags = 0
# detection image width
smallwidth = 70

def detect_and_draw(img, cascade, detected):
    # allocate temporary images

    gray = cv.CreateImage((img.width,img.height), 8, 1)
    image_scale = img.width / smallwidth
    small_img = cv.CreateImage((cv.Round(img.width / image_scale), cv.Round (img.height / image_scale)), 8, 1)

    # convert color input image to grayscale
    cv.CvtColor(img, gray, cv.CV_BGR2GRAY)

    # scale input image for faster processing
    cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)

    cv.EqualizeHist(small_img, small_img)

    if(cascade):
        t = cv.GetTickCount()
        faces = cv.HaarDetectObjects(small_img, cascade, cv.CreateMemStorage(0), haar_scale, min_neighbors, haar_flags, min_size)
        # t = cv.GetTickCount() - t
        # print "detection time = %gms" % (t/(cv.GetTickFrequency()*1000.))
        if faces:
	    if detected == 0:
		# os.system('festival --tts hi &')
		detected = 1
            for ((x, y, w, h), n) in faces:
                # the input to cv.HaarDetectObjects was resized, so scale the 
                # bounding box of each face and convert it to two CvPoints
                pt1 = (int(x * image_scale), int(y * image_scale))
                pt2 = (int((x + w) * image_scale), int((y + h) * image_scale))
                cv.Rectangle(img, pt1, pt2, cv.RGB(255, 0, 0), 3, 8, 0)
		print "Face at: ", pt1[0], ",", pt2[0], "\t", pt1[1], ",", pt2[1]
		# find amount needed to pan/tilt
		span = (pt1[0] + pt2[0]) / 2
		stlt = (pt1[1] + pt2[1]) / 2
		mid = smallwidth /2
		if span < mid:
			 print "left", mid -span
		else:
			 print "right", span - mid

		#os.system('echo "6="' + str(valTilt) + ' > /dev/pi-blaster')
		#os.system('echo "7="' + str(valPan) + ' > /dev/pi-blaster')
	else:
		if detected == 1:
			#print "Last seen at: ", pt1[0], ",", pt2[0], "\t", pt1[1], ",", pt2[1]
			#os.system('festival --tts bye &')
			status = "just disappeared"
		detected = 0

    cv.ShowImage("result", img)
    return detected

if __name__ == '__main__':
    parser = OptionParser(usage = "usage: %prog [options] [filename|camera_index]")
    parser.add_option("-c", "--cascade", action="store", dest="cascade", type="str", help="Haar cascade file, default %default", default = "../data/haarcascades/haarcascade_frontalface_alt.xml")
    (options, args) = parser.parse_args()

    cascade = cv.Load(options.cascade)
    
    cv.NamedWindow("result", 1)


    command = "raspistill -tl 100 -n -rot 180 -o /run/shm/image%d.jpg -w 320 -h 240 -e bmp"
    p=subprocess.Popen(command,shell=True)

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
            detected = detect_and_draw(frame, cascade, detected)
	    # uncomment if you want some spare cpu - reduced from 7fps to 5fps
	    # time.sleep(0.05)
	    t = cv.GetTickCount()  - t
            print "capture = %gfps" % (1000 / (t/(cv.GetTickFrequency()*1000.)))
            if cv.WaitKey(1) >= 0:
                break

    cv.DestroyWindow("result")
