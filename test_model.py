from models.maxime import create_model
from rich import create_learning_data
from keras.models import load_model
import sys
import random

def main():
	model = load_model(sys.argv[2])
	X, Y = create_learning_data(sys.argv[1])
	# model.load(sys.argv[2])

	for i in range(10):
		j = int(random.random() * len(X))
		print X[j:j+1]
		print model.predict(X[j:j+1])
		print Y[j:j+1]
		print ""


if __name__ == "__main__":
	main()