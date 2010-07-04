from wx import *

class ColorController(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(-1,300))
        slider_flag = wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS
        self.slider1 = wx.Slider(self, -1, 50, 0, 255,
                                 size = (300, -1),
                                 style = slider_flag)
        self.slider2 = wx.Slider(self, -1, 50, 0, 255,
                                 size = (300, -1),
                                 style = slider_flag)
        self.slider3 = wx.Slider(self, -1, 50, 0, 255,
                                 size = (300, -1),
                                 style = slider_flag)
        self.slider4 = wx.Slider(self, -1, 50, 0, 255,
                                 size = (300, -1),
                                 style = slider_flag)
        self.slider5 = wx.Slider(self, -1, 50, 0, 255,
                                 size = (300, -1),
                                 style = slider_flag)
        self.slider6 = wx.Slider(self, -1, 50, 0, 255,
                                 size = (300, -1),
                                 style = slider_flag)
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.slider1, 0, wx.EXPAND)
        self.sizer.Add(self.slider2, 0, wx.EXPAND)
        self.sizer.Add(self.slider3, 0, wx.EXPAND)
        self.sizer.Add(self.slider4, 0, wx.EXPAND)
        self.sizer.Add(self.slider5, 0, wx.EXPAND)
        self.sizer.Add(self.slider6, 0, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)

class ScanController(wx.Frame):
    dirname = ''
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(200,100))

        # buttons
        self.color_control_button = wx.Button(self, -1, "color control")
        self.color_controller = ColorController(self, "color parameter")
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
        self.Bind(wx.EVT_BUTTON, self.color_control_cb,
                  self.color_control_button)
        
        #sizer
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.color_control_button, 2, wx.EXPAND)
        self.sizer.Add(self.run_button, 1, wx.EXPAND)
        self.sizer.Add(self.quit_button, 0, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)
        self.Show(True)
    def color_control_cb(self, e):
        self.color_controller.Show(True)
        
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
