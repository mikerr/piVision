piVision
========

Python based vision tests - face / object detection and tracking

filters.py - GUI demo of basic python image filters:

               takes a photo with the raspberry camera, and give options of 
               blur,contour,find_edges,emboss,edge_enhance

             
facedetect.sh - starter script for  facedetect.py


facedetect.py - face detection using the pi camera
<a href="https://www.youtube.com/watch?v=opUfKthZJ00">
<img src=http://i1.ytimg.com/vi/opUfKthZJ00/1.jpg?time=1377977636623 align=right></a>

               draws a red box around each face detected
               (supports muliple faces per frame)
               currently 8fps

colortrack.py - tracking by colour

               blob object tracking based on colour range
               double click object in main window to select colour
               
               
display.py - openCV display test

             repeatedly loads frames from the pi camera to test frame rate
             using BMP or JPEG
