import os


class FileManager:

    @staticmethod
    def save_gauges(gauge_list):
        curr_dir = os.getcwd()
        dir_name = os.path.dirname(curr_dir) + r"\assets\savedGauges.txt"
        outfile = open(dir_name, 'w')
        for gauge in gauge_list:
            outfile.write(str(gauge.id) + "\n")
            outfile.write(gauge.field_name[0] + "\n")
            outfile.write(gauge.second_field_name + "\n")
            outfile.write(gauge.gauge_name + "\n")
            outfile.write(str(gauge.timestamp_value) + "\n")
            outfile.write(gauge.name + "\n")
            outfile.write(str(gauge.statistics) + "\n")
            outfile.write(str(gauge.blue_range_low) + "\n")
            outfile.write(str(gauge.blue_range_high) + "\n")
            outfile.write(str(gauge.green_range_low) + "\n")
            outfile.write(str(gauge.green_range_high) + "\n")
            outfile.write(str(gauge.yellow_range_low) + "\n")
            outfile.write(str(gauge.yellow_range_high) + "\n")
            outfile.write(str(gauge.red_range_low) + "\n")
            outfile.write(str(gauge.red_range_high) + "\n")
            outfile.write("\n")
