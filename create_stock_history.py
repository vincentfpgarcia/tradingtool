from yahoo_finance import Share
import sys
import json
import csv


# Create the list of stock symbol s
symbols = []
with open('data/companylist.csv', 'rb') as csvfile:
  reader = csv.reader(csvfile, delimiter=',', quotechar='|')
  header_skip = False
  for row in reader:
    symbol = row[0][1:-1]
    if not header_skip:
      header_skip = True
      continue
    if symbol!='VIIX':
      symbols.append(symbol)


# Get the history for each stock symbol
data = {}
for symbol in symbols:
  print 'Processing ' + symbol
  try:
    share = Share(symbol)
    data[symbol] = share.get_historical('2013-01-01', '2016-12-31')
  except:
    continue


# Dump the stock history
output_path = 'data/stock_history.json'
with open(output_path, "wb") as f:
  f.write(json.dumps(data, indent=4))

