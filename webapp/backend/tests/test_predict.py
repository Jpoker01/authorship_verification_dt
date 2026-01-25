"""
Unit tests for the prediction router.

Tests the /predict endpoint with various scenarios including:
- Successful predictions
- Validation errors
- Error handling
"""
import pytest
from fastapi.testclient import TestClient

# Constants for text generation and validation
MIN_TEXT_LENGTH = 5000  # Minimum required text length
MAX_TEXT_LENGTH = 50000  # Maximum allowed text length
TEXT_MULTIPLIER = 500  # Used to generate text that meets minimum length requirements
VALID_TEXT = "Valid text. " * TEXT_MULTIPLIER  # Pre-generated valid text for tests
EXCEEDS_MAX_TEXT = "x" * (MAX_TEXT_LENGTH + 1)  # Text that exceeds maximum length


def test_predict_success(client, mock_ml_predict, sample_texts):
    """Test successful prediction with valid inputs."""
    # Configure the mock to return a successful prediction
    mock_ml_predict.return_value = {
        "same_author_probability": 0.75
    }
    
    response = client.post("/predict/", json=sample_texts)
    
    assert response.status_code == 200
    data = response.json()
    
    assert "same_author_probability" in data
    assert data["same_author_probability"] == 0.75
    assert 0.0 <= data["same_author_probability"] <= 1.0
    
    # Verify the ML predict function was called with correct arguments
    mock_ml_predict.assert_called_once_with(
        sample_texts["text1"],
        sample_texts["text2"]
    )


def test_predict_text1_too_short(client, mock_ml_predict):
    """Test prediction fails when text1 is too short."""
    short_text = "This is too short."
    
    response = client.post("/predict/", json={
        "text1": short_text,
        "text2": VALID_TEXT
    })
    
    assert response.status_code == 422  # Validation error
    # ML predict should not be called
    mock_ml_predict.assert_not_called()


def test_predict_text2_too_short(client, mock_ml_predict):
    """Test prediction fails when text2 is too short."""
    short_text = "This is too short."
    
    response = client.post("/predict/", json={
        "text1": VALID_TEXT,
        "text2": short_text
    })
    
    assert response.status_code == 422  # Validation error
    # ML predict should not be called
    mock_ml_predict.assert_not_called()


def test_predict_both_texts_too_short(client, mock_ml_predict):
    """Test prediction fails when both texts are too short."""
    short_text1 = "Too short."
    short_text2 = "Also too short."
    
    response = client.post("/predict/", json={
        "text1": short_text1,
        "text2": short_text2
    })
    
    assert response.status_code == 422  # Validation error
    mock_ml_predict.assert_not_called()


def test_predict_text1_too_long(client, mock_ml_predict):
    """Test prediction fails when text1 exceeds maximum length."""
    response = client.post("/predict/", json={
        "text1": EXCEEDS_MAX_TEXT,
        "text2": VALID_TEXT
    })
    
    assert response.status_code == 422  # Validation error
    mock_ml_predict.assert_not_called()


def test_predict_text2_too_long(client, mock_ml_predict):
    """Test prediction fails when text2 exceeds maximum length."""
    response = client.post("/predict/", json={
        "text1": VALID_TEXT,
        "text2": EXCEEDS_MAX_TEXT
    })
    
    assert response.status_code == 422  # Validation error
    mock_ml_predict.assert_not_called()


def test_predict_missing_text1(client, mock_ml_predict):
    """Test prediction fails when text1 is missing."""
    response = client.post("/predict/", json={
        "text2": VALID_TEXT
    })
    
    assert response.status_code == 422  # Validation error
    mock_ml_predict.assert_not_called()


def test_predict_missing_text2(client, mock_ml_predict):
    """Test prediction fails when text2 is missing."""
    response = client.post("/predict/", json={
        "text1": VALID_TEXT
    })
    
    assert response.status_code == 422  # Validation error
    mock_ml_predict.assert_not_called()


def test_predict_empty_request_body(client, mock_ml_predict):
    """Test prediction fails with empty request body."""
    response = client.post("/predict/", json={})
    
    assert response.status_code == 422  # Validation error
    mock_ml_predict.assert_not_called()


def test_predict_ml_error(client, mock_ml_predict, sample_texts):
    """Test error handling when ML prediction fails."""
    # Configure the mock to raise an exception
    mock_ml_predict.side_effect = Exception("Model loading failed")
    
    response = client.post("/predict/", json=sample_texts)
    
    assert response.status_code == 500  # Internal server error
    data = response.json()
    
    assert "detail" in data
    assert "Prediction failed" in data["detail"]


def test_predict_probability_boundaries(client, mock_ml_predict, sample_texts):
    """Test that probability values are correctly bounded."""
    # Test with probability 0.0
    mock_ml_predict.return_value = {
        "same_author_probability": 0.0
    }
    response = client.post("/predict/", json=sample_texts)
    assert response.status_code == 200
    assert response.json()["same_author_probability"] == 0.0
    
    # Test with probability 1.0
    mock_ml_predict.return_value = {
        "same_author_probability": 1.0
    }
    response = client.post("/predict/", json=sample_texts)
    assert response.status_code == 200
    assert response.json()["same_author_probability"] == 1.0
    
    # Test with probability 0.5
    mock_ml_predict.return_value = {
        "same_author_probability": 0.5
    }
    response = client.post("/predict/", json=sample_texts)
    assert response.status_code == 200
    assert response.json()["same_author_probability"] == 0.5


def test_predict_wrong_http_method(client, sample_texts):
    """Test that GET is not allowed on predict endpoint."""
    response = client.get("/predict/", params=sample_texts)
    
    assert response.status_code == 405  # Method Not Allowed


def test_predict_with_invalid_json(client):
    """Test prediction fails with invalid JSON."""
    response = client.post(
        "/predict/",
        data="invalid json",
        headers={"Content-Type": "application/json"}
    )
    
    assert response.status_code == 422  # Unprocessable Entity
