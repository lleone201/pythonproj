import requests
from iex import reference
import pandas as pd
from io import StringIO
import sys


def is_valid(tickers):
    s = set(reference.symbols()['symbol'])
    return [t.upper() in s for t in tickers]


def save_tickers(n, filename='tickers.txt'):
    url = r'https://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download'
    data = requests.get(url, allow_redirects=True)
    # read csv from a string
    df = pd.read_csv(StringIO(data.text))
    # filter out tickers which are valid and send to a file
    print('\n'.join(df[is_valid(df['Symbol'])].loc[:n-1, 'Symbol']),
          file=open(filename, 'w'))


if __name__ == "__main__":
    try:
        n = int(sys.argv[1])
        filename = sys.argv[2]
        save_tickers(n, filename)
    except IndexError as e:
        print('Format:\n $ python tickers.py <number of tickers> <ticker file name>')
