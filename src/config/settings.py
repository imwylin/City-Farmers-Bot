from pydantic_settings import BaseSettings
from functools import lru_cache
from pydantic import Field

class Settings(BaseSettings):
    # Twitter API Credentials
    CLIENT_ID: str
    CLIENT_SECRET: str
    REDIRECT_URI: str
    
    # Anthropic API
    ANTHROPIC_API_KEY: str
    
    # Redis Configuration
    REDIS_URL: str
    
    # Application Settings
    LOG_LEVEL: str = "INFO"
    ENVIRONMENT: str = "development"
    
    # Add proxy settings with None defaults
    HTTP_PROXY: str | None = None
    HTTPS_PROXY: str | None = None
    NO_PROXY: str | None = None
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings() 