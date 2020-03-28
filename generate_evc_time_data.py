import datetime
import numpy as np
import math
import csv
from random import randrange


class TimeValueGenerator:

    def __init__(self, morning_values, afternoon_values, evening_values, csv_filename):
        self.the_morning_values = morning_values
        self.the_afternoon_values = afternoon_values
        self.the_evening_values = evening_values
        self.the_csv_filename = csv_filename
        self.number_of_values = self.the_morning_values + self.the_afternoon_values + self.the_evening_values


    def generate_time_values(self):
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
        time_values = self._get_time_values()
        datetime_values = self._convert_values_to_datetime(time_values)
        power_values = self._get_power_values()

        header = ['date_time', 'power']
        with open(self.the_csv_filename, 'wt') as f:
            csv_writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
            csv_writer.writerow(header)  # write header
            for i, j in zip(datetime_values, power_values):
                row = [i, j]
                csv_writer.writerow(row)


    def _get_time_values(self):
        """
        This function returns a list of values based on 3 normal distributions. The distributions
        are of means 9, 13 and 18 (representing 9am, 1pm and 6pm) to simulate morning, noon and night.
        The sigma for each distribution is the same (3).

        :param morning_ratio: Integer for the ratio of morning values (eg: 10 time values)
        :param afternoon_ratio: Integer for the ratio of afternoon values (eg: 30 time values)
        :param evening_ratio: Integer for the ratio of evening values (eg: 60 time values)
        :return: List of numbers of range 0 to 23
        """

        time_values = np.random.normal(9, 3, self.the_morning_values)
        morning_time_values = np.round(time_values, 2)
        time_values = np.random.normal(13, 3, self.the_afternoon_values)
        midday_time_values = np.round(time_values, 2)
        time_values = np.random.normal(18, 3, self.the_evening_values)
        evening_time_values = np.round(time_values, 2)

        # Concatenate all values together
        total_values = np.concatenate([morning_time_values, evening_time_values, midday_time_values])
        return self._add_incremental_time_value(total_values)

    def _add_incremental_time_value(self, time_values):
        incremented_values = [int] * self.number_of_values * 5

        counter = 0
        for i, v in enumerate(time_values):
            for j in range(5):
                incremented_values[counter] = np.round(v, 2)
                counter = counter + 1
                v = v + 0.2
        return incremented_values

    def _convert_values_to_datetime(self, time_values):
        """
        This function converts the randomly generated numbers into Datetime equivalents.
        :param time_values: List of ints to convert to datetimes
        :param elements: Number of datetime values to generate. Note: Must same size as time_values list
        :return: List of datetimes
        """
        date_times = [datetime.datetime] * self.number_of_values * 5

        for i, v in enumerate(time_values):

            t1 = datetime.datetime(2020, 0o1, 0o5, 00, 00, 00, 00000)

            hour_value, minute_value = self._convert_to_hours_and_minutes(v)

            # Set the datetime to the values above
            date_times[i] = t1.replace(hour=hour_value, minute=minute_value)
            date_times[i] = date_times[i].strftime("%Y-%m-%d %H:%M:%S")

        return date_times


    def _convert_to_hours_and_minutes(self, time_value):
        """
        Converts the values to hours and minuts. Limited in that it rounds up the minute vaalues
        :param time_value:
        :return: hour value and minute value
        """
        if math.floor(time_value) >= 23:
            hour_value = 23
        else:
            hour_value = math.floor(time_value)
        minute_str = str(time_value - hour_value)[2] + "0"
        if minute_str == "00":
            minute_value = 00
        else:
            minute_value = math.ceil(59 * (int(minute_str) / 100))
        return hour_value, minute_value


    def _get_power_values(self):
        """
        Function for getting random power values in Watts based on known power loads
        for electric vehicle chargers. The value 7.2 KW is added more times as most vehicles
        on the market have this load (eg: BMW i3)
        :param number_of_values: Integer value for number of elements in power value list
        :return: List of values between 7200 - 22000 with emphasis on 7200
        """
        power_draws = [7200, 11000, 22000, 7200, 7200]
        power_values = [int] * self.number_of_values * 5

        for i in range(len(power_values)):
            rand_int = randrange(5)
            power_values[i] = power_draws[rand_int]

        return power_values

