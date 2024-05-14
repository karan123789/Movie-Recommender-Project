import pickle
import streamlit as st
import requests

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
        # Get the genre of the selected movie
        selected_movie_genre = movies[movies['title'] == movie]['genres'].values[0]

        # Filter movies by genre (content-based filtering)
        similar_movies = movies[movies['genres'].apply(lambda x: selected_movie_genre in x)]

        if len(similar_movies) > 5:
            # Get top 5 similar movies
            recommended_movie_names = similar_movies['title'].values[:5]
            recommended_movie_posters = [fetch_poster(movie_id) for movie_id in similar_movies['movie_id'].values[:5]]
        else:
            recommended_movie_names = similar_movies['title'].values
            recommended_movie_posters = [fetch_poster(movie_id) for movie_id in similar_movies['movie_id'].values]

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
