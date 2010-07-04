from opencv import cv
from opencv import highgui
import Image                    # PIL
import os

def load_image(file):
    """
    loading image from file and return a PIL image object.
    """
    return Image.open(os.path.abspath(file))

def extract_color(image,
                  h_min = 0, h_max = 255,
                  s_min = 0, s_max = 255,
                  v_min = 0, v_max = 255):
    ret = image.copy()
    pix = image.load()
    ret_pix = ret.load()
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            pixel = pix[x, y]
            h = pixel[0]
            s = pixel[1]
            v = pixel[2]
            if h < h_min or h > h_max or s < s_min or s < s_max or v < v_min or v > v_max:
                ret_pix[x, y] = (0, 0, 0)
    return ret

def edge_detection(image):
    # NOT IMPLEMENTED
    # convert to OpenCV
    # canny
    # hough
    return True
