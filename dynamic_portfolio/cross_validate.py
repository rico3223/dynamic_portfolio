# importing relevant librairies
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error


cross_val = {
    'fold_length' : 252, # Trading days for 1 year
    'fold_stride' : 60, # Step between folds, here one quarter
    'train_test_ratio' : 0.7, # Fold split ratio for train/test
    'input_length' : 0, # Input for sequences, here at 0
    'horizon' : 1, # We predict for t+1 so here 1
    'output_length' : 1, # Number of targets wanted, here return
}



#Split the dataset by FOLDS
def get_folds(
    df: pd.DataFrame,
    fold_length: cross_val['fold_length'],
    fold_stride: cross_val['fold_stride']):
    '''
    This function slides through the Time Series dataframe of shape (n_timesteps, n_features) to create folds
    - of equal `fold_length`
    - using `fold_stride` between each fold

    Returns a list of folds, each as a DataFrame
    '''

    folds = []
    for idx in range(0, len(df), fold_stride):
        # Exits the loop as soon as the last fold index would exceed the last index
        if (idx + fold_length) > len(df):
            break
        fold = df.iloc[idx:idx + fold_length, :]
        folds.append(fold)
    return folds


#Split FOLDS by Train et Test
#### FOR ONE FOLD !!!!!
def train_test_split(fold: pd.DataFrame,
                     train_test_ratio =  cross_val['train_test_ratio'],
                     input_length = cross_val['input_length'],
                     ):
    '''
    Returns a train dataframe and a test dataframe (fold_train, fold_test)
    from which one can sample (X,y) sequences.
    df_train should contain all the timesteps until round(train_test_ratio * len(fold))
    '''

    # TRAIN SET
    # ======================
    last_train_idx = round(train_test_ratio * len(fold))
    fold_train = fold.iloc[0:last_train_idx, :]

    # TEST SET
    # ======================
<<<<<<< HEAD
    # fold_test starts right after the end of fold_train
    first_test_idx = last_train_idx - input_length
=======
    first_test_idx = last_train_idx - input_length # faut il pas changer le - en + ??
>>>>>>> ed792e921c7e16c27e40524cdc76cebe6054a464
    fold_test = fold.iloc[first_test_idx:, :]

    return (fold_train, fold_test)

<<<<<<< HEAD
def cross_validate_ml(df, model) :
=======
# est ce que les train et test set n s'entremelent pas ?
# changer le ticker BF-B dans la fonction tickers





#Loop for split on FOLDS
def cross_validate_dl(df:pd.DataFrame, fold_length:int, fold_stride:int) :
>>>>>>> ed792e921c7e16c27e40524cdc76cebe6054a464
    '''
    get_folds() create many FOLDS, train_test_split() create a split on ONE FOLDS.
    The goal of this function is to make splits and sequences on each FOLDS.
    Then, apply a model.
    '''
    folds = get_folds(df, fold_length = cross_val['fold_length'], fold_stride = cross_val['fold_stride'])

    scores = []

    for fold in folds:
        (fold_train, fold_test) = train_test_split(fold = fold,
                                                train_test_ratio = cross_val['train_test_ratio'],
                                                input_length = cross_val['input_length'],
                                                horizon = cross_val['horizon']
                                                )


<<<<<<< HEAD
=======
def cross_validate_ml(df:pd.DataFrame, fold_length:int, fold_stride:int) :
    '''
    get_folds() create many FOLDS, train_test_split() create a split on ONE FOLDS.
    The goal of this function is to make splits and sequences on each FOLDS.
    Then, apply a model.
    '''
    folds = get_folds(df, fold_length, fold_stride) # 1 - Creating FOLDS

    for fold_id, fold in enumerate(folds):

        # 2 - CHRONOLOGICAL TRAIN TEST SPLIT of the current FOLD

        (fold_train, fold_test) = train_test_split(fold = fold,
                                                train_test_ratio = train_test_ratio,
                                                input_length = input_length ,
                                                horizon = horizon)

        # 3 - Scanninng fold_train and fold_test for SEQUENCES
>>>>>>> ed792e921c7e16c27e40524cdc76cebe6054a464

        X_train, y_train = fold_train, fold_train['return']

        X_test, y_test = fold_test, fold_test['return']

        # instantiate the model chosen as a parameter
        model = model
        # fit model on each X_train, y_train
        model.fit(X_train, y_train)

        rmse_model = (mean_squared_error(y_test, model.predict(X_test)))**0.5
        scores.append(rmse_model)

    return np.mean(scores)
