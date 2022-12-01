#Importing librairies
import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler, StandardScaler, MinMaxScaler

#Local librairies
from dynamic_portfolio.utils import load_csv, features_creation



def standard_scaler(df: pd.DataFrame):
    scaler = StandardScaler()
    columns = df.columns[1:]

    for column in columns:
        scaled_df = scaler.fit_transform()


    return scaled_df



def robust_scaler():
    pass
