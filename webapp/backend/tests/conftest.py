"""
Pytest configuration and shared fixtures for FastAPI testing.
"""
import sys
import os
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

# Add parent directory to path to allow imports from backend modules
sys.path.insert(0, str(Path(__file__).parent.parent))

# Ensure ACCESS_TOKEN is not set by default for tests
os.environ.pop('ACCESS_TOKEN', None)


@pytest.fixture
def client():
    """
    Create a test client for FastAPI app.
    
    This fixture provides a TestClient instance that can be used
    to make requests to the FastAPI application without starting a server.
    Authentication is disabled for these tests by not setting ACCESS_TOKEN.
    """
    from main import app
    return TestClient(app)


@pytest.fixture
def mock_ml_predict():
    """
    Mock the ML predict function to avoid loading actual models.
    
    Returns a mock that can be configured for different test scenarios.
    """
    with patch("core.ml.predict") as mock_predict:
        yield mock_predict


@pytest.fixture
def sample_texts():
    """
    Provide sample texts for testing that meet the minimum length requirements.
    
    Returns a dictionary with text1 and text2 that are at least 5000 characters.
    """
    # Create texts that meet the minimum 5000 character requirement
    text_base = "This is a sample text for testing authorship verification. " * 100
    return {
        "text1": text_base,
        "text2": text_base + "Additional content for variation. " * 50
    }
