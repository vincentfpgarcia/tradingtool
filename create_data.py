from yahoo_finance import Share
import sys
import json

if sys.argv[1] == "-h" or sys.argv[1] == "--help" or sys.argv[1] == "-help":
	print "python create_data.py output_path compagny_code1 compagny_code2 ..."

output_path = sys.argv[1]
compagny_codes = sys.argv[2:]

data = {}
with open(output_path, "rb") as f:
	buff = f.read()
	if buff != "":
		data = json.loads(buff)

for code in compagny_codes:
	share = Share(code)
	data[code] = share.get_historical('2015-01-01', '2016-01-01')

with open(output_path, "wb") as f:
	f.write(json.dumps(data, indent=4))
