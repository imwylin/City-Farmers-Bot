import requests
from src.config.settings import get_settings
from src.utils.redis_handler import RedisHandler
import logging

logger = logging.getLogger(__name__)

class TwitterBot:
    def __init__(self):
        self.settings = get_settings()
        self.redis_handler = RedisHandler()
    
    async def refresh_token(self, refresh_token: str):
        """Refresh the access token"""
        try:
            data = {
                'refresh_token': refresh_token,
                'grant_type': 'refresh_token',
                'client_id': self.settings.TWITTER_CLIENT_ID
            }
            
            response = requests.post(
                'https://api.x.com/2/oauth2/token',
                data=data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            
            if response.status_code == 200:
                new_tokens = response.json()
                self.redis_handler.store_twitter_tokens("bot_user", new_tokens)
                return new_tokens
            else:
                raise Exception(f"Token refresh failed: {response.text}")
                
        except Exception as e:
            logger.error(f"Failed to refresh token: {str(e)}")
            raise

    async def post_tweet(self, content: str):
        """Post a tweet to Twitter"""
        try:
            # Get stored tokens
            tokens = self.redis_handler.get_twitter_tokens("bot_user")
            logger.info(f"Retrieved tokens from Redis: {tokens is not None}")
            
            if not tokens:
                logger.error("No Twitter tokens found in Redis")
                raise Exception("No Twitter tokens found")
            
            # Try to post tweet
            response = requests.post(
                "https://api.x.com/2/tweets",
                json={"text": content},
                headers={
                    "Authorization": f"Bearer {tokens['access_token']}",
                    "Content-Type": "application/json",
                }
            )
            
            # If token expired, refresh and try again
            if response.status_code == 401 and 'refresh_token' in tokens:
                logger.info("Access token expired, attempting refresh...")
                new_tokens = await self.refresh_token(tokens['refresh_token'])
                
                # Retry with new token
                response = requests.post(
                    "https://api.x.com/2/tweets",
                    json={"text": content},
                    headers={
                        "Authorization": f"Bearer {new_tokens['access_token']}",
                        "Content-Type": "application/json",
                    }
                )
            
            logger.info(f"Twitter API response status: {response.status_code}")
            logger.info(f"Twitter API response: {response.text}")
            
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