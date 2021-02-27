self.fgm_data       = []
self.year           = date[0:4]
self.month          = date[5:7]
self.day            = date[8:10]
self.hour_start     = t_start[0:2]
self.minute_start   = t_start[3:5]
self.second_start   = t_start[6:8]
self.hour_stop      = t_stop[0:2]
self.minute_stop    = t_stop[3:5]
self.second_stop    = t_stop[6:8]
self.date_time      = datetime.datetime(int(self.year), int(self.month), int(self.day), int(self.hour_start), int(self.minute_start), int(self.second_start))
self.doy            = self.date_time.timetuple().tm_yday

self.plt = plot
self.fig = self.plt.figure(1, figsize=(5, 4))       # Plot window size
self.canvas = FigureCanvas(self, -1, self.fig)
self.toolbar = NavigationToolbar(self.canvas)       # matplotlib toolbar
self.toolbar.Realize()

# Now put all into a sizer
# sizer = wx.BoxSizer(wx.VERTICAL)
self.sizer = wx.BoxSizer(wx.VERTICAL)
# This way of adding to sizer allows resizing
# sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
# Best to allow the toolbar to resize!
# sizer.Add(self.toolbar, 0, wx.GROW)
self.sizer.Add(self.toolbar, 0, wx.GROW)
self.SetSizer(self.sizer)
self.Fit()
