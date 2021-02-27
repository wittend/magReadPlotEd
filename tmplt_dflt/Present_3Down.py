        # Subplot 1
        self.ax1 = self.fig.add_subplot(411)
        self.box = self.ax1.get_position()
        self.plt.subplots_adjust(left=self.box.x0, right=self.box.x1-0.08, top=self.box.y1, bottom=0.1, hspace=0.1)
        
        self.ax1.plot(self.Epoch, self.Bx, label='Bx', linewidth=0.5)
        self.title = station_code + ' HamSCI Mag '  + date + ' ' + t_start + ' - ' + t_stop
        self.ax1.set_title(self.title)
        
        self.ax1.set_xlim([self.ep_start, self.ep_stop])    #without this, the time range will not show up properly because there are missing data.
        self.ax1.set_ylabel('Bx (nT)')
        self.ax1.get_xaxis().set_ticklabels([])
        self.ax1.tick_params(axis='x', direction='out', top='on')
        self.ax1.tick_params(axis='y', direction='out', right='on')
        self.ax1.minorticks_on()
        self.ax1.tick_params(axis='x', which ='minor', direction='out', top='on')
        self.ax1.tick_params(axis='y', which ='minor', direction='out', right='on')
        self.ax1.set_ylim(47600, 47800)
        self.ax1.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
        
        # Subplot 2
        self.ax2 = self.fig.add_subplot(412)
        self.ax2.plot(self.Epoch, self.By, label='By', linewidth=0.5)

        self.ax2.set_xlim([self.ep_start, self.ep_stop])     #without this, the time range will not show up properly because there are missing data.       
self.ax2.set_ylabel('By (nT)')
self.ax2.get_xaxis().set_ticklabels([])
self.ax2.tick_params(axis='x', direction='out', top='on')
self.ax2.tick_params(axis='y', direction='out', right='on')
self.ax2.minorticks_on()
self.ax2.tick_params(axis='x', which ='minor', direction='out', top='on')
self.ax2.tick_params(axis='y', which ='minor', direction='out', right='on')
self.ax2.set_ylim(-100, 100)
self.ax2.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

# Subplot 3
self.ax3 = self.fig.add_subplot(413)
self.ax3.plot(self.Epoch, self.Bz, label='Bz', linewidth=0.5)

self.ax3.set_xlim([self.ep_start, self.ep_stop])     #without this, the time range will not show up properly because there are missing data.
self.ax3.set_ylabel('Bz (nT)')
self.ax3.get_xaxis().set_ticklabels([])
self.ax3.tick_params(axis='x', direction='out', top='on')
self.ax3.tick_params(axis='y', direction='out', right='on')
self.ax3.minorticks_on()
self.ax3.tick_params(axis='x', which ='minor', direction='out', top='on')
self.ax3.tick_params(axis='y', which ='minor', direction='out', right='on')
self.ax3.set_ylim(-15400, -15200)
self.ax3.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

# Subplot 4
self.ax4 = self.fig.add_subplot(414)
self.ax4.plot(self.Epoch, self.Bt, label='Bt', linewidth=0.5)
self.ax4.set_xlim([self.ep_start, self.ep_stop])     #without this, the time range will not show up properly because there are missing data.
self.ax4.set_ylabel('Bt (nT)')
self.ax4.get_xaxis().set_ticklabels([])
self.ax4.tick_params(axis='x', direction='out', top='on')
self.ax4.tick_params(axis='y', direction='out', right='on')
self.ax4.minorticks_on()
self.ax4.tick_params(axis='x', which ='minor', direction='out', top='on')
self.ax4.tick_params(axis='y', which ='minor', direction='out', right='on')
self.ax4.set_ylim(50000, 50200)
self.ax4.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

# X-axis
self.ax4.set_xlabel('UT (hh:mm)')
self.date_fmt = '%H:%M'  #'%d-%m-%y %H:%M:%S'  #Choose your xtick format string
self.date_formatter = mdate.DateFormatter(self.date_fmt)
self.ax4.xaxis.set_major_formatter(self.date_formatter)

self.toolbar.update()       # Not sure why this is needed - ADS
