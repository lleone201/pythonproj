import matplotlib.pyplot as plt
import sklearn.linear_model as model
import pandas as pd
import numpy as np
import time
import iex
import datetime as dt
from matplotlib import style
import sys


def time_to_int(t):
    h, m = t.split(':')
    return int(h) * 3600 + int(m) * 60


def int_to_time(i):
    m = (i % 3600) // 60
    h = (i - m) // 3600
    return f'{h:02}:{m:02}'


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + dt.timedelta(n)


def convert_to_datetime(date):
    combined_format = '%Y%m%d%H:%M'
    return dt.datetime.strptime(date, combined_format)


def get_historical_data(ticker, start, end, outfile=None):
    stock = iex.Stock(ticker)
    data = pd.DataFrame()
    for d in daterange(start, end):
        df = pd.DataFrame.from_records(stock.chart(range=d.strftime('%Y%m%d')))
        data = data.append(df)
    data['date'] = data['date'].astype(str) + data['minute'].astype(str)
    data['date'] = data['date'].apply(convert_to_datetime)
    if outfile is not None:
        data.to_csv(outfile)
    return data


def grab_info(ticker, col, infile):
    data = pd.read_csv(infile)
    data = data[data['Ticker'] == ticker].reset_index()
    data = data[['Time', col]]
    data['Time'] = data['Time'].apply(time_to_int)
    return data


def create_model(xs, ys):
    return model.LinearRegression().fit(xs.reshape(-1, 1), ys.reshape(-1, 1))


def graph_data(x, y, px, py, graphfile, col):
    plt.style.use("ggplot")
    fig = plt.figure(1, figsize=(10, 5))
    ax = plt.subplot(111)

    time_x = list(map(int_to_time, x))
    time_px = list(map(int_to_time, px))

    ax.scatter(time_x, y, c='r', label='Real data')
    ax.scatter(time_px, py, c='b', label='Predicted data')
    total_x = x + px
    time_x = list(map(int_to_time, total_x))
    plt.xlabel('Time')
    plt.ylabel(col)
    plt.title(f'Time vs {col}')
    plt.legend()
    plt.gcf().subplots_adjust(bottom=0.15, left=0.15)
    plt.savefig(graphfile)


def model_and_graph(ticker, col, infile, graphfile, t):
    data = grab_info(ticker, col, infile)
    xs, ys = data['Time'].to_numpy(), data[col].to_numpy()
    m = create_model(xs, ys)
    last_minute = time_to_int('18:05')
    px = np.array(range(last_minute+60, last_minute+(t*60)+60, 60))
    py = m.predict(px.reshape(-1, 1)).flatten()
    graph_data(list(xs), list(ys), list(px), list(py), graphfile, col)


if __name__ == "__main__":
    ticker = sys.argv[1]
    info_file = sys.argv[2]
    graph_file = sys.argv[3]
    col = sys.argv[4]
    t = int(sys.argv[5])
    model_and_graph(ticker, col, info_file, graph_file, t)
