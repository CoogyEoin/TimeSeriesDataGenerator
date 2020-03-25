import datetime
import numpy as np
import math
import csv
from random import randrange


def generate_time_values(morning_values, afternoon_values, evening_values, csv_filename):
    """
    This is the main handler function that is responsible for gathering time, datetime and power values and
    writing random power values to a specified CSV file. The power values are based on Electric vehicle charger
    loads. The values are generate using a set of Gaussian distributions of means 9, 13 and 18 to represent 9am,
    1pm and 6pm. The ratio of how many can be changed via the parameters.
    :param morning_values: Number of morning values
    :param afternoon_values: Number of afternoon values
    :param evening_values: Number of evening values
    :param csv_filename: File path the values are to be written to
    :return: None
    """
    number_of_values = morning_values + afternoon_values + evening_values
    time_values = get_time_values(morning_values, afternoon_values, evening_values)
    datetime_values = set_datetime_values(time_values, number_of_values)
    power_values = get_power_values(number_of_values)

    header = ['date_time', 'power']
    with open(csv_filename, 'wt') as f:
        csv_writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        csv_writer.writerow(header)  # write header
        for i, j in zip(datetime_values, power_values):
            row = [i, j]
            csv_writer.writerow(row)


def get_time_values(morning_ratio, afternoon_ratio, evening_ratio):
    """
    This function returns a list of values based on 3 normal distributions. The distributions
    are of means 9, 13 and 18 (representing 9am, 1pm and 6pm) to simulate morning, noon and night.
    The sigma for each distribution is the same (3).

    :param morning_ratio: Integer for the ratio of morning values (eg: 10 time values)
    :param afternoon_ratio: Integer for the ratio of afternoon values (eg: 30 time values)
    :param evening_ratio: Integer for the ratio of evening values (eg: 60 time values)
    :return: List of numbers of range 0 to 23
    """

    time_values = np.random.normal(9, 3, morning_ratio)
    morning_time_values = np.round(time_values, 2)
    time_values = np.random.normal(13, 3, afternoon_ratio)
    midday_time_values = np.round(time_values, 2)
    time_values = np.random.normal(18, 3, evening_ratio)
    evening_time_values = np.round(time_values, 2)
    return np.concatenate([morning_time_values, evening_time_values, midday_time_values])


def set_datetime_values(time_values, elements):
    """
    This function converts the randomly generated numbers into Datetime equivalents.
    :param time_values: List of ints to convert to datetimes
    :param elements: Number of datetime values to generate. Note: Must same size as time_values list
    :return: List of datetimes
    """
    date_times = [datetime.datetime] * elements
    counter = 0
    for i in time_values:
        if i > 23:
            i = 23.000
        t1 = datetime.datetime(2020, 0o1, 0o5, 00, 00, 00, 00000)
        # Get the hour and minute from the random time value
        hour_value = math.floor(i)
        decimals = i - hour_value
        minute_str = str(decimals)[2]
        minute_value = int(minute_str)

        # Set the datetime to the values above
        date_times[counter] = t1.replace(hour=hour_value, minute=minute_value)
        date_times[counter] = date_times[counter].strftime("%Y-%m-%d %H:%M:%S")
        counter += 1

    return date_times


def get_power_values(number_of_values):
    """
    Function for getting random power values in Watts based on known power loads
    for electric vehicle chargers. The value 7.2 KW is added more times as most vehicles
    on the market have this load (eg: BMW i3)
    :param number_of_values: Integer value for number of elements in power value list
    :return: List of values between 7200 - 22000 with emphasis on 7200
    """
    power_draws = [7200, 11000, 22000, 7200, 7200]
    power_values = [int] * number_of_values
    for i in range(number_of_values):
        rand_int = randrange(5)
        power_values[i] = power_draws[rand_int]

    return power_values

