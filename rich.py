from pprint import pprint
from yahoo_finance import Share
import numpy as np
import sys
import json
import random
import os

from keras.optimizers import SGD
from models.maxime import create_model

DAY_IN_PAST = 31

def create_learning_data(path):
	data = {}
	with open(path, "rb") as f:
		text = f.read()
		data = json.loads(text)
	X = []
	Y = []
	for key in data:
		share = data[key]
		for i in range(len(share) - DAY_IN_PAST):
			volume = 0
			x = []
			k = 1
			for j in range(DAY_IN_PAST):
				current_day = i + (DAY_IN_PAST - j)
				x.append(float(share[current_day]['Open']))
				x.append(float(share[current_day]['Close']))
				volume += float(share[current_day]['Volume'])
				k += 1
			x.append(float(share[i]['Open']))
			volume /= DAY_IN_PAST - 1
			volume /= 100000.0
			x.append(volume)
			y = [float(share[i]['Close'])]
			X.append([x])
			Y.append(y)
	X = np.asarray(X)
	Y = np.asarray(Y)
	return X, Y

def train(model, X, Y):
	# sgd = SGD(lr=0.01)
	# model.compile(loss='mse', optimizer=sgd, metrics=['accuracy'])

	model.compile(loss='mse', optimizer='adadelta', metrics=['accuracy'])

	for i in range(1000):
		model.fit(X, Y, nb_epoch=25, batch_size=200)
		if not os.path.exists("save"):
		    os.makedirs("save")
		model.save("save/save_" + str(i) + ".hdf5")


def main():
	np.random.seed(42)

	print "Creating features vector"
	X, Y = create_learning_data(sys.argv[1])
	print "features shape:"
	print "X:", X.shape
	print "Y:", Y.shape

	print "Creating model"
	model = create_model()
	model.summary()
	print "Training"
	train(model, X, Y)


if __name__ == "__main__":
	main()