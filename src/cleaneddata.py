import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer



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



                                                         #VECTORIZITATION = Turns words to numbers
                                                         
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(df["combine_features"])
print(tfidf_matrix.shape)


                                                         #COSINE SIMILARITY = Compares the numbers to find similarities

similarity_matrix=cosine_similarity(tfidf_matrix)
print(similarity_matrix.shape)




def recommend(title):
    matching_titles = df[df["title"].str.lower() == title.lower()]

    if matching_titles.empty:
        return ["Sorry, I could not find that title."]
    index = matching_titles.index[0]


    similarity_scores = list(enumerate(similarity_matrix[index]))
    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = []        #creates an empty list

    for i in similarity_scores[1:6]:
        recommendations.append(df.iloc[i[0]]["title"])

    return recommendations



##test the output
#print(recommend("Avengers"))
#print(recommend("blood & water"))