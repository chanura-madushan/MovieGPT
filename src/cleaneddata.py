import pandas as pd

df = pd.read_csv("data/netflix_titles.csv")

print(df.shape)
print(df["type"].value_counts())

print(df[df["type"]=="Movie"][["title", "release_year", "duration"]].head())    #Show me the title, release year, and duration of movies.
print(df[df["type"]=="TV Show"][["title", "release_year", "duration"]].head())  #Show me the title, release year, and duration of tv shows.

