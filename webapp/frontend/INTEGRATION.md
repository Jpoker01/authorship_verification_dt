# Frontend-Backend Integration

This document describes how the frontend connects to the FastAPI backend.

## Configuration

The frontend uses environment variables to configure the backend API URL. 

### Development

1. Copy `.env.example` to `.env.local`:
   ```bash
   cp .env.example .env.local
   ```

2. The default configuration points to `http://localhost:8000` which is the local backend URL.

### Production

Set the `VITE_API_URL` environment variable to your production backend URL:
```bash
export VITE_API_URL=https://your-backend-domain.com
```

## Running the Full Stack

### Start the Backend

```bash
cd webapp/backend
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`

### Start the Frontend

```bash
cd webapp/frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173` (default Vite port)

## API Integration

The frontend communicates with the backend through the `src/services/api.ts` module:

- **`predictAuthorship(text1, text2)`**: Sends texts to `/predict/` endpoint
- **`checkHealth()`**: Checks backend health at `/health` endpoint

### Request Format

```typescript
{
  text1: "First text to compare",
  text2: "Second text to compare"
}
```

### Response Format

```typescript
{
  same_author_probability: 0.75  // Value between 0 and 1
}
```

The frontend converts this to a percentage (0-100) for display.

## Error Handling

The frontend handles two types of errors:

1. **API Errors**: Server returned an error response (4xx, 5xx)
2. **Network Errors**: Failed to connect to the backend

Both are displayed to the user with appropriate error messages.

## Features

- ✅ Real-time API calls to backend
- ✅ Loading states during analysis
- ✅ Error handling and display
- ✅ Probability conversion (0-1 to percentage)
- ✅ Smooth scrolling to results
- ✅ Environment-based configuration
