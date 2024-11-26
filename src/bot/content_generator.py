from anthropic import Anthropic
from src.config.settings import get_settings
import logging

logger = logging.getLogger(__name__)

class ContentGenerator:
    def __init__(self):
        self.settings = get_settings()
        self.client = Anthropic(api_key=self.settings.ANTHROPIC_API_KEY)
        
    async def generate_tweet(self, content_type: str) -> str:
        """Generate tweet content using Claude"""
        prompts = {
            "educational": "Write a spicy, engaging tweet about aeroponic farming innovation. Be bold and authentic, avoid corporate speak. Include modern farming tech details.",
            "franchise": "Create a tweet about City Farmers franchise opportunities. Focus on the underdog story and potential for local impact. Be authentic and inspiring.",
            "sustainability": "Generate a tweet about sustainable urban farming. Mix humor with deep knowledge, emphasize tech innovation and environmental impact."
        }
        
        try:
            message = await self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=100,
                temperature=0.9,
                system="You are a witty, authentic voice for an innovative urban farming company. You write engaging tweets that mix humor, technical knowledge, and bold statements about agriculture.",
                messages=[{
                    "role": "user",
                    "content": prompts.get(content_type, prompts["educational"])
                }]
            )
            return message.content
        except Exception as e:
            logger.error(f"Failed to generate content: {str(e)}")
            raise 