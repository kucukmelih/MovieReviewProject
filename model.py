import sqlite3
import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise import PredictionImpossible

# GLOBAL CACHED OBJECTS
_model = None
_trainset = None
_movies_df = None

def train_model():
    """
    Fetches user-movie-rating data from the database,
    prepares the training set for the SVD model, and fits the model.
    Trained model and data are cached globally.
    """
    global _model, _trainset, _movies_df

    conn = sqlite3.connect("movies.db")
    df = pd.read_sql_query("SELECT user_id, movie_id, rating FROM Reviews", conn)
    movies_df = pd.read_sql_query("SELECT id, title FROM Movies", conn)
    conn.close()

    reader = Reader(rating_scale=(1, 10))
    data = Dataset.load_from_df(df[['user_id', 'movie_id', 'rating']], reader)
    trainset = data.build_full_trainset()

    model = SVD()
    model.fit(trainset)

    _model = model
    _trainset = trainset
    _movies_df = movies_df

def get_trained_model():
    """
    Returns the trained model. If not trained yet, it trains and returns it.
    """
    if _model is None or _trainset is None or _movies_df is None:
        train_model()
    return _model, _trainset, _movies_df

def recommend_for_user(user_id, model, trainset, movies_df, n=5):
    """
    Recommends top-N movies for a specific user based on estimated ratings
    for movies the user hasn't rated yet.
    
    Parameters:
        user_id (int): ID of the target user
        model (SVD): Trained SVD model
        trainset (Trainset): Surprise training set
        movies_df (DataFrame): DataFrame of movies with IDs and titles
        n (int): Number of recommendations to return (default: 5)
        
    Returns:
        List of tuples: [(movie_id, predicted_rating), ...]
    """
    if user_id not in trainset._raw2inner_id_users:
        raise ValueError(f"User {user_id} not in training data")

    # Get IDs of movies already rated by the user
    rated_items = set(j for (j, _) in trainset.ur[trainset.to_inner_uid(user_id)])

    # Generate candidate movies the user hasn't rated
    candidates = [
        iid for iid in movies_df['id']
        if trainset.to_inner_iid(iid) not in rated_items
    ]

    predictions = []
    for iid in candidates:
        try:
            pred = model.predict(user_id, iid)
            predictions.append((iid, pred.est))
        except PredictionImpossible:
            continue

    # Sort by predicted rating, descending
    predictions.sort(key=lambda x: x[1], reverse=True)
    return predictions[:n]
