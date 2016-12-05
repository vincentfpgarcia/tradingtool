import json
import sys
import datetime
from googlefinance import getQuotes

INVESTMENT_VALUE = 100.0

def check_sell(path):
	with open(path) as f:
		investment = json.loads(f.read())
	for i in range(len(investment)):
		try:
			if investment[i]["investment"] is False or investment[i]["sold"] is True:
				continue
		except:
			continue
		try:
			result = getQuotes(str(investment[i]["symbol"]))[0]
		except:
			print "error while request google finance"
			continue
		new_price = float(result["LastTradePrice"])
		old_price = investment[i]["price"]
		if new_price > old_price * 1.02:
			investment[i]["sold"] = True
			investment[i]["sell_price"] = new_price
			investment[i]["sell_date"] = str(datetime.datetime.now())
	with open(path, "wb") as f:
		f.write(json.dumps(investment, indent=2))

def sell_all(path):
	print "Sell_all"
	with open(path) as f:
		investment = json.loads(f.read())
	for i in range(len(investment)):
		try:
			if investment[i]["investment"] is False or investment[i]["sold"] is True:
				continue
		except:
			continue
		try:
			result = getQuotes(str(investment[i]["symbol"]))[0]
		except:
			print "error while request google finance"
			continue
		print "sell"
		new_price = float(result["LastTradePrice"])
		investment[i]["sold"] = True
		investment[i]["sell_price"] = new_price
		investment[i]["sell_date"] = str(datetime.datetime.now())
	with open(path, "wb") as f:
		f.write(json.dumps(investment, indent=2))

def main():
	sell_all(sys.argv[1])
	exit(0)
	f = open(sys.argv[1])
	investment = json.loads(f.read())
	money = 0
	invested = 0
	for invest in investment:
		try:
			if invest["investment"] is False:
				continue
		except:
			continue
		invested += INVESTMENT_VALUE
		money -= INVESTMENT_VALUE
		try:
			result = getQuotes(str(invest["symbol"]))[0]
		except:
			print "error while request google finance"
			continue
		new_price = float(result["LastTradePrice"])
		old_price = invest["price"]
		print "[" + str(invest["symbol"]) + "]", "new price:", new_price, "old price", old_price, "--", new_price > old_price * 1.02
		money += new_price / old_price * INVESTMENT_VALUE
	print "money:", money
	print "invested:", invested

if __name__ == "__main__":
	main()