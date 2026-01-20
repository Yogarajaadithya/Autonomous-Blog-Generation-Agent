"""
Unit Tests for Agents
=====================

Test each agent in isolation to ensure they work correctly.

WHY UNIT TESTS?
--------------
Unit tests verify that individual pieces work correctly BEFORE
we test the whole system. This helps us:
- Find bugs quickly (easier to debug one agent than the whole workflow)
- Develop faster (test as you code)
- Refactor safely (tests catch regressions)

MOCKING IN TESTS:
----------------
For unit tests, we don't want to call the real OpenAI API because:
- It costs money
- It's slow
- Results vary (hard to assert expected output)

Instead, we "mock" the LLM to return predictable responses.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from blog_agent.models.state import BlogState, DEFAULT_STATE


class TestTitleAgent:
    """Tests for the Title Brainstorming Agent."""
    
    @patch("blog_agent.agents.title_agent.get_llm")
    def test_title_agent_generates_titles(self, mock_get_llm):
        """Test that title agent generates and selects titles."""
        # Arrange: Set up mock LLM responses
        mock_llm = MagicMock()
        
        # First call: generate titles
        mock_llm.invoke.side_effect = [
            Mock(content="""1. How to Master Remote Work in 30 Days
2. 7 Secrets Top Remote Workers Never Share
3. Why Are Remote Workers 40% More Productive?
4. The Ultimate Guide to Work-From-Home Success
5. Remote Work Revolution: Transform Your Career Today"""),
            # Second call: select best title
            Mock(content="The Ultimate Guide to Work-From-Home Success")
        ]
        mock_get_llm.return_value = mock_llm
        
        # Act: Call the agent
        from blog_agent.agents.title_agent import title_agent
        
        state: BlogState = {
            **DEFAULT_STATE,
            "topic": "Remote Work Benefits",
            "style": "professional"
        }
        
        result = title_agent(state)
        
        # Assert: Check the results
        assert "brainstormed_titles" in result
        assert len(result["brainstormed_titles"]) >= 1
        assert "selected_title" in result
        assert result["selected_title"] != ""


class TestContentAgent:
    """Tests for the Content Generation Agent."""
    
    @patch("blog_agent.agents.content_agent.get_llm")
    def test_content_agent_generates_content(self, mock_get_llm):
        """Test that content agent generates blog content."""
        # Arrange
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = Mock(
            content="""## Introduction

Remote work has transformed the modern workplace. Here's why it matters.

## Benefits of Remote Work

Working from home offers numerous advantages including flexibility and productivity.

## Conclusion

Embrace remote work for a better work-life balance."""
        )
        mock_get_llm.return_value = mock_llm
        
        # Act
        from blog_agent.agents.content_agent import content_agent
        
        state: BlogState = {
            **DEFAULT_STATE,
            "topic": "Remote Work Benefits",
            "selected_title": "The Ultimate Guide to Remote Work",
            "style": "professional"
        }
        
        result = content_agent(state)
        
        # Assert
        assert "blog_content" in result
        assert result["blog_content"] != ""
        assert "word_count" in result
        assert result["word_count"] > 0


class TestTranslationAgent:
    """Tests for the Translation Agent."""
    
    @patch("blog_agent.agents.translation_agent.get_llm")
    def test_translation_agent_translates_content(self, mock_get_llm):
        """Test that translation agent translates content."""
        # Arrange
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = Mock(
            content="## Introducción\n\nEl trabajo remoto ha transformado el lugar de trabajo moderno."
        )
        mock_get_llm.return_value = mock_llm
        
        # Act
        from blog_agent.agents.translation_agent import translation_agent
        
        state: BlogState = {
            **DEFAULT_STATE,
            "blog_content": "## Introduction\n\nRemote work has transformed the modern workplace.",
            "target_language": "Spanish"
        }
        
        result = translation_agent(state)
        
        # Assert
        assert "translated_content" in result
        assert result["translated_content"] is not None
        assert "final_content" in result
    
    def test_translation_agent_skips_without_language(self):
        """Test that translation agent skips when no language specified."""
        from blog_agent.agents.translation_agent import translation_agent
        
        state: BlogState = {
            **DEFAULT_STATE,
            "blog_content": "Some content",
            "target_language": None
        }
        
        result = translation_agent(state)
        
        assert result["translated_content"] is None
        assert result["final_content"] == "Some content"
