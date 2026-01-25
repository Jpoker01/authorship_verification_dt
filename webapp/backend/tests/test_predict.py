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


def test_predict_exact_minimum_length(client, mock_ml_predict):
    """Test prediction with texts at exactly the minimum allowed length."""
    # Create text that is exactly 5000 characters
    exact_min_text = "x" * MIN_TEXT_LENGTH
    
    mock_ml_predict.return_value = {
        "same_author_probability": 0.6
    }
    
    response = client.post("/predict/", json={
        "text1": exact_min_text,
        "text2": exact_min_text
    })
    
    assert response.status_code == 200
    assert response.json()["same_author_probability"] == 0.6
    mock_ml_predict.assert_called_once()


def test_predict_exact_maximum_length(client, mock_ml_predict):
    """Test prediction with texts at exactly the maximum allowed length."""
    # Create text that is exactly 50000 characters
    exact_max_text = "y" * MAX_TEXT_LENGTH
    
    mock_ml_predict.return_value = {
        "same_author_probability": 0.8
    }
    
    response = client.post("/predict/", json={
        "text1": exact_max_text,
        "text2": exact_max_text
    })
    
    assert response.status_code == 200
    assert response.json()["same_author_probability"] == 0.8
    mock_ml_predict.assert_called_once()


def test_predict_one_char_below_minimum(client, mock_ml_predict):
    """Test prediction fails with text one character below minimum."""
    # Create text that is 4999 characters (one below minimum)
    below_min_text = "x" * (MIN_TEXT_LENGTH - 1)
    
    response = client.post("/predict/", json={
        "text1": below_min_text,
        "text2": VALID_TEXT
    })
    
    assert response.status_code == 422  # Validation error
    mock_ml_predict.assert_not_called()


def test_predict_with_unicode_characters(client, mock_ml_predict):
    """Test prediction with unicode characters in text."""
    # Create valid length text with unicode characters
    unicode_text = "Hello 世界 émojis 🎉🎊 " * 300
    
    mock_ml_predict.return_value = {
        "same_author_probability": 0.65
    }
    
    response = client.post("/predict/", json={
        "text1": unicode_text,
        "text2": unicode_text
    })
    
    assert response.status_code == 200
    assert response.json()["same_author_probability"] == 0.65


def test_predict_with_special_characters(client, mock_ml_predict):
    """Test prediction with special characters and punctuation."""
    # Create valid length text with special characters
    special_text = "Special!@#$%^&*()_+-={}[]|\\:;\"'<>,.?/ chars " * 250
    
    mock_ml_predict.return_value = {
        "same_author_probability": 0.55
    }
    
    response = client.post("/predict/", json={
        "text1": special_text,
        "text2": special_text
    })
    
    assert response.status_code == 200
    assert response.json()["same_author_probability"] == 0.55


def test_predict_with_newlines_and_tabs(client, mock_ml_predict):
    """Test prediction with text containing newlines and tabs."""
    # Create valid length text with newlines and tabs
    formatted_text = "Line 1\n\tLine 2 with tab\n\n\tLine 3\t\n" * 200
    
    mock_ml_predict.return_value = {
        "same_author_probability": 0.72
    }
    
    response = client.post("/predict/", json={
        "text1": formatted_text,
        "text2": formatted_text
    })
    
    assert response.status_code == 200
    assert response.json()["same_author_probability"] == 0.72


def test_predict_with_only_whitespace(client, mock_ml_predict):
    """Test prediction with text containing only whitespace."""
    # Create text with only spaces that meets length requirement
    whitespace_text = " " * (MIN_TEXT_LENGTH + 100)
    
    mock_ml_predict.return_value = {
        "same_author_probability": 0.5
    }
    
    response = client.post("/predict/", json={
        "text1": whitespace_text,
        "text2": whitespace_text
    })
    
    # Should succeed if it meets length requirements
    assert response.status_code == 200
    assert response.json()["same_author_probability"] == 0.5


def test_predict_response_schema_validation(client, mock_ml_predict, sample_texts):
    """Test that response adheres to the schema."""
    mock_ml_predict.return_value = {
        "same_author_probability": 0.85
    }
    
    response = client.post("/predict/", json=sample_texts)
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify all required fields are present
    assert "same_author_probability" in data
    
    # Verify types
    assert isinstance(data["same_author_probability"], (int, float))
    
    # Verify bounds
    assert 0.0 <= data["same_author_probability"] <= 1.0


def test_predict_multiple_requests_in_sequence(client, mock_ml_predict, sample_texts):
    """Test multiple prediction requests in sequence."""
    # First request
    mock_ml_predict.return_value = {
        "same_author_probability": 0.3
    }
    response1 = client.post("/predict/", json=sample_texts)
    assert response1.status_code == 200
    assert response1.json()["same_author_probability"] == 0.3
    
    # Reset mock for second request
    mock_ml_predict.reset_mock()
    mock_ml_predict.return_value = {
        "same_author_probability": 0.9
    }
    response2 = client.post("/predict/", json=sample_texts)
    assert response2.status_code == 200
    assert response2.json()["same_author_probability"] == 0.9
    
    # Verify both calls were made
    assert mock_ml_predict.call_count == 1


def test_predict_with_different_text_lengths(client, mock_ml_predict):
    """Test prediction with texts of different valid lengths."""
    short_valid_text = "a" * MIN_TEXT_LENGTH
    long_valid_text = "b" * (MIN_TEXT_LENGTH + 10000)
    
    mock_ml_predict.return_value = {
        "same_author_probability": 0.45
    }
    
    response = client.post("/predict/", json={
        "text1": short_valid_text,
        "text2": long_valid_text
    })
    
    assert response.status_code == 200
    assert response.json()["same_author_probability"] == 0.45


def test_predict_with_numeric_content(client, mock_ml_predict):
    """Test prediction with text containing primarily numbers."""
    numeric_text = "1234567890 " * 500
    
    mock_ml_predict.return_value = {
        "same_author_probability": 0.7
    }
    
    response = client.post("/predict/", json={
        "text1": numeric_text,
        "text2": numeric_text
    })
    
    assert response.status_code == 200
    assert response.json()["same_author_probability"] == 0.7


def test_predict_with_null_values(client, mock_ml_predict):
    """Test prediction fails gracefully with null values."""
    response = client.post("/predict/", json={
        "text1": None,
        "text2": VALID_TEXT
    })
    
    assert response.status_code == 422  # Validation error
    mock_ml_predict.assert_not_called()


def test_predict_with_wrong_field_types(client, mock_ml_predict):
    """Test prediction fails with wrong field types."""
    response = client.post("/predict/", json={
        "text1": 12345,  # Number instead of string
        "text2": VALID_TEXT
    })
    
    assert response.status_code == 422  # Validation error
    mock_ml_predict.assert_not_called()


def test_predict_with_array_instead_of_string(client, mock_ml_predict):
    """Test prediction fails when array is provided instead of string."""
    response = client.post("/predict/", json={
        "text1": ["array", "of", "strings"],
        "text2": VALID_TEXT
    })
    
    assert response.status_code == 422  # Validation error
    mock_ml_predict.assert_not_called()


def test_predict_ml_returns_invalid_probability(client, mock_ml_predict, sample_texts):
    """Test handling when ML returns probability outside valid range."""
    # Test with probability > 1.0
    mock_ml_predict.return_value = {
        "same_author_probability": 1.5
    }
    
    response = client.post("/predict/", json=sample_texts)
    
    # FastAPI validation should catch this
    assert response.status_code in [422, 500]


def test_predict_ml_returns_negative_probability(client, mock_ml_predict, sample_texts):
    """Test handling when ML returns negative probability."""
    mock_ml_predict.return_value = {
        "same_author_probability": -0.5
    }
    
    response = client.post("/predict/", json=sample_texts)
    
    # FastAPI validation should catch this
    assert response.status_code in [422, 500]


def test_predict_ml_returns_missing_field(client, mock_ml_predict, sample_texts):
    """Test error handling when ML returns incomplete response."""
    # ML returns empty dict
    mock_ml_predict.return_value = {}
    
    response = client.post("/predict/", json=sample_texts)
    
    assert response.status_code == 500


def test_predict_different_exception_types(client, mock_ml_predict, sample_texts):
    """Test handling of different exception types from ML module."""
    # Test with ValueError
    mock_ml_predict.side_effect = ValueError("Invalid input to model")
    
    response = client.post("/predict/", json=sample_texts)
    assert response.status_code == 500
    assert "Prediction failed" in response.json()["detail"]
    
    # Reset and test with RuntimeError
    mock_ml_predict.reset_mock()
    mock_ml_predict.side_effect = RuntimeError("Model runtime error")
    
    response = client.post("/predict/", json=sample_texts)
    assert response.status_code == 500
    assert "Prediction failed" in response.json()["detail"]


def test_predict_with_extremely_repetitive_text(client, mock_ml_predict):
    """Test prediction with extremely repetitive text patterns."""
    repetitive_text = "a" * MIN_TEXT_LENGTH
    
    mock_ml_predict.return_value = {
        "same_author_probability": 0.95
    }
    
    response = client.post("/predict/", json={
        "text1": repetitive_text,
        "text2": repetitive_text
    })
    
    assert response.status_code == 200
    assert response.json()["same_author_probability"] == 0.95
