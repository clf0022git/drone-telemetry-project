import json
import os
from src.data.input import *


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
                'data': gauge.data,
                'statistics': gauge.statistics,
                'statistics_two': gauge.statistics_two,
                'statistics_values': gauge.statistics_values,
                'statistics_values_two': gauge.statistics_values_two,
                'statistics': gauge.statistics,
                'blue_range': (gauge.blue_range_low, gauge.blue_range_high),
                'green_range': (gauge.green_range_low, gauge.green_range_high),
                'yellow_range': (gauge.yellow_range_low, gauge.yellow_range_high),
                'red_range': (gauge.red_range_low, gauge.red_range_high),
                'position': gauge.position
            }
            gauge_data.append(data)

        # Save the data to a file
        with open(filename, 'w') as outfile:
            json.dump(gauge_data, outfile, indent=4)

    @staticmethod
    def load_gauges(data_manager, filename="savedGauges.json"):
        # Load data from a file
        with open(filename, 'r') as infile:
            gauge_data = json.load(infile)

        # Deserialize the JSON data back into gauge objects
        gauge_list = []
        for data in gauge_data:
            # Create gauge objects here based on the data
            gauge = TemporaryGauge([data["field_name"]], data["gauge_name"], data["timestamp_value"], data["data"])
            gauge.id = data["id"]
            gauge.name = data["name"]
            gauge.statistics = data["statistics"]
            gauge.statistics_two = data["statistics_two"]
            gauge.statistics_values = data["statistics_values"]
            gauge.statistics_values_two = data["statistics_values_two"]
            gauge.blue_range_low = data["blue_range"][0]
            gauge.blue_range_high = data["blue_range"][1]
            gauge.green_range_low = data["green_range"][0]
            gauge.green_range_high = data["green_range"][1]
            gauge.yellow_range_low = data["yellow_range"][0]
            gauge.yellow_range_high = data["yellow_range"][1]
            gauge.red_range_low = data["red_range"][0]
            gauge.red_range_high = data["red_range"][1]
            gauge.position = data["position"]
            gauge_list.append(gauge)

        data_manager.user_selected_gauges_list = gauge_list
        return gauge_list
