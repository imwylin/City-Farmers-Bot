from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from src.bot.twitter_bot import TwitterBot
from src.bot.content_generator import ContentGenerator
import pytz
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class TweetScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler(timezone=pytz.timezone('America/Chicago'))
        self.content_generator = ContentGenerator()
        self.twitter_bot = TwitterBot()

    async def post_scheduled_tweet(self):
        """Post a tweet with rotating content types"""
        try:
            logger.info("Scheduler triggered - attempting to post tweet")
            content_types = ["educational", "decentralized", "shitposting"]
            
            current_time = datetime.now(pytz.timezone('America/Chicago'))
            logger.info(f"Current time in CT: {current_time}")
            hour = current_time.hour
            
            content_type = content_types[hour % len(content_types)]
            logger.info(f"Generating {content_type} tweet...")
            
            content = await self.content_generator.generate_tweet(content_type)
            logger.info(f"Generated content: {content}")
            
            await self.twitter_bot.post_tweet(content)
            logger.info(f"Tweet posted successfully - type: {content_type}")
        except Exception as e:
            if "Too Many Requests" in str(e):
                logger.warning("Rate limit hit - Rescheduling for tomorrow")
                # Remove current job
                self.scheduler.remove_job('tweet_scheduler')
                
                # Calculate tomorrow's date
                tomorrow = datetime.now(pytz.timezone('America/Chicago')) + timedelta(days=1)
                
                # Reschedule for tomorrow
                self.scheduler.add_job(
                    self.post_scheduled_tweet,
                    CronTrigger(
                        year=tomorrow.year,
                        month=tomorrow.month,
                        day=tomorrow.day,
                        hour="9,12,14,16,19",
                        minute="0"
                    ),
                    id="tweet_scheduler",
                    name="Post scheduled tweets"
                )
                logger.info(f"Rescheduled to resume at {tomorrow}")
            else:
                logger.error(f"Failed to post scheduled tweet: {str(e)}")
                logger.exception("Full traceback:")
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