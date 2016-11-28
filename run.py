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
	for i in range(0, 31):
		result.append(data[-1 + i]["Open"])
		result.append(data[-1 + i]["Close"])
	result.append(current_price)
	result = np.array([[result]])
	return result

def invest(current_price, sym, model, accuracy):
	global investment

	result = {
		"symbol":sym,
		"price":current_price,
		"date":str(datetime.datetime.now())
	}

	acc = get_symbol_accuracy(accuracy, sym)
	if acc < 0.5:
		print "accuracy inf 0.5"
		return
	print "create vector"
	X = create_vector(sym, current_price)
	print "shape:", X.shape
	prediction = model.predict(X)
	if prediction[0][0] > current_price * 1.02:
		print "invest in", sym, "for", current_price
		result["investment"] = True
	result["investment"] = False
	investment.append(result)

def main():
	model = load_model(sys.argv[1])
	f = open("data/accuracy.json")
	accuracy = json.loads(f.read())

	wait_for_opening_time()

	symbols = get_symbol_list()
	remaining_symbols = []
	limit = 25
	while len(symbols) > 0 and limit > 0:
		print "remaining_symbols:", symbols
		for sym in symbols:
			print "processing symbol:", sym
			try:
				result = getQuotes(sym)[0]
			except:
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