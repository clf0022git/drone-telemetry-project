# Christopher Fechter
# Planned functionality of handling functions related to the data input
import tkinter as tk
from tkinter import ttk
import pandas as pd


class DataManager:
    def __init__(self):
        self.data_file = None
        self.current_selected_field = None
        self.field_selected = False
        self.current_selected_field_gauges = []
        self.combo = None
        self.datatype_label = None
        self.user_selected_gauges_list = []
        self.user_selected_gauges_label_list = []
        self.label = ''
        self.timestamp_value = 1
        self.metric_indicator = 0  # default to 0 (meters)


    def parse(self, csv_path):
        """Handles the code for parsing the file"""
        self.data_file = pd.read_csv(csv_path, low_memory=False)
        self.data_file = self.data_file.infer_objects()
        # Sets the first column to a type of pandas datetime
        self.data_file["CUSTOM.updateTime"] = pd.to_datetime(format='mixed', arg=self.data_file["CUSTOM.updateTime"])
        # print(self.data_file["CUSTOM.updateTime"])
        self.data_file["CUSTOM.updateTime"] = self.data_file["CUSTOM.updateTime"].round('s')
        self.remove_duplicates()
        print("Parsed!")

    # Function to find duplicate entries in the datafile
    # Method only works for data files with a delineated "CUSTOM.updateTime" column
    # Could be fixed if you simply take the first entry in a data file
    def remove_duplicates(self):
        timestamp_entries = list(self.data_file["CUSTOM.updateTime"])
        # print(len(self.data_file))
        for i, element in enumerate(timestamp_entries):
            if i <= len(timestamp_entries) - 2:  # j can only exist if there is an additional entry after i
                j = i + 1
                if timestamp_entries[i] == timestamp_entries[j]:
                    self.data_file.drop(axis=0, index=j, inplace=True)
        self.data_file = self.data_file.reset_index(drop=True)
        # print(len(self.data_file))

    def load_fields(self, fieldnames_list, datatype_label) -> list:
        self.datatype_label = datatype_label
        fieldnames = []

        for col in self.data_file.columns:
            fieldnames.append(col)
            # print(col)

        for field in fieldnames:
            fieldnames_list.insert(tk.END, field)

        ''' 
        # define iterator i for debugging
        i = 0
        for dt in self.data_file.dtypes:
            i = i + 1
            print(i)
            print(dt)
        '''
        return fieldnames_list

    def check_datatype(self, combo_value) -> list:

        print(combo_value)
        print("Above this is the combo value")

        if self.field_selected:
            if self.current_selected_field[0] == "CUSTOM.updateTime":
                print("You cannot change the datatype of the first updateTime")
            elif combo_value == "bool":
                try:
                    self.data_file[self.current_selected_field[0]] = self.data_file[
                        self.current_selected_field[0]].astype(bool)
                    print("success1")
                except:
                    print("This value cannot be converted to a boolean")
                    return self.identify_gauges(self.current_selected_field, self.combo)
            elif combo_value == "float64":
                try:
                    self.data_file[self.current_selected_field[0]] = self.data_file[
                        self.current_selected_field[0]].astype(float)
                    print("success2")
                except:
                    print("This value cannot be converted to a float")
                    return self.identify_gauges(self.current_selected_field, self.combo)
            elif combo_value == "int64":
                try:
                    self.data_file[self.current_selected_field[0]] = self.data_file[
                        self.current_selected_field[0]].astype(int)
                    print("success3")
                except:
                    print("This value cannot be converted to a integer")
                    return self.identify_gauges(self.current_selected_field, self.combo)
            elif combo_value == "object":
                try:
                    self.data_file[self.current_selected_field[0]] = self.data_file[
                        self.current_selected_field[0]].astype(str)
                    print("success4")
                except:
                    print("This value cannot be converted to a object")
                    return self.identify_gauges(self.current_selected_field, self.combo)

            return self.identify_gauges(self.current_selected_field, self.combo)
        else:
            return []

    def identify_gauges(self, selected_field, combo) -> list:
        """Use an if else tree to determine the kind of gauges for a specific type of data"""
        self.current_selected_field_gauges = []
        self.current_selected_field = selected_field
        self.combo = combo

        '''
        print(selected_field)
        print("test")
        print(self.data_file['CUSTOM.updateTime'].dtype)
        '''

        # probably going to need to be changed to just take in 1 variable instead of indexing a list

        print(self.data_file[self.current_selected_field[0]].dtype)

        if selected_field[0] == "CUSTOM.updateTime":
            self.current_selected_field_gauges = ["Clock",
                                                  "Stopwatch",
                                                  "Running Time"]
            self.combo.current(0)
        elif self.data_file[self.current_selected_field[0]].dtype == "bool":
            self.current_selected_field_gauges = ["X-Plot",
                                                  "On/off light"]
            self.combo.current(1)
        elif self.data_file[self.current_selected_field[0]].dtype == "int64" or self.data_file[
            self.current_selected_field[0]].dtype == "int32":
            self.current_selected_field_gauges = ["Circle - 90°",
                                                  "Circle - 180°",
                                                  "Circle - 270°",
                                                  "Circle - 360°",
                                                  "Number or Character Display",
                                                  "X-by-Y-plot"]
            self.combo.current(2)
            # there needs to be a special case for x by y plot
        elif self.data_file[self.current_selected_field[0]].dtype == "float64" or self.data_file[
            self.current_selected_field[0]].dtype == "float32":
            self.current_selected_field_gauges = ["Circle - 90°",
                                                  "Circle - 180°",
                                                  "Circle - 270°",
                                                  "Circle - 360°",
                                                  "Number or Character Display",
                                                  "X-by-Y-plot"]
            self.combo.current(3)
            # there needs to be a special case for x by y plot
        elif self.data_file[self.current_selected_field[0]].dtype == "object":
            self.current_selected_field_gauges = ["Text Display"]
            self.combo.current(0)
        else:
            print("Unknown Datatype")
            self.current_selected_field_gauges = ["Text Display"]
            self.combo.current(0)

        '''
        for gauge in gauge_names:
            print(gauge)
        '''

        self.field_selected = True

        match self.data_file[selected_field[0]].dtype:
            case "bool":
                self.datatype_label.config(text="Bool")
            case "float64":
                self.datatype_label.config(text="Float")
            case "float32":
                self.datatype_label.config(text="Float")
            case "int64":
                self.datatype_label.config(text="Integer")
            case "int32":
                self.datatype_label.config(text="Integer")
            case "object":
                self.datatype_label.config(text="String")
            case "datetime64[ns]":
                self.datatype_label.config(text="DateTime")
            case _:
                self.datatype_label.config(text="Type not recognized.")

        return self.current_selected_field_gauges

    # Creates a list of labels that show what the user has selected so far and
    # displays them to the screen
    def confirm_selection(self, selected_gauge) -> list:
        current_saved_gauge = TemporaryGauge(self.current_selected_field, selected_gauge, self.timestamp_value)
        self.user_selected_gauges_list.append(current_saved_gauge)

        gauge_name_list = []

        for i, element in enumerate(self.user_selected_gauges_list):
            if len(gauge_name_list) <= 10:
                element.id = i
                gauge_name_list.append(element.field_name[0])

        return gauge_name_list

    def delete_selection(self, index) -> list:

        for i, element in enumerate(self.user_selected_gauges_list):
            if i == index:
                self.user_selected_gauges_list.remove(element)

        gauge_name_list = []

        for element in self.user_selected_gauges_list:
            gauge_name_list.append(element.field_name[0])

        return gauge_name_list

    def set_timestamp(self, current_timestamp):
        self.timestamp_value = current_timestamp
        
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


class TemporaryGauge:
    """Stores a gauge's related information after a user completes a selection"""
    
    def __init__(self, f_name, g_name, t_stamp):
        self.id = None
        self.field_name = f_name
        self.gauge_name = g_name
        self.timestamp_value = t_stamp
        return gauge_names

