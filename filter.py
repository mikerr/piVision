#!/usr/bin/python

# quick demo of some python image filters
# using raspberry pi camera

import subprocess
import Tkinter as tk
from PIL import Image,ImageFilter,ImageChops,ImageTk

imagefile = "/dev/shm/image.jpg"
w = 800
h = 600

def takephoto():
    command = "raspistill -n -w %s -h %s -t 0 -o %s" % (w, h, imagefile)
    subprocess.check_output(command, shell=True)
    image1 = Image.open(imagefile)
    return image1

def newphoto():
	global image1
	image1 =  takephoto()

	tkimage1 = ImageTk.PhotoImage(image1)
	panel1.configure(image=tkimage1)
	panel1.image = tkimage1

def invert():
	global image1
	image1= ImageChops.invert(image1)

	tkimage1 = ImageTk.PhotoImage(image1)
	panel1.configure(image=tkimage1)
	panel1.image = tkimage1

def grayscale():
	global image1
	r, g, b = image1.split()
    	image1 = Image.merge("RGB", (g,g,g))

	tkimage1 = ImageTk.PhotoImage(image1)
	panel1.configure(image=tkimage1)
	panel1.image = tkimage1

def dofilter (theimage,thefilter):
	global image1
	image1 =  image1.filter(thefilter)
	tkimage1 = ImageTk.PhotoImage(image1)
	panel1.configure(image=tkimage1)
	panel1.image = tkimage1
	
# Setup a window
root = tk.Tk()
root.title('Image')

image1 = takephoto()
tkimage1 = ImageTk.PhotoImage(image1)

w = tkimage1.width()
h = tkimage1.height()
root.geometry("%dx%d+%d+%d" % (w, h, 0, 0))

# root has no image argument, so use a label as a panel
panel1 = tk.Label(root, image=tkimage1)
panel1.pack(side='top', fill='both', expand='yes')

# save the panel's image from 'garbage collection'
panel1.image = tkimage1

# Add some buttons
buttonrow = tk.Frame(root)
buttonrow.place(y=0,x=0)

button = tk.Button(buttonrow, text='CAMERA',command = newphoto)
button.pack(side='left',)
button = tk.Button(buttonrow, text='INVERT',command = invert)
button.pack(side='left',)
button = tk.Button(buttonrow, text='GRAY',command = grayscale)
button.pack(side='left',)
# add some filter buttons
button = tk.Button(buttonrow, text='BLUR',command = lambda: dofilter(image1,ImageFilter.BLUR))
button.pack(side='left')
button = tk.Button(buttonrow, text='CONTOUR',command = lambda: dofilter(image1,ImageFilter.CONTOUR))
button.pack(side='left')
button = tk.Button(buttonrow, text='FIND_EDGES',command = lambda: dofilter(image1,ImageFilter.FIND_EDGES))
button.pack(side='left')
button = tk.Button(buttonrow, text='EMBOSS',command = lambda: dofilter(image1,ImageFilter.EMBOSS))
button.pack(side='left')
button = tk.Button(buttonrow, text='EDGE_ENHANCE',command = lambda: dofilter(image1,ImageFilter.EDGE_ENHANCE))
button.pack(side='left')

# resize event:

def onResizeWindow(event):
	global image1
    	image1 = image1.resize((event.width,event.height),Image.NEAREST)
	tkimage1 = ImageTk.PhotoImage(image1)
	panel1.configure(image=tkimage1)
	panel1.image = tkimage1
# root.bind( '<Configure>', onResizeWindow )

root.mainloop()
