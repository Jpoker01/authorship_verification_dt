"""
Machine Learning module for authorship verification.
Uses TF-IDF with absolute difference and logistic classifier.
"""
import joblib
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


class AuthorshipVerifier:
    """
    Authorship verification using TF-IDF with absolute difference.
    """
    
    def __init__(self, model_dir: str = None):
        """
        Initialize the verifier with pre-trained models.
        
        Args:
            model_dir: Directory containing vectorizer.pkl and classifier.pkl
        """
        if model_dir is None:
            # Default to models directory in backend
            model_dir = Path(__file__).parent.parent / "models"
        
        self.model_dir = Path(model_dir)
        self.vectorizer = None
        self.classifier = None
        self._load_models()
    
    def _load_models(self):
        """Load the TF-IDF vectorizer and classifier from disk."""
        vectorizer_path = self.model_dir / "vectorizer.pkl"
        classifier_path = self.model_dir / "classifier.pkl"
        
        if not vectorizer_path.exists() or not classifier_path.exists():
            # Create default models if they don't exist
            self._create_default_models()
            return
        
        try:
            # Try loading with joblib (used in experiments)
            self.vectorizer = joblib.load(vectorizer_path)
            self.classifier = joblib.load(classifier_path)
            
            # Verify the loaded objects are correct types
            if not hasattr(self.vectorizer, 'transform'):
                raise ValueError("Loaded vectorizer doesn't have transform method")
            if not hasattr(self.classifier, 'predict_proba'):
                raise ValueError("Loaded classifier doesn't have predict_proba method")
                
        except Exception as e:
            print(f"Warning: Could not load models: {e}")
            print("Creating default models for demonstration...")
            self._create_default_models()
    
    def _create_default_models(self):
        """
        Create default TF-IDF vectorizer and classifier for demonstration.
        These are simple models that can work without training data.
        """
        # Create TF-IDF vectorizer with parameters similar to experiments
        self.vectorizer = TfidfVectorizer(
            max_features=10000,
            min_df=0.001,
            lowercase=True,
            sublinear_tf=True,
            ngram_range=(1, 1)
        )
        
        # Create logistic regression classifier
        self.classifier = LogisticRegression(
            C=1.0,
            random_state=42,
            max_iter=1000
        )
        
        # Note: These models are untrained and will need training data
        # For a working demo, we'll use a simple heuristic in predict
        self._use_heuristic = True
    
    def predict_probability(self, text1: str, text2: str) -> float:
        """
        Predict the probability that two texts are written by the same author.
        
        Args:
            text1: First text to compare
            text2: Second text to compare
        
        Returns:
            Probability that texts are from the same author (0.0 to 1.0)
        """
        # If using untrained models, use simple heuristic
        if hasattr(self, '_use_heuristic') and self._use_heuristic:
            return self._heuristic_prediction(text1, text2)
        
        try:
            # Transform both texts using TF-IDF vectorizer
            tfidf1 = self.vectorizer.transform([text1])
            tfidf2 = self.vectorizer.transform([text2])
            
            # Compute absolute difference
            features = np.abs(tfidf1 - tfidf2)
            
            # Get probability prediction from classifier
            # predict_proba returns [prob_different, prob_same]
            probabilities = self.classifier.predict_proba(features)
            
            # Return probability of same author (index 1)
            same_author_probability = float(probabilities[0][1])
            
            return same_author_probability
        except Exception as e:
            print(f"Warning: Prediction failed, using heuristic: {e}")
            return self._heuristic_prediction(text1, text2)
    
    def _heuristic_prediction(self, text1: str, text2: str) -> float:
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
    
    def predict(self, text1: str, text2: str) -> dict:
        """
        Predict authorship and return detailed results.
        
        Args:
            text1: First text to compare
            text2: Second text to compare
        
        Returns:
            Dictionary with prediction results
        """
        probability = self.predict_probability(text1, text2)
        
        return {
            "same_author_probability": probability,
            "different_author_probability": 1.0 - probability,
            "prediction": "same_author" if probability > 0.5 else "different_author"
        }


# Global instance
_verifier_instance = None


def get_verifier() -> AuthorshipVerifier:
    """
    Get or create the global verifier instance.
    
    Returns:
        AuthorshipVerifier instance
    """
    global _verifier_instance
    if _verifier_instance is None:
        _verifier_instance = AuthorshipVerifier()
    return _verifier_instance
