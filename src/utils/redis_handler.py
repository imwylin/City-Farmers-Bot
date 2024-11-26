import redis
from src.config.settings import get_settings
import json
import logging

logger = logging.getLogger(__name__)

class RedisHandler:
    def __init__(self):
        self.settings = get_settings()
        self.redis_client = redis.from_url(self.settings.REDIS_URL)
    
    def store_twitter_tokens(self, user_id: str, tokens: dict):
        """Store Twitter OAuth tokens in Redis"""
        try:
            self.redis_client.setex(
                f"twitter_tokens:{user_id}",
                24 * 60 * 60,  # 24 hour expiration
                json.dumps(tokens)
            )
        except Exception as e:
            logger.error(f"Failed to store Twitter tokens: {str(e)}")
            raise
    
    def get_twitter_tokens(self, user_id: str) -> dict:
        """Retrieve Twitter OAuth tokens from Redis"""
        try:
            tokens = self.redis_client.get(f"twitter_tokens:{user_id}")
            if tokens:
                # Parse the JSON string into a dictionary
                if isinstance(tokens, str):
                    return json.loads(tokens)
                return json.loads(tokens.decode('utf-8'))
            return None
        except Exception as e:
            logger.error(f"Failed to retrieve Twitter tokens: {str(e)}")
            raise
    
    def verify_connection(self):
        """Verify Redis connection"""
        try:
            self.redis_client.ping()
            logger.info("Redis connection verified")
            return True
        except Exception as e:
            logger.error(f"Redis verification failed: {str(e)}")
            return False
    
    def has_tokens(self):
        """Check if tokens exist"""
        try:
            tokens = self.get_twitter_tokens("bot_user")
            return bool(tokens)
        except Exception:
            return False
    
    def store_pkce_credentials(self, credentials: dict):
        """Store PKCE credentials in Redis"""
        try:
            self.redis_client.set("pkce_credentials", json.dumps(credentials))
        except Exception as e:
            logger.error(f"Failed to store PKCE credentials: {str(e)}")
            raise
    
    def get_pkce_credentials(self) -> dict:
        """Retrieve PKCE credentials from Redis"""
        try:
            credentials = self.redis_client.get("pkce_credentials")
            return json.loads(credentials) if credentials else None
        except Exception as e:
            logger.error(f"Failed to retrieve PKCE credentials: {str(e)}")
            raise
    
    def clear_all_tokens(self):
        """Clear all stored tokens and credentials"""
        try:
            self.redis_client.delete("pkce_credentials")
            self.redis_client.delete("twitter_tokens:bot_user")
            logger.info("Cleared all tokens from Redis")
        except Exception as e:
            logger.error(f"Failed to clear tokens: {str(e)}")
            raise