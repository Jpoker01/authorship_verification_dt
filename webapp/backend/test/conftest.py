import json

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from pathlib import Path

from .. import main

@pytest.fixture
def client():
    """
    Create a test client for the FastAPI application.
    """
    return TestClient(main.app)

@pytest.fixture
def mock_predict():
    """
    Mack the predict function from predict router to avoid loading the actual model
    """
    with patch('main.predict') as mock_predict:
        yield mock_predict

@pytest.fixture
def sample_texts():
    json.load(Path(__file__).parent / "data" / "sample_texts.json"

