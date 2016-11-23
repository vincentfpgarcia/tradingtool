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

def create_learning_data():
	X = np.load("data/X_train.npy")
	Y = np.load("data/y_train.npy")
	return X, Y

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