from yahoo_finance import Share
import json
import numpy as np
import random
from datetime import datetime
import os
import csv
import constants

# Structure that will be used to store the global dataset and avoid to reload
# it over and over
dataset = None



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

  # If the file already exist, do nothing
  if os.path.exists(constants.STOCK_HISTORY_PATH):
    return

  print 'Creating stock history'

  # Create the list of stock symbols
  symbols = get_symbol_list()

  # Get the history for each stock symbol
  data = {}
  for symbol in symbols:
    print '  Processing ' + symbol
    try:
      share = Share(symbol)
      history = share.get_historical('2013-01-01', '2016-12-31')
      valid   = True
      for day in history:
        if not ('Open' in day and 'Close' in day):
          print symbol
          valid = False
          break
      if valid:
        data[symbol] = history
    except:
      continue

  # Dump the stock history
  output_path = 'data/stock_history.json'
  with open(output_path, "wb") as f:
    f.write(json.dumps(data, indent=4))




def create_global_dataset():

  # If the file already exist, do nothing
  if os.path.exists(constants.GLOBAL_DATASET_PATH):
    return

  print 'Creating global dataset :',

  # Load the JSON containing stock history
  create_stock_history()
  data = json.load(open(constants.STOCK_HISTORY_PATH))

  # Set the random seed
  random.seed(datetime.now())

  # Declare datasets
  data2 = {}

  # Go through all symbols
  for symbol in data:

    # Values for the considered symbol
    share = data[symbol]

    for curr_day in range(0, len(share) - constants.DAY_IN_PAST):

      # Create the X vector with previous days (open and close) and current days (open)
      x = [float(share[curr_day]['Open'])]
      for j in range(1, constants.DAY_IN_PAST+1):
        past_day = curr_day + j
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
  with open(constants.GLOBAL_DATASET_PATH, 'w') as file:
      json.dump(data2, file)

  print ' done'




def create_global_dataset_bis():

  # If the file already exist, do nothing
  if os.path.exists(constants.GLOBAL_DATASET_PATH):
    return

  print 'Creating global dataset :',

  # Load the JSON containing stock history
  create_stock_history()
  data = json.load(open(constants.STOCK_HISTORY_PATH))

  # Set the random seed
  random.seed(datetime.now())

  # Declare datasets
  data2 = {}

  # Go through all symbols
  for symbol in data:

    # Values for the considered symbol
    share = data[symbol]

    for curr_day in range(0, len(share) - constants.DAY_IN_PAST):

      # Create the X vector with previous days (open and close) and current days (open)
      x0 = [float(share[curr_day]['Open'])]
      x1 = []
      for j in range(1, constants.DAY_IN_PAST+1):
        past_day = curr_day + j
        x0.insert(0, float(share[past_day]['Close']))
        x0.insert(0, float(share[past_day]['Open']))
        x1.insert(0, float(share[past_day]['Open']))

      # Create y with current day (close)
      y = float(share[curr_day]['Close'])

      # Create the dictionary entry for the date if needed
      date = data[symbol][curr_day]['Date']
      if not date in data2:
        data2[date] = {}

      # Add the X and y vectors for the current symbol
      data2[date][symbol] = {'X0': x0, 'X1': x1, 'y':y}

  # Save the JSON file
  with open(constants.GLOBAL_DATASET_PATH, 'w') as file:
      json.dump(data2, file)

  print ' done'



def create_learning_data():
  
  # Create the global dataset
  create_global_dataset()

  print 'Creating learning dataset :', 

  # Load the global dataset
  data = json.load(open(constants.GLOBAL_DATASET_PATH))
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



def create_learning_data_bis():
  
  # Create the global dataset
  create_global_dataset()

  print 'Creating learning dataset :', 

  # Load the global dataset
  data = json.load(open(constants.GLOBAL_DATASET_PATH))
  keys = sorted(data.keys())

  # Get X and y data
  X0 = []
  X1 = []
  y  = []
  for i in range(0, int(len(keys)*constants.TRAINING_SIZE)):
    date = keys[i]
    for symbol in data[date].keys():
      X0.append(data[date][symbol]['X0'])
      X1.append(data[date][symbol]['X1'])
      y.append(data[date][symbol]['y'])

  # Convert as Numpy arrays and reshape for Keras
  X0 = np.array(X0)
  X1 = np.array(X1)
  y = np.array(y)
  X0 = X0.reshape(X0.shape[0], 1, X0.shape[1])
  X1 = X1.reshape(X1.shape[0], 1, X1.shape[1])
  y = y.reshape(-1, 1)

  print ' done'

  return X0, X1, y



def create_testing_data():
  
  # Create the global dataset
  create_global_dataset()

  print 'Creating testing dataset :', 

  # Load the global dataset
  data = json.load(open(constants.GLOBAL_DATASET_PATH))
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



def create_testing_data_bis():
  
  # Create the global dataset
  create_global_dataset()

  print 'Creating learning dataset :', 

  # Load the global dataset
  data = json.load(open(constants.GLOBAL_DATASET_PATH))
  keys = sorted(data.keys())

  # Get X and y data
  X0 = []
  X1 = []
  y  = []
  for i in range(int(len(keys)*constants.TRAINING_SIZE), len(keys)):
    date = keys[i]
    for symbol in data[date].keys():
      X0.append(data[date][symbol]['X0'])
      X1.append(data[date][symbol]['X1'])
      y.append(data[date][symbol]['y'])

  # Convert as Numpy arrays and reshape for Keras
  X0 = np.array(X0)
  X1 = np.array(X1)
  y  = np.array(y)
  X0 = X0.reshape(X0.shape[0], 1, X0.shape[1])
  X1 = X1.reshape(X1.shape[0], 1, X1.shape[1])
  y  = y.reshape(-1, 1)

  print ' done'

  return X0, X1, y



def create_testing_data_for_symbol(symbol):
  global dataset

  # Create the global dataset
  create_global_dataset()

  # Load the global dataset
  if dataset is None:
    dataset = json.load(open(constants.GLOBAL_DATASET_PATH))

  # Sort dataset
  keys = sorted(dataset.keys())

  # Get X and y data
  X = []
  y = []
  for i in range(int(len(keys)*constants.TRAINING_SIZE), len(keys)):
    date = keys[i]
    if symbol in dataset[date]:
      X.append(dataset[date][symbol]['X'])
      y.append(dataset[date][symbol]['y'])

  # Manage the case where X is empty
  if len(X) == 0:
    print 'Error with stock %s' % symbol
    return np.empty(0), np.empty(0)

  # Convert as Numpy arrays and reshape for Keras
  X = np.array(X)
  y = np.array(y)
  X = X.reshape(X.shape[0], 1, X.shape[1])
  y = y.reshape(-1, 1)

  return X, y



def create_testing_data_for_symbol_bis(symbol):
  global dataset

  # Create the global dataset
  create_global_dataset()

  # Load the global dataset
  if dataset is None:
    dataset = json.load(open(constants.GLOBAL_DATASET_PATH))

  # Sort dataset
  keys = sorted(dataset.keys())

  # Get X and y data
  X0 = []
  X1 = []
  y  = []
  for i in range(int(len(keys)*constants.TRAINING_SIZE), len(keys)):
    date = keys[i]
    if symbol in dataset[date]:
      X0.append(dataset[date][symbol]['X0'])
      X1.append(dataset[date][symbol]['X1'])
      y.append(dataset[date][symbol]['y'])

  # Manage the case where X is empty
  if len(X0) == 0:
    print 'Error with stock %s' % symbol
    return np.empty(0), np.empty(0)

  # Convert as Numpy arrays and reshape for Keras
  X0 = np.array(X0)
  X1 = np.array(X1)
  y  = np.array(y)
  X0 = X0.reshape(X0.shape[0], 1, X0.shape[1])
  X1 = X1.reshape(X1.shape[0], 1, X1.shape[1])
  y  = y.reshape(-1, 1)

  return X0, X1, y



if __name__ == "__main__":
  create_global_dataset()

