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
            return json.loads(tokens) if tokens else None
        except Exception as e:
            logger.error(f"Failed to retrieve Twitter tokens: {str(e)}")
            raise
    
    def verify_connection(self):
        """Verify Redis connection and token existence"""
        try:
            # Test connection
            self.redis_client.ping()
            
            # Check for tokens
            tokens = self.get_twitter_tokens("bot_user")
            if not tokens:
                logger.error("No Twitter tokens found in Redis")
                return False
                
            logger.info("Redis connection verified and tokens found")
            return True
        except Exception as e:
            logger.error(f"Redis verification failed: {str(e)}")
            return False