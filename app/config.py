"""
Configuration management using Pydantic Settings.

Loads environment variables and provides type-safe access to configuration values.
"""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    # Render provides DATABASE_URL with proper connection string
    database_url: str = "postgresql://localhost:5432/umatter"
    
    # For Render compatibility: override connection args if needed
    database_pool_size: int = 5
    database_max_overflow: int = 10

    # OAuth Providers
    google_client_id: Optional[str] = None
    google_client_secret: Optional[str] = None
    github_client_id: Optional[str] = None
    github_client_secret: Optional[str] = None
    microsoft_client_id: Optional[str] = None
    microsoft_client_secret: Optional[str] = None

    # Security
    secret_key: str = "change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Ollama Configuration (local dev)
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1:8b"
    ollama_timeout: int = 120  # seconds

    # LLM Provider: "ollama", "groq", "huggingface", "openai", or "anthropic"
    llm_provider: str = "ollama"
    
    # Groq Configuration (FREE & FAST - recommended for production)
    groq_api_key: Optional[str] = None
    groq_model: str = "llama-3.1-70b-versatile"
    
    # Hugging Face Configuration (FREE alternative)
    huggingface_api_key: Optional[str] = None
    huggingface_model: str = "meta-llama/Llama-3.1-70B-Instruct"
    
    # OpenAI Configuration (paid but reliable)
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o-mini"
    
    # Anthropic Configuration (paid alternative)
    anthropic_api_key: Optional[str] = None
    anthropic_model: str = "claude-3-5-sonnet-20241022"

    # Application
    frontend_url: str = "http://localhost:3000"
    environment: str = "development"
    api_prefix: str = "/api/v1"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


# Global settings instance
settings = Settings()
