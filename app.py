import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the movies data
movies = pd.read_csv('tmdb_5000_movies.csv')

# Check for and handle missing values
movies = movies.dropna(subset=['overview'])
movies = movies.reset_index(drop=True)

# Preprocess the overview text
vectorizer = CountVectorizer(stop_words='english')
overview_matrix = vectorizer.fit_transform(movies['overview'])

# Compute the cosine similarity matrix
cosine_sim = cosine_similarity(overview_matrix, overview_matrix)

# Function to get movie recommendations
def get_recommendations(movie_title, cosine_sim_matrix, movies_data):
    # Get the index of the movie title
    idx = movies_data[movies_data['original_title'] == movie_title].index[0]

    # Get the pairwise similarity scores
    sim_scores = list(enumerate(cosine_sim_matrix[idx]))

    # Sort the movies based on similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the top 10 similar movies (excluding the input movie itself)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    recommended_movies = movies_data.iloc[movie_indices]

    return recommended_movies

# Streamlit app
st.title('Movie Recommender System')

# Sidebar for user input
st.sidebar.title('Select a Movie')
selected_movie = st.sidebar.selectbox('Choose a movie:', movies['original_title'])

# Get recommendations based on user input
recommended_movies = get_recommendations(selected_movie, cosine_sim, movies)

# Display the selected movie and recommendations
st.write(f'### Selected Movie: {selected_movie}')
st.dataframe(movies[movies['original_title'] == selected_movie][['original_title', 'poster_path']])

st.write('### Recommended Movies:')
st.dataframe(recommended_movies[['original_title', 'poster_path']])
