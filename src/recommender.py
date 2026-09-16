import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv("data/netflix_cleaned.csv")
print(df.shape)

df["combine_features"] = (
    df["title"] + " "
    + df["director"] + " "
    + df["cast"] + " "
    + df["country"] + " "
    + df["listed_in"] + " "
    + df["description"]
)



tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(df["combine_features"])
print(tfidf_matrix.shape)