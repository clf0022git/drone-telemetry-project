# File imports
from src.config.BarGauge import BarGauge
from src.config.CircleGauge import CircleGauge
from src.config.ClockGauge import ClockGauge
from src.config.LightIndicatorGauge import LightIndicatorGauge
from src.config.NumberDisplayGauge import NumberDisplayGauge
from src.config.TextDisplayGauge import TextDisplayGauge
from src.config.XPlotGauge import XPlotGauge
from src.config.XYPlotGauge import XYPlotGauge
from src.data.input import DataManager

# Library imports
import tkinter as tk


class GaugeInstance:

    def __init__(self):
        self.gauge = None
        self.isShowing = False  # Could be used to temporarily show and hide gauges on the window


# Manager class for the gauges
class GaugeManager:
    # Initialization function

    def __init__(self):
        self.name = None
        # List for the gauges that are created during runtimer
        self.gauge_instance_list = []

    def delete_gauges(self):
        self.gauge_instance_list.clear()

    # Function for drawing each of the functions out
    def draw_gauges(self, data_manager: DataManager, gauge_window, alarm_list):
        for i, element in enumerate(data_manager.user_selected_gauges_list):
            print(type(element.statistics_values))
            match element.gauge_name:

                # Case for getting data and drawing the x-by-y plot
                case "X-by-Y-plot":
                    # Instantiate a new instance of a gauge and append it to a list of the one's in use
                    gauge_instance = GaugeInstance()
                    self.gauge_instance_list.append(gauge_instance)

                    gauge_instance.gauge = XYPlotGauge(gauge_window, title=element.name)
                    gauge_instance.gauge.set_bounds(x_bounds=(element.statistics_values.get('Minimum'), (element.statistics_values.get('Maximum'))), y_bounds=(element.statistics_values_two.get('Minimum'), (element.statistics_values_two.get('Maximum'))))
                    if i < 5:
                        gauge_instance.gauge.grid(row=0, column=i)
                    else:
                        gauge_instance.gauge.grid(row=1, column=i - 5)
                # Case for getting the data and drawing the x-graph
                case "X-Plot":
                    gauge_instance = GaugeInstance()
                    self.gauge_instance_list.append(gauge_instance)

                    gauge_instance.gauge = XPlotGauge(gauge_window, title=element.name)
                    gauge_instance.gauge.set_bounds(x_bounds=(element.statistics_values.get('Minimum'), (element.statistics_values.get('Maximum'))))
                    if i < 5:
                        gauge_instance.gauge.grid(row=0, column=i)
                    else:
                        gauge_instance.gauge.grid(row=1, column=i - 5)
                # Case for getting the data and drawing the bar graph
                case "Bar":
                    gauge_instance = GaugeInstance()
                    self.gauge_instance_list.append(gauge_instance)

                    gauge_instance.gauge = BarGauge(gauge_window, title=element.name, orientation='vertical')
                    gauge_instance.gauge.set_bounds(
                        y_bounds=(element.statistics_values.get('Minimum'), element.statistics_values.get('Maximum')))
                    if i < 5:
                        gauge_instance.gauge.grid(row=0, column=i)
                    else:
                        gauge_instance.gauge.grid(row=1, column=i - 5)

                # Case for getting the data and drawing the 90 degree circle graph
                case "Circle - 90°":
                    gauge_instance = GaugeInstance()
                    self.gauge_instance_list.append(gauge_instance)

                    gauge_instance.gauge = CircleGauge(gauge_window, title=element.name, max_degree=90,
                                                       number_range=(element.statistics_values.get('Minimum'),
                                                                     element.statistics_values.get('Maximum')),
                                                       number_step=1)
                    if i < 5:
                        gauge_instance.gauge.grid(row=0, column=i)
                    else:
                        gauge_instance.gauge.grid(row=1, column=i - 5)

                    gauge_instance.gauge.update_value(element.statistics_values.get('Maximum'))

                # Case for getting the data and drawing the 180 degree circle graph
                case "Circle - 180°":
                    gauge_instance = GaugeInstance()
                    self.gauge_instance_list.append(gauge_instance)

                    gauge_instance.gauge = CircleGauge(gauge_window, title=element.name, max_degree=180,
                                                       number_range=(element.statistics_values.get('Minimum'),
                                                                     element.statistics_values.get('Maximum')),
                                                       number_step=1)
                    if i < 5:
                        gauge_instance.gauge.grid(row=0, column=i)
                    else:
                        gauge_instance.gauge.grid(row=1, column=i - 5)

                    gauge_instance.gauge.update_value(element.statistics_values.get('Maximum'))

                # Case for getting the data and drawing the 270 degree circle graph
                case "Circle - 270°":
                    gauge_instance = GaugeInstance()
                    self.gauge_instance_list.append(gauge_instance)

                    gauge_instance.gauge = CircleGauge(gauge_window, title=element.name, max_degree=270,
                                                       number_range=(element.statistics_values.get('Minimum'),
                                                                     element.statistics_values.get('Maximum')),
                                                       number_step=1)
                    if i < 5:
                        gauge_instance.gauge.grid(row=0, column=i)
                    else:
                        gauge_instance.gauge.grid(row=1, column=i - 5)

                    gauge_instance.gauge.update_value(element.statistics_values.get('Maximum'))

                # Case for getting the data and drawing the 360 degree circle graph
                case "Circle - 360°":
                    gauge_instance = GaugeInstance()
                    self.gauge_instance_list.append(gauge_instance)

                    gauge_instance.gauge = CircleGauge(gauge_window, title=element.name, max_degree=360,
                                                       number_range=(element.statistics_values.get('Minimum'),
                                                                     element.statistics_values.get('Maximum')),
                                                       number_step=1)
                    if i < 5:
                        gauge_instance.gauge.grid(row=0, column=i)
                    else:
                        gauge_instance.gauge.grid(row=1, column=i - 5)

                    gauge_instance.gauge.update_value(element.statistics_values.get('Maximum'))

                # Case for getting data and drawing the text display
                case "Text Display":
                    gauge_instance = GaugeInstance()
                    self.gauge_instance_list.append(gauge_instance)

                    gauge_instance.gauge = TextDisplayGauge(gauge_window, title=element.name)
                    if i < 5:
                        gauge_instance.gauge.grid(row=0, column=i)
                    else:
                        gauge_instance.gauge.grid(row=1, column=i - 5)

                # Case for getting the data and drawing the number/character display
                case "Number or Character Display":
                    gauge_instance = GaugeInstance()
                    self.gauge_instance_list.append(gauge_instance)

                    gauge_instance.gauge = NumberDisplayGauge(gauge_window, title=element.name)
                    if i < 5:
                        gauge_instance.gauge.grid(row=0, column=i)
                    else:
                        gauge_instance.gauge.grid(row=1, column=i - 5)

                # Case for drawing the clock
                case "Clock":
                    gauge_instance = GaugeInstance()
                    self.gauge_instance_list.append(gauge_instance)

                    gauge_instance.gauge = ClockGauge(gauge_window, title=element.name, description='CSV Timestamp', mode='clock_csv')
                    if i < 5:
                        gauge_instance.gauge.grid(row=0, column=i)
                    else:
                        gauge_instance.gauge.grid(row=1, column=i - 5)

                    for alarm in alarm_list:
                        gauge_instance.gauge.add_alarm(alarm)

                # Case for drawing the stopwatch
                case "Stopwatch":
                    gauge_instance = GaugeInstance()
                    self.gauge_instance_list.append(gauge_instance)

                    gauge_instance.gauge = ClockGauge(gauge_window, title=element.name, description='Elapsed Time',
                                                      mode='stopwatch')
                    if i < 5:
                        gauge_instance.gauge.grid(row=0, column=i)
                    else:
                        gauge_instance.gauge.grid(row=1, column=i - 5)
                # Case for drawing the running time gauge
                case "Running Time":
                    gauge_instance = GaugeInstance()
                    self.gauge_instance_list.append(gauge_instance)

                    gauge_instance.gauge = ClockGauge(gauge_window, title=element.name, description='Video Time',
                                                      mode='running_time')
                    if i < 5:
                        gauge_instance.gauge.grid(row=0, column=i)
                    else:
                        gauge_instance.gauge.grid(row=1, column=i - 5)

                # Case for drawing the on/off light
                case "On/off light":
                    gauge_instance = GaugeInstance()
                    self.gauge_instance_list.append(gauge_instance)

                    gauge_instance.gauge = LightIndicatorGauge(gauge_window, title=element.name,
                                                               description='System Power')
                    if i < 5:
                        gauge_instance.gauge.grid(row=0, column=i)
                    else:
                        gauge_instance.gauge.grid(row=1, column=i - 5)
                # Default case
                case _:
                    print("Gauge not found")

    # This function will call each of the animation functions for the displayed gauges
    def update_gauges(self, data_manager: DataManager, current_time):
        for i, element in enumerate(data_manager.user_selected_gauges_list):  # Syncs up with the list in this class

            match element.gauge_name:

                # Case for animating the x-by-y plot
                case "X-by-Y-plot":
                    self.gauge_instance_list[i].gauge.update_value(
                        data_manager.data_file.at[current_time, element.field_name[0]],
                        data_manager.data_file.at[current_time, element.second_field_name],
                        data_manager.data_file.at[current_time, element.second_field_name])

                    current_value = data_manager.data_file.at[current_time, element.field_name[0]]
                    current_value_two = data_manager.data_file.at[current_time, element.second_field_name]
                    current_value = "Current value: " + str(current_value) + " and " + str(current_value_two)

                    self.gauge_instance_list[i].gauge.description_label.config(text=current_value)

                # Case for animating the x-graph
                case "X-Plot":
                    self.gauge_instance_list[i].gauge.update_value(
                        data_manager.data_file.at[current_time, element.field_name[0]])

                    current_value = data_manager.data_file.at[current_time, element.field_name[0]]
                    current_value = str(current_value)

                    self.gauge_instance_list[i].gauge.description_label.config(text=current_value)

                # Case for animating the bar graph
                case "Bar-Graph":
                    self.gauge_instance_list[i].gauge.update_value(
                        data_manager.data_file.at[current_time, element.field_name[0]])

                    current_value = data_manager.data_file.at[current_time, element.field_name[0]]
                    current_value = str(current_value)

                    self.gauge_instance_list[i].gauge.description_label.config(text=current_value)

                # Case for animating the 90 degree circle graph
                case "Circle - 90°":
                    self.gauge_instance_list[i].gauge.update_value(
                        data_manager.data_file.at[current_time, element.field_name[0]])

                    current_value = data_manager.data_file.at[current_time, element.field_name[0]]
                    current_value = str(current_value)

                    self.gauge_instance_list[i].gauge.description_label.config(text=current_value)

                # Case for animating the 180 degree circle graph
                case "Circle - 180°":
                    self.gauge_instance_list[i].gauge.update_value(
                        data_manager.data_file.at[current_time, element.field_name[0]])

                    current_value = data_manager.data_file.at[current_time, element.field_name[0]]
                    current_value = str(current_value)

                    self.gauge_instance_list[i].gauge.description_label.config(text=current_value)

                # Case for animating the 270 degree circle graph
                case "Circle - 270°":
                    self.gauge_instance_list[i].gauge.update_value(
                        data_manager.data_file.at[current_time, element.field_name[0]])

                    current_value = data_manager.data_file.at[current_time, element.field_name[0]]
                    current_value = str(current_value)

                    self.gauge_instance_list[i].gauge.description_label.config(text=current_value)

                # Case for animating the 360 degree circle graph
                case "Circle - 360°":
                    # circle_window = GaugeWindow()
                    self.gauge_instance_list[i].gauge.update_value(
                        data_manager.data_file.at[current_time, element.field_name[0]])

                    current_value = data_manager.data_file.at[current_time, element.field_name[0]]
                    current_value = str(current_value)

                    self.gauge_instance_list[i].gauge.description_label.config(text=current_value)

                # Case for animating the text display
                case "Text Display":
                    self.gauge_instance_list[i].gauge.update_value(
                        data_manager.data_file.at[current_time, element.field_name[0]])

                    current_value = data_manager.data_file.at[current_time, element.field_name[0]]
                    current_value = str(current_value)

                    self.gauge_instance_list[i].gauge.description_label.config(text=current_value)

                # Case for animating the number/character display
                case "Number or Character Display":
                    self.gauge_instance_list[i].gauge.update_value(
                        data_manager.data_file.at[current_time, element.field_name[0]])

                    current_value = data_manager.data_file.at[current_time, element.field_name[0]]
                    current_value = str(current_value)

                    self.gauge_instance_list[i].gauge.description_label.config(text=current_value)

                # Case for animating the clock
                case "Clock":
                    self.gauge_instance_list[i].gauge.update_value(data_manager.data_file.at[current_time, element.field_name[0]])

                    current_value = data_manager.data_file.at[current_time, element.field_name[0]]
                    current_value = str(current_value)

                    self.gauge_instance_list[i].gauge.description_label.config(text=current_value)

                # Case for animating the stopwatch
                case "Stopwatch":
                    self.gauge_instance_list[i].gauge.update_value()

                    current_value = data_manager.data_file.at[current_time, element.field_name[0]]
                    current_value = str(current_value)

                    self.gauge_instance_list[i].gauge.description_label.config(text=current_value)

                # Case for animating the running time gauge
                case "Running Time":
                    self.gauge_instance_list[i].gauge.update_value(current_time)

                    current_value = data_manager.data_file.at[current_time, element.field_name[0]]
                    current_value = str(current_value)

                    self.gauge_instance_list[i].gauge.description_label.config(text=current_value)

                # Case for animating the on/off light
                case "On/off light":
                    self.gauge_instance_list[i].gauge.update_value(
                        data_manager.data_file.at[current_time, element.field_name[0]])

                    current_value = data_manager.data_file.at[current_time, element.field_name[0]]
                    current_value = str(current_value)

                    self.gauge_instance_list[i].gauge.description_label.config(text=current_value)

                # Default case
                case _:
                    print("Gauge not found")

    # This function will update the color ranges for each of the gauges
    def update_color_ranges(self, data_manager: DataManager):
        for i, element in enumerate(data_manager.user_selected_gauges_list):
            # Case for changing the color ranges of the X-by-Y-plot
            self.gauge_instance_list[i].gauge.update_colors(
                blue=(element.blue_range_low, element.blue_range_high),
                green=(element.green_range_low, element.green_range_high),
                yellow=(element.yellow_range_low, element.yellow_range_high),
                red=(element.red_range_low, element.red_range_high))


# Example render
if __name__ == "__main__":
    example_window = tk.Tk()
    example_data = [0, 1, 2, 3, 4, 5]

    # X-Y-plot example
    x_y_graph = XYPlotGauge(example_window, title='X-Y-Plot', description="Example Text",
                            connect_dots=True)  # element.second_field_name, data_list1, data_list2, element.timestamp_value)
    x_y_graph.grid(row=0, column=2)

    # X-plot example
    x_plot = XPlotGauge(example_window, title='X-plot', description='Example Text')
    x_plot.grid(row=1, column=2)

    # Bar Graph example

    # Circle 90 example

    # Circle 180 example

    # Circle 270 example

    # Circle 360 example

    # Text Display example
    text_gauge = TextDisplayGauge(example_window, title='Text Gauge', description='')
    text_gauge.grid(row=2, column=0, pady=5)

    # Number Display example
    num_gauge = NumberDisplayGauge(example_window, title='Number Gauge', description='')
    num_gauge.grid(row=2, column=1)

    # Clock Example
    clock_gauge = ClockGauge(example_window, title='Current Time', description='Local Time')
    clock_gauge.grid(row=3, column=0)

    # Stopwatch example
    stopwatch_gauge = ClockGauge(example_window, title='Stopwatch', description='Elapsed Time', mode='stopwatch')
    toggle_button = tk.Button(example_window, text="Start/Stop", command=stopwatch_gauge.toggle_stopwatch)
    stopwatch_gauge.grid(row=3, column=1)

    # Running Time example
    running_gauge = ClockGauge(example_window, title='Running Time', description='Video Time', mode='running_time')
    running_gauge.grid(row=3, column=3)

    # Indicator Light example
    indicator_light = LightIndicatorGauge(example_window, title='Example Gauge', description='Insert Text')
    indicator_light.grid(row=2, column=2)

    example_window.mainloop()
