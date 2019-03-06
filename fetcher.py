import sys


def update_info(ticker):
    pass


if __name__ == "__main__":
    try:
        limit = int(sys.argv[1])
        ticker_file = sys.argv[2]
        info_file = sys.argv[3]
    except IndexError as e:
        print('Format:\n $ python tickers.py <time limit> <input file> <output file>')
