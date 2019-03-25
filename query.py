import requests
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


class InvalidArgumentsException(Exception):
    pass


if __name__ == "__main__":
    if len(sys.argv) < 9:
        raise InvalidArgumentsException(
            'Invalid format\n\nProper format is \n>>> python3 query.py –verbose True/False –file info_filename –ticker ticker –time time')
    verbose = sys.argv[sys.argv.index('-verbose') + 1] == 'True'
    filename = sys.argv[sys.argv.index('-file') + 1]
    ticker = sys.argv[sys.argv.index('-ticker') + 1]
    qtime = sys.argv[sys.argv.index('-time') + 1]
    get_data_at(filename, ticker, qtime, verbose)
