"""Test fixtures and configurations."""

import pytest


@pytest.fixture
def sample_topic():
    """Sample topic for testing."""
    return "Benefits of Remote Work in 2024"


@pytest.fixture
def sample_transcript():
    """Sample transcript for testing."""
    return """
    Today we're going to talk about the incredible benefits of working from home.
    First, there's the obvious time savings from not commuting. That's hours of your 
    life back every single day. Second, you have more control over your environment.
    You can set up your workspace exactly how you like it. Third, many people find
    they're actually more productive at home because there are fewer interruptions.
    """
