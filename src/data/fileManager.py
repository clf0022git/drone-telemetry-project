from src.config.NumberDisplayGauge import NumberDisplayGauge
from src.config.XYPlotGauge import XYPlotGauge
import json
import os


class FileManager:

    @staticmethod
    def save_gauges(gauge_list, filename="savedGauges.json"):
        # Prepare the data for JSON serialization
        gauge_data = []
        for gauge in gauge_list:
            data = {
                'id': gauge.id,
                'field_name': gauge.field_name[0],
                'second_field_name': gauge.second_field_name,
                'gauge_name': gauge.gauge_name,
                'timestamp_value': gauge.timestamp_value,
                'name': gauge.name,
                'statistics': gauge.statistics,
                'blue_range': (gauge.blue_range_low, gauge.blue_range_high),
                'green_range': (gauge.green_range_low, gauge.green_range_high),
                'yellow_range': (gauge.yellow_range_low, gauge.yellow_range_high),
                'red_range': (gauge.red_range_low, gauge.red_range_high)
            }
            gauge_data.append(data)

        # Save the data to a file
        with open(filename, 'w') as outfile:
            json.dump(gauge_data, outfile, indent=4)

    @staticmethod
    def load_gauges(master, data_manager, filename="savedGauges.json"):
        # Load data from a file
        with open(filename, 'r') as infile:
            gauge_data = json.load(infile)

        # Deserialize the JSON data back into gauge objects
        gauge_list = []
        for data in gauge_data:
            pass
            #  Create gauge objects here based on the data
            # if data.gauge_name == 'X-by-Y-plot':
            #     gauge = XYPlotGauge(master)
            # elif data.gauge_name == 'Number or Character Display':
            #     gauge = NumberDisplayGauge(master)
            #gauge_list.append(gauge)

        return gauge_list
