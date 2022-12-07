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






def cross_validate_ml(df, model) :
    '''
    get_folds() create many FOLDS, train_test_split() create a split on ONE FOLDS.
    The goal of this function is to make splits and sequences on each FOLDS.
    Then, apply a model.
    '''
    folds = get_folds(df, fold_length = cross_val['fold_length'], fold_stride = cross_val['fold_stride']) # 1 - Creating FOLDS
    scores =[]
    baseline = []
    for fold in folds:
        # 2 - CHRONOLOGICAL TRAIN TEST SPLIT of the current FOLD
        (fold_train, fold_test) = train_test_split(fold = fold,
                                                train_test_ratio = cross_val['train_test_ratio'],
                                                input_length = cross_val['input_length'] ,
                                                )
        # 3 - Scanninng fold_train and fold_test for SEQUENCES
        X_train, y_train = fold_train, fold_train[['return']].shift(1).replace(np.nan,0)
        X_test, y_test = fold_test, fold_test[['return']].shift(1).replace(np.nan,0)

        model.fit(X_train, y_train)
        rmse_model = (mean_squared_error(y_test, model.predict(X_test)))**0.5
        scores.append(rmse_model)
        rmse_baseline = mean_squared_error(y_test.iloc[[0]], y_train.iloc[[-1]])**0.5
        baseline.append(rmse_baseline)

    return np.mean(scores), np.mean(baseline)

#Custom gridsearch a titre informatif, ce gridsearch nous a permis de choisir le meilleur modele avec les meilleurs hyperparametres
# En fonction des models, les arguments dans la fonction devrait changer
def custom_gridsearch(df, model, max_depth=[2,3,4], criterion = ['friedman_mse', 'squared_error', 'mse'], n_estimator=[50, 75, 100], learning_rate=[0.08, 0.1, 0.12], loss=['squared_error', 'absolute_error', 'huber']):
    counter = 0
    rmse = []
    baseline = []
    params = []
    for max_depth_i in max_depth:
        for criterion_i in criterion:
            for n_estimator_i in n_estimator:
                for learning_rate_i in learning_rate:
                    for loss_i in loss:
                        test = cross_validate_ml(df = df, model = model(max_depth=max_depth_i,
                                                                   criterion = criterion_i,
                                                                   n_estimators = n_estimator_i,
                                                                   learning_rate = learning_rate_i,
                                                                   loss = loss_i))
                        rmse.append(test[0])
                        baseline.append(test[1])
                        params.append((max_depth_i, criterion_i, n_estimator_i, learning_rate_i))
                        counter += 1
                        print(f'model {counter} done with parameters: max_depth = {max_depth_i}, criterion = {criterion_i}, estimators = {n_estimator_i}, learning rate = {learning_rate_i}, loss = {loss_i}, rmse = {test[0]}')
    idx_min = np.argmin(rmse)
    best_params = params[idx_min]

    return best_params, rmse, params
