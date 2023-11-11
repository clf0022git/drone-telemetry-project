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
        self.additional_frame_group = None
        self.additional_listbox = None
        self.additional_label = None
        self.additional_btn = None
        self.remove_additional_btn = None
        self.user_selection_replacement_list = None
        self.current_gauge_temp = None  # Holds temporary gauge when 2nd field needs to be selected
        self.statistics_list = []

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

    def load_fields(self, fieldnames_list, datatype_label):
        self.datatype_label = datatype_label
        fieldnames = []

        for col in self.data_file.columns:
            fieldnames.append(col)
            # print(col)

        for field in fieldnames:
            fieldnames_list.insert(tk.END, field)

        return fieldnames_list, fieldnames

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
                                                  "X-by-Y-plot",
                                                  "Bar"]
            self.combo.current(2)
            # there needs to be a special case for x by y plot
        elif self.data_file[self.current_selected_field[0]].dtype == "float64" or self.data_file[
            self.current_selected_field[0]].dtype == "float32":
            self.current_selected_field_gauges = ["Circle - 90°",
                                                  "Circle - 180°",
                                                  "Circle - 270°",
                                                  "Circle - 360°",
                                                  "Number or Character Display",
                                                  "X-by-Y-plot",
                                                  "Bar"]
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
    def confirm_selection(self, selected_gauge, gauge_group_frame, user_selection_list) -> list:
        gauge_name_list = []
        timestamp_string = "Timestamp: " + str(self.timestamp_value) + " second(s)"
        gauge_name_list.append(timestamp_string)

        if len(self.user_selected_gauges_list) < 10:
            current_saved_gauge = TemporaryGauge(self.current_selected_field, selected_gauge[0], self.timestamp_value)
            self.current_gauge_temp = current_saved_gauge
            print(selected_gauge)

        if selected_gauge[0] == "X-by-Y-plot":
            for element in self.user_selected_gauges_list:
                if len(gauge_name_list) <= 10:
                    temp_gauge = "Gauge #" + str(element.id)
                    gauge_name_list.append(temp_gauge)

            self.user_selection_replacement_list = user_selection_list
            self.instantiate_second_field(gauge_group_frame)
            return gauge_name_list

        if len(self.user_selected_gauges_list) < 10:
            self.user_selected_gauges_list.append(current_saved_gauge)

        for i, element in enumerate(self.user_selected_gauges_list):
            if len(gauge_name_list) <= 10:
                element.id = i + 1
                temp_gauge = "Gauge #" + str(element.id)
                gauge_name_list.append(temp_gauge)

        return gauge_name_list

    def delete_selection(self, index) -> list:

        for i, element in enumerate(self.user_selected_gauges_list):
            if i == index:
                print("deleting")
                print(index)
                self.user_selected_gauges_list.remove(element)

        gauge_name_list = []
        timestamp_string = "Timestamp: " + str(self.timestamp_value) + " second(s)"
        gauge_name_list.append(timestamp_string)

        for element in self.user_selected_gauges_list:
            temp_gauge = "Gauge #" + str(element.id)
            gauge_name_list.append(temp_gauge)

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
                index = element.find('[C')
                if index != -1:
                    i = 0
                    while i < len(self.data_file[element]):
                        if self.data_file.at[i, element] != '':
                            data = self.data_file.at[i, element]
                            self.data_file.at[i, element] = (data * (9 / 5)) + 32
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
                index = element.find('[C')
                if index != -1:
                    i = 0
                    while i < len(self.data_file[element]):
                        if self.data_file.at[i, element] != '':
                            data = self.data_file.at[i, element]
                            self.data_file.at[i, element] = (data - 32) * (5 / 9)
                        i += 1
            # printing a field's data
            print('\nFirst 6 rows in CUSTOM.distance [m]:\n')
            for data in self.data_file['CUSTOM.distance [m]'][:6]:
                print("%10s" % data, end=" "),
                print('\n')
            self.metric_indicator = 0

    def instantiate_second_field(self, frame_group):
        self.additional_frame_group = tk.Frame(frame_group)
        self.additional_frame_group.pack(side=tk.LEFT)
        self.additional_frame_group.pack(padx=10)

        # Create listbox
        self.additional_label = ttk.Label(self.additional_frame_group, font=("Roboto Light", 10),
                                          text="Possible Second Field:")
        self.additional_label.pack(pady=5)
        self.additional_listbox = tk.Listbox(self.additional_frame_group, selectmode=tk.SINGLE, height=5,
                                             exportselection=0, width=30)
        self.additional_listbox.pack(pady=5)
        self.additional_listbox.configure(font=("Roboto Light", 8))

        # Button to select second input
        self.additional_btn = ttk.Button(self.additional_frame_group, text="Select 2nd Field",
                                         command=self.select_second)
        self.additional_btn.pack(pady=10)

        # Button to deny second input
        self.remove_additional_btn = ttk.Button(self.additional_frame_group, text="No 2nd Field",
                                                command=self.remove_second)
        self.remove_additional_btn.pack(pady=10)

        fieldnames = []

        for col in self.data_file.columns:
            fieldnames.append(col)

        for field in fieldnames:
            self.additional_listbox.insert(tk.END, field)

    def delete_second_field(self):
        self.additional_frame_group.destroy()

    def select_second(self):
        gauge_name_list = []
        timestamp_string = "Timestamp: " + str(self.timestamp_value) + " second(s)"
        gauge_name_list.append(timestamp_string)

        current_saved_gauge = self.current_gauge_temp
        selected_gauge = [self.additional_listbox.get(i) for i in self.additional_listbox.curselection()]

        dtype_bool = self.data_file[selected_gauge[0]].dtype == "int64" or self.data_file[
            selected_gauge[0]].dtype == "float64"
        print("This datatype: ")
        print(self.data_file[selected_gauge[0]].dtype)
        if selected_gauge and dtype_bool:
            print(f"Selected Gauge: {', '.join(selected_gauge)}")
            self.user_selection_replacement_list.delete(0, 'end')

            current_saved_gauge.set_second_field(selected_gauge[0])
            if len(self.user_selected_gauges_list) < 10:
                self.user_selected_gauges_list.append(current_saved_gauge)

            for i, element in enumerate(self.user_selected_gauges_list):
                if len(gauge_name_list) <= 10:
                    element.id = i + 1
                    temp_gauge = "Gauge #" + str(element.id)
                    gauge_name_list.append(temp_gauge)

            if len(gauge_name_list) < 10:
                self.user_selection_replacement_list.insert(0, *gauge_name_list)
            else:
                print("You already have ten field selected!")
                self.user_selection_replacement_list.insert(0, *gauge_name_list)
            self.remove_second()
        else:
            print("Please select a field that is an integer or float.")

    def remove_second(self):
        gauge_name_list = []
        timestamp_string = "Timestamp: " + str(self.timestamp_value) + " second(s)"
        gauge_name_list.append(timestamp_string)

        self.user_selection_replacement_list.delete(0, 'end')  # clear list before each call to update
        if len(self.user_selected_gauges_list) <= 10:
            self.user_selected_gauges_list.append(self.current_gauge_temp)
            print("Working!1")

        for i, element in enumerate(self.user_selected_gauges_list):
            if len(gauge_name_list) <= 10:
                element.id = i + 1
                temp_gauge = "Gauge #" + str(element.id)
                gauge_name_list.append(temp_gauge)
            print("Working!2")

        if len(gauge_name_list) <= 11:
            self.user_selection_replacement_list.insert(0, *gauge_name_list)
            print("Working!3")
        self.delete_second_field()

    def display_user_selections(self) -> list:
        user_selection_string_list = []
        for element in self.user_selected_gauges_list:
            user_selection_string = "Gauge ID:" + str(element.id) + ",\n" + "Field 1:" + str(
                element.field_name[0]) + ",\n" + "Field 2:" + str(element.second_field_name) + ",\n" + "Gauge:" + str(
                element.gauge_name) + ",\n"
            user_selection_string_list.append(user_selection_string)
        return user_selection_string_list

    def set_statistics_list(self, stat_list):
        self.statistics_list = stat_list


class TemporaryGauge:
    """Stores a gauge's related information after a user completes a selection"""

    def __init__(self, f_name, g_name, t_stamp):
        self.id = None
        self.field_name = f_name
        self.second_field_name = ""
        self.gauge_name = g_name
        self.timestamp_value = t_stamp
        self.name = ""
        self.blue_range_low = 0
        self.blue_range_high = 0
        self.green_range_low = 0
        self.green_range_high = 0
        self.yellow_range_low = 0
        self.yellow_range_high = 0
        self.red_range_low = 0
        self.red_range_high = 0

    def set_second_field(self, second_field):
        self.second_field_name = second_field
