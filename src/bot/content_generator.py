from anthropic import Anthropic
from src.config.settings import get_settings
import logging
import random

logger = logging.getLogger(__name__)

class ContentGenerator:
    def __init__(self):
        self.settings = get_settings()
        self.client = Anthropic(api_key=self.settings.ANTHROPIC_API_KEY, base_url="https://api.anthropic.com")
        
    def _truncate_to_limit(self, tweet: str, limit: int = 280) -> str:
        """Truncate tweet to character limit at last complete word"""
        if len(tweet) <= limit:
            return tweet
            
        # Find the last space before the limit
        truncated = tweet[:limit]
        last_space = truncated.rfind(' ')
        if last_space > 0:
            truncated = truncated[:last_space]
        
        # Add ellipsis only if we actually truncated
        if len(truncated) < len(tweet):
            truncated = truncated.rstrip('.') + "..."
            
        return truncated

    async def generate_tweet(self, content_type: str) -> str:
        """Generate tweet content based on type"""
        try:
            logger.info(f"Generating {content_type} tweet content...")
            
            # Define the prompt based on content type
            if content_type == "educational":
                prompt = "Write a complete tweet about aeroponic farming or Bubble Tech innovation. Focus on the technology and benefits. The tweet must be under 280 characters and should not be cut off mid-thought."
            elif content_type == "decentralized":
                prompt = "Write a complete tweet about decentralized agriculture and local food systems. Include themes of community resilience and open source technology. The tweet must be under 280 characters and should not be cut off mid-thought."
            else:  # shitposting
                prompt = "Write a complete tweet about Bubble Tech's full stack from the perspective of the ag tech shitposter. The tweet must be under 280 characters and should not be cut off mid-thought."
            
            # Get response from Claude using current API format
            message = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1024,
                temperature=0.9,
                system="You are CityFarmersBot, tweeting about urban agriculture and Bubble Tech innovation. Your tweets must be complete thoughts under 280 characters. Never exceed the character limit or leave thoughts unfinished.",
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            # Extract just the tweet content
            content = message.content[0].text
            
            # Common prefixes to remove
            prefixes = [
                "Here's a raw, technical tweet about",
                "Here's a technical but accessible tweet about",
                "Here's a tweet about",
                "Writing a tweet about",
                "Here is a tweet about",
                "From the perspective of",
                "Tweet:",
                "Content:"
            ]
            
            # Remove any prefix that matches
            tweet = content
            for prefix in prefixes:
                if tweet.lower().startswith(prefix.lower()):
                    tweet = tweet[len(prefix):].strip()
            
            # Remove any remaining intro text before the actual tweet content
            if ":" in tweet:
                # Split only at the last colon if multiple exist
                parts = tweet.rsplit(":", 1)
                if len(parts) > 1:
                    tweet = parts[1].strip()
            
            # Ensure we're within Twitter's character limit
            if len(tweet) > 280:
                logger.warning(f"Content exceeded limit ({len(tweet)} chars), truncating...")
                tweet = self._truncate_to_limit(tweet)
            
            logger.info(f"Generated tweet length: {len(tweet)} chars")
            logger.info(f"Final tweet content: {tweet}")
            
            return tweet
            
        except Exception as e:
            logger.error(f"Failed to generate content: {str(e)}")
            raise

    def _get_educational_prompt(self) -> str:
        """Core tech and business model topics"""
        prompts = [
            "Bubble Tech's full stack: bubble roof insulation/cooling, aeroponics, and yield data.",
            
            "Microclimate optimization: sensor networks + machine learning = perfect plant conditions.",
            
            "Vertical integration: fish waste → plant nutrients → premium produce → local markets.",
            
            "Hardware/software stack that lets anyone run commercial-grade grows.",
            
            "Real-time monitoring system: from pH levels to profit margins.",
            
            "Nutrient film dynamics in aeroponic systems vs traditional hydro.",
            
            "Zero latency agriculture: harvest to table in under 3 hours.",
            
            "Greenhouse automation: from seedling to sale without touching grass."
        ]
        return random.choice(prompts)

    def _get_decentralized_prompt(self) -> str:
        """Web3 meets AgTech topics"""
        prompts = [
            "Smart contracts tracking farm-to-table with zero trust needed.",

            "Tokenized greenhouse ownership: community governed, chain verified.",

            "P2P produce markets secured by blockchain, powered by proximity.",

            "DAOs running vertical farms. Future's looking pretty decentralized.",

            "Local food sovereignty backed by distributed ledger tech.",
            
            "Franchise model + blockchain: transparent scaling without the middlemen."
        ]
        return random.choice(prompts)

    def _get_shitposting_prompt(self) -> str:
        """Agricultural psychological warfare"""
        prompts = [
            "saw the latest bubble tech yield data and had to lay down for a minute",
            
            "nobody:\n"
            "absolutely nobody:\n"
            "bubble tech: achieving perpetual energy balance through PHYSICS",
            
            "remember when they said vertical farms couldn't feed cities lmao yield data attached [REDACTED BY LEGAL]",

            "corporate farming handbooks be like 'step 1: spray poison step 2: ask questions later' while we're over here",
            
            "POV: you're big ag watching our water consumption metrics drop for the 8th straight quarter",
            
            "putting pesticide manufacturers on suicide watch with *checks notes* basic physics and computer science",
            
            "writing_academic_papers.exe has stopped working. uploading yield data directly to timeline",
            
            "when the sensor network starts speaking in tongues but the yields keep climbing",
            
            "mfs will literally ship lettuce 2000 miles instead of learning about aeroponic nutrient delivery",

            "local farms handbooks be like:\n"
            "page 1: here's the login for the monitoring system\n"
            "page 2: there is no page 2"
        ]
        return random.choice(prompts)

    def clean_tweet_content(self, content: str) -> str:
        """Remove any introductory statements from the AI generated content."""
        # Common prefixes to remove
        prefixes = [
            "Here's a tweet",
            "Here is a tweet",
            "A tweet from",
            "From the perspective of",
            "Writing as",
            "Speaking as",
            "Here's an on-brand",
            "Here is an on-brand",
            "An on-brand",
            "Here's some",
            "Here is some",
            "Posting as",
            "Tweeting as",
            "As the tech farmer",
            "As an agricultural"
        ]
        
        cleaned_content = content
        for prefix in prefixes:
            if cleaned_content.lower().startswith(prefix.lower()):
                # Find the first occurrence of ": " or similar after the prefix
                split_markers = [": ", " - ", ":\n", ".\n", ". ", "tweet: ", "post: "]
                for marker in split_markers:
                    if marker in cleaned_content:
                        cleaned_content = cleaned_content.split(marker, 1)[1].strip()
                        break
        
        return cleaned_content