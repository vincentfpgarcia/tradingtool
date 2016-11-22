from yahoo_finance import Share
import sys
import json
import csv



def GetStockList():

  stocks = []
  with open('companylist.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    header_skip = False
    for row in reader:
      if not header_skip:
        header_skip = True
        continue
      stocks.append(row[0][1:-1])
  return stocks



if __name__ == '__main__':

  # Get the list of stock codes
  stocks = GetStockList()
  # print stocks

  # Get the history for each stock
  data = {}
  for code in stocks:
    print 'Processing ' + code
    try:
      share = Share(code)
      data[code] = share.get_historical('2013-01-01', '2016-12-31')
    except:
      continue
  # print data

  # Dump the stock history
  output_path = 'stock_history.json'
  with open(output_path, "wb") as f:
    f.write(json.dumps(data, indent=4))

  # print 'coucou'

