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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
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
