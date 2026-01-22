"""
Configuration settings for the authorship verification backend.
"""
from pathlib import Path


# Model paths
MODEL_DIR = Path(__file__).parent.parent / "models"
VECTORIZER_PATH = MODEL_DIR / "vectorizer.pkl"
CLASSIFIER_PATH = MODEL_DIR / "classifier.pkl"
