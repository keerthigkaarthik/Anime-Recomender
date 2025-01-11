import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

def calculate_similarity_matrix(anime_dataset):
    print("Preparing features...")
    # Use only essential features
    features = ['Genres', 'Type']
    feature_data = {}
    
    for feature in features:
        feature_data[feature] = anime_dataset[feature].fillna('').astype(str)
    
    combined_features = feature_data['Genres'] + ' ' + feature_data['Type']
    
    print("Calculating TF-IDF...")
    vectorizer = TfidfVectorizer(
        max_features=1000,
        stop_words='english',
        strip_accents='unicode',
        dtype=np.float32
    )
    
    feature_vectors = vectorizer.fit_transform(combined_features)
    
    print("Calculating similarity matrix...")
    similarity_matrix = cosine_similarity(
        feature_vectors, 
        dense_output=True
    ).astype(np.float32)
    
    return similarity_matrix

if __name__ == "__main__":
    # Load the CSV
    print("Loading CSV...")
    csv_path = 'CSVS/anime.csv'
    if not os.path.exists(csv_path):
        print(f"Error: Could not find {csv_path}")
        exit(1)
    
    df = pd.read_csv(csv_path)
    
    # Calculate similarity matrix
    similarity_matrix = calculate_similarity_matrix(df)
    
    # Save the matrix
    output_path = 'weeb_shit/similarity_matrix.npy'
    print(f"Saving similarity matrix to {output_path}...")
    np.save(output_path, similarity_matrix)
    print("Done!")
