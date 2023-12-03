# Drone Telemetry Data

## Overview
This project was created for Group 3’s CS 499 project in Fall 2023. Its purpose is to allow users to review the data and footage captured by their drones and analyze it to improve their usage. 

## Features
* Ability to select and load .csv and .mov files
* Data from csv is parsed and its data fields are displayed to and are selectable by the user
* Users can select a gauge to display their selected data
* CSV data can be converted to and from metric to imperial
* The playback speed and timestamp (used for gauge updates) can be changed
* Gauges can be customized to suit the users’ needs (Name, position, size, etc.)
* Gauge information and customizations can be saved and loaded into the program
* Users can view an example render of their gauges
* Users can display all of their gauges
* Videos can be watched using the built-in media player
* Display gauges will update along with the video during playback (update time based on timestamp)

## How to Run
1. Clone this project locally
2. Install all dependencies
3. Run the main.py file with Python version 3.12 or newer.

## Dependencies
* Express install (recommended): `pip install -r requirements.txt`
* Tkinter: pip install tk (should come pre-installed with Windows builds of Python)
* VLC Media Player: pip install python-vlc (this only installs the Python bindings, you must install the media player separately)
* Pandas: pip install pandas
* Numpy: pip install numpy
* Matplotlib: pip install matplotlib

## Program Files
This project contains a number of files, each of which contains or controls different aspects of the program’s functionality

### Config files
* BarGauge.py: GaugeBase subclass containing functionality for the bar gauge
* CircleGauge.py: GaugeBase subclass containing functionality for the circle gauge
* ClockGauge.py: GaugeBase subclass containing functionality for the clock-based gauges (running time, stopwatch, clock)
* CustomizationGaugeManager.py: Controls the display of gauge/graph examples in the GaugeCustomization panel
* GaugeBase.py: Super class that defines base functionality and variables for all Gauge subclasses/files
* GaugeManager.py: Controls the display, positioning, and updating of graph/gauge data
* LightIndicatorGauge.py: GaugeBase subclass containing functionality for the on/off light gauge
* NumberDisplayGauge.py: GaugeBase subclass containing functionality for the number display gauge
* TextDisplayGauge.py: GaugeBase subclass containing functionality for the text display gauge
* XPlotGauge.py: GaugeBase subclass containing functionality for the X-plot graph/gauge
* XYPlotGauge.py: GaugeBase subclass containing functionality for the X-by-Y plot graph/gauge.
### Data files
* fileManager.py: Contains the functions for saving and loading all information (name, data, statistics, color range values) for each of the user-selected gauges
* Input.py: Contains the DataManager class, which is used for parsing and storing information from user-selected data files. This also includes functionality for selecting and searching through data fields, checking the data types, and displaying the appropriate selectable gauge types. Selection of a gauge will store information about that gauge in an instance of the TemporaryGauge class.
* Statistics.py: Contains the class used for calculating the statistics for a selected data type
### GUI files
* Panels.py: Contains all of the function classes and functions used to run the Configuration, GaugeCustomization, and Playback panels in our programs GUI.
* Windows.py: This file contains the instantiation of our program’s main loop and spawns the main window used for the GUI
### Playback files
* Video.py: This file contains all of the functionality for running the video player


## Contributors
* Owen Stinson
* Chris Fechter
* Caleb Walker
* Ryan Uehling
