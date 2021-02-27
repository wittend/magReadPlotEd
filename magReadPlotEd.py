#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#============================================================================================
# RM3100_MagReadPlot.py
# 
# This routine reads ascii file data from HamSCI DASI magnetometers (RM3100) and plot graphs. 
# 
# Hyomin Kim, New Jersey Institute of Technology, hmkim@njit.edu 
# 02/01/2021
#============================================================================================
import wx
# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
import os
import sys
from pathlib import Path
from STCEditorClass import *
from plotPanel import *
# end wxGlade

# ============================================================================
data_dir        = '/PSWS/Srawdata'
plot_dir        = '/PSWS/Splot'
tmplt_user_dir  = './tmplt_user'
tmplt_dflt_dir  = './tmplt_dflt'
# ============================================================================

class TopFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: TopFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((1000, 750))
        self.SetTitle("magReadPlotEd")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("/home/dave/Pictures/img/compass-simple.svg", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)

        # Menu Bar
        self.topFrameMenubar = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "Open", "Open a Logfile")
        self.Bind(wx.EVT_MENU, self.onFileOpen, item)
        wxglade_tmp_menu.AppendSeparator()
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "Exit", "Exit this program")
        self.Bind(wx.EVT_MENU, self.onFileExit, item)
        self.topFrameMenubar.Append(wxglade_tmp_menu, "File")
        wxglade_tmp_menu = wx.Menu()
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "About", "Information about the program")
        self.Bind(wx.EVT_MENU, self.onHelpAbout, item)
        self.topFrameMenubar.Append(wxglade_tmp_menu, "Help")
        self.SetMenuBar(self.topFrameMenubar)
        # Menu Bar end

        # Tool Bar
        self.topFrameToolbar = wx.ToolBar(self, -1)
        tool = self.topFrameToolbar.AddTool(wx.ID_ANY, "Load", wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, (24, 24)), wx.NullBitmap, wx.ITEM_NORMAL, "Select and load log dataset", "Select and load log dataset")
        self.Bind(wx.EVT_TOOL, self.onLoadData, id=tool.GetId())
        tool = self.topFrameToolbar.AddTool(wx.ID_ANY, "Plot", wx.ArtProvider.GetBitmap(wx.ART_EXECUTABLE_FILE, wx.ART_TOOLBAR, (24, 24)), wx.NullBitmap, wx.ITEM_NORMAL, "Plot data as graph", "Plot data as graph")
        self.Bind(wx.EVT_TOOL, self.onPlotData, id=tool.GetId())
        tool = self.topFrameToolbar.AddTool(wx.ID_ANY, "Print", wx.ArtProvider.GetBitmap(wx.ART_PRINT, wx.ART_TOOLBAR, (24, 24)), wx.NullBitmap, wx.ITEM_NORMAL, "Print plotted data", "Print plotted data")
        self.Bind(wx.EVT_TOOL, self.onPrintPlot, id=tool.GetId())
        tool = self.topFrameToolbar.AddTool(wx.ID_ANY, "Save", wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, (24, 24)), wx.NullBitmap, wx.ITEM_NORMAL, "Save plot as bitmap file", "Save plot as bitmap file")
        self.Bind(wx.EVT_TOOL, self.onSavePlot, id=tool.GetId())
        tool = self.topFrameToolbar.AddTool(wx.ID_ANY, "Clear", wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, (24, 24)), wx.NullBitmap, wx.ITEM_NORMAL, "Clear plot and processed data", "Clear plot and processed data")
        self.Bind(wx.EVT_TOOL, self.onPlotClear, id=tool.GetId())
        self.topFrameToolbar.AddSeparator()
        tool = self.topFrameToolbar.AddTool(wx.ID_ANY, "Exit", wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_TOOLBAR, (24, 24)), wx.NullBitmap, wx.ITEM_NORMAL, "Exit this program", "Exit this program")
        self.Bind(wx.EVT_TOOL, self.onExit, id=tool.GetId())
        self.SetToolBar(self.topFrameToolbar)
        self.topFrameToolbar.Realize()
        # Tool Bar end

        self.topNotebook = wx.Notebook(self, wx.ID_ANY, style=wx.NB_BOTTOM)

        self.topNotebookPanel1 = wx.Panel(self.topNotebook, wx.ID_ANY)
        self.topNotebook.AddPage(self.topNotebookPanel1, "Plot")

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        self.topSplitterWindow = wx.SplitterWindow(self.topNotebookPanel1, wx.ID_ANY)
        self.topSplitterWindow.SetMinimumPaneSize(20)
        sizer_1.Add(self.topSplitterWindow, 1, wx.EXPAND, 0)

        self.topLeftSplitterPane = wx.Panel(self.topSplitterWindow, wx.ID_ANY)

        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)

        self.dirTreeCtrl = wx.GenericDirCtrl(self.topLeftSplitterPane, wx.ID_ANY)
        sizer_3.Add(self.dirTreeCtrl, 1, wx.EXPAND, 0)

        self.topRightSplitterPane = wx.Panel(self.topSplitterWindow, wx.ID_ANY)

        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)

        self.panel_1 = wx.Panel(self.topRightSplitterPane, wx.ID_ANY)
        sizer_4.Add(self.panel_1, 1, wx.EXPAND, 0)

        sizer_5 = wx.BoxSizer(wx.VERTICAL)

        self.plotPanel = PlotPanel(self.panel_1)
        sizer_5.Add(self.plotPanel, 1, wx.EXPAND, 0)

        self.topNotebook_pane_1 = wx.Panel(self.topNotebook, wx.ID_ANY)
        self.topNotebook.AddPage(self.topNotebook_pane_1, "Parser")

        grid_sizer_1 = wx.FlexGridSizer(6, 1, 1, 0)

        self.preParseTools = wx.Panel(self.topNotebook_pane_1, wx.ID_ANY)
        grid_sizer_1.Add(self.preParseTools, 1, wx.EXPAND, 0)

        sizer_7 = wx.StaticBoxSizer(wx.StaticBox(self.preParseTools, wx.ID_ANY, "PreParser"), wx.HORIZONTAL)

        self.combo_box_1 = wx.ComboBox(self.preParseTools, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN)
        sizer_7.Add(self.combo_box_1, 0, wx.ALL, 2)

        self.bitmap_button_2 = wx.BitmapButton(self.preParseTools, wx.ID_ANY, wx.NullBitmap)
        self.bitmap_button_2.SetSize(self.bitmap_button_2.GetBestSize())
        sizer_7.Add(self.bitmap_button_2, 0, wx.ALL, 2)

        self.bitmap_button_1 = wx.BitmapButton(self.preParseTools, wx.ID_ANY, wx.NullBitmap)
        self.bitmap_button_1.SetSize(self.bitmap_button_1.GetBestSize())
        sizer_7.Add(self.bitmap_button_1, 0, wx.ALL, 2)

        self.button_1 = wx.ToggleButton(self.preParseTools, wx.ID_ANY, "button_1")
        sizer_7.Add(self.button_1, 0, wx.ALL, 2)

        self.button_2 = wx.Button(self.preParseTools, wx.ID_ANY, "button_2")
        sizer_7.Add(self.button_2, 0, wx.ALL, 2)

        self.button_3 = wx.Button(self.preParseTools, wx.ID_ANY, "button_3")
        sizer_7.Add(self.button_3, 0, wx.ALL, 2)

        self.preParseEditor = STCEditor(self.topNotebook_pane_1, wx.ID_ANY)
        grid_sizer_1.Add(self.preParseEditor, 1, wx.EXPAND, 0)

        self.plotLayoutTools = wx.Panel(self.topNotebook_pane_1, wx.ID_ANY)
        grid_sizer_1.Add(self.plotLayoutTools, 1, wx.EXPAND, 0)

        sizer_8 = wx.StaticBoxSizer(wx.StaticBox(self.plotLayoutTools, wx.ID_ANY, "Plot Layout"), wx.HORIZONTAL)

        self.combo_box_2 = wx.ComboBox(self.plotLayoutTools, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN)
        sizer_8.Add(self.combo_box_2, 0, wx.ALL, 2)

        self.bitmap_button_3 = wx.BitmapButton(self.plotLayoutTools, wx.ID_ANY, wx.NullBitmap)
        self.bitmap_button_3.SetSize(self.bitmap_button_3.GetBestSize())
        sizer_8.Add(self.bitmap_button_3, 0, wx.ALL, 2)

        self.bitmap_button_4 = wx.BitmapButton(self.plotLayoutTools, wx.ID_ANY, wx.NullBitmap)
        self.bitmap_button_4.SetSize(self.bitmap_button_4.GetBestSize())
        sizer_8.Add(self.bitmap_button_4, 0, wx.ALL, 2)

        self.button_4 = wx.ToggleButton(self.plotLayoutTools, wx.ID_ANY, "button_4")
        sizer_8.Add(self.button_4, 0, wx.ALL, 2)

        self.button_5 = wx.Button(self.plotLayoutTools, wx.ID_ANY, "button_5")
        sizer_8.Add(self.button_5, 0, wx.ALL, 2)

        self.button_6 = wx.Button(self.plotLayoutTools, wx.ID_ANY, "button_6")
        sizer_8.Add(self.button_6, 0, wx.ALL, 2)

        self.plotLayoutEditor = STCEditor(self.topNotebook_pane_1, wx.ID_ANY)
        grid_sizer_1.Add(self.plotLayoutEditor, 1, wx.EXPAND, 0)

        self.dataProcessTools = wx.Panel(self.topNotebook_pane_1, wx.ID_ANY)
        grid_sizer_1.Add(self.dataProcessTools, 1, wx.EXPAND, 0)

        sizer_9 = wx.StaticBoxSizer(wx.StaticBox(self.dataProcessTools, wx.ID_ANY, "Data Process"), wx.HORIZONTAL)

        self.combo_box_3 = wx.ComboBox(self.dataProcessTools, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN)
        sizer_9.Add(self.combo_box_3, 0, wx.ALL, 2)

        self.bitmap_button_5 = wx.BitmapButton(self.dataProcessTools, wx.ID_ANY, wx.NullBitmap)
        self.bitmap_button_5.SetSize(self.bitmap_button_5.GetBestSize())
        sizer_9.Add(self.bitmap_button_5, 0, wx.ALL, 2)

        self.bitmap_button_6 = wx.BitmapButton(self.dataProcessTools, wx.ID_ANY, wx.NullBitmap)
        self.bitmap_button_6.SetSize(self.bitmap_button_6.GetBestSize())
        sizer_9.Add(self.bitmap_button_6, 0, wx.ALL, 2)

        self.button_7 = wx.ToggleButton(self.dataProcessTools, wx.ID_ANY, "button_7")
        sizer_9.Add(self.button_7, 0, wx.ALL, 2)

        self.button_8 = wx.Button(self.dataProcessTools, wx.ID_ANY, "button_8")
        sizer_9.Add(self.button_8, 0, wx.ALL, 2)

        self.button_9 = wx.Button(self.dataProcessTools, wx.ID_ANY, "button_9")
        sizer_9.Add(self.button_9, 0, wx.ALL, 2)

        self.dataProcessEditor = STCEditor(self.topNotebook_pane_1, wx.ID_ANY)
        grid_sizer_1.Add(self.dataProcessEditor, 1, wx.EXPAND, 0)

        self.topNotebookPanel2 = wx.Panel(self.topNotebook, wx.ID_ANY)
        self.topNotebook.AddPage(self.topNotebookPanel2, "Edit")

        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)

        self.codeEditor = STCEditor(self.topNotebookPanel2, wx.ID_ANY)
        sizer_2.Add(self.codeEditor, 1, wx.EXPAND, 0)

        self.topNotebookPanel3 = wx.Panel(self.topNotebook, wx.ID_ANY)
        self.topNotebook.AddPage(self.topNotebookPanel3, "Data")

        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)

        self.dataEditor = STCEditor(self.topNotebookPanel3, wx.ID_ANY)
        sizer_6.Add(self.dataEditor, 1, wx.EXPAND, 0)

        self.topNotebookPanel3.SetSizer(sizer_6)

        self.topNotebookPanel2.SetSizer(sizer_2)

        self.dataProcessTools.SetSizer(sizer_9)

        self.plotLayoutTools.SetSizer(sizer_8)

        self.preParseTools.SetSizer(sizer_7)

        grid_sizer_1.AddGrowableRow(1)
        grid_sizer_1.AddGrowableRow(3)
        grid_sizer_1.AddGrowableRow(5)
        grid_sizer_1.AddGrowableCol(0)
        self.topNotebook_pane_1.SetSizer(grid_sizer_1)

        self.panel_1.SetSizer(sizer_5)

        self.topRightSplitterPane.SetSizer(sizer_4)

        self.topLeftSplitterPane.SetSizer(sizer_3)

        self.topSplitterWindow.SplitVertically(self.topLeftSplitterPane, self.topRightSplitterPane)

        self.topNotebookPanel1.SetSizer(sizer_1)

        self.Layout()

        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnNBChanged, self.topNotebook)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnNBChanging, self.topNotebook)
        self.Bind(wx.EVT_CLOSE, self.OnClose, self)
        # end wxGlade

        fd = open(tmplt_dflt_dir + '/Layout_3Down.py')
        self.preParseEditor.SetText(fd.read())
        fd.close()
        fd = open(tmplt_dflt_dir + '/Parse_3Down.py')
        self.plotLayoutEditor.SetText(fd.read())
        fd.close()
        fd = open(tmplt_dflt_dir + '/Present_3Down.py')
        self.dataProcessEditor.SetText(fd.read())
        fd.close()
        
        # self.preParseEditor
        # self.plotLayoutEditor
        # self.dataProcessEditor
        self.homedir = os.environ['HOME'] + data_dir
        tree = self.dirTreeCtrl.GetTreeCtrl()
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelect, id=tree.GetId())       
        self.dirTreeCtrl.SetPath(self.homedir)


    def onFileOpen(self, event):  # wxGlade: TopFrame.<event_handler>
        print("Event handler 'onFileOpen' not implemented!")
        event.Skip()

    def onFileExit(self, event):  # wxGlade: TopFrame.<event_handler>
        print("Event handler 'onFileExit' not implemented!")
        event.Skip()

    def onHelpAbout(self, event):  # wxGlade: TopFrame.<event_handler>
        print("Event handler 'onHelpAbout' not implemented!")
        event.Skip()

    def onLoadData(self, event):  # wxGlade: TopFrame.<event_handler>
        print("Event handler 'onLoadData' not implemented!")
        event.Skip()

    def onPlotData(self, event):  # wxGlade: TopFrame.<event_handler>
        print("Event handler 'onPlotData' not implemented!")
        event.Skip()

    def onPrintPlot(self, event):  # wxGlade: TopFrame.<event_handler>
        print("Event handler 'onPrintPlot' not implemented!")
        event.Skip()

    def onSavePlot(self, event):  # wxGlade: TopFrame.<event_handler>
        print("Event handler 'onSavePlot' not implemented!")
        event.Skip()

    def onPlotClear(self, event):  # wxGlade: TopFrame.<event_handler>
        print("Event handler 'onPlotClear' not implemented!")
        event.Skip()

    def onExit(self, event):  # wxGlade: TopFrame.<event_handler>
        print("Event handler 'onExit' not implemented!")
        event.Skip()

    def OnClose(self, event):  # wxGlade: TopFrame.<event_handler>
        #print("Event handler 'OnClose' not implemented!")
        event.Skip()

    def OnNBChanged(self, event):  # wxGlade: TopFrame.<event_handler>
        #print("Event handler 'OnNBChanged' not implemented!")
        event.Skip()

    def OnNBChanging(self, event):  # wxGlade: TopFrame.<event_handler>
        #print("Event handler 'OnNBChanging' not implemented!")
        event.Skip()

    def OnSelect(self, event):      # wxGlade: TopFrame.<event_handler>
         """
             OnSelect()
         """
         filePath = self.dirTreeCtrl.GetPath()
         if(os.path.isdir(filePath) != True):
             print('self.dirTreeCtrl.GetPath(): ' + self.dirTreeCtrl.GetPath())
             fd = open(self.dirTreeCtrl.GetPath())
             self.dataEditor.SetText(fd.read())
             fd.close()
             self.plotPanel.resetPlot()
             self.plotPanel.readData(self.dirTreeCtrl.GetPath())
             self.plotPanel.Layout()
             self.plotPanel.SendSizeEventToParent()
        
# end of class TopFrame


class TheApp(wx.App):
    def OnInit(self):
        self.topFrame = TopFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.topFrame)
        self.topFrame.Show()
        return True

# end of class TheApp

if __name__ == "__main__":
    magReadPlotEd = TheApp(0)
    magReadPlotEd.MainLoop()
