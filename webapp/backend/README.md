### Backend app for authorship verification diploma thesis

This is a backend application developed as part of a diploma thesis on authorship verification. This application performs the core logic of the full application and provides a REST API for the frontend application.

This app runs on Python 3.11 and uses FastAPI v0.109.1. The full list of used libraries is listed in the "requirements.txt" file.

## Authentication

The application supports optional token-based authentication to restrict access. See [AUTH.md](AUTH.md) for details.

**Quick setup:**
```bash
# Enable authentication
export ACCESS_TOKEN="your_secret_token"

# Access with token
curl "http://localhost:8000/?token=your_secret_token"
```

## Testing

The backend includes comprehensive unit tests for all FastAPI endpoints. To run the tests:

```bash
# Install dependencies
pip install -r requirements.txt
pip install -r test-requirements.txt

# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/test_main.py
```

For more information about the testing setup, see [tests/README.md](tests/README.md).
