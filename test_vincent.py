from yahoo_finance import Share
from pprint import pprint


stock = Share('CRTO')
pprint(stock.get_historical('2016-11-21', '2016-11-23'))
# print stock.get_open()
# print stock.get_price()

