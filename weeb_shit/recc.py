import numpy as np
import pandas as pd
import difflib
from pathlib import Path
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging

logger = logging.getLogger(__name__)

class AnimeRecommender:
    _instance = None
    _similarity_matrix = None
    _anime_dataset = None
    _initialized = False
    
    @classmethod
    def calculate_similarity_matrix(cls, anime_dataset):
        """
        Calculate similarity matrix using TF-IDF and cosine similarity.
        Features used: Genres, Type, Studios, Source, Name
        """
        # Fill NaN values
        features = ['Genres', 'Type', 'Studios', 'Source', 'Name']
        for feature in features:
            anime_dataset[feature] = anime_dataset[feature].fillna('')
            
        # Combine features into a single string for each anime
        combined_features = (anime_dataset['Genres'] + ' ' + 
                           anime_dataset['Type'] + ' ' + 
                           anime_dataset['Studios'] + ' ' + 
                           anime_dataset['Source'] + ' ' + 
                           anime_dataset['Name'])
        
        # Convert text to TF-IDF vectors
        vectorizer = TfidfVectorizer()
        feature_vectors = vectorizer.fit_transform(combined_features)
        
        # Calculate cosine similarity between all anime pairs
        return cosine_similarity(feature_vectors)
    
    def __init__(self):
        if AnimeRecommender._instance is not None:
            raise Exception("This class is a singleton!")
        
        if not self._initialized:
            try:
                logger.info("Loading anime recommender data...")
                # Get the absolute path to the project root
                base_path = Path(__file__).resolve().parent.parent
                
                # Define possible CSV paths (try different relative paths)
                possible_csv_paths = [
                    base_path / 'CSVS' / 'anime.csv',
                    base_path / 'csvs' / 'anime.csv',  # Try lowercase
                    Path('/app/CSVS/anime.csv'),       # Try absolute path in Railway
                    Path('/app/csvs/anime.csv'),       # Try lowercase in Railway
                    base_path / 'anime.csv'            # Try root directory
                ]
                
                # Try to find the CSV file
                csv_path = None
                for path in possible_csv_paths:
                    if path.exists():
                        csv_path = path
                        break
                
                if csv_path is None:
                    logger.error(f"Could not find anime.csv in any of these locations: {[str(p) for p in possible_csv_paths]}")
                    logger.error(f"Current directory contents: {os.listdir(base_path)}")
                    raise FileNotFoundError("Could not find anime.csv file")
                
                logger.info(f"Found anime.csv at: {csv_path}")
                
                # Define similarity matrix path
                similarity_path = base_path / 'weeb_shit' / 'similarity_matrix.npy'
                
                # Load dataset
                try:
                    self._anime_dataset = pd.read_csv(str(csv_path))
                    logger.info("Successfully loaded anime dataset")
                except Exception as e:
                    logger.error(f"Error reading CSV file: {str(e)}")
                    raise
                
                # Load or calculate similarity matrix
                try:
                    if similarity_path.exists():
                        self._similarity_matrix = np.load(str(similarity_path))
                        logger.info("Loaded existing similarity matrix")
                    else:
                        logger.info("Calculating new similarity matrix...")
                        self._similarity_matrix = self.calculate_similarity_matrix(self._anime_dataset)
                        try:
                            np.save(str(similarity_path), self._similarity_matrix)
                            logger.info("Saved new similarity matrix")
                        except Exception as e:
                            logger.warning(f"Could not save similarity matrix: {str(e)}")
                            # Continue anyway since we have the matrix in memory
                except Exception as e:
                    logger.error(f"Error with similarity matrix: {str(e)}")
                    raise
                
                self._initialized = True
                logger.info("Anime recommender initialized successfully")
                
            except Exception as e:
                logger.error(f"Failed to initialize recommender: {str(e)}")
                raise
        
        AnimeRecommender._instance = self

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = AnimeRecommender()
        return cls._instance

    def get_anime_details(self, anime_id):
        """Get relevant details for an anime by ID"""
        try:
            anime = self._anime_dataset[self._anime_dataset['anime_id'] == anime_id].iloc[0]
            return {
                'anime_id': int(anime['anime_id']),
                'name': anime['Name'],
                'english_name': anime['English name'],
                'score': float(anime['Score']) if pd.notnull(anime['Score']) else 0.0,
                'genres': anime['Genres'],
                'type': anime['Type'],
                'episodes': anime['Episodes'],
                'studios': anime['Studios'],
                'source': anime['Source']
            }
        except IndexError:
            logger.error(f"Anime ID {anime_id} not found in dataset")
            return None
        except Exception as e:
            logger.error(f"Error getting anime details: {str(e)}")
            return None
    
    def get_recommendations(self, anime_id, num_recommendations=50):
        if not self._initialized:
            raise Exception("Recommender not properly initialized")
            
        try:
            # Find the index for the given anime_id
            try:
                index_of_anime = self._anime_dataset[self._anime_dataset['anime_id'] == anime_id].index[0]
            except IndexError:
                logger.error(f"Anime ID {anime_id} not found")
                return []  # Return empty list if anime_id not found
            
            # Get similarity scores
            similarity_score = list(enumerate(self._similarity_matrix[index_of_anime]))
            sorted_similarity_scores = sorted(similarity_score, key=lambda x:x[1], reverse=True)
            
            # Get recommendations
            recommendation_ids = [
                int(self._anime_dataset.iloc[anime_tuple[0]]['anime_id'])
                for anime_tuple in sorted_similarity_scores[1:num_recommendations + 1]
            ]
            
            return recommendation_ids
            
        except Exception as e:
            logger.error(f"Error getting recommendations: {str(e)}")
            return []

    def search_anime(self, search_term):
        """Search for anime by name and return their IDs"""
        try:
            search_term = str(search_term).lower()
            
            # Search in both original and English names
            mask = (self._anime_dataset['Name'].str.lower().str.contains(search_term, na=False) |
                    self._anime_dataset['English name'].str.lower().str.contains(search_term, na=False))
            
            matches = self._anime_dataset[mask].head(10)
            
            search_results = []
            for _, anime in matches.iterrows():
                search_results.append({
                    'anime_id': int(anime['anime_id']),
                    'name': anime['Name'],
                    'english_name': anime['English name'],
                    'score': float(anime['Score']) if pd.notnull(anime['Score']) else 0.0,
                    'type': anime['Type']
                })
                
            return search_results
        except Exception as e:
            logger.error(f"Error searching anime: {str(e)}")
            return []
