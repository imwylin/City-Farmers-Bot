from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from src.bot.twitter_bot import TwitterBot
from src.bot.content_generator import ContentGenerator
import pytz
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class TweetScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler(timezone=pytz.timezone('America/Chicago'))
        self.content_generator = ContentGenerator()
        self.twitter_bot = TwitterBot()

    async def post_scheduled_tweet(self):
        """Post a tweet with rotating content types"""
        try:
            # Rotate through different content types
            content_types = ["educational", "decentralized", "shitposting"]
            
            # Get current hour in Central Time
            current_time = datetime.now(pytz.timezone('America/Chicago'))
            hour = current_time.hour
            
            content_type = content_types[hour % len(content_types)]
            logger.info(f"Generating {content_type} tweet...")
            
            content = await self.content_generator.generate_tweet(content_type)
            await self.twitter_bot.post_tweet(content)
            logger.info(f"Tweet posted successfully - type: {content_type}")
        except Exception as e:
            logger.error(f"Failed to post scheduled tweet: {str(e)}")
            raise

    def start(self):
        """Start the scheduler with defined jobs"""
        try:
            if not self.scheduler.running:
                self.scheduler.add_job(
                    self.post_scheduled_tweet,
                    CronTrigger(hour="9,12,14,16,19", minute="0"),
                    id="tweet_scheduler",
                    name="Post scheduled tweets"
                )
                self.scheduler.start()
                logger.info("Tweet scheduler started successfully")
        except Exception as e:
            logger.error(f"Failed to start scheduler: {str(e)}")
            raise

    def shutdown(self):
        """Shutdown the scheduler gracefully"""
        if self.scheduler.running:
            self.scheduler.shutdown()