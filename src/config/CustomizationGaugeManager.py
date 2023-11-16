import numpy as np
from numpy import sin, cos, pi
import plotly.graph_objects as go
import datetime as dt
import datetime as datetime
import tkinter as Tkinter
import tkinter as tk
import tk_tools
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import style
import matplotlib.animation as animation

from src.config.BarGauge import BarGauge
from src.config.CircleGauge import CircleGauge
from src.config.ClockGauge import ClockGauge
from src.config.LightIndicatorGauge import LightIndicatorGauge
from src.config.NumberDisplayGauge import NumberDisplayGauge
from src.config.TextDisplayGauge import TextDisplayGauge
from src.config.XPlotGauge import XPlotGauge
from src.config.XYPlotGauge import XYPlotGauge
from src.data.input import DataManager


# from src.gui.window import GaugeWindow

# Manager class for the gauges
class CustomizationGaugeManager:

    def draw_gauge(self, root, element):
        match element.gauge_name:
            # Case for getting data and drawing the x-by-y plot
            case "X-by-Y-plot":
                xy_plot_gauge = XYPlotGauge(root, title=element.name, description='Drone X-Y Plot',
                                            connect_dots=True)
                xy_plot_gauge.pack(fill=tk.BOTH, expand=True)

                xy_plot_gauge.set_bounds(x_bounds=(-10, 10), y_bounds=(-10, 10))
            case "X-Plot":
                x_plot_gauge = XPlotGauge(root, title=element.name, description='X values plotted over time')
                x_plot_gauge.pack(fill=tk.BOTH, expand=True)
            # Case for getting the data and drawing the bar graph
            case "Bar":
                # Initialize vertical bar gauge
                v_bar_gauge = BarGauge(root, title=element.name, description='Vertical bar description',
                                       orientation='vertical')
                v_bar_gauge.pack(padx=10, pady=10)

                # Change figure size as needed
                v_bar_gauge.set_figure_size(4, 3)

                # Set the bounds for the bar gauges
                v_bar_gauge.set_bounds(
                    y_bounds=(0, element.statistics_values.get('Maximum')))
            # Case for getting the data and drawing  the 90 degree circle graph
            case "Circle - 90°":
                circle_gauge = CircleGauge(root, title=element.name, max_degree=90,
                                           number_range=(0,
                                                         element.statistics_values.get('Maximum')),
                                           number_step=1)
                circle_gauge.pack(padx=10, pady=10)
                circle_gauge.update_value(element.statistics_values.get('Maximum'))

            # Case for getting the data and drawing  the 180 degree circle graph
            case "Circle - 180°":
                circle_gauge = CircleGauge(root, title=element.name, max_degree=180,
                                           number_range=(0,
                                                         element.statistics_values.get('Maximum')),
                                           number_step=1)
                circle_gauge.pack(padx=10, pady=10)
                circle_gauge.update_value(element.statistics_values.get('Maximum'))  # Update to a sample value

            # Case for getting the data and drawing  the 270 degree circle graph
            case "Circle - 270°":
                circle_gauge = CircleGauge(root, title=element.name, max_degree=270,
                                           number_range=(0,
                                                         element.statistics_values.get('Maximum')),
                                           number_step=1)
                circle_gauge.pack(padx=10, pady=10)
                circle_gauge.update_value(element.statistics_values.get('Maximum'))

            # Case for getting the data and drawing  the 360 degree circle graph
            case "Circle - 360°":
                circle_gauge = CircleGauge(root, title=element.name, max_degree=360,
                                           number_range=(0,
                                                         element.statistics_values.get('Maximum')),
                                           number_step=1)
                circle_gauge.pack(padx=10, pady=10)
                circle_gauge.update_value(element.statistics_values.get('Maximum'))

            # Case for getting data and drawing  the text display
            case "Text Display":
                print(element.name)
                text_gauge = TextDisplayGauge(root, title=element.name, description='Current Text')
                text_gauge.pack(padx=10, pady=10)
                text_gauge.update_value("Sample Text")  # Update value example
            # Case for getting the data and drawing the number/character display
            case "Number or Character Display":
                number_gauge = NumberDisplayGauge(root, title=element.name, description='km/h')
                number_gauge.pack(padx=10, pady=10)
                number_gauge.update_value(42)  # Update value example
            # Case for drawing the clock
            case "Clock":
                clock_gauge = ClockGauge(root, title=element.name, description='Local Time')
                clock_gauge.pack(padx=10, pady=10)
            # Case for drawing the stopwatch
            case "Stopwatch":
                stopwatch_gauge = ClockGauge(root, title=element.name, description='Elapsed Time', mode='stopwatch')
                stopwatch_gauge.pack(padx=10, pady=10)

                # Button to toggle the stopwatch start/pause
                toggle_button = tk.Button(root, text="Start/Stop", command=stopwatch_gauge.toggle_stopwatch)
                toggle_button.pack(pady=5)
            # Case for drawing the running time gauge
            case "Running Time":
                running_time_gauge = ClockGauge(root, title=element.name, description='Video Time',
                                                mode='running_time')
                running_time_gauge.pack(padx=10, pady=10)
            # Case for drawing the on/off light
            case "On/off light":
                light_gauge = LightIndicatorGauge(root, title=element.name)
                light_gauge.pack(padx=10, pady=10)

            case _:
                print("Gauge not found")
