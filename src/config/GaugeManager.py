#File imports
from src.config.BarGauge import BarGauge
from src.config.CircleGauge import CircleGauge
from src.config.ClockDisplayGauge import ClockGauge
from src.config.LightIndicatorGauge import LightIndicatorGauge
from src.config.NumberDisplayGauge import NumberDisplayGauge
from src.config.TextDisplayGauge import TextDisplayGauge
from src.config.XPlotGauge import XPlotGauge
from src.config.XYPlotGauge import XYPlotGauge
from src.data.input import DataManager

#Library imports
import tkinter as tk

# Manager class for the gauges
class GaugeManager:
    #Initialization function
    def __init__(self):
        self.name = None
        #self.render_window = GaugeWindow()
        self.gauge_container = []

        #Variables for instantiating each of the gauges
        self.x_y_graph = None
        self.x_plot = None
        self.bar_graph = None
        self.circle_gauge_90 = None
        self.circle_gauge_180 = None
        self.circle_gauge_270 = None
        self.circle_gauge_360 = None
        self.text_gauge = None
        self.num_gauge = None
        self.clock_gauge = None
        self.stopwatch_gauge = None
        self.running_gauge = None
        self.indicator_light = None

        #List containers for each of the gauges' data sets
        self.x_axis_list = []
        self.y_axis_list = []
        self.x_plot_list = []
        self.bar_graph_list = []
        self.circle_gauge_90_list = []
        self.circle_gauge_180_list = []
        self.circle_gauge_270_list = []
        self.circle_gauge_360_list = []
        self.text_gauge_list= []
        self.num_gauge_list = []
        self.clock_gauge_list = []
        self.stopwatch_gauge_list = []
        self.running_gauge_list = []
        self.indicator_light_list = []

        #Alarm values
        self.x_y_alarm = None
        self.x_alarm = None
        self.bar_alarm = None
        self.circle_alarm_90 = None
        self.circle_alarm_180 = None
        self.circle_alarm_270 = None
        self.circle_alarm_360 = None
        self.text_alarm = None
        self.num_alarm = None
        self.clock_alarm = None
        self.stopwatch_alarm = None
        self.running_alarm = None
        self.indicator_alarm = None

        #Increment for animation
        self.anim_inc = 0

    #Function for drawing each of the functions out
    def drawGauges(self, data_manager: DataManager):
        for element in data_manager.user_selected_gauges_list:
            for field_name in element.field_name:
                data_list1 = [value for value in data_manager.data_file.get(field_name, [])]

            match element.gauge_name:

                # Case for getting data and drawing the x-by-y plot
                case "X-by-Y-plot":
                    for counter, in counter.second_field_namefield_name:
                        data_list2 = [value for value in data_manager.data_file.get(element.second_field_name, [])]
                    self.x_y_graph = XYPlotGauge(self.render_window, title= element.field_name, description= element.field_name, connect_dots=True) #element.second_field_name, data_list1, data_list2, element.timestamp_value)
                    #self.x_y_graph.update_colors()
                    self.x_y_graph.grid(row = 0, column = 2)
                    self.x_axis_list = data_list1.copy()
                    self._list = data_list2.copy()

                #Case for getting the data and drawing the x-graph
                case "X-Plot":
                    self.x_plot = XPlotGauge(self.render_window, title= 'X-plot', description= 'Example Text')
                    self.x_plot.grid(row = 1, column = 2)
                    self.x_plot_list = data_list1.copy()

                # Case for getting the data and drawing the bar graph
                case "Bar-Graph":
                    self.bar_graph = BarGauge(element.field_name[0], element.timestamp_value)
                    self.bar_graph_list = data_list1.copy()

                # Case for getting the data and drawing the 90 degree circle graph
                case "Circle - 90°":
                    self.circle_gauge_90 = CircleGauge(element.field_name[0], element.timestamp_value)
                    self.circle_gauge_90.grid(row = 0, column = 0)
                    self.circle_gauge_90_list = data_list1.copy()

                # Case for getting the data and drawing the 180 degree circle graph
                case "Circle - 180°":
                    self.circle_gauge_180 = CircleGauge(element.field_name[0], element.timestamp_value)
                    self.circle_gauge_180.grid(row=0, column=1)
                    self.circle_gauge_180_list = data_list1.copy()

                # Case for getting the data and drawing the 270 degree circle graph
                case "Circle - 270°":
                    self.circle_gauge_270 = CircleGauge(element.field_name[0], element.timestamp_value)
                    self.circle_gauge_270.grid(row = 1, column = 0)
                    self.circle_gauge_270_list = data_list1.copy()

                # Case for getting the data and drawing the 360 degree circle graph
                case "Circle - 360°":
                    # circle_window = GaugeWindow()
                    self.circle_gauge_360 = CircleGauge(element.field_name[0], element.timestamp_value)
                    self.circle_gauge_360.grid(row = 1, column = 1)
                    self.circle_gauge_360_list = data_list1.copy()

                # Case for getting data and drawing the text display
                case "Text Display":
                    self.text_gauge = TextDisplayGauge(self.render_window, name = element.field_name, title = element.field_name, description = '')
                    self.text_gauge.grid(row = 2, column = 0, pady = 5)
                    self.text_gauge_list = data_list1.copy()

                # Case for getting the data and drawing the number/character display
                case "Number or Character Display":
                    self.num_gauge = NumberDisplayGauge(self.render_window, title = element.field_name, description = element.field_name)
                    self.num_gauge.grid(row = 2, column = 1)
                    self.num_gauge_list = data_list1.copy()

                # Case for drawing the clock
                case "Clock":
                    self.clock_gauge = ClockGauge(self.render_window, title='Current Time', description='Local Time')
                    self.clock_gauge.grid(row = 3, column = 0)
                    self.clock_gauge_list = data_list1.copy()

                # Case for drawing the stopwatch
                case "Stopwatch":
                    self.stopwatch_gauge = ClockGauge(self.render_window, title='Stopwatch', description='Elapsed Time', mode='stopwatch')
                    toggle_button = tk.Button(self.render_window, text="Start/Stop", command=stopwatch_gauge.toggle_stopwatch)
                    self.stopwatch_gauge.grid(row = 3, column = 1)
                    self.stopwatch_gauge_list = data_list1.copy()

                # Case for drawing the running time gauge
                case "Running Time":
                    self.running_gauge = ClockGauge(self.render_window, title='Running Time', description='Video Time', mode='running_time')
                    self.running_gauge.grid(row = 3, column = 3)
                    self.running_gauge_list = data_list1.copy()

                # Case for drawing the on/off light
                case "On/off light":
                    self.indicator_light = LightIndicatorGauge(self.render_window, title='', description='')
                    self.indicator_light.grid(row = 2, column = 2)
                    self.indicator_light_list = data_list1.copy()
                #Default case
                case _:
                    print("Gauge not found")


    #This function will call each of the animation functions for the displayed gauges
    def animateGauges(self, data_manager: DataManager):
        token = 3
        for token in data_manager.user_selected_gauges_list:
            for field_name in token.field_name:

                match token.gauge_name:

                    # Case for animating the x-by-y plot
                    case "X-by-Y-plot":
                        self.x_y_graph.update_value(self.x_axis_list[self.anim_inc], self.y_axis_list[self.anim_inc], self.x_y_alarm)

                    # Case for animating the x-graph
                    case "X-Plot":
                        self.x_plot.update_value(self.x_plot_list[self.anim_inc])

                    # Case for animating the bar graph
                    case "Bar-Graph":
                        self.bar_graph.update_value(self.bar_graph_list[self.anim_inc])

                    # Case for animating the 90 degree circle graph
                    case "Circle - 90°":
                        self.circle_gauge_90.update_value(self.circle_gauge_90_list[self.anim_inc])

                    # Case for animating the 180 degree circle graph
                    case "Circle - 180°":
                        self.circle_gauge_180.update_value(self.circle_gauge_180_list[self.anim_inc])

                    # Case for animating the 270 degree circle graph
                    case "Circle - 270°":
                        self.circle_gauge_270.update_value(self.circle_gauge_270_list[self.anim_inc])

                    # Case for animating the 360 degree circle graph
                    case "Circle - 360°":
                        # circle_window = GaugeWindow()
                        self.circle_gauge_360.update_value(self.circle_gauge_360_list[self.anim_inc])

                    # Case for animating the text display
                    case "Text Display":
                        self.text_gauge.update_value(self.text_gauge_list[self.anim_inc])

                    # Case for animating the number/character display
                    case "Number or Character Display":
                        self.num_gauge.update_value(self.num_gauge_list[self.anim_inc])

                    # Case for animating the clock
                    case "Clock":
                        self.clock_gauge.update_value()

                    # Case for animating the stopwatch
                    case "Stopwatch":
                        self.stopwatch_gauge.update_value()

                    # Case for animating the running time gauge
                    case "Running Time":
                        self.running_gauge.update_value()

                    # Case for animating the on/off light
                    case "On/off light":
                        self.indicator_light.update_value(self.indicator_light_list[self.anim_inc])

                    # Default case
                    case _:
                        print("Gauge not found")

    #This function will update the color ranges for each of the gauges
    def update_Ranges(self, data_manager: DataManager):
        for token in data_manager.user_selected_gauges_list:
            for field_name in token.field_name:

                match token.gauge_name:

                    # Case for changing the color ranges of the X-by-Y-plot
                    case "X-by-Y-plot":
                        self.x_y_graph.update_colors()

                    # Case for changing the color ranges of the x-graph
                    case "X-Plot":
                        self.x_plot.update_colors()

                    # Case for changing the color ranges of the bar graph
                    case "Bar-Graph":
                        self.bar_graph.update_colors()

                    # Case for changing the color ranges of the 90 degree circle graph
                    case "Circle - 90°":
                        self.circle_gauge_90.update_colors()

                    # Case for changing the color ranges of the 180 degree circle graph
                    case "Circle - 180°":
                        self.circle_gauge_180.update_colors()

                    # Case for changing the color ranges of the 270 degree circle graph
                    case "Circle - 270°":
                        self.circle_gauge_270.update_colors()

                    # Case for changing the color ranges of the 360 degree circle graph
                    case "Circle - 360°":
                        # circle_window = GaugeWindow()
                        self.circle_gauge_360.update_colors()

                    # Case for changing the color ranges of the text display
                    case "Text Display":
                        self.text_gauge.update_colors()

                    # Case for changing the color ranges of the number/character display
                    case "Number or Character Display":
                        self.num_gauge.update_colors()

                    # Case for changing the color ranges of the clock
                    case "Clock":
                        self.clock_gauge.update_colors()

                    # Case for changing the color ranges of the stopwatch
                    case "Stopwatch":
                        self.stopwatch_gauge.update_colors()

                    # Case for changing the color ranges of the running time gauge
                    case "Running Time":
                        self.running_gauge.update_colors()

                    # Case for changing the color ranges of the on/off light
                    case "On/off light":
                        self.indicator_light.update_colors()

                    # Default case
                    case _:
                        print("Gauge not found")

class GaugeWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        # Window properties
        self.title("Telemetry Data Gauges")
        self.geometry("500x500")
        self.configure(bg="white")

#Example render
if __name__ == "__main__":
    example_window = tk.Tk()
    example_data = [0, 1 ,2, 3, 4, 5]

    #X-Y-plot example
    x_y_graph = XYPlotGauge(example_window, title= 'X-Y-Plot', description= "Example Text", connect_dots=True) #element.second_field_name, data_list1, data_list2, element.timestamp_value)
    x_y_graph.grid(row = 0, column = 2)

    #X-plot example
    x_plot = XPlotGauge(example_window, title= 'X-plot', description= 'Example Text')
    x_plot.grid(row = 1, column = 2)

    #Bar Graph example

    #Circle 90 example

    #Circle 180 example

    #Circle 270 example

    #Circle 360 example

    #Text Display example
    text_gauge = TextDisplayGauge(example_window, title = 'Text Gauge', description = '')
    text_gauge.grid(row = 2, column = 0, pady = 5)

    #Number Display example
    num_gauge = NumberDisplayGauge(example_window, title = 'Number Gauge', description = '')
    num_gauge.grid(row = 2, column = 1)

    #Clock Example
    clock_gauge = ClockGauge(example_window, title='Current Time', description='Local Time')
    clock_gauge.grid(row = 3, column = 0)

    #Stopwatch example
    stopwatch_gauge = ClockGauge(example_window, title='Stopwatch', description='Elapsed Time', mode='stopwatch')
    toggle_button = tk.Button(example_window, text="Start/Stop", command=stopwatch_gauge.toggle_stopwatch)
    stopwatch_gauge.grid(row = 3, column = 1)

    #Running Time example
    running_gauge = ClockGauge(example_window, title='Running Time', description='Video Time', mode='running_time')
    running_gauge.grid(row = 3, column = 3)

    #Indicator Light example
    indicator_light = LightIndicatorGauge(example_window, title='Example Gauge', description='Insert Text')
    indicator_light.grid(row = 2, column = 2)

    example_window.mainloop()
