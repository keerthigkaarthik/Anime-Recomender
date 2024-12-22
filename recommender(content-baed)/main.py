import numpy as np
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# First time: Calculate and save the similarity matrix
def calculate_and_save_similarity():
    anime_dataset = pd.read_csv('anime-dataset-2023.csv')
    important_features = ['Genres', 'Type', 'Studios', 'Source', 'Name']
    
    for feature in important_features:
        anime_dataset[feature] = anime_dataset[feature].fillna('')
    
    concat_features = anime_dataset['Genres'] + ' ' + anime_dataset['Type'] + ' ' + anime_dataset['Studios'] + ' ' + anime_dataset['Source'] + ' ' + anime_dataset['Name']
    vectorizer = TfidfVectorizer()
    feature_vectors = vectorizer.fit_transform(concat_features)
    similarity = cosine_similarity(feature_vectors)
    
    # Save the similarity matrix
    np.save('similarity_matrix.npy', similarity)

# Later: Load the pre-computed similarity matrix
def load_similarity():
    return np.load('similarity_matrix.npy')

# # Use it like this:
# # First time:
# calculate_and_save_similarity()


anime_dataset = pd.read_csv('anime-dataset-2023.csv')
# Subsequent times:
similarity = load_similarity()

#locating target anime
list_of_all_titles = anime_dataset['Name'].tolist()

anime_name = input("Enter name of anime: ") #target anime name

close_match  = difflib.get_close_matches(anime_name, list_of_all_titles, 10)
print("Close match(es): ")
print(close_match)

closest_match = close_match[0]

index_of_anime = anime_dataset[anime_dataset.Name == closest_match].index[0]

similarity_score = list(enumerate(similarity[index_of_anime]))

sorted_similarity_scores = sorted(similarity_score, key=lambda x:x[1], reverse=True)

top_50 = sorted_similarity_scores[:51]

i = 0
print('\nAnime recommendations: \n')
for anime_tuple in top_50:
    index = anime_tuple[0]
    title = anime_dataset[anime_dataset.index == index]['Name'].values[0]
    print(str(i) + ". " + title + "\n")
    i += 1