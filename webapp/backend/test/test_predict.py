import pytest
from fastapi.testclient import TestClient
from ..core import config

def test_predict_success(client: TestClient, mock_predict, sample_texts):
    """Test prediction success with mocked output of the ml.predict function"""
    mock_predict.return_value = {
        "same_author_probability": 0.75
    }

    response = client.post("/predict/", json=sample_texts)
    assert response.status_code == 200

    data = response.json()
    assert data["same_author_probability"] == 0.75

    mock_predict.assert_called_once_with(sample_texts["text1"], sample_texts["text2"])

# TODO: text1 too short
def test_predict_text1_too_short(client, mock_predict, sample_text):
    """Test prediction fails when text1 is too short."""
    short_text = "Short text"

    response = client.post("/predict/", json={
        "text1": short_text,
        "text2": sample_text
    })

    assert response.status_code == 422  # Unprocessable content error
    mock_predict.assert_not_called()

# TODO: text2 to short
def test_predict_text2_too_short(client, mock_predict, sample_text):
    """Test prediction fails when text1 is too short."""
    short_text = "Short text"

    response = client.post("/predict/", json={
        "text1": sample_text,
        "text2": short_text
    })

    assert response.status_code == 422  # Unprocessable content error
    mock_predict.assert_not_called()

# TODO: both texts too short
def test_predict_both_texts_too_short(client, mock_predict, sample_text):
    """Test prediction fails when both texts are too short."""
    short_text = "Short text"
    response = client.post("/predict/", json={
        "text1": short_text,
        "text2": short_text
    })
    assert response.status_code == 422
    mock_predict.assert_not_called()
    
# TODO: text1 too long

# TODO: text2 too long

# TODO: both texts too long

# TODO: missing text 1

# TODO: missing text 2

# TODO: missing both texts

# TODO: predict with unicode characters

# TODO: predict with special characters

# TODO: predict with newlines and tabs

# TODO: predict with white space

# TODO: predict with numeric content

# TODO: empty json body

# TODO: invalid json body


# TODO: wrong http method

# TODO: model not loaded

