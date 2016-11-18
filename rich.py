from pprint import pprint
from yahoo_finance import Share


import keras

from keras.models import Sequential
from keras.layers import Input
from keras.layers import Dense
from keras.optimizers import SGD
import numpy as np



# class Maxime(keras.models.Model):
#   """docstring for Maxime"""
#   def __init__(self):

#     inputs = Input(shape=4, name='input')
#     output = Dense(1)(inputs)

#     super(Maxime, self).__init__(input=inputs, output=output)
    



yahoo = Share('YHOO')
# pprint(yahoo.get_historical('2016-01-01', '2016-11-18'))

tmp = yahoo.get_historical('2016-01-01', '2016-11-18')


# i = 20
# type tmp[0]


# Get data
X = []
Y = []
for i in range(0, len(tmp)-1):

  prev_open = float(tmp[i-1]['Open'])
  prev_close = float(tmp[i-1]['Close'])
  current_open = float(tmp[i]['Open'])
  current_close = float(tmp[i]['Close'])
  current_volume = float(tmp[i]['Volume'])

  x = [prev_open, prev_close, current_open, current_volume]
  y = [current_close]
  X.append(x)
  Y.append(y)
# print Y

X = np.asarray(X)
Y = np.asarray(Y)
# print X.shape
# print Y.shape

# print X[0]
# print np.squeeze(X[0])
# exit()



# Network
# fix random seed for reproducibility
seed = 7
np.random.seed(seed)
# load pima indians dataset
# dataset = numpy.loadtxt("pima-indians-diabetes.csv", delimiter=",")
# split into input (X) and output (Y) variables
# X = dataset[:,0:8]
# Y = dataset[:,8]
# create model


# m = Maxime()




model = Sequential()


model.add(Dense(100, input_dim=4, init='uniform', activation='relu'))
model.add(Dense(100, init='uniform', activation='relu'))
model.add(Dense(100, init='uniform', activation='relu'))
model.add(Dense(100, init='uniform', activation='relu'))
model.add(Dense(100, init='uniform', activation='relu'))
model.add(Dense(1, init='uniform'))

# Compile model
# sgd = SGD(lr=10)
model.compile(loss='mean_squared_error', optimizer='adadelta', metrics=['accuracy'])
# model.compile(loss='mean_squared_error', optimizer=sgd, metrics=['accuracy'])
model.fit(X, Y, nb_epoch=200, batch_size=10)
# print model.predict(X[0,:])

# Compile model
sgd = SGD(lr=0.01)
# model.compile(loss='mean_squared_error', optimizer='adadelta', metrics=['accuracy'])
model.compile(loss='mean_squared_error', optimizer=sgd, metrics=['accuracy'])
model.fit(X, Y, nb_epoch=200, batch_size=10)
# print model.predict(X[0,:])

print "********************************"

# Compile model
sgd = SGD(lr=0.001)
# model.compile(loss='mean_squared_error', optimizer='adadelta', metrics=['accuracy'])
model.compile(loss='mean_squared_error', optimizer=sgd, metrics=['accuracy'])
model.fit(X, Y, nb_epoch=200, batch_size=10)
# print model.predict(X[0,:])



print model.predict(X[0:1])
print Y[0]
# evaluate the model
# scores = model.evaluate(X, Y)

# print
# print(":):):) %s: %.2f%%" % (model.metrics_names[1], scores[1]*100))




# print x
# print y

# print '%f %f %f %d' % (prev_open, prev_close, current_open, current_volume)