import os


class FileManager:

    @staticmethod
    def save_gauges(gauge_list, stats_list):
        curr_dir = os.getcwd()
        dir_name = os.path.dirname(curr_dir) + r"\assets\savedGauges.txt"
        outfile = open(dir_name, 'w')
        for gauge, stat in zip(gauge_list, stats_list):
            outfile.write(gauge.field_name[0] + "\n")
            outfile.write(str(stat))
            outfile.write("\n\n")
