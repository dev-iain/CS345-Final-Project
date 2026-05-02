from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import pandas as pd

df = pd.read_csv("datasets/games_raw.csv")
df = df.dropna()


X = df.drop(columns = ["rating", "id"])
y = df["rating"]

train_X, test_X, train_y, test_y = train_test_split(X, y, test_size = 0.2, random_state = 42)

rand_forest = RandomForestRegressor(n_estimators = 100, random_state = 42)

rand_forest.fit(train_X, train_y)
pred_y = rand_forest.predict(test_X)

rmse = np.sqrt(mean_squared_error(test_y, pred_y))

r2 = r2_score(test_y, pred_y)

print("RMSE:", rmse)
print("R2:", r2)

importances = rand_forest.feature_importances_
feature_names = X.columns

feature_df = pd.DataFrame({
    "feature": feature_names,
    "importance": importances
}).sort_values(by = "importance", ascending = False)

print(feature_df)