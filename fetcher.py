import sys
import requests
import json
import time
import datetime
from iex import Stock


def update_info(ticker, f):
    stock = Stock(ticker)
    ustring = "https://api.iextrading.com/1.0/stock/" + ticker + "/quote"
    data = requests.get(ustring).text
    wdata = json.loads(data)
    currentDT = datetime.datetime.now()
    args = [str(currentDT.hour) + ':' + str(currentDT.minute), wdata['symbol'], wdata['latestPrice'], wdata['latestVolume'], wdata['close'], wdata['open'], wdata['low'], wdata['high']]
    f.write('{0:<10} {1:<10} {2:<20} {3:<20} {4:<10} {5:<10} {6:<10} {7:<10}'.format(*args))
    f.write('\n')
    
def call_update(filename='info.csv'):
    tickers_obj = open(sys.argv[2])
    content = tickers_obj.readlines()
    content = [x.strip() for x in content]
    output_file = open(filename,"w+")
    args = ["Time", "Ticker", "Latest Price", "Latest Volume", "Close", "Open", "Low", "High"]
    output_file.write('{0:<10} {1:<10} {2:<20} {3:<20} {4:<10} {5:<10} {6:<10} {7:<10}'.format(*args))
    output_file.write('\n')
       
    for x in content:
        update_info(x, output_file)

if __name__ == "__main__":
    try:
        limit = int(sys.argv[1])
        ticker_file = sys.argv[2]
        info_file = sys.argv[3]
        
        start_time = time.time()
        while(time.time() - start_time) < limit:
             call_update(info_file)
         
    except IndexError as e:
        print('Format:\n $ python fetcher.py <time limit> <input file> <output file>')