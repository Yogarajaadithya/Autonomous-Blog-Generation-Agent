"""
API Endpoint Tests
==================

Test the FastAPI endpoints using the test client.

WHAT IS A TEST CLIENT?
---------------------
FastAPI provides a TestClient that lets you make HTTP requests
to your app WITHOUT actually starting a server. This means:
- Tests run fast
- No port conflicts
- Can test the full request/response cycle

HOW THESE TESTS WORK:
--------------------
1. Create a TestClient with our FastAPI app
2. Make requests (GET, POST, etc.)
3. Check the response status code and body
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, Mock

from blog_agent.api.main import app


client = TestClient(app)


class TestHealthEndpoint:
    """Tests for the health check endpoint."""
    
    def test_health_returns_200(self):
        """Test that health endpoint returns 200 OK."""
        response = client.get("/api/v1/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
    
    def test_health_includes_version(self):
        """Test that health response includes version."""
        response = client.get("/api/v1/health")
        data = response.json()
        
        assert data["version"] == "0.1.0"


class TestRootEndpoint:
    """Tests for the root endpoint."""
    
    def test_root_returns_welcome_message(self):
        """Test that root endpoint returns welcome message."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "docs" in data


class TestGenerateEndpoint:
    """Tests for the blog generation endpoint."""
    
    def test_generate_requires_topic(self):
        """Test that generate endpoint requires a topic."""
        response = client.post("/api/v1/generate", json={})
        
        # Should return 422 (validation error) without topic
        assert response.status_code == 422
    
    def test_generate_validates_topic_length(self):
        """Test that topic must be at least 3 characters."""
        response = client.post("/api/v1/generate", json={
            "topic": "Hi"  # Too short
        })
        
        assert response.status_code == 422
    
    def test_generate_success(self):
        """Test successful blog generation."""
        from blog_agent.api.dependencies import get_workflow
        
        # Arrange: Create a mock workflow
        mock_workflow = MagicMock()
        mock_workflow.invoke.return_value = {
            "topic": "Test Topic",
            "transcript": None,
            "target_language": None,
            "style": "professional",
            "brainstormed_titles": ["Title 1", "Title 2"],
            "selected_title": "Title 1",
            "blog_content": "# Test Blog\n\nThis is test content.",
            "translated_content": None,
            "final_content": "# Test Blog\n\nThis is test content.",
            "word_count": 5,
            "generation_time": 1.5
        }
        
        # Override the dependency
        app.dependency_overrides[get_workflow] = lambda: mock_workflow
        
        try:
            # Act
            response = client.post("/api/v1/generate", json={
                "topic": "Test Topic"
            })
            
            # Assert
            assert response.status_code == 200
            data = response.json()
            assert data["title"] == "Title 1"
            assert "content" in data
            assert data["word_count"] == 5
        finally:
            # Clean up: Remove the override
            app.dependency_overrides.clear()
