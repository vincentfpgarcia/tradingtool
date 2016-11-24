from pprint import pprint
from yahoo_finance import Share
import numpy as np
import sys
import json
import random
import os
from dataset import create_learning_data

from keras.optimizers import SGD
from models.maxime import create_model


# def create_learning_data():
# 	X = np.load("data/X_train.npy")
# 	Y = np.load("data/y_train.npy")
# 	return X, Y


# def create_learning_data2():

# 	data = json.load(open('data/dataset.json'))
# 	keys = sorted(data.keys())

# 	# Get X and y data
# 	X = []
# 	y = []
# 	for i in range(0, int(len(keys)*constants.TRAINING_SIZE)):
# 		date = keys[i]
# 		for symbol in data[date].keys():
# 			X.append(data[date][symbol]['X'])
# 			y.append(data[date][symbol]['y'])

# # Cnovert as Numpy arrays and reshape for Keras
# 	X = np.array(X)
# 	y = np.array(y)
# 	X = X.reshape(X.shape[0], 1, X.shape[1])
# 	y = y.reshape(-1, 1)

# 	return X, y


def train(model, X, Y):


	for i in range(1000):
		lr = -1
		with open("config.txt", "rb") as f:
			lr = float(f.read())
		print "using lr:", lr
		sgd = SGD(lr=lr)
		model.compile(loss='mse', optimizer=sgd, metrics=['accuracy'])
		# model.compile(loss='mse', optimizer='adadelta', metrics=['accuracy'])
	
		model.fit(X, Y, nb_epoch=10, batch_size=200)
		if not os.path.exists("save"):
		    os.makedirs("save")
		model.save("save/save_" + str(i) + ".hdf5")


def main():
	np.random.seed(42)


	print "Creating features vector"
	# X, Y = create_learning_data()
	X, Y = create_learning_data()
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