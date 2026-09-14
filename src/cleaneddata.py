import pandas as pd

df = pd.read_csv("data/netflix_titles.csv")


#print(df.shape)
#print(df["type"].value_counts())


#print(df[df["type"] == "Movie"][["title", "release_year", "duration"]].head())      # Show me the title, release year, and duration of movies.


#print(df[df["type"] == "TV Show"][["title", "release_year", "duration"]].head())    # Show me the title, release year, and duration of tv shows.


#for content_type in ["Movie", "TV Show"]:                                           # Null values in each content type
#    print(f"\n{content_type}:")
#   print(df[df["type"] == content_type].isnull().sum())

df=df.drop(columns=["show_id","date_added"])

text_columns=["director","cast","country"]
for columns in text_columns:
    df[columns]=df[columns].fillna("unknown")

df["rating"]=df["rating"].fillna("unknown")
df["duration"]=df["duration"].fillna("unknown")

df.to_csv("data/netlfix_cleaned.csv", index=False)

print(df.shape)
print(df.isnull().sum())