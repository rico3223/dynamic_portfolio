# importing relevant librairies
import numpy as np
import pandas as pd
from dynamic_portfolio.params import cross_val

#Split the dataset by FOLDS
def get_folds(
    df: pd.DataFrame,
    fold_length: int,
    fold_stride: int):
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
#### FOR ONE FOLDS !!!!!
def train_test_split(fold: pd.DataFrame,
                     train_test_ratio: float,
                     input_length: int,
                     horizon: int) :
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
    first_test_idx = last_train_idx - input_length
    fold_test = fold.iloc[first_test_idx:, :]

    return (fold_train, fold_test)


#One sequences
### Use in tht next one function
def get_Xi_yi(first_index: int,
              fold: pd.DataFrame,
              horizon: int,
              input_length: int,
              output_length: int):
    '''
    - extracts one sequence from a fold
    - returns a pair (Xi, yi) with:
        * len(Xi) = `input_length` and Xi starting at first_index
        * len(yi) = `output_length`
        * last_Xi and first_yi separated by the gap = horizon -1
    '''

    Xi_start = first_index
    Xi_last = Xi_start + input_length
    yi_start = Xi_last + horizon - 1
    yi_last = yi_start + output_length

    Xi = fold[Xi_start:Xi_last]
    yi = fold[yi_start:yi_last][TARGET]

    return (Xi, yi)


#Many sequences
def get_X_y(fold: pd.DataFrame,
            horizon: int,
            input_length: int,
            output_length: int,
            stride: int,
            shuffle=True):
    """
    - Uses `data`, a 2D-array with axis=0 for timesteps, and axis=1 for (targets+covariates columns)
    - Returns a Tuple (X,y) of two ndarrays :
        * X.shape = (n_samples, input_length, n_covariates)
        * y.shape =
            (n_samples, output_length, n_targets) if all 3-dimensions are of size > 1
            (n_samples, output_length) if n_targets == 1
            (n_samples, n_targets) if output_length == 1
            (n_samples, ) if both n_targets and lenghts == 1
    - You can shuffle the pairs (Xi,yi) of your fold
    """

    X = []
    y = []

    for i in range(0, len(fold), stride):
        ## Extracting a sequence starting at index_i
        Xi, yi = get_Xi_yi(first_index=i,
                           fold=folds_test,
                           horizon=horizon,
                           input_length=input_length,
                           output_length=output_length)
        ## Exits loop as soon as we reach the end of the dataset
        if len(yi) < output_length:
            break
        X.append(Xi)
        y.append(yi)

    X = np.array(X)
    y = np.array(y)
    y = np.squeeze(y)

    if shuffle:
        idx = np.arange(len(X))
        np.random.shuffle(idx)
        X = X[idx]
        y = y[idx]

    return X, y


#Loop for split on FOLDS
def cross_validate_dl() :
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


def cross_validate_ml() :
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

        X_train, y_train = fold_train.drop(columns='return'), fold_train['return']

        X_test, y_test = fold_test.drop(columns='return'), fold_test['return']

        #Rajouter le modèle
