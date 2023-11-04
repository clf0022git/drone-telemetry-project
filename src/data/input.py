# Christopher Fechter
# Planned functionality of handling functions related to the data input
import tkinter as tk
import pandas as pd


class DataManager:
    def __init__(self):
        self.data_file = None
        self.metric_indicator = 0  # default to 0 (meters)

    def parse(self, csv_path):
        """Handles the code for parsing the file"""
        self.data_file = pd.read_csv(csv_path,
                                     dtype={'CUSTOM.isPhoto': 'object',
                                            'CUSTOM.hSpeed [m/s]': 'float64',
                                            'CUSTOM.hSpeed.running_max [m/s]': 'float64',
                                            'OSD.latitude': 'float64',
                                            })
        #print(self.data_file)

    def load_fields(self, fieldnames_list) -> list:
        fieldnames = []

        for col in self.data_file.columns:
            fieldnames.append(col)
            #print(col)

        for field in fieldnames:
            fieldnames_list.insert(tk.END, field)

        i = 0  # define iterator i for debugging
        for dt in self.data_file.dtypes:
            i = i + 1
            #print(i)
            #print(dt)

        return fieldnames_list

    def identify_gauges(self, selected_field) -> list:
        """Use an if else tree to determine the kind of gauges for a specific type of data"""
        gauge_names = []
        #print(selected_field)
        #print("test")
        #print(self.data_file['CUSTOM.updateTime'].dtype)

        # probably going to need to be changed to just take in 1 variable instead of indexing a list
        if selected_field[0] == "CUSTOM.updateTime":
            gauge_names.append("clock")
            gauge_names.append("stopwatch")
            gauge_names.append("running_time")
        elif self.data_file[selected_field[0]].dtype == "bool":
            gauge_names.append("x_plot")
            gauge_names.append("y_plot")
            gauge_names.append("on_off_light")
        elif self.data_file[selected_field[0]].dtype == "int64" or self.data_file[selected_field[0]].dtype == "float64":
            gauge_names.append("circle_90")
            gauge_names.append("circle_180")
            gauge_names.append("circle_270")
            gauge_names.append("circle_360")
            gauge_names.append("num_or_char")
        elif self.data_file[selected_field[0]].dtype == "object":
            gauge_names.append("text_display")
        else:
            gauge_names.append("text_display")

        #for gauge in gauge_names:
            #print(gauge)

        return gauge_names

    def swap_metric(self):
        """Check what metric is already in use and swap to the other one"""
        if self.metric_indicator == 0:  # case for the units being in meters
            for element in self.data_file.columns:
                index = element.find('[m')
                if index != -1:
                    i = 0
                    while i < len(self.data_file[element]):
                        if self.data_file.at[i, element] != '':
                            data = self.data_file.at[i, element]
                            self.data_file.at[i, element] = data * 39.76
                        i += 1
            # printing a field's data
            print('\nFirst 6 rows in CUSTOM.distance [m]:\n')
            for data in self.data_file['CUSTOM.distance [m]'][:6]:
                print("%10s" % data, end=" "),
                print('\n')
            self.metric_indicator = 1
        else:
            for element in self.data_file.columns:
                index = element.find('[m')
                if index != -1:
                    i = 0
                    while i < len(self.data_file[element]):
                        if self.data_file.at[i, element] != '':
                            data = self.data_file.at[i, element]
                            self.data_file.at[i, element] = data / 39.76
                        i += 1
            # printing a field's data
            print('\nFirst 6 rows in CUSTOM.distance [m]:\n')
            for data in self.data_file['CUSTOM.distance [m]'][:6]:
                print("%10s" % data, end=" "),
                print('\n')
            self.metric_indicator = 0