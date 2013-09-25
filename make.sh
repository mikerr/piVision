#!/bin/sh
gcc -std=c++0x  -lopencv_core -lopencv_highgui -L/usr/lib/uv4l/uv4lext/armv6l -luv4lext -Wl,-rpath,'/usr/lib/uv4l/uv4lext/armv6l' camtest.cpp -o camtest
