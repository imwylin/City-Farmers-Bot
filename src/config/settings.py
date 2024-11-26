from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Twitter API Credentials
    TWITTER_CLIENT_ID: str
    TWITTER_CLIENT_SECRET: str
    TWITTER_REDIRECT_URI: str = "https://city-farmers-bot.onrender.com/callback"
    
    # Anthropic API
    ANTHROPIC_API_KEY: str
    
    # Redis Configuration
    REDIS_URL: str
    
    # Application Settings
    LOG_LEVEL: str = "INFO"
    ENVIRONMENT: str = "development"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings() 