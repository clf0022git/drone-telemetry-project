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
        self.render_window = GaugeWindow()
        self.gauge_container = []

        #List containers for each of the
        self.x_y_graph = []
        self.x_plot = []
        self.bar_graph = []
        self.circle_gauge_90 = []
        self.circle_gauge_180 = []
        self.circle_gauge_270 = []
        self.circle_gauge_360 = []
        self.text_gauge = []
        self.num_gauge = []
        self.clock_gauge = []
        self.stopwatch_gauge = []
        self.running_gauge = []
        self.indicator_light = []

    #Function for drawing each of the functions out
    def drawGauges(self, data_manager: DataManager):
        for element in data_manager.user_selected_gauges_list:
            for field_name in element.field_name:
                data_list1 = [value for value in data_manager.data_file.get(field_name, [])]

            match element.gauge_name:

                # Case for getting data and drawing the x-by-y plot
                case "X-by-Y-plot":
                    data_list2 = [value for value in data_manager.data_file.get(element.second_field_name, [])]
                    x_y_graph = XYPlotGauge(self.render_window, title= element.field_name, description= element.field_name, connect_dots=True) #element.second_field_name, data_list1, data_list2, element.timestamp_value)
                    x_y_graph.grid(row = 0, column = 2)
                    #x_y_graph.create_x_by_y_Graph()

                #Case for getting the data and drawing the x-graph
                case "X-Plot":
                    x_plot = XPlotGauge(self.render_window, title= 'X-plot', description= 'Example Text')
                    x_plot.grid(row = 1, column = 2)
                    #x_plot.create_x_graph()

                # Case for getting the data and drawing the bar graph
                case "Bar-Graph":
                    bar_graph = BarGauge(element.field_name[0], data_list1, element.timestamp_value)

                # Case for getting the data and drawing  the 90 degree circle graph
                case "Circle - 90°":
                    circle_gauge_90 = CircleGauge(element.field_name[0], data_list1, element.timestamp_value)
                    circle_gauge_90.grid(row = 0, column = 0)

                # Case for getting the data and drawing  the 180 degree circle graph
                case "Circle - 180°":
                    circle_gauge_180 = CircleGauge(element.field_name[0], data_list1, element.timestamp_value)
                    circle_gauge_180.grid(row=0, column=1)

                # Case for getting the data and drawing  the 270 degree circle graph
                case "Circle - 270°":
                    circle_gauge_270 = CircleGauge(element.field_name[0], data_list1, element.timestamp_value)
                    circle_gauge_270.grid(row = 1, column = 0)

                # Case for getting the data and drawing  the 360 degree circle graph
                case "Circle - 360°":
                    # circle_window = GaugeWindow()
                    circle_gauge_360 = CircleGauge(element.field_name[0], data_list1, element.timestamp_value)
                    circle_gauge_360.grid(row = 1, column = 1)

                # Case for getting data and drawing  the text display
                case "Text Display":
                    text_gauge = TextDisplayGauge(self.render_window, name = element.field_name, title = element.field_name, description = '')
                    text_gauge.grid(row = 2, column = 0, pady = 5)

                # Case for getting the data and drawing the number/character display
                case "Number or Character Display":
                    num_gauge = NumberDisplayGauge(self.render_window, title = element.field_name, description = element.field_name)
                    num_gauge.grid(row = 2, column = 1)

                # Case for drawing the clock
                case "Clock":
                    clock_gauge = ClockGauge(self.render_window, title='Current Time', description='Local Time')
                    clock_gauge.grid(row = 3, column = 0)

                # Case for drawing the stopwatch
                case "Stopwatch":
                    stopwatch_gauge = ClockGauge(self.render_window, title='Stopwatch', description='Elapsed Time', mode='stopwatch')
                    toggle_button = tk.Button(self.render_window, text="Start/Stop", command=stopwatch_gauge.toggle_stopwatch)
                    stopwatch_gauge.grid(row = 3, column = 1)

                # Case for drawing the running time gauge
                case "Running Time":
                    running_gauge = ClockGauge(self.render_window, title='Running Time', description='Video Time', mode='running_time')
                    running_gauge.grid(row = 3, column = 3)

                # Case for drawing the on/off light
                case "On/off light":
                    indicator_light = LightIndicatorGauge(self.render_window, data_list1, title='', description='')
                    indicator_light.grid(row = 2, column = 2)
                #Default case
                case _:
                    print("Gauge not found")


    #This function will call each of the animation functions for the displayed gauges
    '''def animateGauges(self, data_manager: DataManager):
        token = 3
        for token in data_manager.user_selected_gauges_list:
            for field_name in token.field_name:

                match token.gauge_name:

                    # Case for getting data and drawing the x-by-y plot
                    case "X-by-Y-plot":
                        data_list2 = [value for value in data_manager.data_file.get(element.second_field_name, [])]
                        x_y_graph = XYPlotGauge(self.render_window, title=element.field_name, description=element.field_name, connect_dots=True)  # element.second_field_name, data_list1, data_list2, element.timestamp_value)
                        x_y_graph.grid(row=0, column=2)
                        # x_y_graph.create_x_by_y_Graph()

                    # Case for getting the data and drawing the x-graph
                    case "X-Plot":
                        x_plot = XPlotGauge(self.render_window, title='X-plot', description='Example Text')
                        x_plot.grid(row=1, column=2)
                        # x_plot.create_x_graph()

                    # Case for getting the data and drawing the bar graph
                    case "Bar-Graph":
                        bar_graph = BarGauge(element.field_name[0], data_list1, element.timestamp_value)

                    # Case for getting the data and drawing  the 90 degree circle graph
                    case "Circle - 90°":
                        circle_gauge_90 = CircleGauge(element.field_name[0], data_list1, element.timestamp_value)
                        circle_gauge_90.grid(row=0, column=0)

                    # Case for getting the data and drawing  the 180 degree circle graph
                    case "Circle - 180°":
                        circle_gauge_180 = CircleGauge(element.field_name[0], data_list1, element.timestamp_value)
                        circle_gauge_180.grid(row=0, column=1)

                    # Case for getting the data and drawing  the 270 degree circle graph
                    case "Circle - 270°":
                        circle_gauge_270 = CircleGauge(element.field_name[0], data_list1, element.timestamp_value)
                        circle_gauge_270.grid(row=1, column=0)

                    # Case for getting the data and drawing  the 360 degree circle graph
                    case "Circle - 360°":
                        # circle_window = GaugeWindow()
                        circle_gauge_360 = CircleGauge(element.field_name[0], data_list1, element.timestamp_value)
                        circle_gauge_360.grid(row=1, column=1)

                    # Case for getting data and drawing  the text display
                    case "Text Display":
                        text_gauge = TextDisplayGauge(self.render_window, name=element.field_name,
                                                      title=element.field_name, description='')
                        text_gauge.grid(row=2, column=0, pady=5)

                    # Case for getting the data and drawing the number/character display
                    case "Number or Character Display":
                        num_gauge = NumberDisplayGauge(self.render_window, title=element.field_name,
                                                       description=element.field_name)
                        num_gauge.grid(row=2, column=1)

                    # Case for drawing the clock
                    case "Clock":
                        clock_gauge = ClockGauge(self.render_window, title='Current Time', description='Local Time')
                        clock_gauge.grid(row=3, column=0)

                    # Case for drawing the stopwatch
                    case "Stopwatch":
                        stopwatch_gauge = ClockGauge(self.render_window, title='Stopwatch', description='Elapsed Time',
                                                     mode='stopwatch')
                        toggle_button = tk.Button(self.render_window, text="Start/Stop",
                                                  command=stopwatch_gauge.toggle_stopwatch)
                        stopwatch_gauge.grid(row=3, column=1)

                    # Case for drawing the running time gauge
                    case "Running Time":
                        running_gauge = ClockGauge(self.render_window, title='Running Time', description='Video Time',
                                                   mode='running_time')
                        running_gauge.grid(row=3, column=3)

                    # Case for drawing the on/off light
                    case "On/off light":
                        indicator_light = LightIndicatorGauge(self.render_window, data_list1, title='', description='')
                        indicator_light.grid(row=2, column=2)
                    # Default case
                    case _:
                        print("Gauge not found")'''

class GaugeWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        # Window properties
        self.title("Telemetry Data Gauges")
        self.geometry("500x500")
        self.configure(bg="white")

#Example render
example_window = GaugeWindow()
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