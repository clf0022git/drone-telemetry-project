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
* Tkinter: pip install tk (should come pre-installed with Windows builds of Python)
* VLC Media Player: pip install python-vlc (this only installs the Python bindings, you must install the media player separately)
* Pandas: pip install pandas

## Contributors
* Owen Stinson
* Chris Fechter
* Caleb Walker
* Ryan Uehling
