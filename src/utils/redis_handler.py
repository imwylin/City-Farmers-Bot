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
                if isinstance(tokens, bytes):
                    tokens = tokens.decode('utf-8')
                try:
                    return json.loads(tokens)
                except json.JSONDecodeError as e:
                    logger.error(f"JSON decode error: {e}")
                    raise
            return None
        except Exception as e:
            logger.error(f"Failed to retrieve Twitter tokens: {str(e)}")
            raise
    
    def verify_connection(self):
        """Verify Redis connection is working"""
        try:
            self.redis_client.ping()
            return True
        except Exception as e:
            logger.error(f"Redis connection failed: {str(e)}")
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
    
    def store_rate_limit_state(self, resume_time: str):
        """Store rate limit state and resume time"""
        try:
            self.redis_client.setex(
                "rate_limit_state",
                24 * 60 * 60,  # 24 hour expiration
                resume_time
            )
            logger.info(f"Stored rate limit resume time: {resume_time}")
        except Exception as e:
            logger.error(f"Failed to store rate limit state: {str(e)}")
            raise

    def get_rate_limit_state(self) -> str:
        """Get stored rate limit resume time"""
        try:
            resume_time = self.redis_client.get("rate_limit_state")
            if resume_time:
                return resume_time.decode('utf-8')
            return None
        except Exception as e:
            logger.error(f"Failed to get rate limit state: {str(e)}")
            return None

    def clear_rate_limit_state(self):
        """Clear stored rate limit state"""
        try:
            self.redis_client.delete("rate_limit_state")
            logger.info("Cleared rate limit state")
        except Exception as e:
            logger.error(f"Failed to clear rate limit state: {str(e)}")
            raise