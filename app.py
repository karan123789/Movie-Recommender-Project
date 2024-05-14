import pickle
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load movie list (assuming this file still exists)
movies = pd.read_csv('tmdb_5000_movies.csv')
movies = movies[['movie_id', 'title', 'tags']]

# Drop rows with missing tags
movies.dropna(subset=['tags'], inplace=True)

# Function to fetch poster path (you can modify this as needed)
def fetch_poster(movie_id):
    return f"https://image.tmdb.org/t/p/w500/{movie_id}"

# Calculate cosine similarity
cv = CountVectorizer(max_features=5000, stop_words='english')
vector = cv.fit_transform(movies['tags']).toarray()
similarity = cosine_similarity(vector)

def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

        recommended_movies = []
        recommended_posters = []

        for i in distances[1:6]:
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_posters.append(fetch_poster(movies.iloc[i[0]].movie_id))

    except Exception as e:
        st.error("Error occurred while recommending movies.")
        st.error(str(e))
        recommended_movies = []
        recommended_posters = []

    return recommended_movies, recommended_posters

st.header('Movie Recommender System')

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
