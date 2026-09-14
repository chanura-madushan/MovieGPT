from sklearn.feature_extraction.text import TfidfVectorizer
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


df["duration_minutes"] = df["duration"].str.extract(         #Extract durations for movies
    r"(\d+)\s*min"
)[0]

df["duration_minutes"] = pd.to_numeric(     # Convert to numeric
    df["duration_minutes"],
    errors="coerce"
)

df["seasons"] = df["duration"].str.extract(
    r"(\d+)\s*Season",
    expand=False
)

df["seasons"] = pd.to_numeric(      #convert to numeric
    df["seasons"],
    errors="coerce"
)
    

df.to_csv("data/netflix_cleaned.csv", index=False)

print(df.shape)
print(df.isnull().sum())


print(df[["title", "type", "duration", "duration_minutes", "seasons"]])


df["combine_features"] = (
    df["title"]+" "
    + df["director"] + " "
    + df["cast"] + " "
    + df["country"] + " "
    + df["listed_in"] + " "
    + df["description"]
)
print(df[["title", "combine_features"]].head(10))



                                                         #VECTORIZITATION..........
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(df["combine_features"])
print(tfidf_matrix.shape)



