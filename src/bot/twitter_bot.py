import requests
from src.config.settings import get_settings
from src.utils.redis_handler import RedisHandler
import logging
import json

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
            tokens = self.redis_handler.get_twitter_tokens("bot_user")
            logger.info(f"Tokens received in TwitterBot: {tokens}")
            logger.info(f"Token type in TwitterBot: {type(tokens)}")
            
            if not tokens:
                logger.error("No Twitter tokens found in Redis")
                raise Exception("No Twitter tokens found")
            
            # Log token details (safely)
            logger.info("Token validation:")
            logger.info(f"Token type: {type(tokens)}")
            logger.info(f"Available keys: {list(tokens.keys())}")
            
            # Construct and log full request details
            url = "https://api.x.com/2/tweets"
            payload = {"text": content}
            headers = {
                "Authorization": f"Bearer {tokens['access_token']}",
                "Content-Type": "application/json",
            }
            
            logger.info(f"Making request to: {url}")
            logger.info(f"With payload: {payload}")
            logger.info(f"Headers (sanitized): {{'Authorization': 'Bearer ...', 'Content-Type': {headers['Content-Type']}}}")
            
            response = requests.post(url, json=payload, headers=headers)
            
            logger.info("Response details:")
            logger.info(f"Status code: {response.status_code}")
            logger.info(f"Response headers: {dict(response.headers)}")
            logger.info(f"Response body: {response.text}")
            logger.info(f"Response content type: {response.headers.get('content-type')}")
            
            if response.status_code != 201:
                logger.error(f"Twitter API error: {response.text}")
                if response.status_code == 401:
                    logger.info("Attempting token refresh...")
                    if 'refresh_token' in tokens:
                        new_tokens = await self.refresh_token(tokens['refresh_token'])
                        return await self.post_tweet(content)
                raise Exception(f"Failed to post tweet: {response.text}")
                
            tweet_id = response.json()['data']['id']
            logger.info(f"Tweet posted successfully! ID: {tweet_id}")
            logger.info(f"Tweet URL: https://twitter.com/i/web/status/{tweet_id}")
            return tweet_id
            
        except Exception as e:
            logger.error(f"Failed to post tweet: {str(e)}")
            logger.exception("Full traceback:")  # Log full traceback
            raise 