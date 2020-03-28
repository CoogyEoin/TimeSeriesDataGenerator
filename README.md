# TimeSeriesDataGenerator
This is a simple script for generating random timeseries data based on specified periods of the day. The primary purpose for me is to generate timeseries data related to power loads of electric vehicle chargers (eg: The BMW i3 has a load of 7.2 KW).

The script creates the time series data using Gaussian distributions of means 9, 13 and 18 to represent 9am, 1pm and 6pm. The standard deviation of each of these distributions is 3. 

I only created this because I didn't have any data on EV chargers for another project but I knew the peak times of the day. If you want to modify this script or add to it feel free to go ahead I only ask that you star the repo.
