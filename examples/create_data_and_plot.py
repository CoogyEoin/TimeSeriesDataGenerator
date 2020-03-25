import pandas as pd
from matplotlib import pyplot
from generate_evc_time_data import generate_time_values

def main():
    print('Dia duit')

    generate_time_values(20, 30, 50, 'ev_data.csv')

    df = pd.read_csv("ev_data.csv")
    df.groupby('date_time').cumsum()['power'].plot(x='date_time', y='power')
    pyplot.show()


if __name__ == '__main__':
    main()