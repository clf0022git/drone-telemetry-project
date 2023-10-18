import math


def get_statistics(rows):
    """Error! float division by 0"""
    my_data = []
    val_total = 0.0
    enum_total = 0.0
    minimum = 0.0
    maximum = 0.0
    start_search = 0
    for row in rows:
        my_data.append(float(row[7]))
    arr_size = len(my_data)
    for val in my_data:
        if start_search == 0:
            minimum = val
            start_search = 1
        else:
            if val < minimum:
                minimum = val
    start_search = 0
    for val in my_data:
        if start_search == 0:
            maximum = val
            start_search = 1
        else:
            if val > maximum:
                maximum = val
    for val in my_data:
        val_total += val
    average = val_total / arr_size
    for val in my_data:
        enum_total += pow(val - average, 2)
    standard_dev = math.sqrt(enum_total / arr_size)
    print('\nMinimum: ', minimum, '\n')
    print('\nMaximum: ', maximum, '\n')
    print('\nMedian: ', average, '\n')
    print('\nStandard Deviation: ', standard_dev, '\n')


def swap_metric(fields, rows, m_or_f):
    """Check what metric is already in use and swap to the other one"""
    """Error! Does not display changes"""
    if m_or_f == 0:  # case for the units being in meters
        for row in rows:
            i = 0
            while i < len(row):
                index = fields[i].find('[m')
                if index != -1 and row[i] != '':
                    row[i] = str(float(row[i]) * 39.76)
                i += 1
        # printing first 6 rows
        print('\nFirst 6 rows are:\n')
        for row in rows[:6]:
            # parsing each column of a row
            for col in row:
                print("%10s" % col, end=" "),
            print('\n')
        m_or_f = 1
    else:
        for row in rows:
            i = 0
            while i < len(row):
                index = fields[i].find('[m')
                if index != -1 and row[i] != '':
                    row[i] = str(float(row[i]) / 39.76)
                i += 1
        # printing first 6 rows
        print('\nFirst 6 rows are:\n')
        for row in rows[:6]:
            # parsing each column of a row
            for col in row:
                print("%10s" % col, end=" "),
            print('\n')
        m_or_f = 0
