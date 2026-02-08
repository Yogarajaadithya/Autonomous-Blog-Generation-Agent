# 🤖 Autonomous Blog Generation Agent

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Powered-green.svg)](https://github.com/langchain-ai/langgraph)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.128+-009688.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **An intelligent multi-agent system that transforms topics into publish-ready blog posts using LangGraph orchestration**

Transform any topic into a polished, SEO-optimized blog post with optional translation—all powered by a team of AI agents working in harmony.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🎯 **Multi-Agent Architecture** | Three specialized AI agents (Title, Content, Translation) collaborate via LangGraph DAG workflow |
| 📝 **Smart Title Generation** | Brainstorms 5 creative, SEO-friendly titles and selects the optimal one |
| ✍️ **Professional Content** | Generates 800-1200 word blog posts in clean Markdown format |
| 🌍 **Multi-Language Support** | Optional translation to Spanish, French, German, Chinese, and more |
| 🎨 **Customizable Styles** | Professional, casual, technical, or humorous writing tones |
| 🔍 **LangSmith Integration** | Full observability with tracing, debugging, and cost tracking |
| ⚡ **REST API** | FastAPI backend with automatic Swagger documentation |
| 🖥️ **Streamlit UI** | User-friendly web interface for non-technical users |

---

## 📸 Screenshots

### User Interface
*Clean, intuitive Streamlit interface for generating blog posts*

![Streamlit UI](images/image1.png)

### Multi-Language Support
*Choose from multiple target languages for translation*

![Language Options](images/image2.png)

### Generated Results (English)
*Example output: Professional blog post in English*

![English Results](images/image3.png)

### Generated Results (German)
*Same blog post translated to German*

![German Results](images/Image4.png)

---

## 🏗️ Architecture

```
                           ┌─────────────────────────────────────────┐
                           │         Streamlit Frontend              │
                           │      http://localhost:8501              │
                           └─────────────────┬───────────────────────┘
                                             │
                                             ▼
                           ┌─────────────────────────────────────────┐
                           │          FastAPI Backend                │
                           │      http://localhost:8000              │
                           └─────────────────┬───────────────────────┘
                                             │
                                             ▼
┌────────────────────────────────────────────────────────────────────────────────┐
│                           LangGraph Workflow (DAG)                             │
│                                                                                │
│   ┌──────────────┐      ┌──────────────┐      ┌─────────────────────┐         │
│   │ Title Agent  │──────│Content Agent │──────│  Should Translate?  │         │
│   │              │      │              │      │     (Router)        │         │
│   │ • 5 titles   │      │ • 800-1200   │      └──────────┬──────────┘         │
│   │ • Pick best  │      │   words      │                 │                    │
│   │ • Temp: 0.8  │      │ • Markdown   │       ┌─────────┴─────────┐          │
│   └──────────────┘      │ • Temp: 0.7  │       │                   │          │
│                         └──────────────┘       ▼                   ▼          │
│                                        ┌──────────────┐      ┌─────────┐      │
│                                        │ Translation  │      │   END   │      │
│                                        │    Agent     │──────│         │      │
│                                        │ • Temp: 0.3  │      └─────────┘      │
│                                        └──────────────┘                       │
└────────────────────────────────────────────────────────────────────────────────┘
                                             │
                                             ▼
                           ┌─────────────────────────────────────────┐
                           │           OpenAI GPT API                │
                           └─────────────────────────────────────────┘
```

### How It Works

1. **User submits a topic** (e.g., "Benefits of Remote Work")
2. **Title Agent** generates 5 creative titles using GPT with high temperature (0.8) for creativity, then selects the best one based on SEO principles
3. **Content Agent** writes a complete blog post (800-1200 words) using the selected title
4. **Router** checks if translation was requested
5. **Translation Agent** (optional) translates the content while preserving formatting
6. **Final output** is returned with metadata (word count, generation time, etc.)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- [UV Package Manager](https://github.com/astral-sh/uv) (recommended) or pip
- OpenAI API Key

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/Autonomous-Blog-Generation-Agent.git
cd Autonomous-Blog-Generation-Agent

# Install dependencies with UV (recommended)
uv sync

# Or with pip
pip install -e .
```

### Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API keys
# Required:
OPENAI_API_KEY=your-openai-key-here

# Optional (for LangSmith monitoring):
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=blog-generation-agent
LANGCHAIN_API_KEY=your-langsmith-key-here
```

### Running the Application

```bash
# Terminal 1: Start the FastAPI backend
uv run uvicorn blog_agent.api.main:app --reload --port 8000

# Terminal 2: Start the Streamlit frontend
uv run streamlit run src/ui/streamlit_app.py --server.port 8501
```

**Access the application:**
- 🖥️ **Frontend UI:** http://localhost:8501
- 📚 **API Documentation:** http://localhost:8000/docs
- ❤️ **Health Check:** http://localhost:8000/api/v1/health

---

## 📡 API Reference

### Generate Blog Post

```bash
POST /api/v1/generate
```

**Request:**
```json
{
    "topic": "Benefits of Remote Work",
    "transcript": "Optional source material or transcript...",
    "target_language": "Spanish",
    "style": "professional"
}
```

**Response:**
```json
{
    "title": "10 Transformative Benefits of Remote Work in 2026",
    "content": "## Introduction\n\nRemote work has revolutionized...",
    "word_count": 1024,
    "generation_time_seconds": 12.5,
    "was_translated": true,
    "target_language": "Spanish",
    "brainstormed_titles": [
        "10 Transformative Benefits of Remote Work in 2026",
        "Why Remote Work is the Future of Employment",
        "The Ultimate Guide to Remote Work Benefits",
        "How Remote Work is Changing Lives Worldwide",
        "Remote Work Revolution: Benefits You Can't Ignore"
    ]
}
```

### Health Check

```bash
GET /api/v1/health
```

---

## 📁 Project Structure

```
📦 Autonomous-Blog-Generation-Agent
├── 📂 src/
│   ├── 📂 blog_agent/
│   │   ├── 📂 agents/           # AI Agent implementations
│   │   │   ├── title_agent.py      # Brainstorms & selects titles
│   │   │   ├── content_agent.py    # Writes blog content
│   │   │   └── translation_agent.py # Translates content
│   │   │
│   │   ├── 📂 graph/            # LangGraph workflow
│   │   │   ├── workflow.py         # DAG definition
│   │   │   └── router.py           # Conditional routing logic
│   │   │
│   │   ├── 📂 models/           # Data schemas
│   │   │   ├── state.py            # BlogState (shared memory)
│   │   │   └── api_models.py       # Request/Response models
│   │   │
│   │   ├── 📂 api/              # FastAPI backend
│   │   │   ├── main.py             # App initialization
│   │   │   ├── routes.py           # API endpoints
│   │   │   └── dependencies.py     # Dependency injection
│   │   │
│   │   ├── 📂 prompts/          # LLM prompt templates
│   │   │   ├── title_prompts.py
│   │   │   ├── content_prompts.py
│   │   │   └── translation_prompts.py
│   │   │
│   │   └── 📂 utils/            # Utilities
│   │       ├── config.py           # Settings management
│   │       └── llm.py              # LLM client factory
│   │
│   └── 📂 ui/
│       └── streamlit_app.py     # Streamlit frontend
│
├── 📂 tests/                    # Test suite
│   ├── test_agents.py
│   ├── test_workflow.py
│   └── test_api.py
│
├── 📄 pyproject.toml            # Project configuration
├── 📄 BUILD_JOURNAL.md          # Detailed build documentation
└── 📄 README.md                 # This file
```

---

## 🧪 Testing

```bash
# Run all tests
uv run pytest tests/ -v

# Run specific test file
uv run pytest tests/test_agents.py -v

# Run with coverage
uv run pytest tests/ --cov=blog_agent --cov-report=html
```

---

## 🛠️ Technology Stack

| Category | Technology | Purpose |
|----------|------------|---------|
| **Workflow** | [LangGraph](https://github.com/langchain-ai/langgraph) | Multi-agent DAG orchestration |
| **LLM Framework** | [LangChain](https://www.langchain.com/) | LLM utilities & prompt management |
| **AI Model** | [OpenAI GPT](https://openai.com/) | Text generation |
| **Backend** | [FastAPI](https://fastapi.tiangolo.com/) | REST API with async support |
| **Frontend** | [Streamlit](https://streamlit.io/) | Interactive web UI |
| **Validation** | [Pydantic](https://docs.pydantic.dev/) | Data validation & serialization |
| **Monitoring** | [LangSmith](https://smith.langchain.com/) | Tracing, debugging, analytics |
| **Package Manager** | [UV](https://github.com/astral-sh/uv) | Fast Python package management |

---

## 🔍 Monitoring with LangSmith

Enable LangSmith to visualize your agent workflow, debug issues, and track costs:

1. Create an account at [smith.langchain.com](https://smith.langchain.com/)
2. Get your API key
3. Add to `.env`:
   ```
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_PROJECT=blog-generation-agent
   LANGCHAIN_API_KEY=your-key-here
   ```

You'll see:
- Real-time traces of each agent execution
- Token usage and cost breakdown
- Error debugging with full context
- Workflow visualization

---

## 📖 Documentation

For a detailed walkthrough of how this project was built, see:

- 📘 **[BUILD_JOURNAL.md](BUILD_JOURNAL.md)** - Step-by-step guide explaining every component, decision, and concept (beginner-friendly)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [LangChain](https://www.langchain.com/) for the amazing LLM framework
- [LangGraph](https://github.com/langchain-ai/langgraph) for multi-agent orchestration
- [FastAPI](https://fastapi.tiangolo.com/) for the blazing-fast API framework
- [OpenAI](https://openai.com/) for GPT models

---

<p align="center">
  Made with ❤️ using LangGraph + FastAPI + Streamlit
</p>
