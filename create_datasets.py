import json
import numpy as np
import random
from datetime import datetime


# Parameters
DAY_IN_PAST   = 31
TRAINING_SIZE = 0.8

# Load the JSON containing stock history
json_path = 'data/stock_history.json'
data      = json.load(open(json_path))

# Set the random seed
random.seed(datetime.now())

# Declare datasets
X_train = []
X_test  = []
y_train = []
y_test  = []

# Go through all symbols
for symbol in data:

  # Ignore VIXX symbol
  if symbol=='VIIX':
    continue

  print 'Processing ' + symbol

  # Values for the considered symbol
  share = data[symbol]

  for curr_day in range(0, len(data[symbol]) - DAY_IN_PAST):

    # Create the X vector with previous days (open and close) and current days (open)
    x = [float(share[curr_day]['Open'])]
    for j in range(1, DAY_IN_PAST+1):
      past_day = curr_day + j
      x.append(float(share[past_day]['Close']))
      x.append(float(share[past_day]['Open']))

    # Create y with current day (close)
    y = float(share[curr_day]['Close'])

    # Split randomly training and testing data
    if curr_day >= (1.0 - TRAINING_SIZE) * (len(data[symbol])-1):
      X_train.append([x])
      y_train.append([y])
    else:
      X_test.append([x])
      y_test.append([y])

# Convert lists as numpy arrays
X_train = np.array(X_train)
X_test  = np.array(X_test)
y_train = np.array(y_train).reshape(-1,1)
y_test  = np.array(y_test).reshape(-1,1)


# Save training and testing data
np.save('data/X_train.npy', X_train)
np.save('data/y_train.npy', y_train)
np.save('data/X_test.npy', X_test)
np.save('data/y_test.npy', y_test)

# print X_train.shape
# print X_test.shape
# print y_train.shape
# print y_test.shape
