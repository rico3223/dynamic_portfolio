#Importing librairies
import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler, StandardScaler, MinMaxScaler

#Local librairies
from dynamic_portfolio.utils import load_csv, features_creation, clean_data



def scaler(df: pd.DataFrame):

    #Creating our model and backtest dataframes
    model_df, backtest_df = backtest_split(df)

    #Creating a copy of our df
    model_df_scaled = model_df.copy()
    backtest_df_scaled = backtest_df.copy()

    #Selecting relevant columns to scale (we dropped 'return' since its our target and we dropped 'date')
    columns_to_scale = model_df_scaled.drop(columns=['return']).columns

    # Scaling our data based
    for column in columns_to_scale:

        if model_df_scaled[column][0]!= model_df_scaled[column][1]:
            scaler_standard = StandardScaler()
            model_df_scaled[column] = scaler_standard.fit_transform(model_df_scaled[[column]])
            backtest_df_scaled[column] = scaler_standard.transform(backtest_df[[column]])
        else:
            scaler_robust = RobustScaler()
            model_df_scaled[column] = scaler_robust.fit_transform(model_df_scaled[[column]])
            backtest_df_scaled[column] = scaler_robust.transform(backtest_df[[column]])

    return model_df_scaled, backtest_df_scaled


def backtest_split(df: pd.DataFrame, split_ratio:float = 0.8):

    model_df = df.iloc[:round(split_ratio*len(df)), :].copy()
    model_df.reset_index(drop=True, inplace=True)

    backtest_df = df.iloc[round(split_ratio*len(df))+1 : , :].copy()
    backtest_df.reset_index(drop=True, inplace=True)

    return model_df, backtest_df


#update to take in consideration the split
def ready_to_train_df(ticker:str):

    loaded_features_df = features_creation(ticker=ticker)
    cleaned_df = clean_data(loaded_features_df)
    scaled_df = scaler(cleaned_df)

    return scaled_df

def pca():
    pass

# a partir de PCA, quelle features tu retiens ?
