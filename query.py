import requests
import iex
import pandas as pd
import sys


def get_data_at(filename, ticker, query_time, verbose=False):
    data = pd.read_csv(filename)
    row = data[(data['Ticker'] == ticker) & (data['Time'] == query_time)]
    for c, v in row.to_dict('records')[0].items():
        print(f'{c}: {v}')
    if verbose:
        print(f'Number of rows: {len(data)}')
        print(f'Number of columns: {len(data.columns)}')
        print(f'Columns: {", ".join(data.columns)}')


if __name__ == "__main__":
    verbose = sys.argv[1] == '-verbose' or sys.argv[1] == '-v'
    qtime = sys.argv[2]
    filename = sys.argv[3]
    ticker = sys.argv[4]
    get_data_at(filename, ticker, qtime, verbose)
