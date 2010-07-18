from wx import *

class ScanController(wx.Frame):
    dirname = ''
    _slider_var = {}
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(200,100))
        
        
        hsv_bar = self.make_hsv_sliders("parameters for color extraction")
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
        
        #sizer
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        #self.sizer.Add(self.slider1, 0, wx.EXPAND)
        self.sizer.Add(hsv_bar, 0, wx.EXPAND)
        self.sizer.Add(self.run_button, 1, wx.EXPAND)
        self.sizer.Add(self.quit_button, 0, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)
        self.Show(True)
    # hsv
    def make_hsv_sliders(self, text):
        sizer = wx.BoxSizer(wx.VERTICAL)
        slider_text = wx.StaticText(self, -1, text)
        slider_flag = wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS
        slider_h_max = self.make_a_bar("h_max", slider_flag)
        slider_h_min = self.make_a_bar("h_min", slider_flag)
        slider_s_max = self.make_a_bar("s_max", slider_flag)
        slider_s_min = self.make_a_bar("s_min", slider_flag)
        slider_v_max = self.make_a_bar("v_max", slider_flag)
        slider_v_min = self.make_a_bar("v_min", slider_flag)
        sizer.Add(slider_text, 0, wx.EXPAND)
        sizer.Add(slider_h_max, 0, wx.EXPAND)
        sizer.Add(slider_h_min, 0, wx.EXPAND)
        sizer.Add(slider_s_max, 0, wx.EXPAND)
        sizer.Add(slider_s_min, 0, wx.EXPAND)
        sizer.Add(slider_v_max, 0, wx.EXPAND)
        sizer.Add(slider_v_min, 0, wx.EXPAND)
        return sizer
    # callbacks
    def make_a_bar(self, atext, slider_flag):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self, -1, atext)
        slider = wx.Slider(self, -1, 50, 0, 255,
                           size = (300, -1),
                           style = slider_flag)
        sizer.Add(text, 0, wx.EXPAND)
        sizer.Add(slider, 0, wx.EXPAND)
        def local_func(evt):
            self._slider_var[atext] = slider.GetValue()
            print self._slider_var
        slider.Bind(wx.EVT_SLIDER, local_func)
        return sizer
    def OnAbout(self,e):
        # Create a message dialog box
        dlg = wx.MessageDialog(self,
                               """
                               A simple controller for scan your books.
                               """,
                               "About scan-controller", wx.OK)
        dlg.ShowModal() # Shows it
        dlg.Destroy() # finally destroy it when finished.
    def OnExit(self,e):
        self.Close(True)
    def OnOpen(self,e):
        """ Open a file"""
        dlg = wx.FileDialog(self, "Choose a file",
                            self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), 'r')
            self.control.SetValue(f.read())
            f.close()
        dlg.Destroy()
