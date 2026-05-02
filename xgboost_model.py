import xgboost as xgb
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

df = pd.read_csv("datasets/games_raw.csv")
df = df.dropna()

X = df.drop(columns = ["aggregated_rating", "id"])
y = df["aggregated_rating"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

#use approx methods, not exact; max depth can be configured
params = {
    'max_depth': 1, 
    'tree_method': 'approx', 
    'objective': 'reg:squarederror',
    'eval_metric': 'rmse',
    'seed': 42
    }


# early stopping rounds is used to prevent overfitting for test set
bst = xgb.train(params, dtrain, num_boost_round=100, evals=[(dtrain, "train"), (dtest, "test")], early_stopping_rounds=5)


y_pred = bst.predict(dtest)

xgb_rmse = np.sqrt(mean_squared_error(y_test, y_pred))
xgb_r2 = r2_score(y_test, y_pred)
xgb_r = np.sqrt(xgb_r2)
print("XGBoost RMSE:", xgb_rmse)
print("XGBoost R^2:", xgb_r2)
print("XGBoost R:", xgb_r)