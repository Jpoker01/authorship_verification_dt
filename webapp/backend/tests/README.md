# Testing

This directory contains unit tests for the FastAPI backend application.

## Setup

Install test dependencies:

```bash
pip install -r test-requirements.txt
pip install -r requirements.txt
```

## Running Tests

Run all tests:

```bash
pytest tests/
```

Run with verbose output:

```bash
pytest tests/ -v
```

Run specific test file:

```bash
pytest tests/test_main.py
pytest tests/test_predict.py
```

Run specific test:

```bash
pytest tests/test_main.py::test_root_endpoint
```

Run with coverage:

```bash
pytest tests/ --cov=. --cov-report=html
```

## Test Structure

- `conftest.py` - Shared fixtures and configuration
- `test_main.py` - Tests for main application endpoints (root, health)
- `test_predict.py` - Tests for prediction endpoint

## Test Coverage

### Main Endpoints (`test_main.py`)
- Root endpoint (`/`) returns correct metadata
- Health check endpoint (`/health`) returns status
- Method validation (GET only)

### Prediction Endpoint (`test_predict.py`)
- Successful predictions with valid inputs
- Input validation (text length requirements)
- Missing field validation
- Error handling for ML failures
- Probability boundary testing
- HTTP method validation
- Invalid JSON handling
- Edge cases with exact minimum/maximum lengths
- Unicode and special character handling
- Whitespace and formatting tests
- Response schema validation
- Multiple consecutive requests
- Different text lengths combinations
- Numeric content handling
- Type validation (null, wrong types, arrays)
- ML module error scenarios (invalid probabilities, missing fields, different exceptions)
- Repetitive text patterns

## Fixtures

### `client`
Provides a TestClient instance for making requests to the FastAPI app.

### `mock_ml_predict`
Mocks the ML prediction function to avoid loading actual models during testing.

### `sample_texts`
Provides sample text data that meets the minimum length requirements for testing.

## Notes

- Tests use mocking to avoid loading the actual ML models, making tests fast and independent
- All tests are designed to be independent and can run in any order
- The minimum text length is 5000 characters, maximum is 50000 characters
