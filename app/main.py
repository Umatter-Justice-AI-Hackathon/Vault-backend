"""
Main FastAPI application entry point.

Sets up the FastAPI app with middleware, routes, and startup/shutdown events.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base

# Initialize FastAPI app
app = FastAPI(
    title="Umatter API",
    description="Trauma-aware wellbeing chatbot API",
    version="0.1.0",
    docs_url=f"{settings.api_prefix}/docs",
    redoc_url=f"{settings.api_prefix}/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app": "Umatter API",
        "version": "0.1.0",
        "environment": settings.environment,
    }


@app.get("/health")
async def health_check():
    """Detailed health check with service status."""
    # TODO: Add checks for database and Ollama connectivity
    return {
        "status": "healthy",
        "services": {
            "database": "connected",  # Will implement actual check
            "ollama": "connected",  # Will implement actual check
        },
    }


# Import and include routers
# TODO: Add routers as they are created
# from app.api import auth, chat, sessions, analytics
# app.include_router(auth.router, prefix=f"{settings.api_prefix}/auth", tags=["auth"])
# app.include_router(chat.router, prefix=f"{settings.api_prefix}/chat", tags=["chat"])
# app.include_router(sessions.router, prefix=f"{settings.api_prefix}/sessions", tags=["sessions"])
# app.include_router(analytics.router, prefix=f"{settings.api_prefix}/analytics", tags=["analytics"])
