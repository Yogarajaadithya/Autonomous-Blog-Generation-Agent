"""
Translation Agent
================

This agent translates the blog content to a target language.

WHAT THIS AGENT DOES:
--------------------
1. Takes the blog content and target language from state
2. Translates the entire blog post
3. Preserves markdown formatting
4. Returns the translated content

WHEN IS THIS AGENT USED?
-----------------------
This agent is only called when:
- target_language is specified AND not empty
- The router decides translation is needed

If no translation is needed, this agent is skipped entirely.
This is controlled by the CONDITIONAL EDGE in the workflow graph.
"""

from langchain_core.messages import SystemMessage, HumanMessage

from blog_agent.models.state import BlogState
from blog_agent.prompts.translation_prompts import (
    TRANSLATION_SYSTEM_PROMPT,
    TRANSLATION_PROMPT
)
from blog_agent.utils.llm import get_llm


def translation_agent(state: BlogState) -> dict:
    """
    Translate blog content to the target language.
    
    This agent maintains the original structure and formatting
    while producing a natural-sounding translation.
    
    Args:
        state: Current workflow state with blog_content and target_language
    
    Returns:
        dict: State updates with translated_content and final_content
    
    State Changes:
        - translated_content: The translated blog post
        - final_content: Updated to the translated version
    """
    # Get LLM with lower temperature for accurate translation
    # We want consistency, not creativity when translating
    llm = get_llm(temperature=0.3)
    
    # Extract what we need from state
    content = state["blog_content"]
    target_language = state.get("target_language", "")
    
    # Safety check - shouldn't be called without target language
    if not target_language:
        return {
            "translated_content": None,
            "final_content": content
        }
    
    # ═══════════════════════════════════════════════════════════════════
    # Perform the translation
    # ═══════════════════════════════════════════════════════════════════
    
    translation_prompt = TRANSLATION_PROMPT.format(
        target_language=target_language,
        content=content
    )
    
    response = llm.invoke([
        SystemMessage(content=TRANSLATION_SYSTEM_PROMPT),
        HumanMessage(content=translation_prompt)
    ])
    
    translated_content = response.content.strip()
    
    # ═══════════════════════════════════════════════════════════════════
    # Return state updates
    # ═══════════════════════════════════════════════════════════════════
    
    return {
        "translated_content": translated_content,
        "final_content": translated_content  # Update final to translated version
    }


# Export for easy importing
__all__ = ["translation_agent"]
