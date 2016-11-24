import json
import numpy as np
import random
from datetime import datetime
import os

# Paths
STOCK_HISTORY_PATH = 'data/stock_history.json'
DATASET_PATH       = 'data/dataset.json'

# Constants
DAY_IN_PAST        = 31
TRAINING_SIZE      = 0.8


def create_global_dataset():

  print 'Creating global dataset :',

  # Load the JSON containing stock history
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

    for curr_day in range(0, len(share) - DAY_IN_PAST):

      # Create the X vector with previous days (open and close) and current days (open)
      x = [float(share[curr_day]['Open'])]
      for j in range(1, DAY_IN_PAST+1):
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
  for i in range(0, int(len(keys)*TRAINING_SIZE)):
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
  for i in range(int(len(keys)*TRAINING_SIZE), len(keys)):
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

