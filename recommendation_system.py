import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from scipy.sparse import csr_matrix

# Load dataset
df = pd.read_csv('ml-latest-small/modified_merged_data.csv')

# Preprocessing: fill or drop missing values as per requirement
df.fillna(0, inplace=True)  # Example: fill missing values with 0

# Creating user-item matrix
user_movie_matrix = df.pivot_table(index='userId', columns='movieId', values='rating').fillna(0)

# Apply matrix factorization
svd = TruncatedSVD(n_components=10)
latent_matrix = svd.fit_transform(user_movie_matrix)

print("SVD Done")

# Convert to DataFrame for easier handling
user_features = pd.DataFrame(latent_matrix, index=user_movie_matrix.index)

# Combine genre and location data into a single string column
#df['content_features'] = df['genres'] + ' ' + df['address']

# Creating a TF-IDF Vectorizer
#tfidf = TfidfVectorizer(stop_words='english', min_df=0.01)

#tfidf_matrix = tfidf.fit_transform(df['content_features'])

#print(tfidf_matrix.shape)
# Compute cosine similarity matrix
#cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

#print("Cosine similarity Done") 

# Create a mapping of movie ID to index in the DataFrame
#movie_idx = pd.Series(df.index, index=df['movieId']).drop_duplicates()

def get_recommendations(user_id, num_recommendations=5):
    # Get user features
    user_vector = user_features.loc[user_id].values.reshape(1, -1)
    
    # Calculate similarity with other users
    user_similarity = cosine_similarity(user_vector, latent_matrix)
    
    # Sort similar users and extract top N similar users
    similar_users = user_similarity.argsort().flatten()[-num_recommendations:]

    # Get movie preferences of similar users
    similar_users_preferences = user_movie_matrix.iloc[similar_users].mean(axis=0)
    similar_users_preferences.sort_values(ascending=False, inplace=True)

    # Get top N movies from similar users preferences
    top_movies_from_similar_users = similar_users_preferences.head(num_recommendations).index

    # Get content-based recommendations
    content_recommendations = []
    while 1==0:
        for movie_id in top_movies_from_similar_users:
            idx = movie_idx[movie_id]
            sim_scores = list(enumerate(cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:num_recommendations]
            movie_indices = [i[0] for i in sim_scores]
            content_recommendations.extend(movie_indices)

    # Combine and deduplicate recommendations
    combined_recommendations = set(top_movies_from_similar_users).union(set(content_recommendations))
    
    # Return recommended movie IDs
    return list(combined_recommendations)[:num_recommendations]

# Example Usage
recommended_movies = get_recommendations(user_id=1)
print(recommended_movies)


