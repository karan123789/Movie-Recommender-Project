import pickle
import streamlit as st
import requests
import random
import numpy as np

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    if 'poster_path' in data:
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        full_path = "https://via.placeholder.com/500x750.png?text=Poster+Not+Available"
    return full_path

def calculate_similarity(selected_genre, movie_genre):
    # Calculate Jaccard similarity between two genre lists
    selected_set = set(selected_genre)
    movie_set = set(movie_genre)
    intersection = len(selected_set.intersection(movie_set))
    union = len(selected_set.union(movie_set))
    similarity = intersection / union if union > 0 else 0
    return similarity

def recommend(movie):
    try:
        # Check if 'genres' column exists in movies DataFrame
        if 'genres' in movies.columns:
            # Get the genre of the selected movie
            selected_movie_genre = movies[movies['title'] == movie]['genres'].values[0]

            # Calculate similarity scores for all movies based on genre
            movies['similarity'] = movies['genres'].apply(lambda x: calculate_similarity(selected_movie_genre, x))

            # Sort movies by similarity score in descending order
            similar_movies = movies.sort_values(by='similarity', ascending=False)

            if len(similar_movies) > 5:
                # Get top 5 similar movies
                recommended_movie_names = similar_movies['title'].values[1:6]
                recommended_movie_posters = [fetch_poster(movie_id) for movie_id in similar_movies['movie_id'].values[1:6]]
            else:
                recommended_movie_names = similar_movies['title'].values[1:]
                recommended_movie_posters = [fetch_poster(movie_id) for movie_id in similar_movies['movie_id'].values[1:]]

        else:
            # If 'genres' column is missing, recommend random movies
            random_movies = random.sample(list(movies['title']), 5)
            recommended_movie_names = random_movies
            recommended_movie_posters = [fetch_poster(random.choice(movies['movie_id'])) for _ in range(5)]

    except Exception as e:
        st.error("Error occurred while recommending movies.")
        st.error(str(e))
        recommended_movie_names = []
        recommended_movie_posters = []

    return recommended_movie_names, recommended_movie_posters

st.header('Movie Recommender System')

# Load movie list (assuming this file still exists)
movies = pickle.load(open('movie_list.pkl', 'rb'))
movie_list = movies['title'].values

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    for i in range(len(recommended_movie_names)):
        with st.container():
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])
