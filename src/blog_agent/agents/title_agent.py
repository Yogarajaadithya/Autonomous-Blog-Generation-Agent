"""
Title Brainstorming Agent
=========================

This agent generates creative, SEO-friendly blog titles.

WHAT THIS AGENT DOES:
--------------------
1. Takes the topic (and optional transcript) from state
2. Generates 5 title options using the LLM
3. Selects the best title based on SEO principles
4. Writes both the options and selection back to state

HOW LANGGRAPH AGENTS WORK:
--------------------------
An "agent" in LangGraph is just a function that:
- Takes the current state as input
- Does some work (usually calling an LLM)
- Returns a dictionary of state updates

The agent doesn't return the ENTIRE state, just the fields it wants to change.
LangGraph handles merging these updates.

Example:
    # State before: {"topic": "AI", "selected_title": ""}
    # Agent returns: {"selected_title": "The Future of AI"}
    # State after:  {"topic": "AI", "selected_title": "The Future of AI"}
"""

from langchain_core.messages import SystemMessage, HumanMessage

from blog_agent.models.state import BlogState
from blog_agent.prompts.title_prompts import (
    TITLE_SYSTEM_PROMPT,
    TITLE_GENERATION_PROMPT,
    TITLE_SELECTION_PROMPT
)
from blog_agent.utils.llm import get_llm


def title_agent(state: BlogState) -> dict:
    """
    Generate and select a blog title.
    
    This is a LANGGRAPH NODE function. It:
    1. Receives the current state
    2. Generates 5 title options
    3. Selects the best one
    4. Returns state updates
    
    Args:
        state: Current workflow state containing topic and optional transcript
    
    Returns:
        dict: State updates with brainstormed_titles and selected_title
    
    State Changes:
        - brainstormed_titles: List of 5 generated titles
        - selected_title: The best title from the list
    """
    # Get the LLM with slightly higher temperature for creativity
    llm = get_llm(temperature=0.8)
    
    # Extract what we need from state
    topic = state["topic"]
    transcript = state.get("transcript")
    style = state.get("style", "professional")
    
    # Build the transcript section for the prompt
    if transcript:
        transcript_section = f"SOURCE TRANSCRIPT:\n{transcript[:2000]}..."  # Limit length
    else:
        transcript_section = "No transcript provided - generate titles based on topic alone."
    
    # ═══════════════════════════════════════════════════════════════════
    # STEP 1: Generate 5 title options
    # ═══════════════════════════════════════════════════════════════════
    
    generation_prompt = TITLE_GENERATION_PROMPT.format(
        topic=topic,
        transcript_section=transcript_section,
        style=style
    )
    
    generation_response = llm.invoke([
        SystemMessage(content=TITLE_SYSTEM_PROMPT),
        HumanMessage(content=generation_prompt)
    ])
    
    # Parse the numbered list of titles
    raw_titles = generation_response.content.strip()
    titles = []
    for line in raw_titles.split("\n"):
        # Remove numbering (1. 2. etc.) and clean up
        line = line.strip()
        if line and line[0].isdigit():
            # Remove "1. " or "1) " prefix
            title = line.split(".", 1)[-1].split(")", 1)[-1].strip()
            if title:
                titles.append(title)
    
    # Fallback if parsing failed
    if not titles:
        titles = [f"Complete Guide to {topic}"]
    
    # ═══════════════════════════════════════════════════════════════════
    # STEP 2: Select the best title
    # ═══════════════════════════════════════════════════════════════════
    
    # Format titles for selection prompt
    titles_formatted = "\n".join([f"{i+1}. {t}" for i, t in enumerate(titles)])
    
    selection_prompt = TITLE_SELECTION_PROMPT.format(
        titles=titles_formatted,
        topic=topic,
        style=style
    )
    
    selection_response = llm.invoke([
        SystemMessage(content=TITLE_SYSTEM_PROMPT),
        HumanMessage(content=selection_prompt)
    ])
    
    selected_title = selection_response.content.strip()
    
    # Validate selection - make sure it's one of our generated titles
    if selected_title not in titles:
        # If LLM returned something weird, just use the first title
        selected_title = titles[0]
    
    # ═══════════════════════════════════════════════════════════════════
    # Return state updates
    # ═══════════════════════════════════════════════════════════════════
    
    return {
        "brainstormed_titles": titles,
        "selected_title": selected_title
    }


# Export for easy importing
__all__ = ["title_agent"]
