import math


class DataProcessor:

    @staticmethod
    def calc_statistics(field, field_name):
        """Calculate statistics for the given data."""
        my_data = []

        for data in field:
            if not math.isnan(data):
                my_data.append(data)

        if len(my_data) == 0:
            my_data = [0]

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
            'Average': round(average, 2),
            'Standard Deviation': round(standard_dev, 2)
        }

        print(f"{field_name}" + '\n')
        print(f"Statistics: {statistics}" + '\n')
        print('\n')
        return statistics
