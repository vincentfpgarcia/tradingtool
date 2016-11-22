create_stock_history.py
  
  Create the history for each stock in European market. The stock symbols are
  read from the file data/companylist.csv. The history of every stock is stored
  in a JSON file dta/stock_history.json.


create_datasets.py

  Create a training and a testing sets from the stock history JSON file (see
  above). The training and testing sets respectively represent 80% and 20% of
  the dataset. The X and y matrices (training and testing) are stored in .npy
  files (Numpy arrays).