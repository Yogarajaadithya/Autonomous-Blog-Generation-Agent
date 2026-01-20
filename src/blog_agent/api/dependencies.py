"""
FastAPI Dependency Injection
============================

This module provides dependencies that can be injected into route handlers.

WHAT IS DEPENDENCY INJECTION?
----------------------------
Instead of creating objects inside your functions, you "inject" them from outside.
This makes code:
- Testable (swap real LLM for mock in tests)
- Flexible (change implementations without changing routes)
- Clean (route handlers stay focused on their job)

HOW FASTAPI DEPENDENCIES WORK:
-----------------------------
1. Define a function that returns what you need
2. Use Depends() in your route to get that function's return value
3. FastAPI calls the function and passes the result to your route

Example:
    @app.get("/")
    def my_route(workflow = Depends(get_workflow)):
        # workflow is automatically injected!
        pass
"""

from functools import lru_cache
from langgraph.graph import StateGraph

from blog_agent.graph.workflow import create_workflow


@lru_cache()
def get_workflow() -> StateGraph:
    """
    Get the compiled LangGraph workflow.
    
    The @lru_cache decorator ensures we only create the workflow once,
    not on every request. This is important because:
    - Creating the graph has overhead
    - We want the same graph instance for all requests
    - It makes the app faster
    
    Returns:
        StateGraph: The compiled blog generation workflow
    
    Usage in routes:
        @app.post("/generate")
        def generate(workflow = Depends(get_workflow)):
            result = workflow.invoke(...)
    """
    return create_workflow()


# Export for easy importing
__all__ = ["get_workflow"]
