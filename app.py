import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

# Load the movies dataset
movies = pd.read_csv('tmdb_5000_movies.csv')

# Clean the genres column
movies['genres'] = movies['genres'].apply(lambda x: [genre['name'] for genre in eval(x)])

# Combine relevant columns into tags
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
movies['tags'] = movies['tags'].apply(lambda x: " ".join(x))

# Create a CountVectorizer to convert tags into vectors
cv = CountVectorizer(max_features=5000, stop_words='english')
tags_vector = cv.fit_transform(movies['tags']).toarray()

# Calculate cosine similarity
cosine_sim = cosine_similarity(tags_vector)

# Define a function to recommend similar movies
def recommend(movie_title):
    movie_index = movies[movies['title'] == movie_title].index[0]
    similar_movies = list(enumerate(cosine_sim[movie_index]))
    sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)
    recommended_movies = sorted_similar_movies[1:6]  # Exclude the first entry (self-movie)
    recommended_movie_names = [movies.iloc[movie[0]]['title'] for movie in recommended_movies]
    return recommended_movie_names

# Streamlit interface
st.header('Movie Recommender System')

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movies['title'].values
)

if st.button('Show Recommendation'):
    recommended_movie_names = recommend(selected_movie)
    if recommended_movie_names:
        st.success("Recommended Movies:")
        for movie_name in recommended_movie_names:
            st.text(movie_name)
    else:
        st.warning("No recommendations found.")
