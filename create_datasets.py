import json
import numpy as np
import random
from datetime import datetime




DAY_IN_PAST = 31




if __name__ == '__main__':
  
  # a = [1, 2, 3, 4, 5]
  # print a

  # b = np.array(a)
  # print b
  # print b.shape

  # c = b.reshape(1,-1)
  # print c
  # print c.shape

  # d = [c, c, c]
  # print d

  # e = np.array(d)
  # print e

  # d2 = [a,a,a]
  # print d2

  # e2 = np.array(d2)
  # print e2
  # print e2.shape




  json_path = 'stock_history.json'

  training_size = 0.8
  testing_size  = 1. - training_size



  data = json.load(open(json_path))

  X_train = 0
  X_test  = 0



  random.seed(datetime.now())



  for stock in data:

    for i in range(0, len(data[stock])-DAY_IN_PAST):

      rd = random.uniform(0., 1.)
      if rd<=training_size:
        X_train += 1
      else:
        X_test += 1


  print 'train : %f' % (float(X_train) / (X_train+X_test))
  print 'test  : %f' % (float(X_test) / (X_train+X_test))







# def create_learning_data(path):
#   data = {}
#   with open(path, "rb") as f:
#     text = f.read()
#     data = json.loads(text)
#   X = []
#   Y = []
#   for key in data:
#     share = data[key]
#     for i in range(len(share) - DAY_IN_PAST):
#       volume = 0
#       x = []
#       k = 1
#       for j in range(DAY_IN_PAST):
#         current_day = i + (DAY_IN_PAST - j)
#         x.append(float(share[current_day]['Open']))
#         x.append(float(share[current_day]['Close']))
#         # volume += float(share[current_day]['Volume'])
#         k += 1
#       x.append(float(share[i]['Open']))
#       # volume /= DAY_IN_PAST - 1
#       # volume /= 100000.0
#       # x.append(volume)
#       y = [float(share[i]['Close'])]
#       X.append([x])
#       Y.append(y)
#   X = np.asarray(X)
#   Y = np.asarray(Y)
#   return X, Y