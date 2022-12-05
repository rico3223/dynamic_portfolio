# importing relevant librairies
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error

cross_val = {
    'fold_length' : 252, # Working days for 1 year
    'fold_stride' : 60, # Step between folds, here one quarter
    'train_test_ratio' : 0.7, # Split in fold
    'input_length' : 0, # Number of days to move back from last train_index, here 0
    'horizon' : 1, # Number of days ahead to make prediction, here 1
    'output_length' : 1, # Number of targets wanted
}


#Split the dataset by FOLDS
def get_folds(
    df: pd.DataFrame,
    fold_length = cross_val['fold_length'],
    fold_stride = cross_val['fold_stride']):
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
                     train_test_ratio = cross_val['train_test_ratio'],
                     input_length = cross_val['input_length']):
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
    first_test_idx = last_train_idx - input_length # faut il pas changer le - en + ??
    fold_test = fold.iloc[first_test_idx:, :]

    return (fold_train, fold_test)

<<<<<<< HEAD
# est ce que les train et test set n s'entremelent pas ?
# changer le ticker BF-B dans la fonction tickers





#Loop for split on FOLDS
def cross_validate_dl(df:pd.DataFrame, fold_length:int, fold_stride:int) :
=======





def cross_validate_ml(df, model) :
>>>>>>> f8b85e15bd7ca44027c08c380f629f83e2b51802
    '''
    get_folds() create many FOLDS, train_test_split() create a split on ONE FOLDS.
    The goal of this function is to make splits and sequences on each FOLDS.
    Then, apply a model.
    '''
    folds = get_folds(df, fold_length = cross_val['fold_length'], fold_stride = cross_val['fold_stride']) # 1 - Creating FOLDS
    scores =[]
    for fold in folds:

        # 2 - CHRONOLOGICAL TRAIN TEST SPLIT of the current FOLD

        (fold_train, fold_test) = train_test_split(fold = fold,
<<<<<<< HEAD
                                                train_test_ratio = train_test_ratio,
                                                input_length = input_length ,
                                                horizon = horizon)

        # 3 - Scanninng fold_train and fold_test for SEQUENCES

        X_train, y_train = get_X_y(fold = fold_train,
                                horizon = horizon,
                                input_length = input_length ,
                                output_length = output_length,
                                stride = stride )

        X_test, y_test = get_X_y(fold_test,
                                horizon = horizon,
                                input_length = input_length,
                                output_length = output_length,
                                stride = stride)

        #Rajouter le modèle


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
=======
                                                train_test_ratio = cross_val['train_test_ratio'],
                                                input_length = cross_val['input_length'] ,
                                                )
>>>>>>> f8b85e15bd7ca44027c08c380f629f83e2b51802

        # 3 - Scanninng fold_train and fold_test for SEQUENCES

        X_train, y_train = fold_train, fold_train['return']

        X_test, y_test = fold_test, fold_test['return']

        model = model()
        model.fit(X_train, y_train)
        rmse_model = (mean_squared_error(y_test, model.predict(X_test)))**0.5
        scores.append(rmse_model)

    return np.mean(scores)
