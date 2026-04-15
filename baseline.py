import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("datasets/games_raw.csv")
print(df.to_string(max_rows=100))
nan_rows = df.isna().any(axis=1)
df = df[~nan_rows]

X = df.iloc[:, :-1]
print(X)

y = np.array((df.iloc[:, -1] > 0), dtype=np.int64)
print(y)