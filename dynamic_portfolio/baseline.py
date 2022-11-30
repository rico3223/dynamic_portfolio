import numpy as np
import pandas as pd

TARGET_COLUMN_IDX = 1 #A définir

def last_seen_value_baseline(X, y):
    # How many values do you want to predict in the future ?
    output_length = y.shape[-1] # = 1

    # For each sequence, let's consider the last seen value
    # and only the target column
    last_seen_values = X[:,-1, TARGET_COLUMN_IDX].reshape(-1,1)

    # We need to duplicate these values as many times as output_length
    repeated = np.repeat(last_seen_values, axis = 1, repeats = output_length)

    return np.mean(np.abs(y_test - repeated))
