# Token-Based Authentication

The FastAPI backend includes simple token-based authentication to restrict access to chosen individuals.

## How It Works

The application can be configured to require a secret token in the URL query parameters for all requests (except the health endpoint).

### Configuration

Set the `ACCESS_TOKEN` environment variable to enable authentication:

```bash
export ACCESS_TOKEN="your_secret_token_here"
```

If `ACCESS_TOKEN` is not set, the application is publicly accessible (default behavior).

### Usage

When authentication is enabled, all requests must include the token as a query parameter:

```
GET http://your-domain.com/?token=your_secret_token_here
POST http://your-domain.com/predict/?token=your_secret_token_here
```

### Exempt Endpoints

The `/health` endpoint is always accessible without authentication to allow for health checks and monitoring.

### Example

1. **Start the server with authentication:**
   ```bash
   export ACCESS_TOKEN="my_secret_123"
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

2. **Access protected endpoints:**
   ```bash
   # This will be rejected (403 Forbidden)
   curl http://localhost:8000/

   # This will succeed (200 OK)
   curl http://localhost:8000/?token=my_secret_123

   # Health check always works without token
   curl http://localhost:8000/health
   ```

3. **Making predictions:**
   ```bash
   curl -X POST "http://localhost:8000/predict/?token=my_secret_123" \
     -H "Content-Type: application/json" \
     -d '{"text1": "...", "text2": "..."}'
   ```

### Security Considerations

- **HTTPS Required**: Always use HTTPS in production to prevent token exposure.
- **Token Strength**: Use a strong, randomly generated token (recommended: 32+ characters).
- **Token Rotation**: Regularly rotate the token for security.
- **Access Logs**: Monitor access logs for unauthorized attempts.

### Disabling Authentication

To make the application publicly accessible, simply don't set the `ACCESS_TOKEN` environment variable:

```bash
unset ACCESS_TOKEN
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Implementation Details

The authentication is implemented as a FastAPI middleware (`TokenAuthMiddleware`) that:
1. Checks if `ACCESS_TOKEN` is configured
2. If configured, validates the token from query parameters on each request
3. Always allows access to `/health` endpoint
4. Returns 403 Forbidden for invalid or missing tokens
