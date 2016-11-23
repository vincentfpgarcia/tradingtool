from models.maxime import create_model
from rich import create_learning_data
from keras.models import load_model
import sys
import random
import numpy as np

def main():
	model = load_model(sys.argv[1])
	X = np.load("data/X_test.npy")
	Y = np.load("data/y_test.npy")

	money = 0
	total_money = 0
	for i in range(len(X)):

		current = X[i]
		current_value = current[0][-1]

		prediction = model.predict(X[i:i+1])
		if prediction[0][0] > current_value * 1.10:
			print "---"
			print "make transaction"
			print "current money:", money
			print "total money invested:", total_money
			print "current stock value:", current_value, "- prediction:", prediction[0][0], "- true value:", Y[i:i+1][0][0]
			money -= 100.0
			total_money += 100.0
			money += prediction[0][0] / Y[i:i+1][0][0] * 100.0
	print ""
	print "final money:", money, "for", total_money, "invested"


if __name__ == "__main__":
	main()