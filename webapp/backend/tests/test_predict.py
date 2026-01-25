"""
Unit tests for the prediction router.

Tests the /predict endpoint with various scenarios including:
- Successful predictions
- Validation errors
- Error handling
"""
import pytest
from fastapi.testclient import TestClient


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
    long_text = "Valid text. " * 500
    
    response = client.post("/predict/", json={
        "text1": short_text,
        "text2": long_text
    })
    
    assert response.status_code == 422  # Validation error
    # ML predict should not be called
    mock_ml_predict.assert_not_called()


def test_predict_text2_too_short(client, mock_ml_predict):
    """Test prediction fails when text2 is too short."""
    long_text = "Valid text. " * 500
    short_text = "This is too short."
    
    response = client.post("/predict/", json={
        "text1": long_text,
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
    too_long_text = "x" * 50001  # Exceeds max of 50000
    valid_text = "Valid text. " * 500
    
    response = client.post("/predict/", json={
        "text1": too_long_text,
        "text2": valid_text
    })
    
    assert response.status_code == 422  # Validation error
    mock_ml_predict.assert_not_called()


def test_predict_text2_too_long(client, mock_ml_predict):
    """Test prediction fails when text2 exceeds maximum length."""
    valid_text = "Valid text. " * 500
    too_long_text = "x" * 50001  # Exceeds max of 50000
    
    response = client.post("/predict/", json={
        "text1": valid_text,
        "text2": too_long_text
    })
    
    assert response.status_code == 422  # Validation error
    mock_ml_predict.assert_not_called()


def test_predict_missing_text1(client, mock_ml_predict):
    """Test prediction fails when text1 is missing."""
    valid_text = "Valid text. " * 500
    
    response = client.post("/predict/", json={
        "text2": valid_text
    })
    
    assert response.status_code == 422  # Validation error
    mock_ml_predict.assert_not_called()


def test_predict_missing_text2(client, mock_ml_predict):
    """Test prediction fails when text2 is missing."""
    valid_text = "Valid text. " * 500
    
    response = client.post("/predict/", json={
        "text1": valid_text
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
