import numpy as np
import pandas as pd


def baseline_model(df):
    y_train = df
    y_pred = y_train[-1]
    return y_pred

def rmse():
    rmse = (np.mean((y_test[0]-y_pred)**2))**0.5
    return rmse
