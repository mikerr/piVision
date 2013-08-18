#!/usr/bin/python
import subprocess
import Tkinter as tk
from PIL import Image,ImageFilter, ImageTk

imagefile = "image.jpg"
w = 640
h = 480

def takephoto():
    command = "raspistill -n -w %s -h %s -t 0 -o image.jpg" % (w, h)
    subprocess.check_output(command, shell=True)
    image1 = Image.open(imagefile)
    # image1 = image1.resize((640,480),Image.NEAREST)
    return image1

def newphoto():
	global image1
	image1 =  takephoto()
	tkimage1 = ImageTk.PhotoImage(image1)
	panel1.configure(image=tkimage1)
	panel1.image = tkimage1

def dofilter (theimage,thefilter):
	global image1
	processed =  image1.filter(thefilter)
	image1 = processed
	tkimage1 = ImageTk.PhotoImage(processed)
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
button = tk.Button(buttonrow, text='INVERT',command = newphoto)
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
button = tk.Button(buttonrow, text='INVERT',command = lambda: dofilter(image1,ImageFilter.INVERT))

root.mainloop()
