"""
Pydantic schemas for prediction requests and responses.
"""
from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    """Request model for authorship verification."""
    text1: str = Field(..., description="First text to compare", min_length=1)
    text2: str = Field(..., description="Second text to compare", min_length=1)
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "text1": "This is a sample text written by an author.",
                    "text2": "Here is another text that might be by the same person."
                }
            ]
        }
    }


class PredictionResponse(BaseModel):
    """Response model for authorship verification."""
    same_author_probability: float = Field(
        ..., 
        description="Probability that both texts are written by the same author",
        ge=0.0,
        le=1.0
    )
    different_author_probability: float = Field(
        ..., 
        description="Probability that texts are written by different authors",
        ge=0.0,
        le=1.0
    )
    prediction: str = Field(
        ..., 
        description="Predicted classification: 'same_author' or 'different_author'"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "same_author_probability": 0.75,
                    "different_author_probability": 0.25,
                    "prediction": "same_author"
                }
            ]
        }
    }
