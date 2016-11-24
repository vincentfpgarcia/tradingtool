from models.maxime import create_model
from rich import create_learning_data
from keras.models import load_model
import sys
import random
import numpy as np


INITIAL_CAPITAL = 10000.0
PERCENT_OF_CAPITAL_PER_TRANSACTION = 10.0
TRANSACTION_FEE = 0

def main():
	model = load_model(sys.argv[1])
	X = np.load("data/X_test.npy")
	Y = np.load("data/y_test.npy")

	money = INITIAL_CAPITAL

	for i in range(len(X)):

		current = X[i]
		current_value = current[0][0]

		prediction = model.predict(X[i:i+1])
		if prediction[0][0] > current_value * 1.02:
			print "---"
			print "current money:", money
			print "current stock value:", current_value, "- prediction:", prediction[0][0], "- true value:", Y[i:i+1][0][0]
			# investment = money * PERCENT_OF_CAPITAL_PER_TRANSACTION / 100.0
			investment = 100.0
			money -=  investment + TRANSACTION_FEE * 2.0
			revenue = Y[i:i+1][0][0] / current_value * investment
			gain = revenue - investment
			money += revenue

			print "invest:", investment, "- with fee:", TRANSACTION_FEE * 2.0, "- sell:", revenue, "- gain:", gain
	
	print ""
	print "inital capital:", INITIAL_CAPITAL
	print "final money:", money


if __name__ == "__main__":
	main()