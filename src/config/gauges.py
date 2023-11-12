import numpy as np
from numpy import sin, cos, pi
import plotly.graph_objects as go
import datetime as dt
import datetime as datetime
import tkinter as Tkinter
import tkinter as tk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import style
import matplotlib.animation as animation
from src.data.input import DataManager
from src.config.LightIndicator import of_light

#Manager class for the gauges
class GaugeCreator:
   def __init__(self):
      self.name = "yes"
   def drawGauges(self, data_manager: DataManager):
      for element in data_manager.user_selected_gauges_list:
         for field_name in element.field_name:
            data_list1 = [value for value in data_manager.data_file.get(field_name, [])]
         match element.gauge_name:
            #Case for getting data and drawing the x-by-y plot
            case "X-by-Y-plot":
               data_list2 = []
               if element.second_field_name:
                  data_list2 = [value for value in data_manager.data_file.get(element.second_field_name, [])]
               graph = LineGraph(field_name, element.second_field_name, data_list1, data_list2, element.timestamp_value)
               graph.create_x_by_y_Graph() if data_list2 else graph.create_x_Graph()
            #Case for getting the data and drawing the bar graph
            case "Bar-Graph":
               bar_graph = BarGraph(field_name, data_list1, element.timestamp_value)
               bar_graph.createBarGraph()
            #Case for getting the data and drawing  the 90 degree circle graph
            case "Circle - 90°":
               gauge_circle = circle_gauge(field_name, data_list1, element.timestamp_value)
               fig = gauge_circle.draw_circular_gauge(0, 90, self.name)
               fig.show()
            #Case for getting the data and drawing  the 180 degree circle graph
            case "Circle - 180°":
               gauge_circle = circle_gauge(field_name, data_list1, element.timestamp_value)
               fig = gauge_circle.draw_circular_gauge(0, 90, self.name)
               fig.show()
            #Case for getting the data and drawing  the 270 degree circle graph
            case "Circle - 270°":
               gauge_circle = circle_gauge(field_name, data_list1, element.timestamp_value)
               fig = gauge_circle.draw_circular_gauge(0, 90, self.name)
               fig.show()
            #Case for getting the data and drawing  the 360 degree circle graph
            case "Circle - 360°":
               gauge_circle = circle_gauge(field_name, data_list1, element.timestamp_value)
               fig = gauge_circle.draw_circular_gauge(0, 90, self.name)
               fig.show()
            #Case for getting data and drawing  the text display
            case "Text Display":
               text_display = text_gauge(field_name, data_list1, element.timestamp_value)
            #Case for getting the data and drawing the number/character display
            case "Number or Character Display":
               nc_gauge = text_gauge(field_name, data_list1, element.timestamp_value)
            #Case for drawing the clock
            case "Clock":
               text = "insert"
            #Case for drawing the stopwatch
            case "Stopwatch":
               text = "insert"
            #Case for drawing the running time gauge
            case "Running Time":
               text = "insert"
            #Case for drawing the on/off light
            case "On/off light":
               of_gauge = of_light(field_name, data_list1)
            case _:
               print("Gauge not found")

   def animate(self):
      token = 4
#This class contains all the functions for producing a line graph
class LineGraph:
   def __init__(self, fieldName1, fieldName2, dataSet1, dataSet2, time_inc):
      self.name = fieldName1        #Name of the first data field being used
      self.name2 = fieldName2       #Name of the second data field being used
      self.dataSet1 = dataSet1            #data field that will make up the y-values of the graph
      self.dataSet2 = dataSet2           #data field that will make up the x-values of the graph
      self.time = [0]               #Establish start time for animated graph
      self.update_time = time_inc   #Update value for the time array
      self.update_inc = 0
      self.update_data1 = dataSet1  #Used to append data to dataSet1 for animation
      if (len(dataSet2) == 0):
         self.dataSet2 = self.time
      else:
         self.update_data2 = dataSet2  # Used to append data to dataSet1 for animation

   #Function for drawing the base version of the graph
   #Can be used for x-graphs and x-by-y graphs
   def create_x_by_y_Graph(self):
      fig = plt.figure()
      ax1 = fig.add_subplot(1, 1, 1)
      ax1.plot(self.dataSet2, self.dataSet1, marker='o', color='blue')
      plt.xlabel(self.name2)
      plt.ylabel(self.name)
      plt.title(self.name + " over " + self.name2)
      plt.show()

   def create_x_Graph(self):
      fig = plt.figure()
      ax1 = fig.add_subplot(1, 1, 1)
      ax1.plot(self.dataSet2, self.dataSet1, marker='o', color='blue')
      plt.xlabel("Time")
      plt.ylabel(self.name)
      plt.title(self.name + " over time")
      plt.show()

   def animate_graph(self, graph, time):
      self.time.append(self.update_time + self.time[self.update_inc])
      self.dataSet1.append(self.update_data1[self.update_inc])
      if (self.time[self.update_inc] % time == 0):
         self.dataSet2.append(self.time[self.update_inc])
      else:
         self.dataSet2.append(self.update_data2[self.update_inc])
      self.update_inc = self.update_inc + 1
      graph.clear()
      graph.plot(self.time, self.data)

      # Format plot
      plt.title(self.name + ' over ' + self.name2)
      plt.ylabel(self.name)
      plt.xlabel(self.name2)
   #ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
   #Example of command used to call animation function that will redraw the graph with new data

#This class contains all the functions for producing a bar graph
class BarGraph:
   def __init__(self, name, data, time_inc):
      self.name = name  # Name of the data metric being used
      self.data = []  # Data is the array of values for a data metric (column of values) combed from the csv file
      self.time = [0]  # Establish start time for animated graph
      self.update_time = time_inc
      self.update_data = data
      self.update_inc = 0

   #This will create an empty bar graph
   def createBarGraph(self):
      '''fig = plt.bar(self.name, self.data, color='blue')
      ax = fig.add_subplot(1,1,1)
      plt.title(self.name + ' over time')
      plt.ylabel(self.name)
      plt.xlabel("Time")
      plt.show()'''
      fig = plt.figure()
      plt.bar(self.name, self.data, color='blue')
      plt.xlabel(self.name)
      plt.title(self.name)
      plt.show()

   def animate_graph(self, ax):
      self.data.append(self.update_data[self.update_inc])
      self.time.append(self.update_time + self.time[self.update_inc])
      self.update_inc = self.update_inc + 1
      ax.clear()
      ax.plot(self.time, self.data)

      # Format plot
      plt.title(self.name + ' over time')
      plt.ylabel(self.name)
      self.time = self.time + self.update_time

#This class contains everything for creating a text display gauge. This can also be used for number or single digit display
class text_gauge:
   def __init__(self, name, data, time_inc, window):
      self.name = name  # Name of the data metric being used
      self.dataField = []  # Data is the array of values for a data metric (column of values) combed from the csv file
      self.start_time = 0  # Establish start time for animated graph
      self.updateData = data
      self.updateTime = time_inc
      self.inc = 0
      self.window = window
   def create_display(self):
      textDisplay = tk.Label(
         self.window,
         text = self.dataField[self.inc],
         fg="white",
         bg="black",
         width=10,
         height=10
      )
   def updateDisplay(self, time):
      if (time % self.updateTime == 0):
         self.dataField.append(self.updateData[self.inc])
         self.inc += 1

#This class will create a customizable circle gauge
class circle_gauge:
   def __init__(self, name, data, time_inc):
      self.name = name  # Name of the data metric being used
      self.data = []  # Data is the array of values for a data metric (column of values) combed from the csv file
      self.time = [0]  # Establish start time for animated graph
      self.update_time = time_inc
      self.update_data = data
      self.update_inc = 0
      self.max = max

   def degree_to_radian(self, degrees):
      return degrees * pi / 180

   def draw_circular_gauge(self, degree_start, degree_end, annotation_text, r=1.0, padding=0.2, tick_length=0.02):
      radian_start, radian_end = self.degree_to_radian(degree_start), self.degree_to_radian(degree_end)
      theta = np.linspace(radian_start, radian_end, 5000)
      x = r * cos(theta)
      y = r * sin(theta)
      fig = go.Figure()

      # draw the bar
      fig.add_trace(go.Scatter(
         x=x, y=y, mode='markers', marker_symbol='circle', marker_size=15, hoverinfo='skip'
      ))

      # draw the outer border
      for r_outer in [r - padding, r + padding]:
         fig.add_shape(type="circle",
                       xref="x", yref="y",
                       x0=-r_outer, y0=-r_outer, x1=r_outer, y1=r_outer,
                       line_color="black",
                       )

      tick_theta = np.linspace(pi, -pi, 13)
      tick_labels = np.linspace(0, 330, 12)
      tick_start_x, tick_end_x = (r + padding) * cos(tick_theta), (r + padding + tick_length) * cos(tick_theta)
      tick_start_y, tick_end_y = (r + padding) * sin(tick_theta), (r + padding + tick_length) * sin(tick_theta)
      tick_label_x, tick_label_y = (r + padding + 0.04 + tick_length) * cos(tick_theta), (
                 r + padding + 0.04 + tick_length) * sin(tick_theta)

      # add ticks
      for i in range(len(tick_theta)):
         fig.add_trace(go.Scatter(
            x=[tick_start_x[i], tick_end_x[i]],
            y=[tick_start_y[i], tick_end_y[i]],
            mode='text+lines',
            marker=dict(color="black"),
            hoverinfo='skip'
         ))

      # add ticklabels
      fig.add_trace(go.Scatter(
         x=tick_label_x,
         y=tick_label_y,
         text=tick_labels,
         mode='text',
         hoverinfo='skip'
      ))

      ## add text in the center of the plot
      fig.add_trace(go.Scatter(
         x=[0], y=[0],
         mode="text",
         text=[annotation_text],
         textfont=dict(size=30),
         textposition="middle center",
         hoverinfo='skip'
      ))

      ## get rid of axes, ticks, background
      fig.update_layout(
         showlegend=False,
         xaxis_range=[-1.5, 1.5], yaxis_range=[-1.5, 1.5],
         xaxis_visible=False, xaxis_showticklabels=False,
         yaxis_visible=False, yaxis_showticklabels=False,
         template="plotly_white",
         width=800, height=800
      )
      return fig

   #fig = draw_circular_gauge(180, -120, "300")
   #fig.show()

#This class will create a stopwatch
class stopWatch:
   def __init__(self, name, data, frame):
      self.name = name  # Name of the data metric being used
      self.data = []  # Data is the array of values for a data metric (column of values) combed from the csv file
      self.frame = frame

   counter = 66600
   running = False

   '''def counter_label(label):
      def count():
         if running:
            global counter

            # To manage the initial delay.
            if counter == 66600:
               display = "Starting..."
            else:
               tt = datetime.fromtimestamp(counter)
               string = tt.strftime("%H:%M:%S")
               display = string

            label['text'] = display  # Or label.config(text=display)

            # label.after(arg1, arg2) delays by
            # first argument given in milliseconds
            # and then calls the function given as second argument.
            # Generally like here we need to call the
            # function in which it is present repeatedly.
            # Delays by 1000ms=1 seconds and call count again.
            label.after(1000, count)
            counter += 1

      # Triggering the start of the counter.
      count()

      # start function of the stopwatch

   def Start(self, label):
      global running
      running = True
      self.counter_label(label)
      start['state'] = 'disabled'
      stop['state'] = 'normal'
      reset['state'] = 'normal'

   # Stop function of the stopwatch
   def Stop(self):
      global running
      start['state'] = 'normal'
      stop['state'] = 'disabled'
      reset['state'] = 'normal'
      running = False

   # Reset function of the stopwatch
   def Reset(label):
      global counter
      counter = 66600

      # If rest is pressed after pressing stop.
      if running == False:
         reset['state'] = 'disabled'
         label['text'] = 'Welcome!'

      # If reset is pressed while the stopwatch is running.
      else:
         label['text'] = 'Starting...'

   def createStopWatch(self):
      self.frame.minsize(width=250, height=70)
      label = Tkinter.Label(self.frame, text="Stopwatch", fg="black", font="Verdana 30 bold")
      label.pack()
      f = Tkinter.Frame(self.frame)
      start = Tkinter.Button(f, text='Start', width=6, command=lambda: Start(label))
      stop = Tkinter.Button(f, text='Stop', width=6, state='disabled', command=Stop)
      reset = Tkinter.Button(f, text='Reset', width=6, state='disabled', command=lambda: Reset(label))
      f.pack(anchor='center', pady=5)
      start.pack(side="left")
      stop.pack(side="left")
      reset.pack(side="left")
      self.frame.mainloop()'''