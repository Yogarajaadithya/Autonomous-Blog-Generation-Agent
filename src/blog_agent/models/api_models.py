"""
API Request/Response Models
===========================

This module defines the Pydantic models for our FastAPI endpoints.

WHY THIS EXISTS:
---------------
When building an API, you need to clearly define:
1. What data the client should send (Request models)
2. What data the server will return (Response models)

Pydantic provides:
- Automatic validation (reject bad data before it causes problems)
- Type coercion (convert "123" to 123 automatically)
- Documentation (Swagger UI reads these models)
- Serialization (convert Python objects to JSON)

HOW IT WORKS:
-------------
We define classes that inherit from BaseModel.
Each field has a type annotation and optional validation.
FastAPI uses these models to validate incoming requests automatically.

Example:
    @app.post("/generate")
    def generate(request: BlogGenerationRequest):  # Auto-validated!
        ...
"""

from typing import Optional, List
from pydantic import BaseModel, Field


class BlogGenerationRequest(BaseModel):
    """
    What the client sends to generate a blog post.
    
    This is the "input" to our system. The client makes a POST request
    with this JSON body, and we validate it before processing.
    
    Example JSON:
    {
        "topic": "Benefits of remote work",
        "transcript": null,
        "target_language": "Spanish",
        "style": "professional"
    }
    """
    
    topic: str = Field(
        ...,  # ... means required
        min_length=3,
        max_length=500,
        description="The main topic to write about",
        json_schema_extra={"example": "Benefits of Remote Work in 2024"}
    )
    
    transcript: Optional[str] = Field(
        default=None,
        max_length=50000,  # About 10,000 words max
        description="Optional video/podcast transcript to base the blog on"
    )
    
    target_language: Optional[str] = Field(
        default=None,
        description="Language to translate the final content into (e.g., 'Spanish', 'French')"
    )
    
    style: str = Field(
        default="professional",
        description="Writing style: professional, casual, technical, or storytelling"
    )


class BlogGenerationResponse(BaseModel):
    """
    What the server returns after generating a blog post.
    
    This is the "output" of our system. It includes the generated
    content plus metadata about the generation process.
    
    Example JSON:
    {
        "title": "10 Game-Changing Benefits of Remote Work in 2024",
        "content": "# 10 Game-Changing Benefits...\n\n...",
        "word_count": 1250,
        "generation_time_seconds": 12.5,
        "was_translated": true,
        "target_language": "Spanish"
    }
    """
    
    title: str = Field(
        description="The generated blog title"
    )
    
    content: str = Field(
        description="The full blog content in markdown format"
    )
    
    word_count: int = Field(
        description="Number of words in the content"
    )
    
    generation_time_seconds: float = Field(
        description="How long the generation took"
    )
    
    was_translated: bool = Field(
        default=False,
        description="Whether the content was translated"
    )
    
    target_language: Optional[str] = Field(
        default=None,
        description="The language it was translated to (if applicable)"
    )
    
    brainstormed_titles: List[str] = Field(
        default_factory=list,
        description="All the title options that were considered"
    )


class HealthResponse(BaseModel):
    """
    Health check response for monitoring.
    
    This endpoint is used by load balancers and monitoring tools
    to check if the service is running properly.
    """
    
    status: str = Field(
        description="Service status (healthy, degraded, unhealthy)"
    )
    
    version: str = Field(
        description="Application version"
    )


class ErrorResponse(BaseModel):
    """
    Standard error response format.
    
    When something goes wrong, we return a consistent error format
    so clients can handle errors predictably.
    """
    
    error: str = Field(
        description="Error type/code"
    )
    
    message: str = Field(
        description="Human-readable error message"
    )
    
    details: Optional[dict] = Field(
        default=None,
        description="Additional error details (for debugging)"
    )


# Export for easy importing
__all__ = [
    "BlogGenerationRequest",
    "BlogGenerationResponse", 
    "HealthResponse",
    "ErrorResponse"
]
