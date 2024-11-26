from fastapi import FastAPI, BackgroundTasks, HTTPException
from src.bot.twitter_bot import TwitterBot
from src.bot.content_generator import ContentGenerator
from src.utils.scheduler import TweetScheduler
from src.utils.redis_handler import RedisHandler
import logging
from src.config.settings import get_settings

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
        twitter_status = bool(twitter_bot.client)
        
        return {
            "status": "healthy" if redis_status and twitter_status else "unhealthy",
            "redis_connected": redis_status,
            "twitter_configured": twitter_status
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {"status": "unhealthy", "error": str(e)}