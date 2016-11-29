from googlefinance import getQuotes
import json
import sys
from dataset import create_testing_data_for_symbol, get_symbol_list
import datetime
import time
import sys
import numpy as np
from keras.models import load_model

investment = []

def get_symbol_accuracy(data, sym):
	for d in data:
		if d["symbol"] == sym:
			return d["accuracy"]
	return -1

def wait_for_opening_time():
	now = datetime.datetime.now()

	target = datetime.datetime(now.year, now.month, now.day, 15, 29, 59)

	wait = target - now
	waitTime = wait.total_seconds()
	print "current date:", now
	print "target date:", target
	print "waiting for:", waitTime
	if waitTime > 0:
		time.sleep(waitTime)

def create_vector(symbol, current_price):
	result = []
	from yahoo_finance import Share
	share = Share(symbol)
	data = share.get_historical('2016-09-01', '2016-12-31')

	result.append(current_price)

	for i in range(0, 31):
		result.insert(0, data[-1 - i]["Close"])
		result.insert(0, data[-1 - i]["Open"])
	
	result = np.array([[result]])
	return result, data

def invest(current_price, sym, model, accuracy):
	global investment

	result = {
		"symbol":sym,
		"price":current_price,
		"date":str(datetime.datetime.now())
	}
	investment.append(result)

	print "create vector"
	try:
		X, raw_data = create_vector(sym, current_price)
	except:
		result["error"] = "error in create_vector"
	result["raw_data"] = raw_data
	print "shape:", X.shape
	prediction = float(model.predict(X)[0][0])
	result["prediction"] = prediction
	print "prediction:", prediction, "current_price:", current_price
	result["investment"] = False
	if prediction > current_price * 1.02:
		print "invest in", sym, "for", current_price
		result["investment"] = True
	investment[-1] = result


def keep_good_accuracy_symbols(symbols, accuracy):
	result = []
	for sym in symbols:
		acc = get_symbol_accuracy(accuracy, sym)
		if acc < 0.5:
			continue
		result.append(sym)
	return result

def main():
	model = load_model(sys.argv[1])
	f = open("data/accuracy.json")
	accuracy = json.loads(f.read())

	symbols = get_symbol_list()
	symbols = keep_good_accuracy_symbols(symbols, accuracy)
	# symbols = symbols[:1]

	print "kept", len(symbols), "symbols"
	wait_for_opening_time()

	remaining_symbols = []
	limit = 25
	while len(symbols) > 0 and limit > 0:
		print "remaining_symbols:", symbols
		for sym in symbols:
			print "processing symbol:", sym
			try:
				result = getQuotes(sym)[0]
			except:
				print "error while request google finance"
				continue						
			if result["Index"] != "NASDAQ" and result["Index"] != "NYSE":
				continue
			if result["LastTradeDateTime"] == "":
				continue
			d = datetime.datetime.strptime(result["LastTradeDateTime"], '%Y-%m-%dT%H:%M:%SZ')
			now = datetime.datetime.now()
			if now.day == d.day and now >= d:
			# if now >= d:
				try:
					invest(float(result["LastTradePrice"]), sym, model, accuracy)
				except:
					pass
				print "opening of symbol:", sym
				print "at:", now
				print "result:", result
				print ""
				print "---"
			else:
				remaining_symbols.append(sym)
		symbols = remaining_symbols
		remaining_symbols = []
		limit -= 1

	f = open("investment.json", "wb")
	f.write(json.dumps(investment, indent=2))

if __name__ == "__main__":
	main()