from models.maxime import create_model
from rich import create_learning_data
from keras.models import load_model
import sys
import random

def main():
	model = load_model(sys.argv[2])
	X, Y = create_learning_data(sys.argv[1])

	money = 0
	total_money = 0
	for i in range(len(X)):
		print "current money:", money, total_money

		current = X[i]
		current_value = current[0][-1]

		prediction = model.predict(X[i:i+1])
		if prediction[0][0] > current_value:
			money -= current_value
			total_money += current_value
			money += Y[i:i+1][0][0]
	print "final money:", money


if __name__ == "__main__":
	main()