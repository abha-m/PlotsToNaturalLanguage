import pandas as pd
from sklearn import preprocessing

df = pd.read_csv("data/Influenza_NY.csv")
df = df.dropna()
df = df.drop('Unnamed: 0', axis=1)
filtered_by_county_df = df[df["County"] == "ALBANY"]
numeric_cols = list(filtered_by_county_df.corr().columns)

x = filtered_by_county_df[numeric_cols].values #returns a numpy array
min_max_scaler = preprocessing.StandardScaler()
x_scaled = min_max_scaler.fit_transform(x)
df = pd.DataFrame(x_scaled, columns=numeric_cols)
df.corr().fillna(0).to_csv("test.csv")