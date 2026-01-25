"""
Unit tests for the token authentication middleware.

Tests the TokenAuthMiddleware with various scenarios including:
- Public access (no token configured)
- Protected access (token configured)
- Health endpoint exemption
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import os
import sys


@pytest.fixture
def client_no_token():
    """Client without token authentication (ACCESS_TOKEN not set)."""
    # Clear the environment
    os.environ.pop('ACCESS_TOKEN', None)
    
    # Reload modules to pick up the new environment
    modules_to_reload = ['core.config', 'middleware.auth', 'main']
    for module in modules_to_reload:
        sys.modules.pop(module, None)
    
    from main import app
    client = TestClient(app)
    yield client
    
    # Cleanup after test
    os.environ.pop('ACCESS_TOKEN', None)
    for module in modules_to_reload:
        sys.modules.pop(module, None)


@pytest.fixture
def client_with_token():
    """Client with token authentication enabled."""
    # Set the token
    os.environ['ACCESS_TOKEN'] = 'test_secret_token'
    
    # Reload modules to pick up the new environment
    modules_to_reload = ['core.config', 'middleware.auth', 'main']
    for module in modules_to_reload:
        sys.modules.pop(module, None)
    
    from main import app
    client = TestClient(app)
    yield client
    
    # Cleanup after test
    os.environ.pop('ACCESS_TOKEN', None)
    for module in modules_to_reload:
        sys.modules.pop(module, None)


def test_public_access_no_token_configured(client_no_token):
    """Test that all endpoints are accessible when no token is configured."""
    # Test root endpoint
    response = client_no_token.get("/")
    assert response.status_code == 200
    
    # Test health endpoint
    response = client_no_token.get("/health")
    assert response.status_code == 200


def test_health_endpoint_always_accessible_with_token(client_with_token):
    """Test that health endpoint is always accessible even when token is configured."""
    response = client_with_token.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root_endpoint_requires_token(client_with_token):
    """Test that root endpoint requires token when authentication is enabled."""
    # Without token
    response = client_with_token.get("/")
    assert response.status_code == 403
    assert "Access denied" in response.json()["detail"]
    
    # With correct token
    response = client_with_token.get("/?token=test_secret_token")
    assert response.status_code == 200


def test_predict_endpoint_requires_token(client_with_token):
    """Test that predict endpoint requires token when authentication is enabled."""
    # Without token
    response = client_with_token.post("/predict/", json={
        "text1": "test" * 2000,
        "text2": "test" * 2000
    })
    assert response.status_code == 403
    assert "Access denied" in response.json()["detail"]


def test_wrong_token_rejected(client_with_token):
    """Test that wrong token is rejected."""
    response = client_with_token.get("/?token=wrong_token")
    assert response.status_code == 403
    assert "Access denied" in response.json()["detail"]


def test_empty_token_rejected(client_with_token):
    """Test that empty token is rejected."""
    response = client_with_token.get("/?token=")
    assert response.status_code == 403


def test_correct_token_grants_access(client_with_token):
    """Test that correct token grants access to protected endpoints."""
    response = client_with_token.get("/?token=test_secret_token")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_token_in_all_requests(client_with_token):
    """Test that token works for multiple different requests."""
    # Test root
    response = client_with_token.get("/?token=test_secret_token")
    assert response.status_code == 200
    
    # Test docs access (if available)
    response = client_with_token.get("/docs?token=test_secret_token")
    # Docs might return 200 or redirect, just ensure it's not 403
    assert response.status_code != 403


def test_case_sensitive_token(client_with_token):
    """Test that token matching is case-sensitive."""
    response = client_with_token.get("/?token=TEST_SECRET_TOKEN")
    assert response.status_code == 403
    
    response = client_with_token.get("/?token=test_secret_token")
    assert response.status_code == 200


def test_health_without_token_with_auth_enabled(client_with_token):
    """Test health endpoint doesn't require token even when auth is enabled."""
    response = client_with_token.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
