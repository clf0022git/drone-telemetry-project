import tkinter as tk
import pandas as pd
import csv
import time
import datetime
import subprocess
import os
import sys
import traceback
from tkinter import ttk, filedialog

from src.config.ClockGauge import ClockGauge
from src.config.CustomizationGaugeManager import CustomizationGaugeManager
from src.config.TextDisplayGauge import TextDisplayGauge
from src.playback.video import VideoPlayer
from src.data.input import DataManager
from src.data.statistics import DataProcessor
from src.config.GaugeManager import *
from src.data.fileManager import FileManager

m_or_f = 0  # 0 = f and 1 = m


class ConfigurationPanel(ttk.Frame):
    """
    Panel for configuration settings like selecting telemetry data fields,
    specifying display gauges, etc.
    """

    def __init__(self, parent, playback_panel, stats_panel):
        super().__init__(parent)

        # Connection to gauge panel
        self.gauge_customization_panel = None

        # Instantiate a DataManager object
        self.data_manager = DataManager()
        self.data_processor = DataProcessor()
        self.statistics_list = []

        self.label = ttk.Label(self, font=("Roboto Black", 14), text="Configuration Panel")
        self.label.pack(pady=10)
        self.playback_panel = playback_panel
        self.stats_panel = stats_panel
        self.file_manager = FileManager

        # Styles for tkinter widgets
        button_style = ttk.Style()
        button_style.configure("TButton", font=("Roboto Light", 8))
        button_style.configure("TLabel", font=("Roboto Light", 8))
        button_style.configure("TRadiobutton", font=("Roboto Light", 8))

        # Button to load video file
        self.load_video_btn = ttk.Button(self, text="Load Video", command=self.load_video)
        self.load_video_btn.pack(pady=5)

        # Button to load CSV file
        self.load_csv_btn = ttk.Button(self, text="Load CSV", command=self.load_csv)
        self.load_csv_btn.pack(pady=5)

        self.metric_group = tk.Frame(self)
        self.metric_group.pack(pady=5, side=tk.TOP)

        self.metricButton = ttk.Button(self.metric_group, text="Swap to Metric or Imperial", command=self.swap_metric)
        self.metricButton.pack(pady=5, side=tk.TOP)

        self.metric_label = ttk.Label(self.metric_group, font=("Roboto Light", 10),
                                      text="Current Metrics: Meters and Celsius")
        self.metric_label.pack(pady=5, side=tk.TOP)

        # Frames that hold the fieldnames and their options
        self.fieldnames_gauge_group = tk.Frame(self)
        self.fieldnames_gauge_group.pack(pady=5, side=tk.TOP)
        self.timestamp_group = tk.Frame(self.fieldnames_gauge_group)
        self.timestamp_group.pack(padx=10, side=tk.LEFT)
        self.fieldnames_group = tk.Frame(self.fieldnames_gauge_group)
        self.fieldnames_group.pack(padx=10, side=tk.LEFT)
        self.datatypes_group = tk.Frame(self.fieldnames_gauge_group)
        self.datatypes_group.pack(padx=10, side=tk.LEFT)
        self.gauge_options_group = tk.Frame(self.fieldnames_gauge_group)
        self.gauge_options_group.pack(padx=10, side=tk.LEFT)
        self.user_selection_group = tk.Frame(self.fieldnames_gauge_group)
        self.user_selection_group.pack(side=tk.LEFT)

        # Possible way to show the second listbox of fieldnames
        self.second_field_group = tk.Frame(self)
        self.second_field_group.pack(pady=5)

        # Combobox that allows timestamp specification
        self.timestamp_label = ttk.Label(self.timestamp_group, font=("Roboto Light", 10), text="Timestamp:")
        self.timestamp_label.pack(pady=5, side=tk.TOP)
        self.timestamp_default_label = ttk.Label(self.timestamp_group,
                                                 text="Default - 1 sec / Data Entry")
        self.timestamp_default_label.pack(pady=5, side=tk.TOP)
        self.available_timestamps = ["1", "2", "3", "5"]
        self.timestamp_combo = ttk.Combobox(self.timestamp_group, value=self.available_timestamps, width=10)
        self.timestamp_combo.current(0)
        self.timestamp_combo.pack(pady=5, side=tk.TOP)
        self.timestamp_combo.bind("<<ComboboxSelected>>", self.change_timestamp)
        self.timestamp_combo.configure(font=("Roboto Light", 8))

        # Listbox to select one field
        self.fieldnames_label = ttk.Label(self.fieldnames_group, font=("Roboto Light", 10), text="Available Fields:")
        self.fieldnames_label.pack(pady=5)
        self.fieldnames_entry_box = ttk.Entry(self.fieldnames_group, font=("Roboto Light", 10))
        self.fieldnames_entry_box.pack(pady=5)
        self.fieldnames_entry_box.bind("<KeyRelease>", self.search_fields)
        self.fieldnames_list = tk.Listbox(self.fieldnames_group, selectmode=tk.SINGLE, height=5, exportselection=0,
                                          width=30)
        self.fieldnames_list.pack(pady=5)
        self.fieldnames_list.configure(font=("Roboto Light", 8))
        self.fieldnames = []
        self.fieldnames_searched = []

        # Button to show gauges
        self.show_gauges_btn = ttk.Button(self.fieldnames_group, text="Select Field", command=self.show_gauges)
        self.show_gauges_btn.pack(pady=10)

        # Combobox that allows changing datatypes
        self.current_datatype_label = ttk.Label(self.datatypes_group, font=("Roboto Light", 10),
                                                text="Current Datatype:")
        self.current_datatype_label.pack(pady=5)
        self.current_datatype_text = ttk.Label(self.datatypes_group, text="No item selected.")
        self.current_datatype_text.pack(pady=5)

        self.datatypes_label = ttk.Label(self.datatypes_group, font=("Roboto Light", 10), text="Change Datatype:")
        self.datatypes_label.pack(pady=5)
        self.available_datatypes = ["object", "bool", "int64", "float64"]
        self.datatype_combo = ttk.Combobox(self.datatypes_group, value=self.available_datatypes, width=10)
        self.datatype_combo.current(0)
        self.datatype_combo.pack(pady=5)
        self.datatype_combo.bind("<<ComboboxSelected>>", self.change_datatype)
        self.datatype_combo.configure(font=("Roboto Light", 8))

        # Listbox to show gauge options for a field
        self.gauge_types_label = ttk.Label(self.gauge_options_group, font=("Roboto Light", 10), text="Possible Gauges:")
        self.gauge_types_label.pack(pady=5)
        self.gauge_types_list = tk.Listbox(self.gauge_options_group, selectmode=tk.SINGLE, height=5, exportselection=0,
                                           width=30)
        self.gauge_types_list.pack(pady=5)
        self.gauge_types_list.configure(font=("Roboto Light", 8))
        self.gauge_types = []

        # Button to select field with gauge
        self.select_field_btn = ttk.Button(self.gauge_options_group, text="Select Gauge", command=self.select_field)
        self.select_field_btn.pack(pady=10)

        # Defines a listbox for user selections to be placed into
        self.user_selection_label = ttk.Label(self.user_selection_group, font=("Roboto Light", 10),
                                              text="Current Selections:")
        self.user_selection_label.pack(pady=5)
        self.user_selection_list = tk.Listbox(self.user_selection_group, selectmode=tk.SINGLE, height=5,
                                              exportselection=0, width=30)
        self.user_selection_list.pack(pady=5)
        self.user_selection_list.configure(font=("Roboto Light", 8))

        # Button to select field with gauge
        self.select_field_btn = ttk.Button(self.user_selection_group, text="Remove Choice", command=self.remove_field)
        self.select_field_btn.pack(pady=10)

        # Button to select field with gauge
        # self.generate_gauges_btn = ttk.Button(self, text="Generate Gauges", command=self.generate_gauges)
        # self.generate_gauges_btn.pack(pady=10, side=tk.TOP)

        self.speed_label = ttk.Label(self, font=("Roboto Light", 10), text="Playback Speed:")
        self.speed_label.pack(pady=5)

        # Using radio buttons for playback speed options
        self.speed_frame = ttk.Frame(self)
        self.speed_frame.pack(pady=5)

        self.playback_speed_list = ['1X', '5X', '1X backwards']
        self.playback_speed = tk.StringVar(value=self.playback_speed_list[0])

        self.speed_combobox = ttk.Combobox(self.speed_frame, textvariable=self.playback_speed,
                                           values=self.playback_speed_list, state='readonly')
        self.speed_combobox.grid(row=0, column=0, padx=5, pady=2)
        self.speed_combobox.bind('<<ComboboxSelected>>', self.set_playback_speed)

    def swap_metric(self):
        global m_or_f

        if self.data_manager.data_file.empty:
            print("Please load data before use")
            return

        self.data_manager.swap_metric()
        if m_or_f == 0:
            self.metric_label.config(text="Current Metrics: Feet and Fahrenheit")
            m_or_f = 1
        else:
            self.metric_label.config(text="Current Metrics: Meters and Celsius")
            m_or_f = 0

        self.get_statistics()
        self.gauge_customization_panel.update_gauges(True)

    def get_statistics(self):
        if len(self.data_manager.user_selected_gauges_list) == 0:
            print("No fields selected")
            return None

        for element in self.data_manager.user_selected_gauges_list:
            field = element.field_name[0]
            print(element.field_name[0])
            print("Help me")
            if self.data_manager.data_file[field].dtype == "int64" or self.data_manager.data_file[
                field].dtype == "float64":
                stats = self.data_processor.calc_statistics(self.data_manager.data_file[field], field)
                print(type(self.statistics_list))
                self.statistics_list.append(stats)
                element.set_statistics_text(stats)
                element.statistics_values = stats
            else:
                # This entry has no statistics
                self.statistics_list.append("This entry has no statistics")
                print("This gauge has no statistics associated with it.")
            if element.second_field_name != "":
                field = element.second_field_name
                if self.data_manager.data_file[field].dtype == "int64" or self.data_manager.data_file[
                    field].dtype == "float64":
                    stats = self.data_processor.calc_statistics(self.data_manager.data_file[field], field)
                    element.set_statistics_two_text(stats)
                    element.statistics_values_two = stats
                else:
                    # This entry has no statistics
                    print("This has no stats!")
        self.data_manager.set_statistics_list(self.statistics_list)

    def load_video(self):
        """Prompt the user to select a video file."""
        video_path = filedialog.askopenfilename(
            filetypes=[("MOV files", "*.mov"), ("MP4 files", "*.mp4"), ("All files", "*.*")],
            title="Select a Video File")
        if video_path:  # If a file is selected
            print(f"Video File Loaded: {video_path}")
            self.playback_panel.set_video_path(video_path)

    def load_csv(self):
        """Prompt the user to select a CSV file."""
        csv_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")], title="Select a CSV File")
        if csv_path:  # If a file is selected
            print(f"CSV File Loaded: {csv_path}")

        if not csv_path:
            return

        self.data_manager.parse(csv_path)
        self.fieldnames_list, self.fieldnames = self.data_manager.load_fields(self.fieldnames_list,
                                                                              self.current_datatype_text)
        print(self.fieldnames_list)

    def update_field_list(self, new_list):
        """Used by search_fields to update the listbox while the user is searching"""
        self.fieldnames_list.delete(0, tk.END)
        for field in new_list:
            self.fieldnames_list.insert(tk.END, field)

    def search_fields(self, e):
        """Called when user types in the fieldnames_entry_box to search for a specific field"""
        user_typed_input = self.fieldnames_entry_box.get()

        if user_typed_input == '':
            self.fieldnames_searched = self.fieldnames
        else:
            self.fieldnames_searched = []
            for field in self.fieldnames:
                if user_typed_input.lower() in field.lower():
                    self.fieldnames_searched.append(field)
                    self.update_field_list(self.fieldnames_searched)

    def show_gauges(self):
        """Show the user the gauges that are available to them"""
        selected_field = None
        self.gauge_types_list.delete(0, 'end')  # clear list before each call to update

        selected_field = [self.fieldnames_list.get(i) for i in self.fieldnames_list.curselection()]

        if selected_field:
            print(f"Selected Field: {', '.join(selected_field)}")
            # add the elements to the gauge_types listbox
            self.gauge_types_list.insert(0, *self.data_manager.identify_gauges(selected_field, self.datatype_combo))
            # Functionality to ask user about the type of the data probably in between identifying gauges and
            # updating the list

        else:
            print("Please select a field.")

    def remove_field(self):
        """Removes one of the user's selections from their choices that they've picked so far"""
        k = 0
        selected_field = [self.user_selection_list.get(i) for i in self.user_selection_list.curselection()]

        for element in self.user_selection_list.curselection():
            if element != 0:
                k = element - 1
            else:
                print("you cannot select the timestamp field.")
                return

        if selected_field:
            print(f"Selected Gauge: {', '.join(selected_field)}")
            self.user_selection_list.delete(0, 'end')  # clear list before each call to update
            self.user_selection_list.insert(0, *self.data_manager.delete_selection(k))
        else:
            print("Please select a field to remove.")

        self.get_statistics()
        self.gauge_customization_panel.update_gauges(True)

    def select_field(self):
        """Will call functionality to send selected fields to function"""
        selected_gauge = [self.gauge_types_list.get(i) for i in self.gauge_types_list.curselection()]

        if selected_gauge:
            print(f"Selected Gauge: {', '.join(selected_gauge)}")
            self.user_selection_list.delete(0, 'end')  # clear list before each call to update
            print("Called!")
            gt_list = self.data_manager.confirm_selection(selected_gauge, self.fieldnames_gauge_group,
                                                          self.user_selection_list, self.gauge_customization_panel,
                                                          self)
            if len(gt_list) <= 10:
                self.user_selection_list.insert(0, *gt_list)
                # Functionality to ask user about the type of the data probably in between identifying gauges and
                # updating the list
            else:
                print("You already have ten fields selected!")
                self.user_selection_list.insert(0, *gt_list)

        else:
            print("Please select a gauge.")

        self.get_statistics()
        print("Gauges sent!")
        self.gauge_customization_panel.update_gauges(True)

    def change_datatype(self, e):
        self.gauge_types_list.delete(0, 'end')
        self.gauge_types_list.insert(0, *self.data_manager.check_datatype(self.datatype_combo.get()))

    def change_timestamp(self, e):
        self.data_manager.set_timestamp(self.timestamp_combo.get())
        print(self.timestamp_combo.get())
        self.user_selection_list.delete(0, 'end')  # clear list before each call to update
        gt_list = ["Timestamp: " + str(self.data_manager.timestamp_value) + " second(s)"]
        for element in self.data_manager.user_selected_gauges_list:
            temp_gauge = "Gauge #" + str(element.id)
            gt_list.append(temp_gauge)
        self.user_selection_list.insert(0, *gt_list)

    def generate_gauges(self):
        print("button works")
        gauge_creator = GaugeManager()
        # for items in self.data_manager.user_selected_gauges_list:
        gauge_creator.drawGauges(self.data_manager)

    def set_playback_speed(self, event=None):
        speed_str = self.playback_speed.get()

        # Check if the current video is reversed
        is_reversed = 'reversed' in self.playback_panel.video_player.video_path

        if speed_str == '1X backwards':
            speed = 1
            backwards = 'backwards'
            if self.playback_panel.video_player and not is_reversed:
                self.playback_panel.reverse_video()
        else:
            speed = int(speed_str[:-1])
            backwards = ''

            # If the current video is reversed and the new speed is not '1X backwards', switch to original
            if is_reversed and speed_str != '1X backwards':
                # Remove '_reversed' from the file name to get the original video
                original_video_path = self.playback_panel.video_player.video_path.replace('_reversed', '')
                print(original_video_path)
                if os.path.exists(original_video_path):
                    self.playback_panel.is_video_reversed = False
                    self.playback_panel.set_video_path(original_video_path)
                else:
                    print(f"Original video file does not exist: {original_video_path}")

        print(f"Setting playback speed to: {speed}X {backwards}")

        if self.playback_panel.video_player:
            self.playback_panel.video_player.set_speed(speed)


class GaugeCustomizationPanel(ttk.Frame):
    """
    Panel for displaying statistics of selected telemetry data fields.
    """

    def __init__(self, parent):
        super().__init__(parent)

        self.label = ttk.Label(self, font=("Roboto Black", 14), text="Gauge Customization Panel")
        self.label.pack(pady=10)
        self.data_manager = None
        self.gauge_manager = CustomizationGaugeManager()
        self.fileManager = FileManager

        # Frame to hold the gauge viewer
        self.gauge_viewer_frame = tk.Frame(self)
        self.gauge_viewer_frame.pack(pady=5)

        self.current_gauge_text_label = tk.Label(self.gauge_viewer_frame, font=("Roboto Medium", 10),
                                                 text="No Gauge Selected")
        self.current_gauge_text_label.pack(side=tk.TOP, pady=10)

        self.gauge_viewer_contents_frame = tk.Frame(self.gauge_viewer_frame)
        self.gauge_viewer_contents_frame.pack(side=tk.TOP)

        self.current_gauge_left_btn = tk.Button(self.gauge_viewer_contents_frame, text="<", command=self.scroll_left)
        self.current_gauge_left_btn.pack(side=tk.LEFT)

        self.left_gauge_info_frame = tk.Frame(self.gauge_viewer_contents_frame)
        self.left_gauge_info_frame.pack(side=tk.LEFT)

        self.left_gauge_info_label = tk.Label(self.left_gauge_info_frame, font=("Roboto Light", 10),
                                              text="Basic Gauge Info:")
        self.left_gauge_info_label.pack(side=tk.TOP)

        self.current_gauge_text = tk.Text(self.left_gauge_info_frame, height=5, width=35)
        self.current_gauge_text.config(state="disabled", font=("Roboto Light", 10))
        self.current_gauge_text.pack(side=tk.TOP)
        self.current_gauge_position = 0
        self.current_gauge_text_list = []

        self.right_gauge_info_frame = tk.Frame(self.gauge_viewer_contents_frame)
        self.right_gauge_info_frame.pack(side=tk.LEFT)

        self.right_gauge_info_label = tk.Label(self.right_gauge_info_frame, font=("Roboto Light", 10),
                                               text="Gauge Statistics:")
        self.right_gauge_info_label.pack(side=tk.TOP)

        self.current_gauge_statistics_text = tk.Text(self.right_gauge_info_frame, height=5, width=35)
        self.current_gauge_statistics_text.config(state="disabled", font=("Roboto Light", 10))
        self.current_gauge_statistics_text.pack(side=tk.TOP)
        self.current_gauge_statistics_position = 0
        self.current_gauge_statistics_text_list = []

        self.current_gauge_right_btn = tk.Button(self.gauge_viewer_contents_frame, text=">", command=self.scroll_right)
        self.current_gauge_right_btn.pack(side=tk.LEFT)

        self.saveButton = ttk.Button(self, text="Save Data", command=self.save_data)
        self.saveButton.pack(pady=2)
        self.current_gauge_view_and_settings = tk.Frame(self)
        self.current_gauge_view_and_settings.pack(side=tk.TOP)

        # Set up all the frames for the gauge settings
        self.current_gauge_settings_frame = tk.Frame(self.current_gauge_view_and_settings)
        self.current_gauge_settings_frame.pack(side=tk.LEFT)

        self.name_frame = tk.Frame(self.current_gauge_settings_frame)
        self.name_frame.pack(side=tk.TOP)
        self.blue_frame = tk.Frame(self.current_gauge_settings_frame)
        self.blue_frame.pack(side=tk.TOP)
        self.green_frame = tk.Frame(self.current_gauge_settings_frame)
        self.green_frame.pack(side=tk.TOP)
        self.yellow_frame = tk.Frame(self.current_gauge_settings_frame)
        self.yellow_frame.pack(side=tk.TOP)
        self.red_frame = tk.Frame(self.current_gauge_settings_frame)
        self.red_frame.pack(side=tk.TOP)

        self.current_gauge_name_label = tk.Label(self.name_frame, font=("Roboto Medium", 10), text="Gauge Name:")
        self.current_gauge_name_label.pack(side=tk.LEFT)
        self.current_gauge_name_entry = tk.Entry(self.name_frame)
        self.current_gauge_name_entry.pack(side=tk.LEFT)
        self.current_gauge_name_btn = tk.Button(self.name_frame, text="Submit", command=self.change_name)
        self.current_gauge_name_btn.pack(side=tk.LEFT)

        self.current_gauge_blue_label = tk.Label(self.blue_frame, font=("Roboto Medium", 10), text="Blue Range:")
        self.current_gauge_blue_label.pack(side=tk.LEFT)
        self.current_gauge_blue_one_entry = tk.Entry(self.blue_frame, width=5)
        self.current_gauge_blue_one_entry.pack(side=tk.LEFT)
        self.current_gauge_blue_two_entry = tk.Entry(self.blue_frame, width=5)
        self.current_gauge_blue_two_entry.pack(side=tk.LEFT)
        self.current_gauge_blue_btn = tk.Button(self.blue_frame, text="Submit", command=self.change_blue)
        self.current_gauge_blue_btn.pack(side=tk.LEFT)

        self.current_gauge_green_label = tk.Label(self.green_frame, font=("Roboto Medium", 10), text="Green Range:")
        self.current_gauge_green_label.pack(side=tk.LEFT)
        self.current_gauge_green_one_entry = tk.Entry(self.green_frame, width=5)
        self.current_gauge_green_one_entry.pack(side=tk.LEFT)
        self.current_gauge_green_two_entry = tk.Entry(self.green_frame, width=5)
        self.current_gauge_green_two_entry.pack(side=tk.LEFT)
        self.current_gauge_green_btn = tk.Button(self.green_frame, text="Submit", command=self.change_green)
        self.current_gauge_green_btn.pack(side=tk.LEFT)

        self.current_gauge_yellow_label = tk.Label(self.yellow_frame, font=("Roboto Medium", 10), text="Yellow Range:")
        self.current_gauge_yellow_label.pack(side=tk.LEFT)
        self.current_gauge_yellow_one_entry = tk.Entry(self.yellow_frame, width=5)
        self.current_gauge_yellow_one_entry.pack(side=tk.LEFT)
        self.current_gauge_yellow_two_entry = tk.Entry(self.yellow_frame, width=5)
        self.current_gauge_yellow_two_entry.pack(side=tk.LEFT)
        self.current_gauge_yellow_btn = tk.Button(self.yellow_frame, text="Submit",
                                                  command=self.change_yellow)
        self.current_gauge_yellow_btn.pack(side=tk.LEFT)

        self.current_gauge_red_label = tk.Label(self.red_frame, font=("Roboto Medium", 10), text="Red Range:")
        self.current_gauge_red_label.pack(side=tk.LEFT)
        self.current_gauge_red_one_entry = tk.Entry(self.red_frame, width=5)
        self.current_gauge_red_one_entry.pack(side=tk.LEFT)
        self.current_gauge_red_two_entry = tk.Entry(self.red_frame, width=5)
        self.current_gauge_red_two_entry.pack(side=tk.LEFT)
        self.current_gauge_red_btn = tk.Button(self.red_frame, text="Submit", command=self.change_red)
        self.current_gauge_red_btn.pack(side=tk.LEFT)

        # Frame that will hold the current way the gauge looks

        self.current_gauge_view = tk.Frame(self.current_gauge_view_and_settings)
        self.current_gauge_view.pack(side=tk.LEFT)

        self.display_gauge_window_btn = tk.Button(self, text="Show Gauges on Window", command=self.create_window)
        self.display_gauge_window_btn.pack(side=tk.TOP)

        self.gauge_window = None

        self.display_gauge_manager = GaugeManager()  # Ryan's gauge manager

        # TODO: Add widgets to display statistics like min, max, average, etc.

    def create_window(self):
        if self.gauge_window is not None:
            self.gauge_window.destroy()
            self.display_gauge_manager.delete_gauges()
        self.gauge_window = tk.Toplevel()
        self.gauge_window.title("Gauge View")
        self.gauge_window.geometry("1000x700")
        self.gauge_window.resizable(True, True)
        self.display_gauge_manager.draw_gauges(self.data_manager, self.gauge_window)
        self.display_gauge_manager.update_color_ranges(self.data_manager)

    def draw_range_options(self):
        self.current_gauge_blue_label = tk.Label(self.blue_frame, font=("Roboto Medium", 10), text="Blue Range:")
        self.current_gauge_blue_label.pack(side=tk.LEFT)
        self.current_gauge_blue_one_entry = tk.Entry(self.blue_frame, width=5)
        self.current_gauge_blue_one_entry.pack(side=tk.LEFT)
        self.current_gauge_blue_two_entry = tk.Entry(self.blue_frame, width=5)
        self.current_gauge_blue_two_entry.pack(side=tk.LEFT)
        self.current_gauge_blue_btn = tk.Button(self.blue_frame, text="Submit", command=self.change_blue)
        self.current_gauge_blue_btn.pack(side=tk.LEFT)

        self.current_gauge_green_label = tk.Label(self.green_frame, font=("Roboto Medium", 10), text="Green Range:")
        self.current_gauge_green_label.pack(side=tk.LEFT)
        self.current_gauge_green_one_entry = tk.Entry(self.green_frame, width=5)
        self.current_gauge_green_one_entry.pack(side=tk.LEFT)
        self.current_gauge_green_two_entry = tk.Entry(self.green_frame, width=5)
        self.current_gauge_green_two_entry.pack(side=tk.LEFT)
        self.current_gauge_green_btn = tk.Button(self.green_frame, text="Submit", command=self.change_green)
        self.current_gauge_green_btn.pack(side=tk.LEFT)

        self.current_gauge_yellow_label = tk.Label(self.yellow_frame, font=("Roboto Medium", 10), text="Yellow Range:")
        self.current_gauge_yellow_label.pack(side=tk.LEFT)
        self.current_gauge_yellow_one_entry = tk.Entry(self.yellow_frame, width=5)
        self.current_gauge_yellow_one_entry.pack(side=tk.LEFT)
        self.current_gauge_yellow_two_entry = tk.Entry(self.yellow_frame, width=5)
        self.current_gauge_yellow_two_entry.pack(side=tk.LEFT)
        self.current_gauge_yellow_btn = tk.Button(self.yellow_frame, text="Submit",
                                                  command=self.change_yellow)
        self.current_gauge_yellow_btn.pack(side=tk.LEFT)

        self.current_gauge_red_label = tk.Label(self.red_frame, font=("Roboto Medium", 10), text="Red Range:")
        self.current_gauge_red_label.pack(side=tk.LEFT)
        self.current_gauge_red_one_entry = tk.Entry(self.red_frame, width=5)
        self.current_gauge_red_one_entry.pack(side=tk.LEFT)
        self.current_gauge_red_two_entry = tk.Entry(self.red_frame, width=5)
        self.current_gauge_red_two_entry.pack(side=tk.LEFT)
        self.current_gauge_red_btn = tk.Button(self.red_frame, text="Submit", command=self.change_red)
        self.current_gauge_red_btn.pack(side=tk.LEFT)

    def delete_range_options(self):
        for widget in self.red_frame.winfo_children():
            widget.destroy()
        for widget in self.blue_frame.winfo_children():
            widget.destroy()
        for widget in self.green_frame.winfo_children():
            widget.destroy()
        for widget in self.yellow_frame.winfo_children():
            widget.destroy()

    def change_name(self):
        if len(self.data_manager.user_selected_gauges_list) != 0:
            new_name = self.current_gauge_name_entry.get()
            self.data_manager.user_selected_gauges_list[self.current_gauge_position].name = new_name
            # self.current_gauge_text_label.config(text=new_name)
            print(new_name)
            for widget in self.current_gauge_view.winfo_children():
                widget.destroy()
            self.gauge_manager.draw_gauge(self.current_gauge_view,
                                          self.data_manager.user_selected_gauges_list[self.current_gauge_position])

        self.current_gauge_name_entry.delete(0, 'end')

    def change_blue(self):
        """Only changes the blue range if it fits within the detected minimum and maximum and the blue high is above
        the blue low"""
        current_gauge_stats = self.data_manager.user_selected_gauges_list[self.current_gauge_position]

        if len(self.data_manager.user_selected_gauges_list) != 0:
            if self.current_gauge_blue_one_entry.get() == "":
                blue_low = 0
            else:
                blue_low = float(self.current_gauge_blue_one_entry.get())

            if current_gauge_stats.statistics_values.get(
                    'Minimum') <= blue_low <= current_gauge_stats.statistics_values.get('Maximum'):
                current_gauge_stats.blue_range_low = blue_low
            if self.current_gauge_blue_two_entry.get() == "":
                blue_high = 0
            else:
                blue_high = float(self.current_gauge_blue_two_entry.get())

            if current_gauge_stats.statistics_values.get(
                    'Minimum') <= blue_low <= current_gauge_stats.statistics_values.get(
                    'Maximum') and blue_high > blue_low:
                current_gauge_stats.blue_range_high = blue_high
            print(blue_low)
            print(blue_high)
        self.current_gauge_blue_one_entry.delete(0, 'end')
        self.current_gauge_blue_two_entry.delete(0, 'end')

    def change_green(self):
        current_gauge_stats = self.data_manager.user_selected_gauges_list[self.current_gauge_position]
        if len(self.data_manager.user_selected_gauges_list) != 0:
            if self.current_gauge_green_one_entry.get() == "":
                green_low = 0
            else:
                green_low = float(self.current_gauge_green_one_entry.get())

            if current_gauge_stats.statistics_values.get(
                    'Minimum') <= green_low <= current_gauge_stats.statistics_values.get('Maximum'):
                current_gauge_stats.green_range_low = green_low
            if self.current_gauge_green_two_entry.get() == "":
                green_high = 0
            else:
                green_high = float(self.current_gauge_green_two_entry.get())

            if current_gauge_stats.statistics_values.get(
                    'Minimum') <= green_high <= current_gauge_stats.statistics_values.get(
                    'Maximum') and green_high > green_low:
                current_gauge_stats.green_range_high = green_high
            print(green_low)
            print(green_high)
        self.current_gauge_green_one_entry.delete(0, 'end')
        self.current_gauge_green_two_entry.delete(0, 'end')

    def change_yellow(self):
        current_gauge_stats = self.data_manager.user_selected_gauges_list[self.current_gauge_position]
        if len(self.data_manager.user_selected_gauges_list) != 0:
            if self.current_gauge_yellow_one_entry.get() == "":
                yellow_low = 0
            else:
                yellow_low = float(self.current_gauge_yellow_one_entry.get())

            if current_gauge_stats.statistics_values.get(
                    'Minimum') <= yellow_low <= current_gauge_stats.statistics_values.get('Maximum'):
                current_gauge_stats.yellow_range_low = yellow_low

            if self.current_gauge_yellow_two_entry.get() == "":
                yellow_high = 0
            else:
                yellow_high = float(self.current_gauge_yellow_two_entry.get())
            if current_gauge_stats.statistics_values.get(
                    'Minimum') <= yellow_high <= current_gauge_stats.statistics_values.get(
                    'Maximum') and yellow_high > yellow_low:
                current_gauge_stats.yellow_range_high = yellow_high
            print(yellow_low)
            print(yellow_high)
        self.current_gauge_yellow_one_entry.delete(0, 'end')
        self.current_gauge_yellow_two_entry.delete(0, 'end')

    def change_red(self):
        current_gauge_stats = self.data_manager.user_selected_gauges_list[self.current_gauge_position]
        if len(self.data_manager.user_selected_gauges_list) != 0:
            if self.current_gauge_red_one_entry.get() == "":
                red_low = 0
            else:
                red_low = float(self.current_gauge_red_one_entry.get())

            if current_gauge_stats.statistics_values.get(
                    'Minimum') <= red_low <= current_gauge_stats.statistics_values.get('Maximum'):
                current_gauge_stats.red_range_low = red_low

            if self.current_gauge_red_two_entry.get() == "":
                red_high = 0
            else:
                red_high = float(self.current_gauge_red_two_entry.get())

            if current_gauge_stats.statistics_values.get(
                    'Minimum') <= red_high <= current_gauge_stats.statistics_values.get(
                    'Maximum') and red_high > red_low:
                current_gauge_stats.red_range_high = red_high
            print(red_low)
            print(red_high)
        self.current_gauge_red_one_entry.delete(0, 'end')
        self.current_gauge_red_two_entry.delete(0, 'end')

    def scroll_right(self):
        if self.current_gauge_position < len(self.data_manager.user_selected_gauges_list) - 1:
            self.current_gauge_position = self.current_gauge_position + 1
        self.update_gauges(False)

    def scroll_left(self):
        if self.current_gauge_position > 0:
            self.current_gauge_position = self.current_gauge_position - 1
        self.update_gauges(False)

    def set_data_manager(self, config_panel: ConfigurationPanel):
        self.data_manager = config_panel.data_manager

    def update_gauges(self, reset_position):
        if reset_position:
            self.current_gauge_position = 0
        if len(self.data_manager.user_selected_gauges_list) > 0:
            self.delete_range_options()
            print("Current Position")
            print(self.current_gauge_position)
            print(self.data_manager.user_selected_gauges_list[self.current_gauge_position].gauge_name)
            g_name = self.data_manager.user_selected_gauges_list[self.current_gauge_position].gauge_name
            if g_name in ["Circle - 90°", "Circle - 180°", "Circle - 270°", "Circle - 360°", "Bar"]:
                print("Drawing the range options!")
                self.draw_range_options()
            # Clears temp widget
            for widget in self.current_gauge_view.winfo_children():
                widget.destroy()
            self.current_gauge_text_list = self.data_manager.display_user_selections()
            self.current_gauge_statistics_text_list = self.data_manager.statistics_list
            self.current_gauge_text.config(state="normal")
            self.current_gauge_statistics_text.config(state="normal")
            self.current_gauge_text.delete("1.0", "end")
            self.current_gauge_statistics_text.delete("1.0", "end")
            self.current_gauge_text.insert(tk.END, self.current_gauge_text_list[self.current_gauge_position])
            temp_statistics = self.data_manager.user_selected_gauges_list[self.current_gauge_position].statistics + \
                              self.data_manager.user_selected_gauges_list[self.current_gauge_position].statistics_two
            self.current_gauge_statistics_text.insert(tk.END, temp_statistics)
            print(temp_statistics)
            # if self.data_manager.user_selected_gauges_list[self.current_gauge_position].name == "":
            temp_text = "Gauge #" + str(self.data_manager.user_selected_gauges_list[self.current_gauge_position].id)
            self.current_gauge_text_label.config(text=temp_text)
            self.data_manager.user_selected_gauges_list[self.current_gauge_position].name = str(self.data_manager.user_selected_gauges_list[self.current_gauge_position].field_name[0])
            if self.data_manager.user_selected_gauges_list[self.current_gauge_position].second_field_name:
                self.data_manager.user_selected_gauges_list[self.current_gauge_position].name = str(self.data_manager.user_selected_gauges_list[self.current_gauge_position].name) + " X " + str(self.data_manager.user_selected_gauges_list[self.current_gauge_position].second_field_name)
            # else:
            temp_text = str(self.data_manager.user_selected_gauges_list[self.current_gauge_position].name)
            # self.current_gauge_text_label.config(text=temp_text)
            self.current_gauge_text.config(state="disabled")
            self.current_gauge_statistics_text.config(state="disabled")
            self.gauge_manager.draw_gauge(self.current_gauge_view,
                                          self.data_manager.user_selected_gauges_list[self.current_gauge_position])
            # Going to need to save the temporary widget that is created

    def save_data(self):
        self.fileManager.save_gauges(self.data_manager.user_selected_gauges_list)


class PlaybackPanel(ttk.Frame):
    """
    Panel for video and telemetry data playback.
    """

    def __init__(self, parent):
        super().__init__(parent)

        self.label = ttk.Label(self, font=("Roboto Black", 14), text="Playback Panel")
        self.label.pack(pady=10)

        # Video Player (initialization postponed until a video is selected)
        self.video_player = None
        self.video_path = None

        self.current_time = 0

        self.is_seeking = False

        self.is_video_reversed = False

        # Control panel
        control_panel = ttk.Frame(self)
        control_panel.pack(side="bottom", fill="x")

        # Current time label
        self.current_time_label = ttk.Label(control_panel, text="00:00")
        self.current_time_label.pack(side="left")

        # Seek bar
        self.seek_var = tk.DoubleVar()
        self.seek_bar = ttk.Scale(control_panel, variable=self.seek_var, from_=0, to=100, orient="horizontal",
                                  command=self.start_seek)
        self.seek_bar.pack(side="left", fill="x", expand=True)
        self.seek_bar.bind("<ButtonRelease-1>", self.stop_seek)

        # Total time label
        self.total_time_label = ttk.Label(control_panel, text="00:00")
        self.total_time_label.pack(side="right")

        # Play button
        self.play_button = ttk.Button(control_panel, text="Play", command=self.play_video)
        self.play_button.pack(side="left")

        # Pause button
        self.pause_button = ttk.Button(control_panel, text="Pause", command=self.pause_video)
        self.pause_button.pack(side="left")

        # Set initial state of control buttons
        self.play_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.DISABLED)

        self.update_ui()

        # Ref to customization panel
        self.gauge_customization_panel = None

    def set_video_path(self, video_path):
        self.video_path = video_path
        if self.video_path:  # if a file is selected
            # self.video_path = video_path
            if self.video_player is None:
                self.video_player = VideoPlayer(self, self.video_path)
                self.video_player.pack(fill="both", expand=True)
                self.video_player.bind_event("second-changed", self.update_graphs)
                self.video_player.is_video_backwards = False
                # self.video_player.bind_event("second-changed", self.on_second_changed)
                # self.video_player.bind_event("duration-changed", self.on_duration_changed)
            else:
                self.video_player.set_video_path(self.video_path)
                self.video_player.is_video_backwards = False

            # Enable control buttons now that a video is loaded
            self.play_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.NORMAL)

    def update_graphs(self, current_time):
        """Updates the gauges with current information"""

        # Change the input based on the timestamp
        allow_update = False
        time_temp = current_time
        timestamp = int(self.gauge_customization_panel.data_manager.timestamp_value)

        if time_temp % timestamp == 0:
            allow_update = True

        if allow_update:
            self.gauge_customization_panel.display_gauge_manager.update_gauges(self.gauge_customization_panel.data_manager, time_temp/timestamp)
            print("It updated on this timestamp: ")
            print(time_temp)
            print(time_temp/timestamp)
            print(timestamp)


    def play_video(self):
        if self.video_player:
            self.video_player.play()
            self.seek_bar["to"] = self.video_player.player.get_length() / 1000

    def pause_video(self):
        if self.video_player:
            self.video_player.pause()

    def start_seek(self, event):
        self.is_seeking = True

    def stop_seek(self, event):
        self.video_player.player.set_time(int(self.seek_var.get() * 1000))  # Seconds to milliseconds
        self.is_seeking = False

    def update_ui(self):
        """Update the UI every 500ms."""
        if self.video_player and self.video_player.player.is_playing():
            # Get the current and total time of the video
            current_time = self.video_player.player.get_time() / 1000  # Milliseconds to seconds
            total_time = self.video_player.player.get_length() / 1000  # Milliseconds to seconds

            # Set the total time once if it's not already set
            if self.seek_bar['to'] != total_time:
                self.seek_bar['to'] = total_time
                self.total_time_label['text'] = time.strftime('%H:%M:%S', time.gmtime(total_time))

            # Update the current time label
            self.current_time_label['text'] = time.strftime('%H:%M:%S', time.gmtime(current_time))

            # Update seek bar position only if the user is not seeking
            if not self.is_seeking:
                self.seek_var.set(current_time)

        # Schedule the update_ui method to be called after 500ms
        self.after(500, self.update_ui)

    def reverse_video(self):
        if not self.video_path:
            print("No video loaded to reverse")
            return

        # Determine the file extension and reversed file name
        base, ext = os.path.splitext(self.video_path)
        if ext.lower() not in ['.mp4', '.mov']:
            print("Unsupported file format for reversing")
            return

        reversed_video_path = f"{base}_reversed{ext}"

        # Check if the reversed video file already exists
        if os.path.exists(reversed_video_path):
            print(f"Reversed video already exists: {reversed_video_path}")
            self.is_video_reversed = True
            self.video_player.is_video_backwards = True
            self.set_video_path(reversed_video_path)
        else:
            try:
                # Use ffmpeg to reverse the video
                def run_command(command):
                    subprocess.run(command, shell=True, check=True)

                def split_video(input_vdeo, segment_length=30):
                    # Create a directory to store the segments
                    if not os.path.exists('segments'):
                        os.makedirs('segments')

                    cmd = f'ffmpeg -i {input_vdeo} -c copy -map 0 -segment_time {segment_length} -f segment -reset_timestamps 1 segments/output%03d.mp4'
                    run_command(cmd)

                def reverse_segments():
                    files = os.listdir('segments')
                    reversed_fls = []

                    for file in files:
                        if file.endswith('.mp4'):
                            reversed_fl = 'reversed_' + file
                            cmd = f'ffmpeg -i segments/{file} -vf reverse -af areverse segments/{reversed_fl}'
                            run_command(cmd)
                            reversed_fls.append(f'segments/{reversed_fl}')

                    return reversed_fls

                def combine_videos(files, output_video=reversed_video_path):
                    with open('file_list.txt', 'w') as f:
                        for file in files:
                            f.write(f"file '{file}'\n")

                    cmd = f'ffmpeg -f concat -safe 0 -i file_list.txt -c copy {output_video}'
                    run_command(cmd)

                    # Cleanup
                    os.remove('file_list.txt')

                input_video = self.video_path
                split_video(input_video)
                reversed_files = reverse_segments()
                combine_videos(reversed_files)

                # Replace the old video path with the new reversed video path
                self.is_video_reversed = True
                self.video_player.is_video_backwards = True
                self.set_video_path(reversed_video_path)
            except subprocess.CalledProcessError as e:
                self.is_video_reversed = False
                self.video_player.is_video_backwards = False
                print(f"ffmpeg error: {e}")
                traceback.print_exc(file=sys.stderr)
            except Exception as e:
                self.is_video_reversed = False
                self.video_player.is_video_backwards = False
                print(f"An error occurred while reversing the video: {e}")
                traceback.print_exc(file=sys.stderr)


class StatisticsPanel(ttk.Frame):
    """
    Panel for displaying statistics of selected telemetry data fields.
    """

    def __init__(self, parent):
        super().__init__(parent)

        self.label = ttk.Label(self, font=("Roboto Black", 14), text="Statistics Panel")
        self.label.pack(pady=10)

        # TODO: Add widgets to display statistics like min, max, average, etc.

# Additional panels can be added here...
