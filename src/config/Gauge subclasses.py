import numpy as np
import datetime as dt
import tkinter as tk
import tk_tools
from matplotlib import pyplot as plt
from matplotlib import style
import matplotlib.animation as animation
import panel as pn
pn.extension('echarts')
#class GaugeCreator:

#This class contains all the functions for producing a line graph
class LineGraph:
   def __init__(self, name, data, time_inc):
      self.name = name        #Name of the data metric being used
      self.data = []         #Data is the array of values for a data metric (column of values) combed from the csv file
      self.time = [0]         #Establish start time for animated graph
      self.update_time = time_inc
      self.update_data = data
      self.update_inc = 0

   #Function for drawing the base version of the graph
   #Can be used for x-graphs and x-by-y graphs
   def createlineGraph(self):
      style.use('ggplot')
      #plt.plot(self.start_time, self.data, linewidth=5)
      plt.title(self.name + ' over time')
      fig = plt.figure()
      ax = fig.add_subplot(0, 0, 0)
      plt.ylabel(self.name)
      plt.xlabel("Time")
      plt.show()
   def animate_graph(self, ax):
      self.data.append(self.update_data[self.update_inc])
      self.time.append(self.update_time + self.time[self.update_inc])
      self.update_inc = self.update_inc + 1
      ax.clear()
      ax.plot(self.time, self.data)

      # Format plot
      plt.xticks(rotation=45, ha='right')
      plt.subplots_adjust(bottom=0.30)
      plt.title(self.name + ' over time')
      plt.ylabel(self.name)
      self.time = self.time + self.update_time
   #ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
   #Example of command used to call animation function that will redraw the graph with new data

#This class contains all the functions for producing a bar graph
class BarGraph:
   def __init__(self, name, data, time_inc):
      self.name = name  # Name of the data metric being used
      self.data = [0]  # Data is the array of values for a data metric (column of values) combed from the csv file
      self.time = [0]  # Establish start time for animated graph
      self.update_time = time_inc
      self.update_data = data
      self.update_inc = 0

   #This will create an empty bar graph
   def createBarGraph(self):
      fig = plt.bar(self.name, self.data, color='blue')
      ax = fig.add_subplot(1,1,1)
      plt.title(self.name + ' over time')
      plt.ylabel(self.name)
      plt.xlabel("Time")
      plt.show()

   def animate_graph(self, ax):
      self.data.append(self.update_data[self.update_inc])
      self.time.append(self.update_time + self.time[self.update_inc])
      self.update_inc = self.update_inc + 1
      ax.clear()
      ax.plot(self.time, self.data)

      # Format plot
      plt.xticks(rotation=45, ha='right')
      plt.subplots_adjust(bottom=0.30)
      plt.title(self.name + ' over time')
      plt.ylabel(self.name)
      self.time = self.time + self.update_time

#This class contains everything for creating a text display gauge. This can also be used for number or single digit display
class text_gauge:
   def __init__(self, name, data, time_inc):
      self.name = name  # Name of the data metric being used
      self.data = data  # Data is the array of values for a data metric (column of values) combed from the csv file
      self.start_time = 0  # Establish start time for animated graph
      self.update = time_inc
   def create_display(self):
      #self.display = self.canvas.
      label = tk.Label(
         text = self.data,
         fg="white",
         bg="black",
         width=10,
         height=10
      )

#This class will create an on/off light
class OF_light:
   def __init__(self, name, data, frame):
      self.name = name  # Name of the data metric being used
      self.data = []  # Data is the array of values for a data metric (column of values) combed from the csv file
      self.frame = frame

   #This function will spawn the light
   def create_light(self):
      led = tk_tools.Led(self.frame, size=50)
      led.pack()

      led.to_red()
      led.to_green(on=True)

#This class will create a customizable circle gauge
class circle_gauge:
   def __init__(self, name, data, metric, max, time_inc, low_bound, mid_bound, up_bound, lb_color, mb_color, ub_color):
      self.name = name  # Name of the data metric being used
      self.data = []  # Data is the array of values for a data metric (column of values) combed from the csv file
      self.time = [0]  # Establish start time for animated graph
      self.dtype = metric
      self.update_time = time_inc
      self.update_data = data
      self.update_inc = 0
      self.max = max
      self.lower_bound = low_bound     #User defined lower bound value
      self.middle_bound = mid_bound    #User defined middle bound value
      self.upper_bound = up_bound      #User defined upper bound value
      self.lb_color = lb_color         #User defined lower bound color
      self.mb_color = mb_color         #User defined middle bound color
      self.ub_color = ub_color         #User defined upper bound color
   def create_cGauge(self):
      pn.indicators.Gauge(name = self.name, bounds = (0, self.max), format='{value} ' + self.dtype,  colors = [(self.lower_bound, self.lb_color), (self.middle_bound, self.mb_color), (self.upper_bound, self.ub_color)])