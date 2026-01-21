# Implementation Notes

## FastAPI Backend for Authorship Verification

This document describes the implementation details of the authorship verification backend.

### Approach

The backend implements authorship verification using the following methodology from the experiments:

1. **TF-IDF Vectorization**: Text is converted to numerical features using Term Frequency-Inverse Document Frequency
2. **Absolute Difference**: Features are computed as the absolute difference between TF-IDF vectors of two texts
3. **Logistic Regression**: A classifier predicts whether the texts are from the same author

### Implementation Details

#### Model Loading

The system attempts to load pre-trained models from `models/vectorizer.pkl` and `models/classifier.pkl` using joblib (consistent with the experiments). If models are unavailable or invalid, it falls back to a heuristic-based approach.

#### Heuristic Fallback

When pre-trained models are not available, the system uses a simple heuristic based on:
- Text length ratio
- Word overlap between texts
- Average sentence length similarity

This provides reasonable predictions for demonstration purposes.

#### API Design

The API follows RESTful principles with:
- POST /predict/ - Main prediction endpoint
- GET / - API information
- GET /health - Health check

All endpoints return JSON responses and include proper error handling.

#### Security Considerations

- CORS is enabled for development but includes warnings for production use
- No security vulnerabilities found in CodeQL analysis
- Input validation through Pydantic schemas
- Error handling to prevent information leakage

### Testing

The implementation has been tested with:
- Normal text pairs
- Edge cases (empty texts, very short texts)
- Different writing styles
- Various text lengths

All tests pass successfully.

### Libraries Used

All libraries are consistent with the experiments:
- fastapi - Web framework
- scikit-learn - ML library (TfidfVectorizer, LogisticRegression)
- numpy - Numerical operations
- joblib - Model serialization
- uvicorn - ASGI server
- pydantic - Data validation

### Future Improvements

To use trained models:
1. Train models using the notebook: `experiments/notebooks/traditional/20251208_JP_traditional_word_TF-IDF_absolute_difference.ipynb`
2. Save the best vectorizer as `webapp/backend/models/vectorizer.pkl`
3. Save the best classifier as `webapp/backend/models/classifier.pkl`
4. Restart the backend

The models should be pickled using joblib for compatibility.
