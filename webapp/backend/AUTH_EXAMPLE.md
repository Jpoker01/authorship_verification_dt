# Example: Using Token Authentication

This example demonstrates how to use the token-based authentication feature.

## Setup

1. Set your secret token:
```bash
export ACCESS_TOKEN="my_super_secret_token_12345"
```

2. Start the server:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Testing with curl

### Without token (will fail with 403):
```bash
curl http://localhost:8000/
# Response: {"detail":"Access denied. Valid token required."}
```

### With correct token (will succeed):
```bash
curl "http://localhost:8000/?token=my_super_secret_token_12345"
# Response: {"message":"Authorship Verification DT - backend","version":"1.0.0","docs":"/docs"}
```

### Health endpoint (always works, no token needed):
```bash
curl http://localhost:8000/health
# Response: {"status":"ok"}
```

### Making a prediction:
```bash
curl -X POST "http://localhost:8000/predict/?token=my_super_secret_token_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "text1": "'$(python3 -c "print('Sample text for authorship verification. ' * 300)")'",
    "text2": "'$(python3 -c "print('Another sample text for comparison. ' * 300)")'"
  }'
```

## Python Client Example

```python
import requests

# Configuration
BASE_URL = "http://localhost:8000"
TOKEN = "my_super_secret_token_12345"

# Helper function to add token
def make_request(endpoint, method="GET", json_data=None):
    url = f"{BASE_URL}{endpoint}"
    params = {"token": TOKEN}
    
    if method == "GET":
        response = requests.get(url, params=params)
    elif method == "POST":
        response = requests.post(url, params=params, json=json_data)
    
    return response

# Test root endpoint
response = make_request("/")
print("Root:", response.json())

# Test prediction
text1 = "Sample text for authorship verification. " * 300
text2 = "Another sample text for comparison. " * 300

response = make_request(
    "/predict/",
    method="POST",
    json_data={"text1": text1, "text2": text2}
)
print("Prediction:", response.json())

# Health check (no token needed, but token doesn't hurt)
response = requests.get(f"{BASE_URL}/health")
print("Health:", response.json())
```

## JavaScript/Fetch Example

```javascript
const BASE_URL = 'http://localhost:8000';
const TOKEN = 'my_super_secret_token_12345';

// Helper function
async function makeRequest(endpoint, options = {}) {
    const url = new URL(`${BASE_URL}${endpoint}`);
    url.searchParams.append('token', TOKEN);
    
    const response = await fetch(url, options);
    return response.json();
}

// Test root endpoint
const rootData = await makeRequest('/');
console.log('Root:', rootData);

// Test prediction
const text1 = 'Sample text for authorship verification. '.repeat(300);
const text2 = 'Another sample text for comparison. '.repeat(300);

const predictionData = await makeRequest('/predict/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text1, text2 }),
});
console.log('Prediction:', predictionData);
```

## Deployment Considerations

### Production Deployment

1. **Use HTTPS**: Always use HTTPS to prevent token interception
   ```nginx
   # Nginx configuration example
   server {
       listen 443 ssl;
       server_name yourdomain.com;
       
       ssl_certificate /path/to/cert.pem;
       ssl_certificate_key /path/to/key.pem;
       
       location / {
           proxy_pass http://localhost:8000;
       }
   }
   ```

2. **Strong Token**: Generate a secure random token
   ```bash
   # Generate a strong token (Linux/Mac)
   python3 -c "import secrets; print(secrets.token_urlsafe(32))"
   # Example output: Xg7_p2vK9HmN4qR8-sT5zL3bY6wC1dF0eA
   ```

3. **Environment Variables**: Use a `.env` file (never commit it!)
   ```bash
   # .env file
   ACCESS_TOKEN=your_generated_token_here
   ```

4. **Token Rotation**: Regularly change the token for security

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Token is passed as environment variable at runtime
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Run with Docker
docker run -p 8000:8000 -e ACCESS_TOKEN="your_token" your-image
```

## Disabling Authentication

To disable authentication and make the app public:

```bash
unset ACCESS_TOKEN
uvicorn main:app --host 0.0.0.0 --port 8000
```

Or in Docker:
```bash
docker run -p 8000:8000 your-image
# (without -e ACCESS_TOKEN)
```
