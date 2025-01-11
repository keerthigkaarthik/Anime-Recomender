import numpy as np
import pandas as pd
import difflib
from pathlib import Path
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
                base_path = Path(__file__).resolve().parent
                similarity_path = base_path / 'similarity_matrix.npy'
                
                # Load dataset
                self._anime_dataset = pd.read_csv(str(base_path / 'anime-dataset-2023.csv'))
                
                # Load or calculate similarity matrix
                if similarity_path.exists():
                    self._similarity_matrix = np.load(str(similarity_path))
                else:
                    logger.info("Similarity matrix not found. Calculating...")
                    self._similarity_matrix = self.calculate_similarity_matrix(self._anime_dataset)
                    np.save(str(similarity_path), self._similarity_matrix)
                    logger.info("Similarity matrix calculated and saved.")
                
                self._initialized = True
                logger.info("Anime recommender data loaded successfully")
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
        anime = self._anime_dataset[self._anime_dataset['anime_id'] == anime_id].iloc[0]
        return {
            'anime_id': int(anime['anime_id']),
            'name': anime['Name'],
            'english_name': anime['English name'],
            'score': float(anime['Score']),
            'genres': anime['Genres'],
            'type': anime['Type'],
            'episodes': anime['Episodes'],
            'studios': anime['Studios'],
            'source': anime['Source']
        }
    
    def get_recommendations(self, anime_id, num_recommendations=50):
        if not self._initialized:
            raise Exception("Recommender not properly initialized")
            
        try:
            # Find the index for the given anime_id
            try:
                index_of_anime = self._anime_dataset[self._anime_dataset['anime_id'] == anime_id].index[0]
            except IndexError:
                return None, []  # Return None if anime_id not found
            
            # Get the input anime details
            input_anime = self.get_anime_details(anime_id)
            
            # Get similarity scores
            similarity_score = list(enumerate(self._similarity_matrix[index_of_anime]))
            sorted_similarity_scores = sorted(similarity_score, key=lambda x:x[1], reverse=True)
            
            # Get recommendations
            recommendations = []
            for anime_tuple in sorted_similarity_scores[1:num_recommendations + 1]:
                index = anime_tuple[0]
                similarity = anime_tuple[1]
                recommended_id = self._anime_dataset.iloc[index]['anime_id']
                anime_details = self.get_anime_details(recommended_id)
                anime_details['similarity_score'] = float(similarity)
                recommendations.append(anime_details)
                
            return input_anime, recommendations
            
        except Exception as e:
            logger.error(f"Error getting recommendations: {str(e)}")
            raise

    def search_anime(self, search_term):
        """Search for anime by name and return their IDs"""
        search_term = search_term.lower()
        search_results = []
        
        # Search in both original and English names
        mask = (self._anime_dataset['Name'].str.lower().str.contains(search_term, na=False) |
                self._anime_dataset['English name'].str.lower().str.contains(search_term, na=False))
        
        matches = self._anime_dataset[mask].head(10)
        
        for _, anime in matches.iterrows():
            search_results.append({
                'anime_id': int(anime['anime_id']),
                'name': anime['Name'],
                'english_name': anime['English name'],
                'score': float(anime['Score']),
                'type': anime['Type']
            })
            
        return search_results
