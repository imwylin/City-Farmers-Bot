from fastapi import FastAPI, BackgroundTasks
from src.bot.twitter_bot import TwitterBot
from src.bot.content_generator import ContentGenerator
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

@app.post("/post-tweet")
async def create_tweet(background_tasks: BackgroundTasks, content_type: str = "educational"):
    """Endpoint to generate and post a tweet"""
    try:
        content_generator = ContentGenerator()
        twitter_bot = TwitterBot()
        
        # Generate content
        content = await content_generator.generate_tweet(content_type)
        
        # Post tweet in background
        background_tasks.add_task(twitter_bot.post_tweet, content)
        
        return {"status": "Tweet generation initiated", "content": content}
    except Exception as e:
        logger.error(f"Failed to create tweet: {str(e)}")
        raise 