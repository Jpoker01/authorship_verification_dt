import pytest
from fastapi.testclient import TestClient
from ..core import config

# TODO: success
def test_predict_success(client: TestClient, mock_predict, sample_texts):
    mock_predict.return_value = {
        "same_author_probability": 0.75
    }

    response = client.post("/predict/", json=sample_texts)
    assert response.status_code == 200

    data = response.json()
    assert data["same_author_probability"] == 0.75

    mock_predict.assert_called_once_with(sample_texts["text1"], sample_texts["text2"])
    
# TODO: text1 too short

# TODO: text2 to short

# TODO: both texts too short

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

