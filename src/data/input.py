# Planned functionality of handling functions related to the data input
import pandas as pd


class DataManager:
    def __init__(self):
        self.datafile = None

    def identify_gauges(self, datatype) -> list:
        """Use an if else tree to determine the kind of gauges for a specific type of data"""
