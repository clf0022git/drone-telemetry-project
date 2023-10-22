# Christopher Fechter
# Planned functionality of handling functions related to the data input
import tkinter as tk
import pandas as pd


class DataManager:
    def __init__(self):
        self.data_file = None

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
