from sklearn.linear_model import LinearRegression, SGDRegressor, HuberRegressor
from sklearn.linear_model import Lars, Lasso, RANSACRegressor, Ridge, TheilSenRegressor
from sklearn.linear_model import ElasticNet
from sklearn.ensemble import RandomForestRegressor, BaggingRegressor, AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor, VotingRegressor, StackingRegressor
from sklearn.svm import SVR
from xgboost import XGBRegressor
from sklearn.neighbors import KNeighborsRegressor

def model_linear_regression():
    model_lr = LinearRegression().fit(X_train, y_train)
    model_lr.score(X_test, y_test)

def model_knn():
    model_knn = KNeighborsRegressor(n_neighbors=2).fit(X_train, y_train)

def model_sgdr():
    model_lin_reg_sgd = SGDRegressor(loss='squared_error').fit(X_train, y_train)
    model_lin_reg_sgd.score(X_test, y_test)

def model_huberr():
    model_huberr = HuberRegressor().fit(X_train, y_train)
    model_huberr.score(X_test, y_test)

def model_lars():
    model_lars = Lars().fit(X_train, y_train)
    model_lars.score(X_test, y_test)

def model_lasso():
    model_lasso = Lasso().fit(X_train, y_train)
    model_lasso.score(X_test, y_test)

def model_ransacr():
    model_ransacr = RANSACRegressor().fit(X_train, y_train)
    model_ransacr.score(X_test, y_test)

def model_ridge():
    model_ridge = Ridge().fit(X_train, y_train)
    model_ridge.score(X_test, y_test)

def model_theilsenr():
    model_theilsenr = TheilSenRegressor().fit(X_train, y_train)
    model_theilsenr.score(X_test, y_test)

def model_svr():
    model_svr = SVR().fit(X_train, y_train)
    model_svr.score(X_test, y_test)

def model_elasticnet():
    model_elasticnet = ElasticNet().fit(X_train, y_train)
    model_elasticnet.score(X_test, y_test)

def model_forestreg():
    model_forestreg = RandomForestRegressor().fit(X_train, y_train)
    model_forestreg.score(X_test, y_test)

def model_baggingr():
    model_baggingr = BaggingRegressor().fit(X_train, y_train)
    model_baggingr.score(X_test, y_test)

def model_daboostr():
    model_daboostr = AdaBoostRegressor().fit(X_train, y_train)
    model_daboostr.score(X_test, y_test)

def model_gradboostr():
    model_gradboostr = GradientBoostingRegressor().fit(X_train, y_train)
    model_gradboostr.score(X_test, y_test)

def model_XGBR():
    model_XGBR = XGBRegressor().fit(X_train, y_train)
    model_XGBR.score(X_test, y_test)


def model_Votingr():
    model_Votingr = VotingRegressor().fit(X_train, y_train)
    model_Votingr.score(X_test, y_test)


def model_stackingr():
    model_stackingr = StackingRegressor().fit(X_train, y_train)
    model_stackingr.score(X_test, y_test)
