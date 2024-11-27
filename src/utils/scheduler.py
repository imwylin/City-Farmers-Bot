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
            logger.info("=== Scheduler Triggered ===")
            logger.info("Attempting to post scheduled tweet...")
            
            content_types = ["educational", "decentralized", "shitposting"]
            current_time = datetime.now(pytz.timezone('America/Chicago'))
            logger.info(f"Current time in CT: {current_time}")
            hour = current_time.hour
            
            content_type = content_types[hour % len(content_types)]
            logger.info(f"Selected content type: {content_type}")
            
            content = await self.content_generator.generate_tweet(content_type)
            logger.info(f"Generated content: {content}")
            
            await self.twitter_bot.post_tweet(content)
            logger.info(f"Tweet posted successfully - type: {content_type}")
            
        except Exception as e:
            if "Too Many Requests" in str(e):
                logger.warning("=== Rate Limit Handler ===")
                logger.warning("Rate limit detected - Initiating rescheduling process")
                
                try:
                    # Remove current job
                    logger.info("Removing current schedule...")
                    self.scheduler.remove_job('tweet_scheduler')
                    logger.info("Current schedule removed successfully")
                    
                    # Calculate tomorrow's date
                    tomorrow = datetime.now(pytz.timezone('America/Chicago')) + timedelta(days=1)
                    logger.info(f"Calculated resume time: {tomorrow}")
                    
                    # Reschedule for tomorrow
                    logger.info("Creating new schedule...")
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
                    logger.info(f"New schedule created successfully")
                    logger.info(f"Tweets will resume at: {tomorrow}")
                    logger.info("=== Rescheduling Complete ===")
                    
                except Exception as reschedule_error:
                    logger.error(f"Failed to reschedule: {str(reschedule_error)}")
                    logger.exception("Rescheduling error traceback:")
                    raise
                    
            else:
                logger.error("=== Scheduler Error ===")
                logger.error(f"Failed to post scheduled tweet: {str(e)}")
                logger.exception("Error traceback:")
                raise

    def start(self):
        """Start the scheduler with defined jobs"""
        try:
            if not self.scheduler.running:
                logger.info("=== Starting Scheduler ===")
                logger.info("Creating initial schedule...")
                self.scheduler.add_job(
                    self.post_scheduled_tweet,
                    CronTrigger(hour="9,12,14,16,19", minute="0"),
                    id="tweet_scheduler",
                    name="Post scheduled tweets"
                )
                self.scheduler.start()
                logger.info("Initial schedule created")
                logger.info("Scheduler started successfully")
                logger.info("=== Startup Complete ===")
        except Exception as e:
            logger.error("=== Startup Error ===")
            logger.error(f"Failed to start scheduler: {str(e)}")
            logger.exception("Startup error traceback:")
            raise

    def shutdown(self):
        """Shutdown the scheduler gracefully"""
        if self.scheduler.running:
            self.scheduler.shutdown()