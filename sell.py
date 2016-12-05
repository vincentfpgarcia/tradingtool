import json
import sys
from googlefinance import getQuotes

INVESTMENT_VALUE = 100.0

def main():
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