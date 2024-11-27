from farcaster import Warpcast
from src.config.settings import get_settings
import logging

logger = logging.getLogger(__name__)

class FarcasterBot:
    def __init__(self):
        self.settings = get_settings()
        self.client = Warpcast(mnemonic=self.settings.FARCASTER_MNEMONIC)
    
    async def post_cast(self, content: str):
        """Post a cast to Farcaster"""
        try:
            logger.info("Attempting to post to Farcaster...")
            response = self.client.post_cast(text=content)
            cast_hash = response.cast.hash
            logger.info(f"Cast posted successfully! Hash: {cast_hash}")
            return cast_hash
        except Exception as e:
            logger.error(f"Failed to post to Farcaster: {str(e)}")
            raise 