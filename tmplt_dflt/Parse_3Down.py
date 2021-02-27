self.f = open(fileName)
self.header_index = 0
self.csv_f = csv.reader(self.f, delimiter=",")
# self.fgm_data = []
for row in self.csv_f:
    self.fgm_data.append(row)
self.date_time_array = np.array([self.year+'-'+self.month+'-'+self.day + ' ' + self.fgm_data[i][0][19:27] for i in range(self.header_index, len(self.fgm_data))])
self.pattern = '%Y-%m-%d %H:%M:%S'
self.epoch_temp = np.array([datetime.datetime.strptime(x, self.pattern) for x in self.date_time_array])
self.Bx_temp = np.array([float(self.fgm_data[i][3][4:11]) for i in range(self.header_index, len(self.fgm_data))])
self.By_temp = np.array([float(self.fgm_data[i][4][4:11]) for i in range(self.header_index, len(self.fgm_data))])
self.Bz_temp = np.array([float(self.fgm_data[i][5][4:11]) for i in range(self.header_index, len(self.fgm_data))])
#Array slicing/indexing
self.start = datetime.datetime(int(self.year), int(self.month), int(self.day), int(self.hour_start), int(self.minute_start), int(self.second_start))
self.stop = datetime.datetime(int(self.year), int(self.month), int(self.day), int(self.hour_stop), int(self.minute_stop), int(self.second_stop))
self.start_index = bisect.bisect_left(self.epoch_temp, self.start)
self.stop_index = bisect.bisect_left(self.epoch_temp, self.stop)
self.Epoch = self.epoch_temp[self.start_index : self.stop_index]
self.Bx = 1000*self.Bx_temp[self.start_index : self.stop_index]  #*1000: uT to nT
self.By = 1000*self.By_temp[self.start_index : self.stop_index]
self.Bz = 1000*self.Bz_temp[self.start_index : self.stop_index]
       
# Specify date_str/time range for x-axis range
self.ep_start = datetime.datetime(int(self.year), int(self.month), int(self.day), int(self.hour_start), int(self.minute_start), int(self.second_start))
self.ep_stop = datetime.datetime(int(self.year), int(self.month), int(self.day), int(self.hour_stop), int(self.minute_stop), int(self.second_stop))

#This is for Pi magnetometer (PNI)
self.Bx[np.where(self.Bx[:] >= 999999.0)] = np.nan
self.By[np.where(self.By[:] >= 999999.0)] = np.nan
self.Bz[np.where(self.Bz[:] >= 999999.0)] = np.nan

#Moving average
self.N = 10 #WindowWidth in sec
self.Bx = np.array(moving_average(self.Bx, self.N))
self.By = np.array(moving_average(self.By, self.N))
self.Bz = np.array(moving_average(self.Bz, self.N))
self.Epoch = np.array(self.Epoch[0:len(self.Bx)])  #to match the new array size with the moving averaged array. 
self.Bt = np.sqrt(self.Bx**2 + self.By**2 + self.Bz**2)
