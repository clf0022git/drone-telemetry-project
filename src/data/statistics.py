import math
from tkinter import filedialog


class DataProcessor:

    @staticmethod
    def calc_statistics(field, field_name, file):
        """Calculate statistics for the given data."""
        my_data = []

        for data in field:
            if not math.isnan(data):
                my_data.append(data)

        if not my_data or math.isnan(min(my_data)):
            output_file = open(file, "a")
            output_file.write(f"{field_name}" + '\n')
            output_file.write("No data available." + '\n')
            output_file.write('\n')
            return None

        # Calculate statistics.
        minimum = min(my_data)
        maximum = max(my_data)
        average = sum(my_data) / len(my_data)
        variance = sum((val - average) ** 2 for val in my_data) / len(my_data)
        standard_dev = math.sqrt(variance)

        # Compile statistics in a dictionary.
        statistics = {
            'Minimum': minimum,
            'Maximum': maximum,
            'Average': average,
            'Standard Deviation': standard_dev
        }

        output_file = open(file, "a")
        output_file.write(f"{field_name}" + '\n')
        output_file.write(f"Statistics: {statistics}" + '\n')
        output_file.write('\n')
        return statistics
