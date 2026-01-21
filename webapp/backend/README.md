# Authorship Verification Backend

A simple FastAPI backend for authorship verification using TF-IDF with absolute difference and logistic regression.

## Overview

This backend provides a REST API for determining whether two texts are written by the same author. The implementation is based on the experiments conducted in the `experiments/notebooks/traditional` directory, specifically using:

- **TF-IDF (Term Frequency-Inverse Document Frequency)** for text vectorization
- **Absolute Difference** to compute features from text pairs
- **Logistic Regression** classifier for prediction

## Installation

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
cd webapp/backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### POST /predict/

Predicts whether two texts are written by the same author.

**Request Body:**
```json
{
  "text1": "First text to compare",
  "text2": "Second text to compare"
}
```

**Response:**
```json
{
  "same_author_probability": 0.75,
  "different_author_probability": 0.25,
  "prediction": "same_author"
}
```

### GET /

Returns basic API information.

### GET /health

Health check endpoint.

## Example Usage

```bash
curl -X POST http://localhost:8000/predict/ \
  -H "Content-Type: application/json" \
  -d '{
    "text1": "This is a sample text written by an author.",
    "text2": "Here is another text that might be by the same person."
  }'
```

## Models

The backend uses pre-trained models stored in the `models/` directory:
- `vectorizer.pkl` - TF-IDF vectorizer
- `classifier.pkl` - Logistic regression classifier

If these models are not available or invalid, the backend will use a simple heuristic-based approach for demonstration purposes.

## Structure

```
backend/
├── main.py              # FastAPI application entry point
├── requirements.txt     # Python dependencies
├── core/
│   └── ml.py           # ML logic and model loading
├── routers/
│   └── predict.py      # Prediction endpoint
├── schemas/
│   └── prediction.py   # Request/response schemas
└── models/
    ├── vectorizer.pkl  # TF-IDF vectorizer
    └── classifier.pkl  # Classifier model
```

## Dependencies

- FastAPI - Web framework
- Uvicorn - ASGI server
- scikit-learn - Machine learning library
- numpy - Numerical computations
- pydantic - Data validation
