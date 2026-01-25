"""
Unit tests for main FastAPI endpoints.

Tests the root and health check endpoints.
"""
import pytest
from fastapi.testclient import TestClient


def test_root_endpoint(client):
    """Test the root endpoint returns correct response."""
    response = client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "message" in data
    assert "version" in data
    assert "docs" in data
    assert data["message"] == "Authorship Verification DT - backend"
    assert data["version"] == "1.0.0"
    assert data["docs"] == "/docs"


def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "status" in data
    assert data["status"] == "ok"


def test_root_endpoint_method_not_allowed(client):
    """Test that POST is not allowed on root endpoint."""
    response = client.post("/")
    
    assert response.status_code == 405  # Method Not Allowed


def test_health_endpoint_method_not_allowed(client):
    """Test that POST is not allowed on health endpoint."""
    response = client.post("/health")
    
    assert response.status_code == 405  # Method Not Allowed
