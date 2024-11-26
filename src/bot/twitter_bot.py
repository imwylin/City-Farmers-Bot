import requests
from src.config.settings import get_settings
from src.utils.redis_handler import RedisHandler
import logging

logger = logging.getLogger(__name__)

class TwitterBot:
    def __init__(self):
        self.settings = get_settings()
        self.redis_handler = RedisHandler()
    
    async def post_tweet(self, content: str):
        """Post a tweet to Twitter"""
        try:
            # Get stored tokens
            tokens = self.redis_handler.get_twitter_tokens("bot_user")
            logger.info("Retrieved Twitter tokens from Redis")
            
            if not tokens:
                logger.error("No Twitter tokens found in Redis")
                raise Exception("No Twitter tokens found")
            
            # Post tweet
            response = requests.post(
                "https://api.x.com/2/tweets",
                json={"text": content},
                headers={
                    "Authorization": f"Bearer {tokens['access_token']}",
                    "Content-Type": "application/json",
                }
            )
            
            if response.status_code != 201:
                logger.error(f"Twitter API error: {response.text}")
                raise Exception(f"Failed to post tweet: {response.text}")
                
            tweet_id = response.json()['data']['id']
            logger.info(f"Tweet posted successfully! ID: {tweet_id}")
            logger.info(f"Tweet content: {content[:50]}...")
            return tweet_id
            
        except Exception as e:
            logger.error(f"Failed to post tweet: {str(e)}")
            raise 