"""
Routing Logic (Conditional Edges)
=================================

This module defines the ROUTER for our workflow.

WHAT IS A ROUTER?
----------------
In LangGraph, a router is a function that decides which path to take next.
It's used for CONDITIONAL EDGES - branches in the workflow where the next
step depends on some condition.

Our workflow has one key decision point:
    After content generation → Translate OR Skip to end?

HOW CONDITIONAL EDGES WORK:
--------------------------
1. You define a function that takes state and returns a string
2. That string is the NAME of the next node to go to
3. LangGraph uses this to route the workflow

Example:
    Content Agent → should_translate() → "translate" OR "end"
    
    If "translate": go to Translation Agent
    If "end": skip to END node

WHY IS THIS POWERFUL?
--------------------
This allows dynamic workflows where the path isn't predetermined.
Based on user input (target_language), we take different routes.
"""

from blog_agent.models.state import BlogState


def should_translate(state: BlogState) -> str:
    """
    Decide whether to translate the content.
    
    This is a ROUTING FUNCTION used by LangGraph's conditional edges.
    It examines the current state and returns the name of the next node.
    
    Decision Logic:
        - If target_language is set and not empty → "translate"
        - Otherwise → "end" (skip translation)
    
    Args:
        state: Current workflow state
    
    Returns:
        str: Name of the next node ("translate" or "end")
    
    Visual Flow:
        Content Agent
             │
             ▼
        ┌────────────────┐
        │ should_translate│
        └───────┬────────┘
                │
        ┌───────┴───────┐
        │               │
        ▼               ▼
    "translate"       "end"
        │               │
        ▼               │
    Translation        │
       Agent           │
        │              │
        ▼              │
       END ◄───────────┘
    """
    target_language = state.get("target_language")
    
    # Check if translation was requested
    if target_language and target_language.strip():
        return "translate"
    else:
        return "end"


# Export for easy importing
__all__ = ["should_translate"]
