import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Embedding, Input, Dense, Flatten, Concatenate

# Sample DataFrame
df = pd.DataFrame({
    'userId': [1, 2, 3, 4, 5],
    'movieId': [10, 20, 30, 40, 50],
    'address': ['New York', 'Los Angeles', 'New York', 'Chicago', 'Los Angeles'],
    'rating': [5, 3, 4, 2, 1]
})

df = pd.read_csv('ml-latest-small/modified_merged_data.csv', names=['movieId', 'userId', 'address', 'rating'])
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')


# Encode categorical data
user_encoder = LabelEncoder()
item_encoder = LabelEncoder()
location_encoder = LabelEncoder()

df['userId'] = user_encoder.fit_transform(df['userId'])
df['movieId'] = item_encoder.fit_transform(df['movieId'])
df['address'] = location_encoder.fit_transform(df['address'])

print("Encoding Done")

# Splitting the dataset
train, test = train_test_split(df, test_size=0.2, random_state=42)

# Model parameters
num_users = df['userId'].nunique()
num_items = df['movieId'].nunique()
num_locations = df['address'].nunique()
embedding_size = 64

# Neural Collaborative Filtering Model with Location

# Inputs
user_input = Input(shape=(1,), name='user_input')
item_input = Input(shape=(1,), name='item_input')
location_input = Input(shape=(1,), name='location_input')

# User, Item, and Location Embeddings
user_embedding = Embedding(num_users, embedding_size, name='user_embedding')(user_input)
item_embedding = Embedding(num_items, embedding_size, name='item_embedding')(item_input)
location_embedding = Embedding(num_locations, embedding_size, name='location_embedding')(location_input)

# Flatten the embeddings
user_vec = Flatten()(user_embedding)
item_vec = Flatten()(item_embedding)
location_vec = Flatten()(location_embedding)

# Concatenate the embeddings
concat = Concatenate()([user_vec, item_vec, location_vec])

# Neural network
dense = Dense(128, activation='relu')(concat)
dense = Dense(64, activation='relu')(dense)
output = Dense(1, activation='sigmoid')(dense)

# Define the model
model = Model(inputs=[user_input, item_input, location_input], outputs=output)

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

print("Training starteed")
# Train the model
model.fit(
    [train.userId, train.movieId, train.address],
    train.rating,
    batch_size=32,
    epochs=5,
    validation_split=0.1,
    verbose=1
)
print("Training ended")

# Evaluate the model
metrics = model.evaluate([test.userId, test.movieId, test.address], test.rating)

print(metrics)
