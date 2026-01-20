"""
FastAPI Application
===================

This is the entry point for our web server.

WHAT THIS FILE DOES:
-------------------
1. Creates the FastAPI application instance
2. Configures middleware (CORS, etc.)
3. Includes all route modules
4. Sets up logging and error handling

HOW TO RUN:
----------
    uv run uvicorn src.blog_agent.api.main:app --reload

This command:
- Uses 'uv run' to run in our virtual environment
- Starts 'uvicorn' (the web server)
- Points to 'src.blog_agent.api.main:app' (this file, the 'app' variable)
- '--reload' enables auto-restart on code changes (development only!)

WHAT HAPPENS ON STARTUP:
-----------------------
1. FastAPI app is created
2. CORS middleware is added (allows cross-origin requests)
3. Routes are registered
4. Server starts listening on port 8000

You can then visit:
- http://localhost:8000/docs - Swagger UI (interactive API docs)
- http://localhost:8000/redoc - ReDoc (alternative docs)
- http://localhost:8000/api/v1/health - Health check
- http://localhost:8000/api/v1/generate - Main endpoint (POST)
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from blog_agent.api.routes import router
from blog_agent import __version__


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    
    This handles startup and shutdown events:
    - Code before 'yield' runs on startup
    - Code after 'yield' runs on shutdown
    
    We use this for:
    - Loading models/resources on startup
    - Cleaning up connections on shutdown
    - Logging startup/shutdown events
    """
    # ═══════════════════════════════════════════════════════════════════
    # STARTUP
    # ═══════════════════════════════════════════════════════════════════
    print("=" * 50)
    print(f"🚀 Blog Generation Agent v{__version__}")
    print("=" * 50)
    print("📝 API Documentation: http://localhost:8000/docs")
    print("❤️  Health Check: http://localhost:8000/api/v1/health")
    print("=" * 50)
    
    # Yield control back to FastAPI (app runs here)
    yield
    
    # ═══════════════════════════════════════════════════════════════════
    # SHUTDOWN
    # ═══════════════════════════════════════════════════════════════════
    print("👋 Shutting down Blog Generation Agent...")


# ═══════════════════════════════════════════════════════════════════════════
# CREATE THE APPLICATION
# ═══════════════════════════════════════════════════════════════════════════

app = FastAPI(
    title="Blog Generation Agent",
    description="""
    🤖 **Autonomous Blog Generation Engine**
    
    Generate high-quality blog posts using AI agents:
    - **Title Agent**: Creates SEO-friendly titles
    - **Content Agent**: Writes engaging blog content
    - **Translation Agent**: Translates to other languages
    
    Built with LangGraph and FastAPI.
    """,
    version=__version__,
    lifespan=lifespan,
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc
)


# ═══════════════════════════════════════════════════════════════════════════
# MIDDLEWARE
# ═══════════════════════════════════════════════════════════════════════════

# CORS (Cross-Origin Resource Sharing)
# This allows web browsers to call our API from different domains
# For development, we allow everything. In production, restrict this!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: ["https://yourdomain.com"]
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# ═══════════════════════════════════════════════════════════════════════════
# INCLUDE ROUTERS
# ═══════════════════════════════════════════════════════════════════════════

# This adds all routes from our routes.py file
app.include_router(router)


# ═══════════════════════════════════════════════════════════════════════════
# ROOT ENDPOINT
# ═══════════════════════════════════════════════════════════════════════════

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - redirects to documentation.
    
    When someone visits http://localhost:8000/, they see this message
    with a link to the actual API docs.
    """
    return {
        "message": "Welcome to the Blog Generation Agent API",
        "docs": "/docs",
        "health": "/api/v1/health"
    }


# Export for importing (used by uvicorn)
__all__ = ["app"]
