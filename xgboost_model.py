import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score

df = pd.read_csv("datasets/games_raw.csv")
df = df.dropna()

X = df.drop(columns = ["aggregated_rating", "id"])
y = df["aggregated_rating"]

train_X, test_X, train_y, test_y = train_test_split(X, y, test_size = 0.2, random_state = 42)

print("Running basic XGBoost")

xgb = XGBRegressor(random_state = 42)
xgb.fit(train_X, train_y)
pred_y = xgb.predict(test_X)

rmse = np.sqrt(mean_squared_error(test_y, pred_y))
r2 = r2_score(test_y, pred_y)

print("Basic RMSE: ", rmse)
print("Basic R2: ", r2)

print("\nRunning GridSearch")

param_grid = {
    "n_estimators": [50, 100],
    "max_depth": [3, 5],
    "learning_rate": [0.1, 0.2],
    "subsample": [0.8, 1.0]
}

xgb_model = XGBRegressor(random_state = 42)

grid = GridSearchCV(
    xgb_model,
    param_grid,
    scoring="r2",
    cv=3,
    n_jobs=-1
)

grid.fit(train_X, train_y)

print("Best parameters: ", grid.best_params_)
print("Best CV score: ", grid.best_score_)

best_model = grid.best_estimator_
pred_y = best_model.predict(test_X)

rmse = np.sqrt(mean_squared_error(test_y, pred_y))
r2 = r2_score(test_y, pred_y)

print("\nTuned RMSE: ", rmse)
print("Tunded R2: ", r2)

print("\nFeature Importance: ")
importances = best_model.feature_importances_

feat_df = pd.DataFrame({
    "feature": X.columns,
    "importance": importances
})

feat_df = feat_df.sort_values(by = "importance", ascending = False)

print(feat_df)
