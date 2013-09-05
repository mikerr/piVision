piVision
========

Simple python based vision tests

filters.py - GUI demo of basic python image filters:

               takes a photo with the raspberry camera, and give options of 
               blur,contour,find_edges,emboss,edge_enhance

             
facedetect.sh - starter script for  facedetect.py

facedetect.py - face detection using the pi camera

               draws a red box around each face detected
               (supports muliple faces per frame)


display.py - openCV display test

             repeatedly loads frames from the pi camera to test frame rate
             using BMP or JPEG
