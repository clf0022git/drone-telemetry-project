import math
from src.data.input import DataManager


class DataProcessor:

    @staticmethod
    def calc_statistics(field):
        """Calculate statistics for the given data."""
        my_data = []

        for data in field:
            if not math.isnan(data):
                my_data.append(data)

        if not my_data or math.isnan(min(my_data)):
            print("No data available.")
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

        print(f"Statistics: {statistics}")
        return statistics
