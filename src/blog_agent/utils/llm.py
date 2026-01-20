"""
LLM (Large Language Model) Client Setup
========================================

This module creates and configures the LLM client we'll use throughout the app.

WHY THIS EXISTS:
---------------
- Centralizes LLM configuration in one place
- Makes it easy to swap LLM providers (OpenAI → Azure → etc.)
- Ensures consistent settings across all agents
- Handles API key loading securely

HOW IT WORKS (AZURE OPENAI):
----------------------------
We use AzureChatOpenAI which connects to your Azure deployment.
Azure OpenAI requires:
- Endpoint URL (your Azure resource URL)
- API Key (from Azure portal)
- Deployment Name (the model you deployed)
- API Version (Azure API version)
"""

from langchain_openai import AzureChatOpenAI

from blog_agent.utils.config import get_settings


def get_llm(
    temperature: float = 0.7,
    deployment: str | None = None
) -> AzureChatOpenAI:
    """
    Get a configured Azure OpenAI LLM instance.
    
    WHY TEMPERATURE?
    ----------------
    Temperature controls randomness in the AI's responses:
    - 0.0 = Very deterministic, same input → same output
    - 0.7 = Good balance of creativity and consistency (our default)
    - 1.0 = Maximum creativity, but may be inconsistent
    
    For blog writing, 0.7 gives us creative content without being too random.
    
    Args:
        temperature: Controls creativity (0.0 = robotic, 1.0 = wild)
        deployment: Override the default deployment name from settings
    
    Returns:
        AzureChatOpenAI: A configured LLM ready to use
    
    Example:
        >>> llm = get_llm()
        >>> response = llm.invoke("Write a haiku about coding")
        >>> print(response.content)
    """
    settings = get_settings()
    
    return AzureChatOpenAI(
        azure_endpoint=settings.azure_openai_endpoint,
        api_key=settings.azure_openai_api_key,
        api_version=settings.azure_openai_api_version,
        azure_deployment=deployment or settings.azure_openai_deployment,
        temperature=temperature,
    )


# Export for easy importing
__all__ = ["get_llm"]
