# # generate_similarity.py
# import numpy as np
# import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import os

# def clean_csv(input_path, output_path):
#     print("Loading and cleaning CSV...")
#     # Read only the columns we need
#     needed_columns = [
#         'anime_id', 'Genres', 
#         'English name', 'Type', 'Episodes', 
#         'Studios', 'Source',
#     ]
    
#     df = pd.read_csv(input_path, usecols=needed_columns)
    
#     # Save cleaned CSV
#     print("Saving cleaned CSV...")
#     df.to_csv(output_path, index=False)
#     return df

# def calculate_similarity_matrix(anime_dataset):
#     print("Preparing features...")
#     # Use important features for similarity
#     features = ['Genres', 'Type', 'Studios', 'English name', 'Source', 'Episodes']
#     feature_data = {}
    
#     for feature in features:
#         feature_data[feature] = anime_dataset[feature].fillna('').astype(str)
    
#     combined_features = (
#         feature_data['Genres'] + ' ' + 
#         feature_data['Type'] + ' ' + 
#         feature_data['Studios'] + ' ' + 
#         feature_data['English name'] + ' ' + 
#         feature_data['Source'] + ' ' + 
#         feature_data['Episodes']
#     )
    
#     print("Calculating TF-IDF...")
#     vectorizer = TfidfVectorizer(
#         max_features=1000,
#         stop_words='english',
#         strip_accents='unicode',
#         dtype=np.float32
#     )
    
#     feature_vectors = vectorizer.fit_transform(combined_features)
    
#     print("Calculating similarity matrix...")
#     similarity_matrix = cosine_similarity(
#         feature_vectors, 
#         dense_output=True
#     ).astype(np.float32)
    
#     return similarity_matrix

# if __name__ == "__main__":
#     input_csv = 'CSVS/anime.csv'
#     cleaned_csv = 'CSVS/anime_cleaned.csv'
    
#     if not os.path.exists(input_csv):
#         print(f"Error: Could not find {input_csv}")
#         exit(1)
    
#     # Clean the CSV first
#     df = clean_csv(input_csv, cleaned_csv)
#     print(f"Cleaned CSV saved to {cleaned_csv}")
    
#     # Calculate similarity matrix
#     similarity_matrix = calculate_similarity_matrix(df)
    
#     # Save the matrix
#     output_path = 'weeb_shit/similarity_matrix.npy'
#     print(f"Saving similarity matrix to {output_path}...")
#     np.save(output_path, similarity_matrix)
    
#     # Print size info
#     matrix_size_mb = similarity_matrix.nbytes / (1024 * 1024)
#     print(f"Matrix size: {matrix_size_mb:.2f} MB")
#     print("Done!")

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import save_npz, csr_matrix
import os

def clean_csv(input_path, output_path):
    print("Loading and cleaning CSV...")
    needed_columns = [
            'anime_id', 'Genres', 
            'English name', 'Type', 'Episodes', 
            'Studios', 'Source',
        ]
    
    df = pd.read_csv(input_path, usecols=needed_columns)
    df.to_csv(output_path, index=False)
    return df

def calculate_sparse_similarity_matrix(anime_dataset, top_k=20):
    print("Preparing features...")
    # Only use the most important features for similarity
    features = ['Genres', 'Studios']  # Reduced feature set
    feature_data = {}
    
    for feature in features:
        feature_data[feature] = anime_dataset[feature].fillna('').astype(str)
    
    combined_features = feature_data['Genres'] + ' ' + feature_data['Studios']
    
    print("Calculating TF-IDF...")
    vectorizer = TfidfVectorizer(
        max_features=500,  # Reduced features
        stop_words='english',
        dtype=np.float32
    )
    
    feature_vectors = vectorizer.fit_transform(combined_features)
    
    print("Calculating similarity matrix...")
    num_items = feature_vectors.shape[0]
    rows = []
    cols = []
    data = []
    
    # Calculate similarities in batches
    batch_size = 1000
    for i in range(0, num_items, batch_size):
        end = min(i + batch_size, num_items)
        batch_similarities = cosine_similarity(
            feature_vectors[i:end], 
            feature_vectors,
            dense_output=False
        )
        
        # For each item, keep only top_k most similar items
        for idx, row in enumerate(batch_similarities):
            row = row.toarray()[0]
            top_indices = np.argpartition(row, -top_k)[-top_k:]
            for j in top_indices:
                if row[j] > 0.1:  # Only keep similarities above threshold
                    rows.append(i + idx)
                    cols.append(j)
                    data.append(np.float32(row[j]))
    
    # Create sparse matrix with only top similarities
    sparse_matrix = csr_matrix((data, (rows, cols)), shape=(num_items, num_items), dtype=np.float32)
    
    return sparse_matrix

if __name__ == "__main__":
    input_csv = 'CSVS/anime.csv'
    cleaned_csv = 'CSVS/anime_cleaned.csv'
    
    if not os.path.exists(input_csv):
        print(f"Error: Could not find {input_csv}")
        exit(1)
    
    # Clean the CSV first
    df = clean_csv(input_csv, cleaned_csv)
    print(f"Cleaned CSV saved to {cleaned_csv}")
    
    # Calculate sparse similarity matrix
    sparse_similarity = calculate_sparse_similarity_matrix(df)
    
    # Save the sparse matrix
    output_path = 'weeb_shit/similarity_matrix.npz'
    print(f"Saving sparse similarity matrix to {output_path}...")
    save_npz(output_path, sparse_similarity)
    
    # Print size info
    matrix_size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"Matrix size: {matrix_size_mb:.2f} MB")
    print("Done!")
