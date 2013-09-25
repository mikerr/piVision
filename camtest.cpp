/* Compile with

   gcc -std=c++0 -lopencv_core -lopencv_highgui 
   -L/usr/lib/uv4l/uv4lext/armv6l -luv4lext -Wl,-rpath,'/usr/lib/uv4l/uv4lext/armv6l' 
   test.cpp -o test 
*/

#include "opencv2/highgui/highgui.hpp"
#include <iostream>
#include <chrono>

using namespace std;
using namespace chrono;
using namespace cv;

int main(int argc, char** argv){
    VideoCapture cap(-1);
    if (!cap.isOpened())
    {
        cout << "Cannot open camera" << endl;
        return -1;
    }
   cap.set(CV_CAP_PROP_FRAME_WIDTH, 320);
   cap.set(CV_CAP_PROP_FRAME_HEIGHT, 240);

   namedWindow("Output",CV_WINDOW_AUTOSIZE);

    unsigned long f = 0;
    auto start = monotonic_clock::now();
    while (1)
    {
        Mat frame;
        bool bSuccess = cap.read(frame);

        if (!bSuccess)
        {
        cout << "Cannot read a frame from camera" << endl;
        break;
        }

        auto elapse = duration_cast<seconds>(monotonic_clock::now() - start).count();
        ++f;
        auto fps = elapse ? f / elapse : 0;
        if (!(elapse % 5) && fps) // print the framerate every 5s, for 1s
            cout << "fps: " << fps << ", total frames: " << f
                 << " elapsed time: " << elapse << "s\n";

        imshow("Output", frame);

        if (waitKey(30) == 27)
        {
        cout << "Exit, fps: " << fps << endl;
        break;
        }
    }
    return 0;
}

