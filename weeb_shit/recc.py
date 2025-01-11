import numpy as np
import pandas as pd
import difflib
from pathlib import Path
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging
import gc  # For garbage collection

logger = logging.getLogger(__name__)

class AnimeRecommender:
   _instance = None
   _similarity_matrix = None
   _anime_dataset = None
   _initialized = False
   
   def __init__(self):
       if AnimeRecommender._instance is not None:
           raise Exception("This class is a singleton!")
       
       if not self._initialized:
           try:
               logger.info("Loading anime recommender data...")
               
               # Try to find the CSV and similarity matrix
               csv_path = None
               matrix_path = None
               
               possible_csv_paths = [
                   'CSVS/anime.csv',
                   'csvs/anime.csv',
                   'anime.csv',
                   '/app/CSVS/anime.csv',
                   '/app/csvs/anime.csv',
                   '/app/anime.csv'
               ]
               
               possible_matrix_paths = [
                   'weeb_shit/similarity_matrix.npz',
                   '/app/weeb_shit/similarity_matrix.npz',
                   'similarity_matrix.npz'
               ]
               
               for path in possible_csv_paths:
                   if os.path.exists(path):
                       csv_path = path
                       break
               
               for path in possible_matrix_paths:
                   if os.path.exists(path):
                       matrix_path = path
                       break
               
               if csv_path is None:
                   raise FileNotFoundError(f"Could not find anime.csv in any of: {possible_csv_paths}")
               if matrix_path is None:
                   raise FileNotFoundError(f"Could not find similarity_matrix.npz in any of: {possible_matrix_paths}")
               
               logger.info(f"Found CSV at: {csv_path}")
               logger.info(f"Found similarity matrix at: {matrix_path}")
               
               # Load dataset with minimal memory usage
               try:
                   self._anime_dataset = pd.read_csv(
                       csv_path,
                       dtype={
                           'anime_id': 'int32',
                           'Genres': 'category',
                           'English name': 'category',
                           'Type': 'category',
                           'Episodes': 'category',
                           'Studios': 'category',
                           'Source': 'category'
                       }
                   )
                  # Load pre-calculated similarity matrix
                   logger.info("Loading similarity matrix...")
                   npz_file = np.load(matrix_path)
                   self._similarity_matrix = npz_file['arr_0']  # Load the first array from the npz file
                   logger.info("Similarity matrix loaded successfully")
                   
               except Exception as e:
                   logger.error(f"Error loading data: {str(e)}")
                   raise
               
               self._initialized = True
               
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
               'english_name': str(anime['English name']),
               'genres': str(anime['Genres']),
               'type': str(anime['Type']),
               'episodes': str(anime['Episodes']),
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
           
           # Convert anime_id to int if it's a string
           anime_id = int(anime_id)
           
           # Find the index for the given anime_id
           matching_anime = self._anime_dataset[self._anime_dataset['anime_id'] == anime_id]
           if matching_anime.empty:
               logger.warning(f"No anime found with anime_id {anime_id}")
               return []
               
           index_of_anime = matching_anime.index[0]
           
           # Get similarity scores for this anime
           similarity_scores = self._similarity_matrix[index_of_anime]
           
           # Get top indices efficiently
           top_indices = np.argsort(similarity_scores)[-num_recommendations-1:][::-1][1:]
           
           # Get anime IDs for recommendations
           recommendation_ids = []
           for idx in top_indices:
               try:
                   recommended_id = int(self._anime_dataset.iloc[idx]['anime_id'])
                   recommendation_ids.append(recommended_id)
               except Exception as e:
                   logger.error(f"Error processing recommendation index {idx}: {str(e)}")
                   continue
           
           return recommendation_ids
           
       except Exception as e:
           logger.error(f"Error getting recommendations: {str(e)}")
           return []

   def search_anime(self, search_term):
       try:
           search_term = str(search_term).lower()
           
           # Search in the English name
           mask = self._anime_dataset['English name'].str.lower().str.contains(search_term, na=False)
           matches = self._anime_dataset[mask].head(10)
           
           return [{
               'anime_id': int(anime['anime_id']),
               'english_name': str(anime['English name']),
               'genres': str(anime['Genres']),
               'type': str(anime['Type']),
               'episodes': str(anime['Episodes']),
               'studios': str(anime['Studios']),
               'source': str(anime['Source'])
           } for _, anime in matches.iterrows()]
           
       except Exception as e:
           logger.error(f"Error searching anime: {str(e)}")
           return []
