To use tickers.py, enter the following command.
python3 tickers.py number_of_tickers ticker filename

To use fetcher.py, enter the following command.
python3 fetcher.py time_lim ticker_filename info_filename

To use query.py, enter the following command.
python3 query.py –verbose True/False –file info_filename –ticker ticker –time time
The time format for the above command should be HH:MM, hours are out of 24.]

To use predictor.py, enter the following command.
python3 predictor.py ticker info_filename graph_filename column time

DOCUMENTATION:
tickers.py:

fetcher.py:
  update_info: Gets quote data for specific ticker and writes to output file in a csv format
  call_update: Opens output file and calls update_info() for each ticker than it gets from the tickers.txt
               Outputs the data to the use specified output file in csv format

query.py:

predictor.py:
