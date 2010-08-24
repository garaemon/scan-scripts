from wx import *
import os
from image import *
import copy

class HSVColorController(wx.BoxSizer):
    _slider_var = {}
    def __init__(self, parent):
        self._parent = parent
        wx.BoxSizer.__init__(self, wx.VERTICAL)
        #wx.Frame.__init__(self, parent, title=title, size=(200,100))
        # hsv bar
        hsv_bar = self.makeHSVSliders("parameters for color extraction")
        min_color_image =  wx.EmptyImage(30, 30)
        max_color_image =  wx.EmptyImage(30, 30)
        
        self._min_bitmap = wx.StaticBitmap(self._parent, -1,
                                           min_color_image.ConvertToBitmap(),
                                           (0, 0),
                                           (30, 30))
        self._max_bitmap = wx.StaticBitmap(self._parent, -1,
                                           max_color_image.ConvertToBitmap(),
                                           (0, 0),
                                           (30, 30))
        self._min_max_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self._min_max_sizer.Add(self._min_bitmap, 0, wx.EXPAND)
        self._min_max_sizer.Add(self._max_bitmap, 0, wx.EXPAND)
        # arrange
        self.Add(self._min_max_sizer, 0, wx.EXPAND)
        self.Add(hsv_bar, 0, wx.EXPAND)
        self.Fit(self._parent)
    def update_min_max_image(self):
        """
        update self.min_bitmap and self.max_bitmap from
        self._slider_var.
        """
        min_image = HSVwxImage(self._slider_var['h_min'] / 255.0 * 360,
                               self._slider_var['s_min'] / 255.0,
                               self._slider_var['v_min'] / 255.0,
                               30, 30)
        max_image = HSVwxImage(self._slider_var['h_max'] / 255.0 * 360,
                               self._slider_var['s_max'] / 255.0,
                               self._slider_var['v_max'] / 255.0,
                               30, 30)
        self._min_bitmap.SetBitmap(min_image.ConvertToBitmap())
        self._max_bitmap.SetBitmap(max_image.ConvertToBitmap())
        return True
    def makeHSVSliders(self, text):
        sizer = wx.BoxSizer(wx.VERTICAL)
        slider_text = wx.StaticText(self._parent, -1, text)
        slider_flag = wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS
        slider_h_max = self.makeBar("h_max", slider_flag, 255, 255)
        slider_h_min = self.makeBar("h_min", slider_flag, 255, 0)
        slider_s_max = self.makeBar("s_max", slider_flag,
                                       initial_value = 255.0)
        slider_s_min = self.makeBar("s_min", slider_flag,
                                       initial_value = 0.0)
        slider_v_max = self.makeBar("v_max", slider_flag,
                                       initial_value = 255.0)
        slider_v_min = self.makeBar("v_min", slider_flag,
                                       initial_value = 0.0)
        sizer.Add(slider_text, 0, wx.EXPAND)
        sizer.Add(slider_h_max, 0, wx.EXPAND)
        sizer.Add(slider_h_min, 0, wx.EXPAND)
        sizer.Add(slider_s_max, 0, wx.EXPAND)
        sizer.Add(slider_s_min, 0, wx.EXPAND)
        sizer.Add(slider_v_max, 0, wx.EXPAND)
        sizer.Add(slider_v_min, 0, wx.EXPAND)
        return sizer
    def makeBar(self, atext, slider_flag,
                _max = 255.0, initial_value = 0.0):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self._parent, -1, atext)
        self._slider_var[atext] = initial_value
        slider = wx.Slider(self._parent, -1, initial_value, 0, _max,
                           size = (300, -1),
                           style = slider_flag)
        sizer.Add(text, 0, wx.EXPAND)
        
        sizer.Add(slider, 0, wx.EXPAND)
        def local_func(evt):
            self._slider_var[atext] = slider.GetValue()
            self.update_min_max_image()
            return
        slider.Bind(wx.EVT_SLIDER, local_func)
        return sizer
    def TryColorExtract(self, fname):
        """
        this function take a path to a image file and do color extraction
        using current HSV parameters.
        """
        i = ImageContainer(fname)
        i.Binalize(self._slider_var['h_min'],
                   self._slider_var['h_max'],
                   self._slider_var['s_min'],
                   self._slider_var['s_max'],
                   self._slider_var['v_min'],
                   self._slider_var['v_max'])
        i.show()
        
        
class ScanController(wx.Frame):
    dirname = ''
    _files = []
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(200,100))
        # initialize
        # color indicator
        self._hsv = HSVColorController(self)
        self._test_color_extract_button = wx.Button(self,
                                                    -1,
                                                    "Test Color Extract")
        # buttons
        self.run_button = wx.Button(self, -1, "run")
        
        self.quit_button = wx.Button(self, -1, "Quit")
        
        # menu bar
        filemenu= wx.Menu()
        menuOpen = filemenu.Append(wx.ID_OPEN, "&Open",
                                   " Open a file to edit")
        menuAbout= filemenu.Append(wx.ID_ABOUT, "&About",
                                   " Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit",
                                   " Terminate the program")
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File")
        self.SetMenuBar(menuBar)

        # events
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_BUTTON, self.OnExit, self.quit_button)
        self.Bind(wx.EVT_BUTTON, self.testColorExtract,
                  self._test_color_extract_button)
        
        #sizer
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self._hsv, 1, wx.EXPAND)
        self.sizer.Add(self._test_color_extract_button, 1, wx.EXPAND)
        self.sizer.Add(self.run_button, 1, wx.EXPAND)
        self.sizer.Add(self.quit_button, 0, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)
        self.Show(True)
    # callbacks
    def testColorExtract(self, e):
        """
        this callback is bound to test_color_extract_button.
        """
        if len(self._files) >= 1:
            test_file = self._files[0]
            self._hsv.TryColorExtract(test_file)
    def OnAbout(self, e):
        # Create a message dialog box
        dlg = wx.MessageDialog(self,
                               """
                               A simple controller for scan your books.
                               """,
                               "About scan-controller", wx.OK)
        dlg.ShowModal() # Shows it
        dlg.Destroy() # finally destroy it when finished.
    def OnExit(self, e):
        self.Close(True)
    def OnOpen(self, e):
        """ Open a file"""
        dlg = wx.FileDialog(self, "Choose a file",
                            self.dirname, "", "*.*", wx.OPEN | wx.MULTIPLE)
        if dlg.ShowModal() == wx.ID_OK:
            self._files = dlg.GetPaths()
            #print self._files
            #i = ImageContainer(self._files[0])
            #i.show()
        dlg.Destroy()
