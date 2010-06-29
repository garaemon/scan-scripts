#include <cv.h>
#include <highgui.h>
#include <math.h>
#define SCALING 0.4

using namespace cv;

int main(int argc, char** argv)
{
    Mat src, dst, color_dst, a, b, src2;
    if( argc != 2 || !(src=imread(argv[1], 0)).data)
        return -1;
    //threshold(src2, src, 200, 255, THRESH_BINARY);
    Canny( src, dst, 470, 850, 3);
    cvtColor( dst, color_dst, CV_GRAY2BGR );

#if 1
    vector<Vec2f> lines;
    HoughLines( dst, lines, 1, CV_PI/180, 300 );

    for( size_t i = 0; i < lines.size(); i++ )
    {
        float rho = lines[i][0];
        float theta = lines[i][1];
        double a = cos(theta), b = sin(theta);
        double x0 = a*rho, y0 = b*rho;
        Point pt1(cvRound(x0 + 2000*(-b)),
                  cvRound(y0 + 2000*(a)));
        Point pt2(cvRound(x0 - 2000*(-b)),
                  cvRound(y0 - 2000*(a)));
        line( color_dst, pt1, pt2, Scalar(0,0,255), 3, 8 );
    }
#else
    vector<Vec4i> lines;
    HoughLinesP( dst, lines, 1, CV_PI/180, 300,
                 600, 60 );
    for( size_t i = 0; i < lines.size(); i++ )
    {
        line( color_dst, Point(lines[i][0], lines[i][1]),
            Point(lines[i][2], lines[i][3]), Scalar(0,0,255), 3, 8 );
    }
#endif
    namedWindow( "Source", 1 );
    namedWindow( "Detected Lines", 1 );
    resize(src, a, Size(), SCALING, SCALING);
    resize(color_dst, b, Size(), SCALING, SCALING);
    imshow( "Source", a );
    imshow( "Detected Lines", b);
    

    waitKey(0);
    return 0;
}

