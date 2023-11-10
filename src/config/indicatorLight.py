
#This class will create an on/off light
class of_light:
   def __init__(self, name, data, min, median, max,frame):
      self.name = name  # Name of the data metric being used
      self.data = []  # Data is the array of values for a data metric (column of values) combed from the csv file
      self.frame = frame
      self.min = min
      self.max = max
      self.median = median

   #This function will spawn the light
   def create_light(self):
      for elements in self.data:
         data_label = self.name + "\n".format(elements)
         if elements < self.median:
            self.frame.itemconfig(my_oval, fill="red")  # Fill the circle with RED