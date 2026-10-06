import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors


# Load the cleaned dataset
df = pd.read_csv("data/netflix_cleaned.csv")


# Create one big text column for each movie/show
df["combine_features"] = (
    df["title"] + " "
    + df["director"] + " "
    + df["cast"] + " "
    + df["country"] + " "
    + df["listed_in"] + " "
    + df["description"]
)


# Convert text into numbers
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(df["combine_features"])


# Create a model that finds the nearest/similar titles
model = NearestNeighbors(
    metric="cosine",
    algorithm="brute"
)

model.fit(tfidf_matrix)


def recommend(title):

    # Find the title in the dataset
    matching_titles = df[
        df["title"].str.lower() == title.lower()
    ]

    # If title does not exist
    if matching_titles.empty:
        return ["Sorry, I could not find that title."]

    # Get the row number
    index = matching_titles.index[0]

    # Get the movie/show vector
    movie_vector = tfidf_matrix[index]

    # Find the 6 closest titles
    distances, indices = model.kneighbors(
        movie_vector,
        n_neighbors=6
    )

    recommendations = []

    # Skip the first result because it is the movie itself
    for i in indices[0][1:]:
        recommendations.append(df.iloc[i]["title"])

    return recommendations


def clean_text(text):
    # Make text lowercase
    # Treat & and "and" as the same
    return text.lower().replace("&", "and")


def find_title(user_input):

    # Clean what the user typed
    user_input = clean_text(user_input)

    # Check every title
    for title in df["title"]:

        # Clean dataset title
        clean_title = clean_text(title)

        # Ignore extremely short titles
        if len(clean_title) < 3:
            continue

        # Check if title appears in user's sentence
        if clean_title in user_input:
            return title

    # No title found
    return None