"""
Workflow Integration Tests
==========================

Test the complete LangGraph workflow end-to-end.

WHY INTEGRATION TESTS?
---------------------
While unit tests verify individual agents, integration tests verify:
- Agents work together correctly
- State flows properly between agents
- Routing logic works as expected
- The compiled graph executes correctly
"""

import pytest
from unittest.mock import patch, MagicMock, Mock
from blog_agent.graph.router import should_translate
from blog_agent.models.state import BlogState, DEFAULT_STATE


class TestRouter:
    """Tests for the workflow router."""
    
    def test_should_translate_returns_translate_when_language_set(self):
        """Test router returns 'translate' when target_language is set."""
        state: BlogState = {
            **DEFAULT_STATE,
            "target_language": "Spanish"
        }
        
        result = should_translate(state)
        
        assert result == "translate"
    
    def test_should_translate_returns_end_when_no_language(self):
        """Test router returns 'end' when no target_language."""
        state: BlogState = {
            **DEFAULT_STATE,
            "target_language": None
        }
        
        result = should_translate(state)
        
        assert result == "end"
    
    def test_should_translate_returns_end_when_empty_language(self):
        """Test router returns 'end' when target_language is empty string."""
        state: BlogState = {
            **DEFAULT_STATE,
            "target_language": "   "  # Whitespace only
        }
        
        result = should_translate(state)
        
        assert result == "end"


class TestWorkflowCreation:
    """Tests for workflow creation and compilation."""
    
    def test_workflow_compiles_successfully(self):
        """Test that the workflow compiles without errors."""
        from blog_agent.graph.workflow import create_workflow
        
        workflow = create_workflow()
        
        assert workflow is not None
    
    @patch("blog_agent.graph.workflow.title_agent")
    @patch("blog_agent.graph.workflow.content_agent")
    def test_workflow_runs_without_translation(
        self, mock_content, mock_title
    ):
        """Test workflow runs correctly without translation."""
        # Setup mocks
        mock_title.return_value = {
            "brainstormed_titles": ["Title 1"],
            "selected_title": "Title 1"
        }
        mock_content.return_value = {
            "blog_content": "Content here",
            "word_count": 2,
            "final_content": "Content here"
        }
        
        from blog_agent.graph.workflow import create_workflow
        
        workflow = create_workflow()
        
        result = workflow.invoke({
            **DEFAULT_STATE,
            "topic": "Test Topic",
            "target_language": None
        })
        
        assert "final_content" in result
        # Translation agent should not have been called
        assert result.get("translated_content") is None
