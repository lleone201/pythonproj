import requests
import iex


def save_tickers(n, file='tickers.txt'):
    url = r'https://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download'
    size = 0
    data = requests.get(url,  allow_redirects=True)
    with open(file, 'wb') as f:
        while size < n:
            ticker =
            if iex.
            f.write(data.content)


if __name__ == "__main__":
    save_tickers(5)
