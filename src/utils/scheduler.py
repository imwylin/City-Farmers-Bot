from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from src.bot.twitter_bot import TwitterBot
from src.bot.content_generator import ContentGenerator
import logging

logger = logging.getLogger(__name__)

class TweetScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.content_generator = ContentGenerator()
        self.twitter_bot = TwitterBot()

    async def post_scheduled_tweet(self):
        """Post a tweet with rotating content types"""
        try:
            # Rotate through different content types
            content_types = ["educational", "franchise", "sustainability"]
            hour = self.scheduler.get_current_job().next_run_time.hour
            content_type = content_types[hour % len(content_types)]
            
            content = await self.content_generator.generate_tweet(content_type)
            await self.twitter_bot.post_tweet(content)
            logger.info(f"Scheduled tweet posted successfully - type: {content_type}")
        except Exception as e:
            logger.error(f"Failed to post scheduled tweet: {str(e)}")

    def start(self):
        """Start the scheduler with defined jobs"""
        # Post tweets at optimal times throughout the day
        self.scheduler.add_job(
            self.post_scheduled_tweet,
            CronTrigger(hour="9,12,14,16,19", minute="0"),  # Added 12pm and 4pm slots
            id="tweet_scheduler",
            name="Post scheduled tweets"
        )
        self.scheduler.start()
        logger.info("Tweet scheduler started") 