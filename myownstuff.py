import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression

data = pd.read_csv("datasets/games_raw.csv", index_col="id")
data = data.dropna()
vectorized = data.to_numpy(dtype=np.float32)

print(data.to_string(max_rows=10))
# X = vectorized[:, 0] #aggregated score

# y = vectorized[:, 5] #positive reviews
moredata = data[["aggregated_rating", "normalized"]]

data["averaged"] = ((data["aggregated_rating"] + data["rating"]) / 2)
print(data.to_string(max_rows = 10))
X = data[["averaged"]]
y = moredata["normalized"]
reg=LinearRegression().fit(X,y)
print("R^2:", reg.score(X,y))
print("Slope:", reg.coef_[0])
# Scatter plot of actual data
plt.scatter(X, y, alpha=0.5)

# Plot regression line
y_pred = reg.predict(X)
plt.plot(X, y_pred)

plt.xlabel("Aggregated Rating")
plt.ylabel("Positive Reviews")
plt.title("Linear Regression: Critic Reviews vs Player Reviews")
plt.show()
