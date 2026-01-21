"""
Machine Learning module for authorship verification.
Uses TF-IDF with absolute difference and logistic classifier.
"""
import joblib
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


# Module-level variables for models
_vectorizer = None
_classifier = None
_use_heuristic = True
_models_loaded = False


def _load_models():
    """Load the TF-IDF vectorizer and classifier from disk."""
    global _vectorizer, _classifier, _use_heuristic, _models_loaded
    
    if _models_loaded:
        return
    
    model_dir = Path(__file__).parent.parent / "models"
    vectorizer_path = model_dir / "vectorizer.pkl"
    classifier_path = model_dir / "classifier.pkl"
    
    if not vectorizer_path.exists() or not classifier_path.exists():
        # Use heuristic if models don't exist
        _use_heuristic = True
        _models_loaded = True
        return
    
    try:
        # Try loading with joblib (used in experiments)
        _vectorizer = joblib.load(vectorizer_path)
        _classifier = joblib.load(classifier_path)
        
        # Verify the loaded objects are correct types
        if not hasattr(_vectorizer, 'transform'):
            raise ValueError("Loaded vectorizer doesn't have transform method")
        if not hasattr(_classifier, 'predict_proba'):
            raise ValueError("Loaded classifier doesn't have predict_proba method")
        
        _use_heuristic = False
    except Exception as e:
        print(f"Warning: Could not load models: {e}")
        print("Using heuristic-based prediction...")
        _use_heuristic = True
    
    _models_loaded = True


def _heuristic_prediction(text1: str, text2: str) -> float:
    """
    Simple heuristic-based prediction for demo when models are not trained.
    Uses basic text similarity features.
    
    Args:
        text1: First text
        text2: Second text
    
    Returns:
        Probability estimate based on simple features
    """
    # Handle empty texts
    if not text1 or not text2:
        return 0.5  # Neutral probability for empty texts
    
    # Simple features
    max_len = max(len(text1), len(text2))
    if max_len == 0:
        len_ratio = 1.0
    else:
        len_ratio = min(len(text1), len(text2)) / max_len
    
    # Word overlap
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    if len(words1) == 0 or len(words2) == 0:
        word_overlap = 0.0
    else:
        word_overlap = len(words1 & words2) / max(len(words1), len(words2))
    
    # Average sentence length similarity
    sentences1 = [s.strip() for s in text1.split('.') if s.strip()]
    sentences2 = [s.strip() for s in text2.split('.') if s.strip()]
    
    if sentences1 and sentences2:
        avg_len1 = np.mean([len(s.split()) for s in sentences1])
        avg_len2 = np.mean([len(s.split()) for s in sentences2])
        if avg_len1 + avg_len2 > 0:
            len_sim = 1 - abs(avg_len1 - avg_len2) / (avg_len1 + avg_len2)
        else:
            len_sim = 0.5
    else:
        len_sim = 0.5
    
    # Combine features (simple weighted average)
    probability = 0.3 * len_ratio + 0.4 * word_overlap + 0.3 * len_sim
    
    return float(probability)


def predict_probability(text1: str, text2: str) -> float:
    """
    Predict the probability that two texts are written by the same author.
    
    Args:
        text1: First text to compare
        text2: Second text to compare
    
    Returns:
        Probability that texts are from the same author (0.0 to 1.0)
    """
    # Load models on first call
    _load_models()
    
    # If using heuristic, return heuristic prediction
    if _use_heuristic:
        return _heuristic_prediction(text1, text2)
    
    try:
        # Transform both texts using TF-IDF vectorizer
        tfidf1 = _vectorizer.transform([text1])
        tfidf2 = _vectorizer.transform([text2])
        
        # Compute absolute difference
        features = np.abs(tfidf1 - tfidf2)
        
        # Get probability prediction from classifier
        # predict_proba returns [prob_different, prob_same]
        probabilities = _classifier.predict_proba(features)
        
        # Return probability of same author (index 1)
        same_author_probability = float(probabilities[0][1])
        
        return same_author_probability
    except Exception as e:
        print(f"Warning: Prediction failed, using heuristic: {e}")
        return _heuristic_prediction(text1, text2)


def predict(text1: str, text2: str) -> dict:
    """
    Predict authorship and return probability.
    
    Args:
        text1: First text to compare
        text2: Second text to compare
    
    Returns:
        Dictionary with same_author_probability
    """
    probability = predict_probability(text1, text2)
    
    return {
        "same_author_probability": probability
    }
