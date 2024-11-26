from fastapi import FastAPI, BackgroundTasks, HTTPException, Request, Query
from fastapi.responses import RedirectResponse
from src.bot.twitter_bot import TwitterBot
from src.bot.content_generator import ContentGenerator
from src.utils.scheduler import TweetScheduler
from src.utils.redis_handler import RedisHandler
import logging
from src.config.settings import get_settings
import base64
import hashlib
import re
import os
from requests_oauthlib import OAuth2Session
import json
import datetime
import random

app = FastAPI()
settings = get_settings()

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize scheduler at module level
scheduler = TweetScheduler()

@app.on_event("startup")
async def start_scheduler():
    """Start the scheduler when the app starts"""
    try:
        scheduler.start()
        logger.info("Scheduler started successfully on app startup")
    except Exception as e:
        logger.error(f"Failed to start scheduler: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown_scheduler():
    """Shutdown the scheduler gracefully"""
    try:
        scheduler.scheduler.shutdown()
        logger.info("Scheduler shut down successfully")
    except Exception as e:
        logger.error(f"Error shutting down scheduler: {str(e)}")

# Add a root endpoint to prevent 404s
@app.get("/")
async def root():
    return {"status": "running", "message": "City Farmers Bot API"}

@app.post("/post-tweet")
async def create_tweet(background_tasks: BackgroundTasks, content_type: str = "educational"):
    """Endpoint to generate and post a tweet"""
    try:
        logger.info(f"Received request to create {content_type} tweet")
        content_generator = ContentGenerator()
        twitter_bot = TwitterBot()
        
        # Generate content
        logger.info("Attempting to generate content...")
        content = await content_generator.generate_tweet(content_type)
        
        # Post tweet in background
        logger.info("Adding tweet to background tasks...")
        background_tasks.add_task(twitter_bot.post_tweet, content)
        
        return {"status": "Tweet generation initiated", "content": content}
    except Exception as e:
        logger.error(f"Failed to create tweet: {str(e)}")
        logger.exception("Full traceback:")  # This will log the full stack trace
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Check system health"""
    try:
        # Test Redis
        redis_handler = RedisHandler()
        redis_connected = redis_handler.verify_connection()
        has_tokens = redis_handler.has_tokens() if redis_connected else False
        
        return {
            "status": "healthy" if redis_connected and has_tokens else "unhealthy",
            "redis_connected": redis_connected,
            "has_tokens": has_tokens
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {"status": "unhealthy", "error": str(e)}

# OAuth 2.0 Configuration
auth_url = "https://twitter.com/i/oauth2/authorize"
token_url = "https://api.x.com/2/oauth2/token"
scopes = ["tweet.read", "users.read", "tweet.write", "offline.access"]

# Replace the runtime PKCE setup with a Redis-based one
async def get_pkce_credentials():
    redis_handler = RedisHandler()
    credentials = redis_handler.get_pkce_credentials()
    
    if not credentials:
        # Generate new credentials if none exist
        code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
        code_verifier = re.sub("[^a-zA-Z0-9]+", "", code_verifier)
        code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
        code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
        code_challenge = code_challenge.replace("=", "")
        
        credentials = {
            "code_verifier": code_verifier,
            "code_challenge": code_challenge
        }
        redis_handler.store_pkce_credentials(credentials)
    
    return credentials

@app.get("/auth/twitter")
async def twitter_auth():
    """Start OAuth flow"""
    credentials = await get_pkce_credentials()
    oauth = OAuth2Session(
        settings.CLIENT_ID,
        redirect_uri=settings.REDIRECT_URI,
        scope=scopes
    )
    authorization_url, state = oauth.authorization_url(
        auth_url,
        code_challenge=credentials["code_challenge"],
        code_challenge_method="S256"
    )
    return RedirectResponse(authorization_url)

@app.get("/oauth/callback")
async def twitter_callback(
    code: str = Query(..., description="Authorization code from Twitter"),
    state: str = Query(..., description="State parameter for CSRF protection")
):
    """Handle OAuth callback"""
    try:
        credentials = await get_pkce_credentials()
        oauth = OAuth2Session(
            settings.CLIENT_ID,
            redirect_uri=settings.REDIRECT_URI,
            scope=scopes
        )
        
        token = oauth.fetch_token(
            token_url=token_url,
            client_secret=settings.CLIENT_SECRET,
            code_verifier=credentials["code_verifier"],
            code=code
        )
        
        redis_handler = RedisHandler()
        redis_handler.store_twitter_tokens("bot_user", token)
        
        return {"message": "Successfully authenticated with Twitter"}
    except Exception as e:
        logger.error(f"Failed to handle Twitter callback: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reset-auth")
async def reset_auth():
    """Clear stored tokens and PKCE credentials"""
    try:
        redis_handler = RedisHandler()
        redis_handler.clear_all_tokens()
        return {"message": "Successfully cleared all tokens"}
    except Exception as e:
        logger.error(f"Failed to clear tokens: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/test-tweet")
async def test_tweet():
    """Post a simple test tweet"""
    try:
        twitter_bot = TwitterBot()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        test_id = ''.join(random.choices('0123456789', k=4))  # Random 4-digit number
        content = f"Test tweet {test_id} from City Farmers Bot - checking API connectivity at {timestamp}"
        
        logger.info("Attempting to post test tweet")
        tweet_id = await twitter_bot.post_tweet(content)
        
        return {
            "status": "success",
            "tweet_id": tweet_id,
            "url": f"https://twitter.com/i/web/status/{tweet_id}"
        }
    except Exception as e:
        logger.error(f"Test tweet failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))