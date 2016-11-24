# from yahoo_finance import Share
# from pprint import pprint
import dataset

# X, y = dataset.create_learning_data()
# print X.shape
# print y.shape

# X, y = dataset.create_testing_data_for_symbol('ORAN')
# print X.shape
# print y.shape

# # print X

# for a in X:
#   for b in a[0]:
#     print '%f, ' % b, 
#   print

print dataset.get_symbol_list()


# stock = Share('CRTO')
# pprint(stock.get_historical('2016-11-21', '2016-11-23'))
# print stock.get_open()
# print stock.get_price()

# a = []
# a.insert(0, 1)
# a.insert(0, 2)
# a.insert(0, 3)
# a.insert(0, 4)

# print a

# a = {}
# if 'toto' in a:
#   a['toto']['foo'] = 3
# else:
#   a['toto'] = {}
#   a['toto']['foo'] = 3
# print a

# a = {'foo':2, 'bar':3}
# # a['foo'] = 2
# print a