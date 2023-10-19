from tkinter import filedialog

import math
import csv


class DataProcessor:
    def __init__(self, fields, rows):
        self.fields = fields
        self.rows = rows
        self.metric_indicator = 0  # default to 0 (meters)

    def get_statistics(self):
        """Calculate statistics for the given data."""
        if not self.rows or not self.rows[0]:
            print("No data available.")
            return None

        # Extract relevant data.
        my_data = [float(row[7]) for row in self.rows]  # Assumes data is in the 8th column

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

    def swap_metric(self):
        """Swap units between meters and inches in the dataset."""
        if not self.rows:
            print("No data available to convert.")
            return None

        conversion_factor = 39.3701  # accurate conversion factor from meters to inches

        if self.metric_indicator == 0:  # units are in meters, convert to inches
            self.metric_indicator = 1
            conversion = lambda x: x * conversion_factor
        else:  # units are in inches, convert to meters
            self.metric_indicator = 0
            conversion = lambda x: x / conversion_factor

        for row in self.rows:
            for i, field in enumerate(self.fields):
                if '[m' in field and row[i]:
                    row[i] = str(conversion(float(row[i])))

        return self.rows  # returns updated rows

    def load_csv(self):
        """Prompt the user to select a CSV file."""
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")], title="Select a CSV File")
        if filename:  # If a file is selected
            print(f"CSV File Loaded: {filename}")
            # reading csv file
            with open(filename, 'r') as csvfile:
                # creating a csv reader object
                csvreader = csv.reader(csvfile)

                # extracting field names through first row
                self.fields = next(csvreader)

                # extracting each data row one by one
                for row in csvreader:
                    self.rows.append(row)

                # get total number of rows
                print("Total no. of rows: %d" % csvreader.line_num)

            # printing the field names
            print('Field names are:' + ', '.join(field for field in self.fields))

# Example usage:
# fields_example = ['Field1', 'Field2[m]', ...]  # Replace with actual fields
# rows_example = [...]  # Replace with actual rows data

# processor = DataProcessor(fields_example, rows_example)
# statistics = processor.get_statistics()
# updated_rows = processor.swap_metric()
