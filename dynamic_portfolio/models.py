from sklearn.linear_model import LinearRegression, SGDRegressor, HuberRegressor
from sklearn.linear_model import Lars, Lasso, RANSACRegressor, Ridge, TheilSenRegressor
from sklearn.linear_model import ElasticNet
from sklearn.ensemble import RandomForestRegressor, BaggingRegressor, AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor, VotingRegressor, StackingRegressor
from sklearn.svm import SVR
from xgboost import XGBRegressor
from sklearn.neighbors import KNeighborsRegressor

from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np
import joblib
from sklearn.base import TransformerMixin, BaseEstimator


class FeatureImportance(TransformerMixin, BaseEstimator):
    def __init__(self,threshold=1e-15):
        self.threshold = threshold
    def fit(self, X, y):
        self.rf = RandomForestRegressor().fit(X,y)
        return self
    def transform(self, X, y=None):
        r = np.where(self.rf.feature_importances_>self.threshold)[0]
        return X[:,r.tolist()]

def train_model(df:pd.DataFrame,name:str="model"):
    """train and fine tune XGboost model and save it as pikkle """
#preprocess step for the input df
# #train process for model
    model = make_pipeline(FeatureImportance(), XGBRegressor())
    # find a way to add the treshold as parameter for the gridsearch
    # gridsearch or randomizedsearch ?
    #GridsearchCV for fine_tuned
    #remember to add some print
    search = GridSearchCV()
    model = search.best_estimator_

    #save model
    joblib.dump(model, "model/XGBoost_model.joblib")
