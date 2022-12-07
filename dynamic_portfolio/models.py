from sklearn.linear_model import LinearRegression, SGDRegressor, HuberRegressor
from sklearn.linear_model import Lars, Lasso, RANSACRegressor, Ridge, TheilSenRegressor
from sklearn.linear_model import ElasticNet
from sklearn.ensemble import RandomForestRegressor, BaggingRegressor, AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor, VotingRegressor, StackingRegressor
from sklearn.svm import SVR
import preprocess as prep
from xgboost import XGBRegressor
from sklearn.neighbors import KNeighborsRegressor
import  dynamic_portfolio.utils as utils
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np
import joblib
from sklearn.base import TransformerMixin, BaseEstimator
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)



class FeatureImportance(TransformerMixin, BaseEstimator):
    def __init__(self,threshold=1e-15):
        self.threshold = threshold
    def fit(self, X, y):
        self.rf = RandomForestRegressor().fit(X,y)
        return self
    def transform(self, X, y=None):
        r = np.where(self.rf.feature_importances_>self.threshold)[0]
        return X[:,r.tolist()]

def full_training(force_retrain=False, model=XGBRegressor):
    tickers = utils.return_tickers()
    for ticker in tickers:
        X_train = prep.ready_to_train_df(ticker)
        y_train = prep.ready_to_train_df(ticker)['return'].shift(1).replace(np.nan,0)
        if not force_retrain :
            try :
                model = joblib.load(f"raw_data/models/{ticker}_XGBoostDefault.joblib")
            except :
                model = model(n_jobs=-1)
                print("fitting model...")
                model.fit(X_train, y_train)
                joblib.dump(model, f"raw_data/models/{ticker}_XGBoostDefault.joblib")
        else :
            model = model(n_jobs=-1)
            print("fitting model...")
            model.fit(X_train, y_train)
            joblib.dump(model, f"raw_data/models/{ticker}_GradientBoostingDefault.joblib")


def pred():
    tickers = utils.return_tickers()
    preds = []
    for ticker in tickers:
        model = joblib.load(f"raw_data/models/{ticker}_GradientBoostingDefault.joblib")
        X_test = prep.ready_to_test_df(ticker)
        pred_ticker = pd.DataFrame(model.predict(X_test),columns=[f"{ticker}"], index = X_test.index)
        preds.append(pred_ticker)
        print(f"ticker {ticker} done index # {tickers.index(ticker)}")
    final_df = pd.concat(preds, axis=1)
    final_df = final_df.loc['2021-01-04':].dropna(axis=1)
    final_df.to_csv("raw_data/results/gradientboosting_pred.csv")



if __name__=="__main__":
    full_training()
    pred()
