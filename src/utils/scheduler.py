from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from src.bot.twitter_bot import TwitterBot
from src.bot.content_generator import ContentGenerator
import pytz
import logging
from datetime import datetime, timedelta
from src.utils.redis_handler import RedisHandler

logger = logging.getLogger(__name__)

class TweetScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler(timezone=pytz.timezone('America/Chicago'))
        self.content_generator = ContentGenerator()
        self.twitter_bot = TwitterBot()

    def _calculate_next_slot_after_wait(self, current_time: datetime) -> datetime:
        """Calculate the next available slot after a 24-hour wait period"""
        # Calculate minimum resume time (24 hours from now)
        min_resume_time = current_time + timedelta(days=1)
        
        # Find next scheduled hour after the 24-hour wait
        scheduled_hours = [9, 12, 14, 16, 19]
        min_hour = min_resume_time.hour
        next_hour = next((h for h in scheduled_hours if h > min_hour), scheduled_hours[0])
        
        # If no remaining slots today, move to next day
        resume_time = min_resume_time
        if next_hour <= min_hour:
            resume_time += timedelta(days=1)
            next_hour = scheduled_hours[0]
        
        return resume_time.replace(hour=next_hour, minute=0, second=0, microsecond=0)

    async def _handle_rate_limit_reschedule(self, current_time: datetime):
        """Common logic for handling rate limit rescheduling"""
        try:
            # Remove current job
            logger.info("Removing current schedule...")
            self.scheduler.remove_job('tweet_scheduler')
            logger.info("Current schedule removed successfully")
            
            # Calculate resume times
            min_resume_time = current_time + timedelta(days=1)
            resume_time = self._calculate_next_slot_after_wait(current_time)
            
            logger.info(f"Current time: {current_time}")
            logger.info(f"24-hour minimum wait until: {min_resume_time}")
            logger.info(f"Next scheduled slot after wait: {resume_time}")
            
            # Store rate limit state in Redis
            self.redis_handler = RedisHandler()
            self.redis_handler.store_rate_limit_state(resume_time.isoformat())
            
            # Reschedule for next available slot after 24-hour wait
            logger.info("Creating new schedule...")
            self.scheduler.add_job(
                self.post_scheduled_tweet,
                CronTrigger(
                    year=resume_time.year,
                    month=resume_time.month,
                    day=resume_time.day,
                    hour="9,12,14,16,19",
                    minute="0",
                    timezone='America/Chicago'
                ),
                id="tweet_scheduler",
                name="Post scheduled tweets"
            )
            logger.info(f"New schedule created successfully")
            logger.info(f"Tweets will resume at: {resume_time}")
            logger.info("=== Rescheduling Complete ===")
        except Exception as e:
            logger.error(f"Failed to handle rate limit reschedule: {str(e)}")
            raise

    async def post_scheduled_tweet(self):
        """Post tweet with rotating content types"""
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
            
            # Post to Twitter
            await self.twitter_bot.post_tweet(content)
            logger.info(f"Tweet posted successfully - type: {content_type}")
            
        except Exception as e:
            if "Too Many Requests" in str(e):
                logger.warning("=== Rate Limit Handler ===")
                logger.warning("Rate limit detected - Waiting 24 hours before next scheduled slot")
                
                try:
                    current_time = datetime.now(pytz.timezone('America/Chicago'))
                    await self._handle_rate_limit_reschedule(current_time)
                except Exception as reschedule_error:
                    logger.error(f"Failed to reschedule: {str(reschedule_error)}")
                    logger.exception("Rescheduling error traceback:")
                    raise
            else:
                logger.error("=== Scheduler Error ===")
                logger.error(f"Failed to post scheduled tweet: {str(e)}")
                logger.exception("Error traceback:")
                raise

    async def handle_rate_limit(self):
        """Handle rate limit from external trigger"""
        logger.warning("=== External Rate Limit Handler ===")
        logger.warning("Rate limit reported - Waiting 24 hours before next scheduled slot")
        
        try:
            current_time = datetime.now(pytz.timezone('America/Chicago'))
            await self._handle_rate_limit_reschedule(current_time)
        except Exception as reschedule_error:
            logger.error(f"Failed to reschedule: {str(reschedule_error)}")
            logger.exception("Rescheduling error traceback:")
            raise

    def start(self):
        """Start the scheduler with defined jobs"""
        try:
            if not self.scheduler.running:
                logger.info("=== Starting Scheduler ===")
                logger.info("Creating initial schedule...")
                
                # Check for stored rate limit state
                self.redis_handler = RedisHandler()
                stored_resume_time = self.redis_handler.get_rate_limit_state()
                
                if stored_resume_time:
                    resume_time = datetime.fromisoformat(stored_resume_time)
                    current_time = datetime.now(pytz.timezone('America/Chicago'))
                    
                    if resume_time > current_time:
                        logger.info(f"Found stored rate limit state. Waiting until: {resume_time}")
                        self.scheduler.start()
                        self.scheduler.add_job(
                            self.post_scheduled_tweet,
                            CronTrigger(
                                year=resume_time.year,
                                month=resume_time.month,
                                day=resume_time.day,
                                hour="9,12,14,16,19",
                                minute="0",
                                timezone='America/Chicago'
                            ),
                            id="tweet_scheduler",
                            name="Post scheduled tweets"
                        )
                        return
                
                # Normal startup if no rate limit state
                current_time = datetime.now(pytz.timezone('America/Chicago'))
                logger.info(f"Current time (CT): {current_time}")
                
                self.scheduler.start()
                
                job = self.scheduler.add_job(
                    self.post_scheduled_tweet,
                    CronTrigger(hour="9,12,14,16,19", minute="0", timezone='America/Chicago'),
                    id="tweet_scheduler",
                    name="Post scheduled tweets"
                )
                
                if job and hasattr(job, 'next_run_time'):
                    logger.info(f"Next scheduled run: {job.next_run_time}")
                
                logger.info("Initial schedule created")
                logger.info("Scheduler started successfully")
                logger.info("=== Startup Complete ===")
        except Exception as e:
            logger.error("=== Startup Error ===")
            logger.error(f"Failed to start scheduler: {str(e)}")
            logger.exception("Startup error traceback:")
            raise

    def shutdown(self):
        """Handle shutdown request"""
        if not self.scheduler.running:
            return
            
        if self.get_next_run_time():
            # Silently preserve
            return
            
        logger.info("No pending jobs - shutting down scheduler")
        self.scheduler.shutdown()

    def get_next_run_time(self):
        """Get the next scheduled run time"""
        try:
            job = self.scheduler.get_job('tweet_scheduler')
            if job:
                return job.next_run_time
            return None
        except Exception as e:
            logger.error(f"Failed to get next run time: {str(e)}")
            return None

    def is_running(self):
        """Check if scheduler is running"""
        return self.scheduler.running and self.scheduler.get_job('tweet_scheduler') is not None