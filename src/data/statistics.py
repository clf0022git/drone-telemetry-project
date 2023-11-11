import math


class DataProcessor:

    @staticmethod
    def calc_statistics(field, field_name):
        """Calculate statistics for the given data."""
        my_data = []

        for data in field:
            if not math.isnan(data):
                my_data.append(data)

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

        print(f"{field_name}" + '\n')
        print(f"Statistics: {statistics}" + '\n')
        print('\n')
        return statistics
