from yahoo_finance import Share
import json
import numpy as np
import random
from datetime import datetime
import os
import csv
import constants

# Paths
STOCK_HISTORY_PATH = 'data/stock_history.json'
DATASET_PATH       = 'data/dataset.json'

# Structure that will be used to store the global dataset and avoid to reload
# it over and over
data = None



def get_symbol_list():
  symbols = []
  with open('data/companylist.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    header_skip = False
    for row in reader:
      symbol = row[0][1:-1]
      if not header_skip:
        header_skip = True
        continue
      if symbol!='VIIX':
        symbols.append(symbol)
  return sorted(symbols)



def create_stock_history():

  print 'Creating global dataset'

  # Create the list of stock symbols
  symbols = get_symbol_list()

  # Get the history for each stock symbol
  data = {}
  for symbol in symbols:
    print '  Processing ' + symbol
    try:
      share = Share(symbol)
      # data[symbol] = share.get_historical('2013-01-01', '2016-12-31')
      history = share.get_historical('2013-01-01', '2016-12-31')
      for day in history:
        if not ('Open' in day and 'Close' in day):
          print symbol
    except:
      continue

  # Dump the stock history
  output_path = 'data/stock_history.json'
  with open(output_path, "wb") as f:
    f.write(json.dumps(data, indent=4))




def create_global_dataset():

  print 'Creating global dataset :',

  # Load the JSON containing stock history
  if not os.path.exists(STOCK_HISTORY_PATH):
    create_stock_history()
  data = json.load(open(STOCK_HISTORY_PATH))

  # Set the random seed
  random.seed(datetime.now())

  # Declare datasets
  data2 = {}

  # Go through all symbols
  for symbol in data:

    # Ignore VIXX symbol
    if symbol=='VIIX':
      continue

    # print 'Processing ' + symbol

    # Values for the considered symbol
    share = data[symbol]

    for curr_day in range(0, len(share) - constants.DAY_IN_PAST):

      # Create the X vector with previous days (open and close) and current days (open)
      x = [float(share[curr_day]['Open'])]
      for j in range(1, constants.DAY_IN_PAST+1):
        past_day = curr_day + j
        # print share[past_day]
        if not 'Close' in share[past_day]:
          print symbol
          print share[past_day]
        x.insert(0, float(share[past_day]['Close']))
        x.insert(0, float(share[past_day]['Open']))

      # Create y with current day (close)
      y = float(share[curr_day]['Close'])

      # Create the dictionary entry for the date if needed
      date = data[symbol][curr_day]['Date']
      if not date in data2:
        data2[date] = {}

      # Add the X and y vectors for the current symbol
      data2[date][symbol] = {'X': x, 'y':y}

  # Save the JSON file
  with open(DATASET_PATH, 'w') as file:
      json.dump(data2, file)

  print ' done'



def create_learning_data():
  
  # Create the global dataset if needed
  if not os.path.exists(DATASET_PATH):
    create_global_dataset()

  print 'Creating learning dataset :', 

  # Load the global dataset
  data = json.load(open(DATASET_PATH))
  keys = sorted(data.keys())

  # Get X and y data
  X = []
  y = []
  for i in range(0, int(len(keys)*constants.TRAINING_SIZE)):
    date = keys[i]
    for symbol in data[date].keys():
      X.append(data[date][symbol]['X'])
      y.append(data[date][symbol]['y'])

  # Convert as Numpy arrays and reshape for Keras
  X = np.array(X)
  y = np.array(y)
  X = X.reshape(X.shape[0], 1, X.shape[1])
  y = y.reshape(-1, 1)

  print ' done'

  return X, y



def create_testing_data():
  
  # Create the global dataset if needed
  if not os.path.exists(DATASET_PATH):
    create_global_dataset()

  print 'Creating testing dataset :', 

  # Load the global dataset
  data = json.load(open('data/dataset.json'))
  keys = sorted(data.keys())

  # Get X and y data
  X = []
  y = []
  for i in range(int(len(keys)*constants.TRAINING_SIZE), len(keys)):
    date = keys[i]
    for symbol in data[date].keys():
      X.append(data[date][symbol]['X'])
      y.append(data[date][symbol]['y'])

  # Convert as Numpy arrays and reshape for Keras
  X = np.array(X)
  y = np.array(y)
  X = X.reshape(X.shape[0], 1, X.shape[1])
  y = y.reshape(-1, 1)

  print ' done'

  return X, y



def create_testing_data_for_symbol(symbol):
  global data

  # Create the global dataset if needed
  if not os.path.exists(DATASET_PATH):
    create_global_dataset()

  # Load the global dataset
  if data is None:
    data = json.load(open('data/dataset.json'))

  # Sort data
  keys = sorted(data.keys())

  # Get X and y data
  X = []
  y = []
  for i in range(int(len(keys)*constants.TRAINING_SIZE), len(keys)):
    date = keys[i]
    if symbol in data[date]:
      X.append(data[date][symbol]['X'])
      y.append(data[date][symbol]['y'])

  if len(X) == 0:
    return [], []
  # Convert as Numpy arrays and reshape for Keras
  X = np.array(X)
  y = np.array(y)
  X = X.reshape(X.shape[0], 1, X.shape[1])
  y = y.reshape(-1, 1)

  return X, y



if __name__ == "__main__":
  create_global_dataset()

