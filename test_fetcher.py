import sys
import requests
import json
import time
import iex
import pandas as pd


def get_one_minute(ticker):
    stock = iex.Stock(ticker)
    quote = stock.quote()
    quote['time'] = time.strftime(
        '%H:%M', time.gmtime(int(quote['latestUpdate']) // 1000))
    new_cols = ["Time", "Ticker", "latestPrice",
                "latestVolume", "Close", "Open", "low", "high"]
    quote_cols = ["time", "symbol", "latestPrice",
                  "latestVolume", "close", "open", "low", "high"]
    # return the row for the current minute
    return {c: quote[q] for q, c in zip(quote_cols, new_cols)}


def update_info(tickers, limit, outfile):
    # start timer
    start_time = time.time()
    try:
        data = pd.read_csv(outfile, index_col=0)
    except pd.errors.EmptyDataError:
        data = pd.DataFrame(columns=["Time", "Ticker", "latestPrice",
                                             "latestVolume", "Close", "Open", "low", "high"])
        data.set_index(['Time', 'Ticker'], inplace=True)
    # while time_elapsed < limit
    # while (time.time() - start_time) < limit:
    # get one minute's data for every ticker in the list
    updated_data = pd.DataFrame.from_records(
        [get_one_minute(t) for t in tickers], index=['Time', 'Ticker'])
    data.combine_first(updated_data).to_csv(outfile)
    # only get once per minute
    # time.sleep(60)
    # rename the columns


get_one_minute('AAPL')


def call_update(filename='info.csv'):
    tickers_obj = open(sys.argv[2])
    content = tickers_obj.readlines()
    content = [x.strip() for x in content]
    output_file = open(filename, "w+")
    args = ["Time", "Ticker", "latestPrice",
            "latestVolume", "Close", "Open", "low", "high"]
    output_file.write(
        '{0:<10} {1:<10} {2:<20} {3:<20} {4:<10} {5:<10} {6:<10} {7:<10}'.format(*args))
    output_file.write('\n')

    for x in content:
        update_info(x, filename)


if __name__ == "__main__":
    try:
        limit = int(sys.argv[1])
        ticker_file = sys.argv[2]
        info_file = sys.argv[3]

        start_time = time.time()
        while (time.time() - start_time) < limit:
            call_update(info_file)

    except IndexError as e:
        print('Format:\n $ python fetcher.py <time limit> <input file> <output file>')
