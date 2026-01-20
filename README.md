# Autonomous Blog Generation Agent

🤖 An AI-powered blog generation engine using LangGraph and FastAPI.

## Features

- **Multi-Agent Workflow**: Title brainstorming, content generation, optional translation
- **DAG Architecture**: Directed Acyclic Graph for complex agent orchestration
- **REST API**: FastAPI backend for easy integration
- **Monitoring**: LangSmith integration for tracing and debugging

## Quick Start

```bash
# 1. Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# 2. Run the server
uv run uvicorn src.blog_agent.api.main:app --reload

# 3. Open API docs
# Visit http://localhost:8000/docs
```

## Documentation

See [BUILD_JOURNAL.md](BUILD_JOURNAL.md) for a detailed guide on how this project was built.

## Project Structure

```
src/blog_agent/
├── agents/         # Individual AI agents
├── graph/          # LangGraph workflow definition
├── models/         # Pydantic data models
├── api/            # FastAPI endpoints
├── prompts/        # AI prompt templates
└── utils/          # Utility functions
```

## License

MIT
