"""
API Routes
==========

This module defines all the HTTP endpoints for our blog generation service.

HOW FASTAPI ROUTES WORK:
-----------------------
Routes are functions decorated with HTTP method decorators (@app.get, @app.post, etc.)
Each route:
1. Has a path (e.g., "/api/v1/generate")
2. Has a request model (what the client sends)  
3. Has a response model (what we return)
4. Contains the logic to process the request

ENDPOINT DESIGN:
---------------
We follow RESTful conventions:
- POST /api/v1/generate - Create a new blog post
- GET /api/v1/health - Check service status

The "/api/v1" prefix allows for future versioning:
- v1 stays stable
- v2 can have breaking changes
"""

import time
from fastapi import APIRouter, HTTPException, Depends
from langgraph.graph import StateGraph

from blog_agent.models.api_models import (
    BlogGenerationRequest,
    BlogGenerationResponse,
    HealthResponse,
    ErrorResponse
)
from blog_agent.models.state import BlogState
from blog_agent.api.dependencies import get_workflow


# Create a router (groups related routes together)
router = APIRouter(prefix="/api/v1", tags=["Blog Generation"])


@router.post(
    "/generate",
    response_model=BlogGenerationResponse,
    responses={
        200: {"description": "Blog generated successfully"},
        500: {"model": ErrorResponse, "description": "Generation failed"}
    }
)
async def generate_blog(
    request: BlogGenerationRequest,
    workflow: StateGraph = Depends(get_workflow)
) -> BlogGenerationResponse:
    """
    Generate a blog post from a topic.
    
    This is the main endpoint of our service. It:
    1. Validates the incoming request
    2. Runs the LangGraph workflow
    3. Returns the generated content
    
    The workflow runs through:
    - Title Agent (generates titles)
    - Content Agent (writes the post)
    - Translation Agent (optional, if target_language specified)
    
    Request Body:
        topic: What to write about (required)
        transcript: Source material (optional)
        target_language: Translation language (optional)
        style: Writing style (default: professional)
    
    Returns:
        The generated blog post with metadata
    """
    try:
        # Record start time
        start_time = time.time()
        
        # Prepare initial state
        initial_state: BlogState = {
            "topic": request.topic,
            "transcript": request.transcript,
            "target_language": request.target_language,
            "style": request.style,
            # Initialize with defaults
            "brainstormed_titles": [],
            "selected_title": "",
            "blog_content": "",
            "translated_content": None,
            "final_content": "",
            "word_count": 0,
            "generation_time": 0.0,
        }
        
        # Run the workflow
        # This executes: title_agent → content_agent → (translation_agent?)
        result = workflow.invoke(initial_state)
        
        # Calculate generation time
        generation_time = time.time() - start_time
        
        # Build response
        return BlogGenerationResponse(
            title=result["selected_title"],
            content=result["final_content"],
            word_count=result["word_count"],
            generation_time_seconds=round(generation_time, 2),
            was_translated=bool(result.get("translated_content")),
            target_language=request.target_language,
            brainstormed_titles=result["brainstormed_titles"]
        )
        
    except Exception as e:
        # Log the error (in production, use proper logging)
        print(f"Error generating blog: {e}")
        
        raise HTTPException(
            status_code=500,
            detail={
                "error": "generation_failed",
                "message": f"Failed to generate blog: {str(e)}"
            }
        )


@router.get(
    "/health",
    response_model=HealthResponse
)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.
    
    This endpoint is used by:
    - Load balancers (to know if this instance is healthy)
    - Monitoring tools (to check service status)
    - Kubernetes (for liveness/readiness probes)
    
    Returns:
        Service status and version
    """
    from blog_agent import __version__
    
    return HealthResponse(
        status="healthy",
        version=__version__
    )


# Export for easy importing
__all__ = ["router"]
