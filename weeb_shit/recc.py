import numpy as np
import pandas as pd
from pathlib import Path
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging
import gc 

logger = logging.getLogger(__name__)

class AnimeRecommender:
    _instance = None
    _similarity_matrix = None
    _anime_dataset = None
    _initialized = False
    
    @classmethod
    def calculate_similarity_matrix(cls, anime_dataset):
        try:
            # Fill NaN values
            features = ['Genres', 'Type', 'Studios', 'Source', 'Name']
            feature_data = {}
            for feature in features:
                feature_data[feature] = anime_dataset[feature].fillna('')
            
            # Combine features efficiently
            combined_features = (
                feature_data['Genres'] + ' ' + 
                feature_data['Type'] + ' ' + 
                feature_data['Studios'] + ' ' + 
                feature_data['Source'] + ' ' + 
                feature_data['Name']
            )
            
            # Clear feature_data to free memory
            del feature_data
            gc.collect()
            
            # Use smaller chunk size for TF-IDF
            vectorizer = TfidfVectorizer(max_features=5000)
            feature_vectors = vectorizer.fit_transform(combined_features)
            
            del combined_features
            gc.collect()
            
            # Calculate similarity with lower precision to save memory
            similarity_matrix = cosine_similarity(feature_vectors, dense_output=False)
            return similarity_matrix.astype(np.float32)  # Use float32 instead of float64
            
        except Exception as e:
            logger.error(f"Error calculating similarity matrix: {str(e)}")
            raise
    
    def __init__(self):
        if AnimeRecommender._instance is not None:
            raise Exception("This class is a singleton!")
        
        if not self._initialized:
            try:
                logger.info("Loading anime recommender data...")
                
                # Try to find the CSV file
                csv_path = None
                possible_paths = [
                    'CSVS/anime.csv',
                    'csvs/anime.csv',
                    'anime.csv',
                    '/app/CSVS/anime.csv',
                    '/app/csvs/anime.csv',
                    '/app/anime.csv'
                ]
                
                for path in possible_paths:
                    if os.path.exists(path):
                        csv_path = path
                        break
                
                if csv_path is None:
                    raise FileNotFoundError(f"Could not find anime.csv in any of: {possible_paths}")
                
                logger.info(f"Found CSV at: {csv_path}")
                
                # Load only necessary columns to save memory
                columns_needed = ['anime_id', 'Name', 'English name', 'Score', 
                                'Genres', 'Type', 'Studios', 'Source', 'Episodes']
                
                try:
                    self._anime_dataset = pd.read_csv(
                        csv_path,
                        usecols=columns_needed,
                        dtype={
                            'anime_id': 'int32',
                            'Score': 'float32',
                            'Episodes': 'float32'
                        }
                    )
                    
                    # Convert string columns to category to save memory
                    string_columns = ['Name', 'English name', 'Genres', 'Type', 'Studios', 'Source']
                    for col in string_columns:
                        if col in self._anime_dataset.columns:
                            self._anime_dataset[col] = self._anime_dataset[col].astype('category')
                            
                except Exception as e:
                    logger.error(f"Error reading CSV: {str(e)}")
                    raise
                
                # Calculate similarity matrix (don't save to disk in production)
                logger.info("Calculating similarity matrix...")
                self._similarity_matrix = self.calculate_similarity_matrix(self._anime_dataset)
                logger.info("Similarity matrix calculation complete")
                
                self._initialized = True
                gc.collect()  # Final garbage collection
                
            except Exception as e:
                logger.error(f"Failed to initialize recommender: {str(e)}")
                raise
        
        AnimeRecommender._instance = self

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            try:
                cls._instance = AnimeRecommender()
            except Exception as e:
                logger.error(f"Error getting instance: {str(e)}")
                raise
        return cls._instance

    def get_anime_details(self, anime_id):
        try:
            anime = self._anime_dataset[self._anime_dataset['anime_id'] == anime_id].iloc[0]
            return {
                'anime_id': int(anime['anime_id']),
                'name': str(anime['Name']),
                'english_name': str(anime['English name']),
                'score': float(anime['Score']) if pd.notnull(anime['Score']) else 0.0,
                'genres': str(anime['Genres']),
                'type': str(anime['Type']),
                'episodes': float(anime['Episodes']) if pd.notnull(anime['Episodes']) else 0.0,
                'studios': str(anime['Studios']),
                'source': str(anime['Source'])
            }
        except Exception as e:
            logger.error(f"Error getting anime details for ID {anime_id}: {str(e)}")
            return None

    def get_recommendations(self, anime_id, num_recommendations=5):
        try:
            if not self._initialized:
                raise Exception("Recommender not initialized")
            
            index_of_anime = self._anime_dataset[self._anime_dataset['anime_id'] == anime_id].index[0]
            similarity_scores = self._similarity_matrix[index_of_anime].toarray().flatten()
            
            # Get top indices efficiently
            top_indices = np.argpartition(similarity_scores, -num_recommendations-1)[-num_recommendations-1:]
            top_indices = top_indices[np.argsort(similarity_scores[top_indices])][::-1][1:]
            
            return [int(self._anime_dataset.iloc[i]['anime_id']) for i in top_indices]
            
        except Exception as e:
            logger.error(f"Error getting recommendations: {str(e)}")
            return []

    def search_anime(self, search_term):
        try:
            search_term = str(search_term).lower()
            mask = (
                self._anime_dataset['Name'].str.lower().str.contains(search_term, na=False) |
                self._anime_dataset['English name'].str.lower().str.contains(search_term, na=False)
            )
            matches = self._anime_dataset[mask].head(10)
            
            return [{
                'anime_id': int(anime['anime_id']),
                'name': str(anime['Name']),
                'english_name': str(anime['English name']),
                'score': float(anime['Score']) if pd.notnull(anime['Score']) else 0.0,
                'type': str(anime['Type'])
            } for _, anime in matches.iterrows()]
            
        except Exception as e:
            logger.error(f"Error searching anime: {str(e)}")
            return []
