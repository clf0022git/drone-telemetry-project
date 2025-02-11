import math
import numpy as np
from numpy import sin, cos, pi
import tkinter as tk
from src.config.BarGauge import BarGauge
from src.config.CircleGauge import CircleGauge
from src.config.ClockGauge import ClockGauge
from src.config.LightIndicatorGauge import LightIndicatorGauge
from src.config.NumberDisplayGauge import NumberDisplayGauge
from src.config.TextDisplayGauge import TextDisplayGauge
from src.config.XPlotGauge import XPlotGauge
from src.config.XYPlotGauge import XYPlotGauge
from src.data.input import DataManager


# Manager class for the gauges
class CustomizationGaugeManager:

    def draw_gauge(self, root, element):
        match element.gauge_name:
            # Case for getting data and drawing the x-by-y plot
            case "X-by-Y-plot":
                xy_plot_gauge = XYPlotGauge(root, title=element.name,
                                            connect_dots=True)
                xy_plot_gauge.pack(fill=tk.BOTH, expand=True)

                xy_plot_gauge.set_bounds(
                    x_bounds=(element.statistics_values.get('Minimum'), (element.statistics_values.get('Maximum'))),
                    y_bounds=(element.statistics_values_two.get('Minimum'), (element.statistics_values_two.get('Maximum'))))
                xy_plot_gauge.resize(element.size * 400, element.size * 300)
                print("Generate size?")
                print(element.size)

            case "X-Plot":
                x_plot_gauge = XPlotGauge(root, title=element.name, description='X values plotted over time')
                x_plot_gauge.set_bounds(
                    y_bounds=(element.statistics_values.get('Minimum'), (element.statistics_values.get('Maximum'))))
                x_plot_gauge.pack(fill=tk.BOTH, expand=True)
                x_plot_gauge.resize(element.size *400, element.size*300)
                print("Generate size?")
                print(element.size)
            # Case for getting the data and drawing the bar graph
            case "Bar":
                # Initialize vertical bar gauge
                v_bar_gauge = BarGauge(root, title=element.name,
                                       orientation='vertical')
                v_bar_gauge.pack(padx=10, pady=10)

                # Set the bounds for the bar gauges
                v_bar_gauge.set_bounds(
                    y_bounds=(element.statistics_values.get('Minimum'), element.statistics_values.get('Maximum')))

                # Change figure size as needed
                v_bar_gauge.resize(element.size * 400, element.size * 300)

            # Case for getting the data and drawing  the 90 degree circle graph
            case "Circle - 90°":
                step_interval = 1
                element_subtraction = element.statistics_values.get('Maximum') - element.statistics_values.get(
                    'Minimum')
                if element_subtraction != 0:
                    step_interval = element_subtraction / 2
                circle_gauge = CircleGauge(root, title=element.name, max_degree=90,
                                           number_range=(element.statistics_values.get('Minimum'),
                                                         element.statistics_values.get('Maximum')),
                                           number_step=step_interval)
                circle_gauge.pack(padx=10, pady=10)
                circle_gauge.update_value(element.statistics_values.get('Maximum'))
                circle_gauge.resize(element.size * 400, element.size * 300)

            # Case for getting the data and drawing  the 180 degree circle graph
            case "Circle - 180°":
                step_interval = 1
                element_subtraction = element.statistics_values.get('Maximum') - element.statistics_values.get(
                    'Minimum')
                if element_subtraction != 0:
                    step_interval = element_subtraction / 5
                circle_gauge = CircleGauge(root, title=element.name, max_degree=180,
                                           number_range=(element.statistics_values.get('Minimum'),
                                                         element.statistics_values.get('Maximum')),
                                           number_step=step_interval)
                circle_gauge.pack(padx=10, pady=10)
                circle_gauge.update_value(element.statistics_values.get('Maximum'))  # Update to a sample value
                circle_gauge.resize(element.size * 400, element.size * 300)

            # Case for getting the data and drawing  the 270 degree circle graph
            case "Circle - 270°":
                step_interval = 1
                element_subtraction = element.statistics_values.get('Maximum') - element.statistics_values.get(
                    'Minimum')
                if element_subtraction != 0:
                    step_interval = element_subtraction / 7
                circle_gauge = CircleGauge(root, title=element.name, max_degree=270,
                                           number_range=(element.statistics_values.get('Minimum'),
                                                         element.statistics_values.get('Maximum')),
                                           number_step=step_interval)
                circle_gauge.pack(padx=10, pady=10)
                circle_gauge.update_value(element.statistics_values.get('Maximum'))
                circle_gauge.resize(element.size * 400, element.size * 300)

            # Case for getting the data and drawing  the 360 degree circle graph
            case "Circle - 360°":

                step_interval = 1
                element_subtraction = element.statistics_values.get('Maximum') - element.statistics_values.get(
                    'Minimum')
                if element_subtraction != 0:
                    step_interval = element_subtraction / 10
                circle_gauge = CircleGauge(root, title=element.name, max_degree=360,
                                           number_range=(element.statistics_values.get('Minimum'),
                                                         element.statistics_values.get('Maximum')),
                                           number_step=step_interval)
                circle_gauge.pack(padx=10, pady=10)
                circle_gauge.update_value(element.statistics_values.get('Maximum'))
                circle_gauge.resize(element.size * 400, element.size * 300)

            # Case for getting data and drawing  the text display
            case "Text Display":
                print(element.name)
                text_gauge = TextDisplayGauge(root, title=element.name)
                text_gauge.pack(padx=10, pady=10)
                text_gauge.update_value("Sample Text")  # Update value example
                text_gauge.resize(element.size, element.size)

            # Case for getting the data and drawing the number/character display
            case "Number or Character Display":
                number_gauge = NumberDisplayGauge(root, title=element.name)
                number_gauge.pack(padx=10, pady=10)
                number_gauge.update_value(42)  # Update value example
                number_gauge.resize(element.size, element.size)

            # Case for drawing the clock
            case "Clock":
                clock_gauge = ClockGauge(root, title=element.name, description='Local Time')
                clock_gauge.pack(padx=10, pady=10)
                clock_gauge.resize(element.size, element.size)
            # Case for drawing the stopwatch
            case "Stopwatch":
                stopwatch_gauge = ClockGauge(root, title=element.name, description='Elapsed Time', mode='stopwatch')
                stopwatch_gauge.pack(padx=10, pady=10)

                # Button to toggle the stopwatch start/pause
                toggle_button = tk.Button(root, text="Start/Stop", command=stopwatch_gauge.toggle_stopwatch)
                toggle_button.pack(pady=5)
                stopwatch_gauge.resize(element.size, element.size)

            # Case for drawing the running time gauge
            case "Running Time":
                running_time_gauge = ClockGauge(root, title=element.name, description='Video Time',
                                                mode='running_time')
                running_time_gauge.pack(padx=10, pady=10)
                running_time_gauge.resize(element.size, element.size)

            # Case for drawing the on/off light
            case "On/off light":
                light_gauge = LightIndicatorGauge(root, title=element.name)
                light_gauge.pack(padx=10, pady=10)
                light_gauge.resize(element.size * 200, element.size * 150)

            case _:
                print("Gauge not found")
