import pandas as pd

df = pd.read_csv("data/netflix_titles.csv")

print(df.shape)
print(df["type"].value_counts())

