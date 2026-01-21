"""
Machine Learning module for authorship verification.
Uses TF-IDF with absolute difference and logistic classifier.
"""
import joblib
from pathlib import Path
import numpy as np


# Module-level variables for models
_vectorizer = None
_classifier = None
_models_loaded = False


def _load_models():
    """Load the TF-IDF vectorizer and classifier from disk."""
    global _vectorizer, _classifier, _models_loaded
    
    if _models_loaded:
        return
    
    model_dir = Path(__file__).parent.parent / "models"
    vectorizer_path = model_dir / "vectorizer.pkl"
    classifier_path = model_dir / "classifier.pkl"
    
    if not vectorizer_path.exists():
        raise FileNotFoundError(
            f"Vectorizer model not found at {vectorizer_path}. "
            "Please train and save the model first."
        )
    
    if not classifier_path.exists():
        raise FileNotFoundError(
            f"Classifier model not found at {classifier_path}. "
            "Please train and save the model first."
        )
    
    # Try loading with joblib (used in experiments)
    _vectorizer = joblib.load(vectorizer_path)
    _classifier = joblib.load(classifier_path)
    
    # Verify the loaded objects are correct types
    if not hasattr(_vectorizer, 'transform'):
        raise ValueError(
            "Loaded vectorizer doesn't have transform method. "
            "Please ensure the correct model file is saved."
        )
    if not hasattr(_classifier, 'predict_proba'):
        raise ValueError(
            "Loaded classifier doesn't have predict_proba method. "
            "Please ensure the correct model file is saved."
        )
    
    _models_loaded = True


def predict_probability(text1: str, text2: str) -> float:
    """
    Predict the probability that two texts are written by the same author.
    
    Args:
        text1: First text to compare
        text2: Second text to compare
    
    Returns:
        Probability that texts are from the same author (0.0 to 1.0)
    
    Raises:
        FileNotFoundError: If model files are not found
        ValueError: If loaded models are invalid
    """
    # Load models on first call
    _load_models()
    
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


def predict(text1: str, text2: str) -> dict:
    """
    Predict authorship and return probability.
    
    Args:
        text1: First text to compare
        text2: Second text to compare
    
    Returns:
        Dictionary with same_author_probability
    
    Raises:
        FileNotFoundError: If model files are not found
        ValueError: If loaded models are invalid
    """
    probability = predict_probability(text1, text2)
    
    return {
        "same_author_probability": probability
    }
