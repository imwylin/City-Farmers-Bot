from fastapi import FastAPI, BackgroundTasks, HTTPException, Request
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

app = FastAPI()
settings = get_settings()

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize and start the scheduler
scheduler = TweetScheduler()
@app.on_event("startup")
async def start_scheduler():
    scheduler.start()

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
        redis_status = redis_handler.verify_connection()
        
        # Test Twitter client
        twitter_bot = TwitterBot()
        tokens = twitter_bot.redis_handler.get_twitter_tokens("bot_user")
        twitter_status = bool(tokens)
        
        return {
            "status": "healthy" if redis_status and twitter_status else "unhealthy",
            "redis_connected": redis_status,
            "twitter_configured": twitter_status
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {"status": "unhealthy", "error": str(e)}

# Add OAuth 2.0 Configuration
auth_url = "https://twitter.com/i/oauth2/authorize"
token_url = "https://api.x.com/2/oauth2/token"
scopes = ["tweet.read", "users.read", "tweet.write", "offline.access"]

# PKCE Setup
code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
code_verifier = re.sub("[^a-zA-Z0-9]+", "", code_verifier)
code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
code_challenge = code_challenge.replace("=", "")

@app.get("/auth/twitter")
async def twitter_auth():
    """Start OAuth flow"""
    oauth = OAuth2Session(
        settings.TWITTER_CLIENT_ID,
        redirect_uri=settings.TWITTER_REDIRECT_URI,
        scope=scopes
    )
    authorization_url, state = oauth.authorization_url(
        auth_url,
        code_challenge=code_challenge,
        code_challenge_method="S256"
    )
    return RedirectResponse(authorization_url)

@app.get("/callback")
async def twitter_callback(code: str, state: str):
    """Handle Twitter OAuth callback"""
    try:
        oauth = OAuth2Session(
            settings.TWITTER_CLIENT_ID,
            redirect_uri=settings.TWITTER_REDIRECT_URI,
            scope=scopes
        )
        
        # Get access token
        token = oauth.fetch_token(
            token_url=token_url,
            client_secret=settings.TWITTER_CLIENT_SECRET,
            code_verifier=code_verifier,
            code=code
        )
        
        # Store in Redis
        redis_handler = RedisHandler()
        redis_handler.store_twitter_tokens("bot_user", token)
        
        return {"message": "Successfully authenticated with Twitter"}
    except Exception as e:
        logger.error(f"Failed to handle Twitter callback: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))