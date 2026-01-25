import os
from pathlib import Path

MODEL_DIR = Path(__file__).parent.parent / "models"
VECTORIZER_PATH = MODEL_DIR  / "vectorizer.pkl"
CLASSIFIER_PATH = MODEL_DIR  / "classifier.pkl"

# Access control configuration
# Set ACCESS_TOKEN environment variable to require token-based authentication
# If not set, the app will be publicly accessible
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", None)
