from opencv import cv
from opencv import highgui
import Image                    # PIL
import os
import wx

def pilToImage(pil):
    wximage = wx.EmptyImage(pil.size[0], pil.size[1])
    wximage.SetData(pil.convert('RGB').tostring())
    return wximage

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
