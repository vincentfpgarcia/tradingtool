from pprint import pprint
from yahoo_finance import Share
import numpy as np
import sys
import json

import keras
from keras.models import Sequential, Model
from keras.layers import Input
from keras.layers import Dense
from keras.optimizers import SGD
from keras.layers.normalization import BatchNormalization

def create_learning_data():
	data_path = sys.argv[1]
	data = {}
	with open(data_path, "rb") as f:
		text = f.read()
		data = json.loads(text)
	X = []
	Y = []
	for key in data:
		share = data[key]
		for i in range(len(share) - 1):
			prev_open = float(share[i-1]['Open'])
			prev_close = float(share[i-1]['Close'])
			current_open = float(share[i]['Open'])
			current_close = float(share[i]['Close'])
			current_volume = float(share[i]['Volume'])
			x = [prev_open, prev_close, current_open, current_volume / 100000.0]
			y = [current_close]
			X.append(x)
			Y.append(y)
	X = np.asarray(X)
	Y = np.asarray(Y)
	return X, Y



def create_model():
	model = Sequential()
	
	inputs = Input(shape=(4,))
	x = inputs

	x = BatchNormalization()(inputs)
	x = Dense(1000)(x)

	outputs = Dense(1)(x)

	model = Model(input=inputs, output=outputs)

	return model



def train(model, X, Y):
	# sgd = SGD(lr=0.01)
	# model.compile(loss='mse', optimizer=sgd, metrics=['accuracy'])

	model.compile(loss='mse', optimizer='adadelta', metrics=['accuracy'])

	model.fit(X, Y, nb_epoch=2000, batch_size=100)



def main():
	np.random.seed(42)

	print "Creating features vector"
	X, Y = create_learning_data()

	print "Creating model"
	model = create_model()
	model.summary()
	print "Training"
	train(model, X, Y)

	print X[1:2]
	print model.predict(X[1:2])
	print Y[1:2]



if __name__ == "__main__":
	main()