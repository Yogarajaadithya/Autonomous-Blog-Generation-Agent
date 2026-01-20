"""
Content Generation Agent
========================

This agent writes the actual blog post content.

WHAT THIS AGENT DOES:
--------------------
1. Takes the selected title and topic from state
2. Generates a full blog post (800-1200 words)
3. Uses the optional transcript as source material
4. Writes the content back to state

THE GENERATION PROCESS:
----------------------
1. Build context from topic, title, and optional transcript
2. Call the LLM with specific formatting instructions
3. Calculate word count for metadata
4. Return the content and word count
"""

from langchain_core.messages import SystemMessage, HumanMessage

from blog_agent.models.state import BlogState
from blog_agent.prompts.content_prompts import (
    CONTENT_SYSTEM_PROMPT,
    CONTENT_GENERATION_PROMPT,
    CONTENT_WITH_TRANSCRIPT_SECTION,
    CONTENT_NO_TRANSCRIPT_SECTION
)
from blog_agent.utils.llm import get_llm


def content_agent(state: BlogState) -> dict:
    """
    Generate the full blog post content.
    
    This agent takes the selected title and writes a complete blog post.
    It uses a lower temperature (0.7) for more consistent, coherent writing.
    
    Args:
        state: Current workflow state with topic, selected_title, and optional transcript
    
    Returns:
        dict: State updates with blog_content and word_count
    
    State Changes:
        - blog_content: The full blog post in markdown format
        - word_count: Number of words in the content
    """
    # Get LLM with balanced temperature for coherent but engaging writing
    llm = get_llm(temperature=0.7)
    
    # Extract what we need from state
    topic = state["topic"]
    title = state["selected_title"]
    transcript = state.get("transcript")
    style = state.get("style", "professional")
    
    # ═══════════════════════════════════════════════════════════════════
    # Build the transcript section
    # ═══════════════════════════════════════════════════════════════════
    
    if transcript and transcript.strip():
        # Limit transcript length to avoid context window issues
        transcript_text = transcript[:5000]  # ~1000 words
        transcript_section = CONTENT_WITH_TRANSCRIPT_SECTION.format(
            transcript=transcript_text
        )
    else:
        transcript_section = CONTENT_NO_TRANSCRIPT_SECTION
    
    # ═══════════════════════════════════════════════════════════════════
    # Generate the content
    # ═══════════════════════════════════════════════════════════════════
    
    content_prompt = CONTENT_GENERATION_PROMPT.format(
        title=title,
        topic=topic,
        style=style,
        transcript_section=transcript_section
    )
    
    response = llm.invoke([
        SystemMessage(content=CONTENT_SYSTEM_PROMPT),
        HumanMessage(content=content_prompt)
    ])
    
    blog_content = response.content.strip()
    
    # ═══════════════════════════════════════════════════════════════════
    # Calculate word count
    # ═══════════════════════════════════════════════════════════════════
    
    # Simple word count: split on whitespace
    word_count = len(blog_content.split())
    
    # ═══════════════════════════════════════════════════════════════════
    # Return state updates
    # ═══════════════════════════════════════════════════════════════════
    
    return {
        "blog_content": blog_content,
        "word_count": word_count,
        # If no translation is needed, this becomes the final content
        "final_content": blog_content
    }


# Export for easy importing
__all__ = ["content_agent"]
