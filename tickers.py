import requests
import iex
import pandas as pd
from io import StringIO
import sys

# wrote just to save time finding valid tickers


def get_valid_tickers(outfile='valid_tickers.csv'):
    """
    Gets all valid tickers into a file 'valid_tickers.csv' to save computation time.
    """
    url = r'https://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download'
    data = requests.get(url, allow_redirects=True)
    # read csv from a string
    df = pd.read_csv(StringIO(data.text))
    newdf = df[filter_valid(df['Symbol'])].loc[:, 'Symbol']
    newdf.to_csv('valid_tickers.csv')


def filter_valid(tickers):
    """
    Returns a list of bools, the ith of which indicates whether the ith ticker in the input is valid or not.
    """
    valid_tickers = set(pd.read_csv(
        'valid_tickers.csv', index_col=0, squeeze=True, header=None))
    return [i in valid_tickers for i in tickers]


def save_tickers(n, filename='tickers.txt'):
    """
    Gets a csv of tickers from nasdaq.com and filters them based on whether they are valid or not. Then, outputs the first n to a file 'tickers.txt'.
    """
    url = r'https://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download'
    data = requests.get(url, allow_redirects=True)
    # read csv from a string
    df = pd.read_csv(StringIO(data.text))
    # filter out tickers which are valid and send to a file
    df[filter_valid(df['Symbol'])].loc[:n-1, 'Symbol'].to_csv(filename,
                                                              index=False,
                                                              header=False)


if __name__ == "__main__":
    try:
        n = int(sys.argv[1])
        filename = sys.argv[2]
        save_tickers(n, filename)
    except IndexError as e:
        print('Format:\n $ python tickers.py <number of tickers> <ticker file name>')
