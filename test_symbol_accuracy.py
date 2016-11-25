from dataset import create_testing_data_for_symbol, get_symbol_list
from keras.models import load_model
import sys

INITIAL_CAPITAL = 10000.0
PERCENT_OF_CAPITAL_PER_TRANSACTION = 10.0
TRANSACTION_FEE = 0

def compare(x, y):
	if x[1] < y[1]:
		return 1
	return -1

def main():
	model = load_model(sys.argv[1])
	symbols = get_symbol_list()
	gains = []
	for sym in symbols:
		X, Y = create_testing_data_for_symbol(sym)
		print "----"

		money = INITIAL_CAPITAL
		for i in range(len(X)):
			current = X[i]
			current_value = current[0][-1]

			prediction = model.predict(X[i:i+1])
			if prediction[0][0] > current_value * 1.02:
				investment = 100.0
				money -=  investment + TRANSACTION_FEE * 2.0
				revenue = Y[i:i+1][0][0] / current_value * investment
				gain = revenue - investment
				money += revenue
		print ""
		print "symbol:", sym
		total_gain = money - INITIAL_CAPITAL
		percent_gain = ((money / INITIAL_CAPITAL) - 1.0) * 100.0
		print "gain:", total_gain, "(", percent_gain, ")"

		gains.append([sym, total_gain, percent_gain])

	gains.sort(compare)
	for item in gains:
		print item

if __name__ == "__main__":
	main()