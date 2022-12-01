#Importing librairies
import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler, StandardScaler, MinMaxScaler

#Local librairies
from dynamic_portfolio.utils import load_csv, features_creation



def scaler(df: pd.DataFrame):

    #Creating a copy of our dataframe to scale
    df_scaled = df.copy()

    #Selecting relevant columns to scale (we dropped 'return' since its our target and we dropped 'date')
    columns_to_scale = df_scaled.drop(columns=['return', 'date']).columns

    # Scaling our data based
    for column in columns_to_scale:

        if df_scaled[column][0]!= df_scaled[column][1]:
            scaler_standard = StandardScaler()
            df_scaled[column] = scaler_standard.fit_transform(df_scaled[[column]])

        else:
            scaler_robust = RobustScaler()
            df_scaled[column] = scaler_robust.fit_transform(df_scaled[[column]])

    return df_scaled
