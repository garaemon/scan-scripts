from opencv import cv
from opencv import highgui
import Image                    # PIL
import os
import wx
import math

def pilTowxImage(pil):
    "convert a PIL image to wxImage"
    wximage = wx.EmptyImage(pil.size[0], pil.size[1])
    wximage.SetData(pil.convert('RGB').tostring())
    return wximage

def wxImageToPil(wximage):
    "convert a wxImage to PIL image"
    pil = Image.new('RGB', (wximage.GetWidth(), wximage.GetHeight()))
    pil.fromstring(wximage.GetData())
    return pil

class PILImageFrame(wx.Frame):
    """ a class for display a PIL image.
    """
    def __init__(self, pilimage, width=200):
        
        self._pilimage = pilimage
        #orgimage = pilToImage(self._pilimage).ConvertToBitmap()
        orgimage = pilToImage(self._pilimage)
        #wx.StaticBitmap(self, -1, self._image)
        org_size = orgimage.GetSize()
        scaled_size = (width, int(width / float(org_size[0]) * org_size[1]))
        wx.Frame.__init__(self, None, title = "image",
                          size = scaled_size)
        self._image = orgimage.Scale(scaled_size[0],
                                     scaled_size[1]).ConvertToBitmap()
        wx.StaticBitmap(self, -1, self._image)

class ImageContainer(object):
    _path = False
    _org_image = False                  # PIL Image
    _binary_image = False
    _showedp = False
    def __init__(self, path):
        self._path = path
        #self._org_image = load_image(path)
    def show(self):
        self._showedp = True
        if not self._org_image:
            self._org_image = load_image(self._path)
        f = PILImageFrame(self._org_image)
        #f.show()
        f.Show()
    def showedp(self):
        return self._showedp
    def binalize(self, h_min, h_max, s_min, s_max, v_min, v_max):
        self._binary_image = extract_color(self._org_image, h_min, h_max,
                                           s_min, s_max, v_min, v_max)
        f = PILImageFrame(self._binary_image)
        f.Show()
    
def load_image(file):
    """
    loading image from file and return a PIL image object.
    """
    return Image.open(os.path.abspath(file))

def extract_color(image,
                  h_min = 0, h_max = 360,
                  s_min = 0, s_max = 1.0,
                  v_min = 0, v_max = 1.0):
    ret = image.copy()
    pix = image.load()
    ret_pix = ret.load()
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            pixel = pix[x, y]
            hsv_pixel = RGB2HSV(pix[0], pix[1], pix[2])
            h = pixel[0]
            s = pixel[1]
            v = pixel[2]
            if h < h_min or h > h_max or s < s_min \
                    or s < s_max or v < v_min or v > v_max:
                ret_pix[x, y] = (0, 0, 0)
    return ret

def edge_detection(image):
    # NOT IMPLEMENTED
    # convert to OpenCV
    # canny
    # hough
    return True

# RGB -> HSV
# R, G, B, S, V -> 0 ~ 1
# h -> 0 ~ 360
def RGB2HSV( r, g, b ):
    r, g, b = map( float, (r,g,b ) )
    if r == g and g == b:
        ma = r
        mi = r
        h = 0
        v = r
    elif r > g and r > b:
        ma = r
        mi = min( g , b )
        h = 60 * ( g - b ) / ( ma - mi ) + 0
    elif g > b and g >= r:
        ma = g
        mi = min( b , r )
        h = 60 * ( b - r ) / ( ma - mi ) + 120
    elif b >= r and b >= g:
        ma = b
        mi = min( r , g )
        h = 60 * ( r - g ) / ( ma - mi ) + 240
    else:
        raise Exception("error")
    if ma == 0:
        return 0, 0, 0
    s = (ma - mi) / ma
    v = ma
    return h, s, v

# HSV -> RGB
def HSV2RGB( h, s, v ):
    hi = math.floor(h / 60.0) % 6
    f =  (h / 60.0) - math.floor(h / 60.0)
    p = v * (1.0 - s)
    q = v * (1.0 - (f*s))
    t = v * (1.0 - ((1.0 - f) * s))
    if hi == 0:
        return (v, t, p)
    elif hi == 1:
        return (q, v, p)
    elif hi == 2:
        return (q, v, t)
    elif hi == 3:
        return (p, q, v)
    elif hi == 4:
        return (t, p, v)
    elif hi == 5:
        return (v, p, q)

def HSVPILImage(h, s, v, width, height):
    "make a PIL image from HSV value and width, height."
    ret = Image.new('RGB', (width, height))
    pix = ret.load()
    r, g, b = HSV2RGB(h, s, v)
    r *= 255.0
    g *= 255.0
    b *= 255.0
    for x in range(width):
        for y in range(height):
            pix[x, y] = (r, g, b)
    return ret

def HSVwxImage(h, s, v, width, height):
    "make a wx.Image from HSV value and width and height."
    pil = HSVPILImage(h, s, v, width, height)
    return pilTowxImage(pil)
