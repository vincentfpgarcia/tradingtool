from dataset import create_testing_data_for_symbol, get_symbol_list
from keras.models import load_model
import sys

INITIAL_CAPITAL = 10000.0
PERCENT_OF_CAPITAL_PER_TRANSACTION = 10.0
TRANSACTION_FEE = 0

def compare(x, y):
	if x[3] < y[3]:
		return 1
	return -1

def main():
	model = load_model(sys.argv[1])
	symbols = get_symbol_list()
	gains = []
	for sym in symbols:
		print "----"
		X, Y = create_testing_data_for_symbol(sym)

		money = INITIAL_CAPITAL
		true_pos = 0
		false_pos = 0
		for i in range(len(X)):
			current = X[i]
			current_value = current[0][-1]

			prediction = model.predict(X[i:i+1])
			if prediction[0][0] > current_value * 1.01:
				investment = 100.0
				money -=  investment + TRANSACTION_FEE * 2.0
				revenue = Y[i:i+1][0][0] / current_value * investment
				gain = revenue - investment
				money += revenue
				if gain > 0.0:
					true_pos += 1
				else:
					false_pos += 1
		print ""
		print "symbol:", sym
		total_gain = money - INITIAL_CAPITAL
		percent_gain = ((money / INITIAL_CAPITAL) - 1.0) * 100.0
		print "gain:", total_gain, "(", percent_gain, ")"
		accuracy = 0 if false_pos+true_pos == 0 else float(true_pos)/float(false_pos+true_pos)
		print "true pos:", true_pos, "false pos:", false_pos, "accuracy:", accuracy

		gains.append([sym, true_pos, false_pos, accuracy, total_gain, percent_gain])

	gains.sort(compare)
	for item in gains:
		print item

if __name__ == "__main__":
	# import dataset

	# X, y = dataset.create_testing_data_for_symbol('CBI')

	# print X
	main()