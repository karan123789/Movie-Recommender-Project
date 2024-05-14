import pandas as pd
import streamlit as st
import random

# Load the movies dataset
movies = pd.read_csv('tmdb_5000_movies.csv')

def recommend(movie_title):
    try:
        # Get the row corresponding to the selected movie
        selected_movie = movies[movies['original_title'] == movie_title]

        # Get the keywords, genre, ID, budget, and popularity of the selected movie
        selected_keywords = selected_movie['keywords'].iloc[0]
        selected_genre = selected_movie['genres'].iloc[0]
        selected_id = selected_movie['id'].iloc[0]
        selected_budget = selected_movie['budget'].iloc[0]
        selected_popularity = selected_movie['popularity'].iloc[0]

        # Filter movies by keywords, genre, ID, budget, and popularity
        similar_movies = movies[
            (movies['keywords'].str.contains(selected_keywords)) &
            (movies['genres'].str.contains(selected_genre)) &
            (movies['id'] != selected_id) &
            (movies['budget'] <= selected_budget * 1.5) &  # Allowing for 50% difference in budget
            (movies['popularity'] >= selected_popularity * 0.8)  # Only recommend popular movies (80% of selected movie's popularity)
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
