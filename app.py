import pandas as pd
import streamlit as st
import random

# Load the movies dataset
movies = pd.read_csv('tmdb_5000_movies.csv')

def recommend(movie_title):
    try:
        # Get the row corresponding to the selected movie
        selected_movie = movies[movies['original_title'] == movie_title]

        # Get the genre, keywords, and ID of the selected movie
        selected_genre = selected_movie['genres'].iloc[0]
        selected_keywords = selected_movie['keywords'].iloc[0]
        selected_id = selected_movie['id'].iloc[0]

        # Filter movies by genre, keywords, and ID
        similar_movies = movies[
            (movies['genres'].str.contains(selected_genre)) &
            (movies['keywords'].str.contains(selected_keywords)) &
            (movies['id'] != selected_id)
        ]

        # Get top 5 similar movies by popularity
        recommended_movies = similar_movies.nlargest(5, 'popularity')

        return recommended_movies[['original_title', 'poster_path']].values.tolist()
    except Exception as e:
        st.error("Error occurred while recommending movies.")
        st.error(str(e))
        return []

st.header('Movie Recommender System')

# Create a dropdown to select a movie
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movies['original_title'].values
)

if st.button('Show Recommendation'):
    recommended_movies = recommend(selected_movie)
    if recommended_movies:
        for movie_name, poster_path in recommended_movies:
            st.text(movie_name)
            st.image(f"https://image.tmdb.org/t/p/w500/{poster_path}")
    else:
        st.warning("No recommendations found.")
