import sys
import requests
import json
import time
import datetime
from iex import Stock

#For some reason the Stock(ticker).quote() function outputs to the screen
def update_info(ticker, f):
    """
    Gets quote data for specific ticker and writes to output file in a csv format
    """
    stock = Stock(ticker).quote()
    currentDT = datetime.datetime.now()
    args = [str(currentDT.hour) + ':' + str(currentDT.minute), stock['symbol'], stock['latestPrice'], stock['latestVolume'], stock['close'], stock['open'], stock['low'], stock['high']]
    f.write(",".join(map(str,args)))
    f.write('\n')
    
def call_update(filename='info.csv'):
    """
    Opens output file and calls update_info() for each ticker than it gets from the tickers.txt
    Outputs the data to the use specified output file in csv format
    """
    tickers_obj = open(sys.argv[2])
    content = tickers_obj.readlines()
    content = [x.strip() for x in content]
    output_file = open(filename,"w+")
    #Writes first line of column names
    args = ["Time", "Ticker", "Latest Price", "Latest Volume", "Close", "Open", "Low", "High"]
    output_file.write(",".join(map(str,args)))
    output_file.write('\n')
       
    for x in content:
        update_info(x, output_file)

if __name__ == "__main__":
    try:
        limit = int(sys.argv[1])
        ticker_file = sys.argv[2]
        info_file = sys.argv[3]
        
        #While loop makes the program run for user specified amount of time
        start_time = time.time()
        while(time.time() - start_time) < limit:
             call_update(info_file)
          
    except IndexError as e:
        print('Format:\n $ python fetcher.py <time limit> <input file> <output file>')