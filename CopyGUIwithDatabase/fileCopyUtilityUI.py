import wx
import time
import fileCopyUtility
import fileCopyUtilityDBConnection as db
import os

class SelectDirectories(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(SelectDirectories, self).__init__(None)

        self.setUpGUI()

    def setUpGUI(self):
        self.setUpMenuBar()
        self.statusBar = self.CreateStatusBar()

        self.SetTitle('File Copy Utility')
        self.SetSize((575, 250))

        self.setUpPanel()

    def setUpMenuBar(self):
        self.menuBar = wx.MenuBar()
        self.addFileMenu()
        self.addAboutMenu()

        self.SetMenuBar(self.menuBar)

    def addFileMenu(self):
        fileButton = wx.Menu()
        exitItem = fileButton.Append(wx.ID_EXIT, 'Quit', 'Exit the program')
        self.menuBar.Append(fileButton, 'File')
        self.Bind(wx.EVT_MENU, self.Quit, exitItem)

    def addAboutMenu(self):
        aboutButton = wx.Menu()
        infoItem = aboutButton.Append(wx.ID_ANY, 'Info', 'Display info about the program')
        self.menuBar.Append(aboutButton, 'About')
        self.Bind(wx.EVT_MENU, self.About, infoItem)
        
    def Quit(self, event):
        self.Close()

    def About(self, event):
        info = 'This utility will search for text files in the "copy from" directory'\
               ' which have been created or modified within the past 24 hours, and then'\
               ' copy them into the "copy to" folder.  The user picks the "copy from" and'\
               ' "copy to" folders, then initiates the file transfer with the "Transfer'\
               ' Files" button.'
        
        message_box = wx.MessageDialog(self, message=info)
        message_box.ShowModal()
        message_box.Destroy()

    def setUpPanel(self):
        self.panel = fileCopyUtilityPanel(self)


class fileCopyUtilityPanel(wx.Panel):
    """This panel will hold inputs to get a 'Copy From' and a 'Copy To' directory, and a button
    which initiates a copy utility"""

    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.starting_directory = os.getcwd()
        self.layoutButtonsAndBoxes()
        self.bindButtons()
        self.updateLastRunDate('event')

    def createInputTextBoxes(self):
        self.copy_from_input = wx.TextCtrl(self)
        self.copy_to_input = wx.TextCtrl(self)

    def createStaticTextBoxes(self):
        self.copy_from_label = wx.StaticText(self, label='Copy from:')
        self.copy_to_label = wx.StaticText(self, label='Copy to:')
        self.last_run_label = wx.StaticText(self, label='Last copy date/time:')
        self.last_run_result = wx.StaticText(self, label='')

    def createButtons(self):
        self.copy_from_button = wx.Button(self, wx.ID_ANY, 'Browse')
        self.copy_to_button = wx.Button(self, wx.ID_ANY, 'Browse')
        self.last_run_button = wx.Button(self, wx.ID_ANY, 'Update last run date')
        self.initiate_button = wx.Button(self, wx.ID_ANY, 'Initiate Search and Copy')        

    def createSizers(self):
        self.from_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.to_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.last_run_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.initiate_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.vertical_sizer = wx.BoxSizer(wx.VERTICAL)

    def putItemsInHorizontalSizers(self):
        self.from_sizer.Add(self.copy_from_label, proportion=1, flag=wx.ALL, border=5)
        self.from_sizer.Add(self.copy_from_input, proportion=5, flag=wx.ALL|wx.EXPAND, border=5)
        self.from_sizer.Add(self.copy_from_button, proportion=0, flag=wx.ALL, border=5)

        self.to_sizer.Add(self.copy_to_label, proportion=1, flag=wx.ALL, border=5)
        self.to_sizer.Add(self.copy_to_input, proportion=5, flag=wx.ALL|wx.EXPAND, border=5)
        self.to_sizer.Add(self.copy_to_button, proportion=0, flag=wx.ALL, border=5)

        self.last_run_sizer.Add(self.last_run_label, proportion = 1, flag=wx.ALL, border=5)
        self.last_run_sizer.Add(self.last_run_result, proportion=5, flag=wx.ALL|wx.EXPAND, border=5)
        self.last_run_sizer.Add(self.last_run_button, proportion=0, flag=wx.ALL, border=5)

        self.initiate_sizer.Add(self.initiate_button, proportion=0, flag=wx.ALIGN_CENTER|wx.EXPAND)

    def putHorizontalSizersInVerticalSizer(self):
        self.vertical_sizer.Add(self.from_sizer, proportion=0, flag=wx.ALL|wx.EXPAND, border=5)
        self.vertical_sizer.Add(self.to_sizer, proportion=0, flag=wx.ALL|wx.EXPAND, border=5)
        self.vertical_sizer.Add(self.last_run_sizer, proportion=0, flag=wx.ALL|wx.EXPAND, border=5)
        self.vertical_sizer.Add(self.initiate_sizer, proportion=0, flag=wx.CENTER|wx.ALL, border=5)

        self.SetSizer(self.vertical_sizer)
        self.vertical_sizer.Fit(self)

    def layoutButtonsAndBoxes(self):
        self.createInputTextBoxes()
        self.createStaticTextBoxes()
        self.createButtons()
        self.createSizers()

        self.putItemsInHorizontalSizers()
        self.putHorizontalSizersInVerticalSizer()

    def bindButtons(self):
        self.Bind(wx.EVT_BUTTON, self.setCopyFromDirectory, self.copy_from_button)
        self.Bind(wx.EVT_BUTTON, self.setCopyToDirectory, self.copy_to_button)
        self.Bind(wx.EVT_BUTTON, self.updateLastRunDate, self.last_run_button)
        self.Bind(wx.EVT_BUTTON, self.initiateCopy, self.initiate_button)

    def setCopyToDirectory(self, event):
        self.setTextToBrowsedToDirectory(self.copy_to_input)

    def setCopyFromDirectory(self, event):
        self.setTextToBrowsedToDirectory(self.copy_from_input)
    
    def setTextToBrowsedToDirectory(self, field_to_update):
        prompt = 'Please select the desired directory:'
        choose_directory = wx.DirDialog(self, prompt)
        if choose_directory.ShowModal() == wx.ID_OK:
            directory = choose_directory.GetPath()
            field_to_update.SetLabel(directory)
        choose_directory.Destroy()
        os.chdir(self.starting_directory)

    def updateLastRunDate(self, event):
        self.last_run_time_stamp = self.getLastRunTimeStamp()
        if self.last_run_time_stamp is None:
            print('the is None branch:', self.last_run_time_stamp)
            last_run_date = 'No previous runs'
        else:
            last_run_date = time.ctime(self.last_run_time_stamp)
        self.last_run_result.SetLabel(last_run_date)

    def getLastRunTimeStamp(self):
        database = db.copyUtilityDB()
        last_run_date = database.retrieveLastCopyDate()
        database.closeDBConnection()
        print(last_run_date)
        print(type(last_run_date))
        return last_run_date

    def insertTimeStampIntoDatabase(self):
        now = time.time()
        database = db.copyUtilityDB()
        database.insertNewCopyDate(now)
        database.closeDBConnection()
        
    def initiateCopy(self, event):
        copy_from_directory = self.copy_from_input.GetValue()
        copy_to_directory = self.copy_to_input.GetValue()
        print(self.last_run_result.GetLabel())
        if self.last_run_result.GetLabel() in ('', 'No previous runs'):
            self.last_run_time_stamp = 24*3600
        self.insertTimeStampIntoDatabase()
        fileCopyUtility.reviewAndCopy(copy_from_directory, copy_to_directory, self.last_run_time_stamp)


        
if __name__ == '__main__':
    app = wx.App()
    frame = SelectDirectories()
    frame.Show()
    app.MainLoop()
        
