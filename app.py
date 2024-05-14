import pickle
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load movie list (assuming this file still exists)
movies = pd.read_csv('tmdb_5000_movies.csv')
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

def convert(text):
    L = []
    for i in ast.literal_eval(text):
        L.append(i['name']) 
    return L 

def convert3(text):
    L = []
    counter = 0
    for i in ast.literal_eval(text):
        if counter < 3:
            L.append(i['name'])
        counter += 1
    return L 

def fetch_director(text):
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            L.append(i['name'])
    return L 

def collapse(L):
    L1 = []
    for i in L:
        L1.append(i.replace(" ",""))
    return L1

movies.dropna(inplace=True)
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert3)
movies['cast'] = movies['cast'].apply(lambda x: x[0:3])
movies['crew'] = movies['crew'].apply(fetch_director)
movies['cast'] = movies['cast'].apply(collapse)
movies['crew'] = movies['crew'].apply(collapse)
movies['genres'] = movies['genres'].apply(collapse)
movies['keywords'] = movies['keywords'].apply(collapse)
movies['overview'] = movies['overview'].apply(lambda x: x.split())
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
new = movies.drop(columns=['overview', 'genres', 'keywords', 'cast', 'crew'])
new['tags'] = new['tags'].apply(lambda x: " ".join(x))

# Calculate cosine similarity
cv = CountVectorizer(max_features=5000, stop_words='english')
vector = cv.fit_transform(new['tags']).toarray()
similarity = cosine_similarity(vector)

def fetch_poster(movie_id):
    return f"https://image.tmdb.org/t/p/w500/{movie_id}"

def recommend(movie):
    try:
        index = new[new['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

        recommended_movies = []
        recommended_posters = []

        for i in distances[1:6]:
            recommended_movies.append(new.iloc[i[0]].title)
            recommended_posters.append(fetch_poster(new.iloc[i[0]].movie_id))

    except Exception as e:
        st.error("Error occurred while recommending movies.")
        st.error(str(e))
        recommended_movies = []
        recommended_posters = []

    return recommended_movies, recommended_posters

st.header('Movie Recommender System')

movie_list = new['title'].values

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
