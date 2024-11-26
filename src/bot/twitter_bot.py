import tweepy
from src.config.settings import get_settings
from src.utils.redis_handler import RedisHandler
import logging

logger = logging.getLogger(__name__)

class TwitterBot:
    def __init__(self):
        self.settings = get_settings()
        self.redis_handler = RedisHandler()
        self.client = tweepy.Client(
            consumer_key=self.settings.TWITTER_CLIENT_ID,
            consumer_secret=self.settings.TWITTER_CLIENT_SECRET,
        )
    
    async def post_tweet(self, content: str):
        """Post a tweet to Twitter"""
        try:
            # Get stored tokens
            tokens = self.redis_handler.get_twitter_tokens("bot_user")
            if not tokens:
                raise Exception("No Twitter tokens found")
            
            # Update client with access token
            self.client.access_token = tokens["access_token"]
            
            # Post tweet
            response = await self.client.create_tweet(text=content)
            logger.info(f"Tweet posted successfully: {response.data['id']}")
            return response.data['id']
            
        except Exception as e:
            logger.error(f"Failed to post tweet: {str(e)}")
            raise 