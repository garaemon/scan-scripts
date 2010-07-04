from wx import *

class ScanController(wx.Frame):
    def __init__(self, parent, ID, title):
        wx.Frame.__init__(self, parent, ID, title,
                         wxDefaultPosition, wxSize(200, 150))
        self.CreateStatusBar()
        self.SetStatusText("This is the statusbar")

        menu = wxMenu()
        menu.Append(ID_ABOUT, "&About",
                    "More information about this program")
        menu.AppendSeparator()
        menu.Append(ID_EXIT, "E&xit", "Terminate the program")

        menuBar = wxMenuBar()
        menuBar.Append(menu, "&File");

        self.SetMenuBar(menuBar)



        

