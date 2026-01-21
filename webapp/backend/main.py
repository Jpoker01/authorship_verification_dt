"""
FastAPI backend for authorship verification.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import predict

app = FastAPI(
    title="Authorship Verification API",
    description="API for verifying if two texts are written by the same author using TF-IDF and logistic regression",
    version="1.0.0"
)

# Configure CORS
# WARNING: allow_origins=["*"] is used for development/demo purposes.
# In production, replace with specific origins (e.g., ["https://yourdomain.com"])
# or use environment variables to configure allowed origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Replace with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(predict.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Authorship Verification API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}
