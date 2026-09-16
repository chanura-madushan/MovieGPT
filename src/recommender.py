import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("data/netflix_cleaned.csv")


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



similarity_matrix = cosine_similarity(tfidf_matrix)



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

    recommendations = []

    for i in similarity_scores[1:6]:
        recommendations.append(df.iloc[i[0]]["title"])

    return recommendations

def clean_text(text):
    return text.lower().replace("&", "and")


def find_title(user_input):
    user_input = clean_text(user_input)
    for title in df["title"]:
        clean_title = clean_text(title)

        if len(clean_title) < 3:
            continue
        if clean_title in user_input:
            return title
    return None
