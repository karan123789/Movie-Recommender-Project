import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load your CSV file
movies = pd.read_csv('tmdb_5000_movies.csv')

# Drop rows with missing values in these columns
movies = movies.dropna(subset=['overview', 'genres', 'keywords', 'cast', 'crew'])

# Function to create tags from multiple columns
def combine_tags(row):
    return ' '.join([str(row['overview']), ' '.join(eval(row['genres'])), ' '.join(eval(row['keywords'])),
                     ' '.join(eval(row['cast'])), ' '.join(eval(row['crew']))])

# Apply the function to create the 'tags' column
movies['tags'] = movies.apply(combine_tags, axis=1)

# Initialize CountVectorizer and transform 'tags' into vectors
cv = CountVectorizer(max_features=5000, stop_words='english')
vector = cv.fit_transform(movies['tags']).toarray()

# Compute cosine similarity
similarity = cosine_similarity(vector)

# Function to recommend movies based on similarity
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    for i in distances[1:6]:
        print(movies.iloc[i[0]]['title'])
