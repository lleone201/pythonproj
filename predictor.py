import matplotlib.pyplot as plt
import sklearn.linear_model as model
import pandas as pd
import numpy as np
import time
import iex
import datetime as dt
from matplotlib import style


def time_to_int(t):
    h, m = t.split(':')
    return int(h) * 3600 + int(m) * 60


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


def create_model(data, col):
    return model.LinearRegression().fit(data[0].reshape(-1, 1), data[1].reshape(-1, 1))


def graph_data(data, predicted, coefs, graphfile):
    plt.style.use("fivethirtyeight")
    plt.grid(False)
    fig = plt.figure(1)
    ax = plt.subplot(111)
    ax.scatter(data[0], data[1], color='r')
    ax.scatter(predicted[0], predicted[1], color='b')
    m, b = coefs
    total_x = list(data[:, 0]) + list(predicted[:, 0])
    print(total_x)

    def f(x):
        return (m * x) + b
    total_y = list(map(f, total_x))
    print(total_y)
    ax.plot(total_x, total_y)
    plt.savefig(graphfile)


def model_and_graph(ticker, col, infile, graphfile, t):
    data = grab_info(ticker, col, infile).to_numpy()
    m = create_model(data, col)
    last_minute = time_to_int('18:05')
    next_t_minutes = np.array(range(last_minute+1, last_minute+t+1))
    coefs = (float(m.coef_), float(m.intercept_))
    print(next_t_minutes)
    predicted = m.predict(next_t_minutes.reshape(-1, 1)).flatten()
    predicted = np.array([next_t_minutes, predicted], np.float32).transpose()
    graph_data(data, predicted, coefs, graphfile)


if __name__ == "__main__":
    model_and_graph('AAPL', 'latestPrice', 'test.csv', 'graph.png', 3)
