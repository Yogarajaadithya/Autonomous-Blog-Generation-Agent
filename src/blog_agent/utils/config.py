"""
Configuration Management Module
================================

This module handles all application settings and configuration.

WHY THIS EXISTS:
---------------
- Centralizes all configuration in one place
- Loads secrets from environment variables (never hardcode API keys!)
- Provides type-safe settings with validation
- Makes it easy to switch between development and production

HOW IT WORKS:
-------------
1. Load .env file using python-dotenv
2. Create a Settings class with Pydantic for validation
3. Access settings anywhere via get_settings() function
"""

import os
from functools import lru_cache
from typing import Optional

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

# Load environment variables from .env file
# This MUST be called before accessing os.environ
load_dotenv()


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Pydantic automatically reads from environment variables
    and validates the types. If a required field is missing,
    it will raise an error immediately.
    """
    
    # Azure OpenAI Configuration
    azure_openai_api_key: str = Field(
        default="",
        description="Your Azure OpenAI API key"
    )
    azure_openai_endpoint: str = Field(
        default="",
        description="Azure OpenAI endpoint URL"
    )
    azure_openai_api_version: str = Field(
        default="2025-01-01-preview",
        description="Azure OpenAI API version"
    )
    azure_openai_deployment: str = Field(
        default="gpt-4.1",
        description="Azure OpenAI deployment name"
    )
    
    # LangSmith Configuration (for monitoring)
    langchain_tracing_v2: bool = Field(
        default=True,
        description="Enable LangSmith tracing"
    )
    langchain_project: str = Field(
        default="blog-generation-agent",
        description="LangSmith project name for organizing traces"
    )
    langchain_api_key: Optional[str] = Field(
        default=None,
        description="LangSmith API key (optional but recommended)"
    )
    
    # Application Settings
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR)"
    )
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        # Allow environment variables in any case
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings (cached).
    
    The @lru_cache decorator ensures we only load settings once,
    not every time we call this function. This is important for
    performance since loading from disk is slow.
    
    Returns:
        Settings: Application configuration object
    
    Example:
        >>> settings = get_settings()
        >>> print(settings.azure_openai_deployment)
        'gpt-4.1'
    """
    return Settings()


# Export for easy importing
__all__ = ["Settings", "get_settings"]
