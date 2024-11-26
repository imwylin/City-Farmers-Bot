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