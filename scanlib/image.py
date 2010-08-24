import platform
arch = platform.system()
if arch == "Linux":
    from opencv import cv
    from opencv import highgui
    import Image                    # PIL
elif arch == "Darwin":
    import cv
    from PIL import Image
import os
import wx
import math
import colorsys

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
    def __init__(self, pilimage, width=600):
        
        self._pilimage = pilimage
        #orgimage = pilToImage(self._pilimage).ConvertToBitmap()
        orgimage = pilTowxImage(self._pilimage)
        #wx.StaticBitmap(self, -1, self._image)
        org_size = orgimage.GetSize()
        scaled_size = (width, int(width / float(org_size[0]) * org_size[1]))
        wx.Frame.__init__(self, None, title = "image",
                          size = scaled_size)
        self._image = orgimage.Scale(scaled_size[0],
                                     scaled_size[1]).ConvertToBitmap()
        bitmap = wx.StaticBitmap(self, -1, self._image)
        self.Bind(wx.EVT_LEFT_DOWN, self.clickCallback) # does not work...
    def clickCallback(self, e):
        pos = e.GetPosition()
        print pos

class ImageContainer(object):
    _path = False
    _org_image = False                  # PIL Image
    _binary_image = False
    _showedp = False
    def __init__(self, path):
        self._path = path
        self._org_image = load_image(path)
    def Show(self):
        self._showedp = True
        if not self._org_image:
            self._org_image = load_image(self._path)
        f = PILImageFrame(self._org_image)
        f.Show()
    def Showedp(self):
        return self._showedp
    def Binalize(self, h_min, h_max, s_min, s_max, v_min, v_max):
        print (h_min, h_max, s_min, s_max, v_min, v_max)
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
                  h_min = 0, h_max = 1.0,
                  s_min = 0, s_max = 1.0,
                  v_min = 0, v_max = 1.0):
    ret = image.copy()
    pix = image.load()
    ret_pix = ret.load()
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            pixel = pix[x, y]
            hsv_pixel = colorsys.rgb_to_hsv(pixel[0] / 255.0, pixel[1] / 255.0, pixel[2] / 255.0)
            h = hsv_pixel[0]
            s = hsv_pixel[1]
            v = hsv_pixel[2]
            if h < h_min or h > h_max or s < s_min \
                    or s > s_max or v < v_min or v > v_max:
                ret_pix[x, y] = (0, 0, 0) # not inside, paint it black...
            else:
                ret_pix[x, y] = (255, 255, 255)
    return ret

def edge_detection(image):
    # NOT IMPLEMENTED
    # convert to OpenCV
    # canny
    # hough
    return True


def HSVPILImage(h, s, v, width, height):
    "make a PIL image from HSV value and width, height."
    ret = Image.new('RGB', (width, height))
    pix = ret.load()
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    r *= 255.0
    g *= 255.0
    b *= 255.0
    for x in range(width):
        for y in range(height):
            pix[x, y] = (int(round(r)), int(round(g)), int(round(b)))
    return ret

def HSVwxImage(h, s, v, width, height):
    "make a wx.Image from HSV value and width and height."
    pil = HSVPILImage(h, s, v, width, height)
    return pilTowxImage(pil)
