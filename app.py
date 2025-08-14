import pickle
import streamlit as st
import requests
import random
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
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
def recommend(movie):
    try:
        # Check if necessary columns exist in movies DataFrame
        if 'genres' in movies.columns and 'keywords' in movies.columns and 'tags' in movies.columns:
            # Get genre, keywords, and tags of the selected movie
            selected_movie_genre = movies[movies['title'] == movie]['genres'].values[0]
            selected_movie_keywords = movies[movies['title'] == movie]['keywords'].values[0]
            selected_movie_tags = movies[movies['title'] == movie]['tags'].values[0]
            # Combine genres, keywords, and tags into a single text column
            movies['combined_features'] = movies['genres'] + ' ' + movies['keywords'] + ' ' + movies['tags']
            # Create TF-IDF vectors for combined features
            tfidf_vectorizer = TfidfVectorizer()
            tfidf_matrix = tfidf_vectorizer.fit_transform(movies['combined_features'])
            # Compute cosine similarity between selected movie and all other movies
            selected_movie_index = movies[movies['title'] == movie].index[0]
            cosine_similarities = cosine_similarity(tfidf_matrix[selected_movie_index:selected_movie_index+1], tfidf_matrix).flatten()
            # Sort movies by cosine similarity scores in descending order
            similar_movies_indices = cosine_similarities.argsort()[::-1][1:]  # Exclude the selected movie
            similar_movies = movies.iloc[similar_movies_indices]
            if len(similar_movies) > 5:
                # Get top 5 similar movies
                recommended_movie_names = similar_movies['title'].values[:5]
                recommended_movie_posters = [fetch_poster(movie_id) for movie_id in similar_movies['movie_id'].values[:5]]
            else:
                recommended_movie_names = similar_movies['title'].values
                recommended_movie_posters = [fetch_poster(movie_id) for movie_id in similar_movies['movie_id'].values]
        else:
            # If required columns are missing, recommend random movies
            random_movies = random.sample(list(movies['title']), 5)
            recommended_movie_names = random_movies
            recommended_movie_posters = [fetch_poster(random.choice(movies['movieid'])) for  in range(5)]
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
