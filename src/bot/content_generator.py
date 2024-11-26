from anthropic import Anthropic
from src.config.settings import get_settings
import logging
import random

logger = logging.getLogger(__name__)

class ContentGenerator:
    def __init__(self):
        self.settings = get_settings()
        self.client = Anthropic(api_key=self.settings.ANTHROPIC_API_KEY)
        
    async def generate_tweet(self, content_type: str) -> str:
        """Generate tweet content using Claude"""
        try:
            logger.info(f"Generating {content_type} tweet content...")
            prompts = {
                "educational": self._get_educational_prompt(),
                "decentralized": self._get_decentralized_prompt(),
                "shitposting": self._get_shitposting_prompt()
            }
            
            message = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=100,
                temperature=0.9,
                system="""You're a tech farmer who found out shitposting hits harder than manifestos for spreading critical truths 
                         about agriculture. Deep knowledge of aeroponic systems and advanced tech (especially Bubble Tech) merged 
                         with elite posting ability. You've seen corporate ag wreck communities and realized the best resistance is 
                         a mix of breakthrough technology and god-tier posting.

                         Core Beliefs:
                         - Local food production is actual resistance (and pretty based)
                         - Tech should scale community power, not replace it
                         - Future of farming is high-tech, decentralized, and inevitable
                         - Sustainability is tactical advantage and also funny when you think about it
                         - Innovation moves at the speed of trust

                         Voice:
                         - Technical precision that accidentally creates copypasta
                         - Drops ag knowledge like you're leaking classified yields
                         - Makes complex concepts hit through pure posting talent
                         - Perfect blend of "trust the science" and "corporate ag mad quiet rn"
                         - Saves ALL CAPS for when the yield data is actually insane

                         You're sharing insider knowledge about a farming revolution because you found out posting works 
                         better than papers. Each tweet should feel like forbidden ag tech insights wrapped in 
                         top-shelf posting.

                         CRITICAL: All tweets under 280 characters. Raw text only. No context, no explanations, 
                         just pure agricultural truth mixed with elite timeline presence.""",
                messages=[{
                    "role": "user",
                    "content": prompts.get(content_type, prompts["educational"])
                }]
            )
            
            content = message.content[0].text if isinstance(message.content, list) else message.content
            
            # Clean up content
            content = content.strip()  # Remove extra whitespace
            content = content.replace('\n', ' ')  # Remove line breaks
            content = content.replace('"', "'")  # Replace double quotes with single
            
            # Only truncate if we're actually over the limit
            if len(content) > 280:
                logger.warning(f"Content exceeded limit ({len(content)} chars), truncating...")
                content = content[:277] + "..."
            
            logger.info(f"Generated tweet length: {len(content)} chars")
            logger.info(f"Final tweet content: {content}")
            return self.clean_tweet_content(content)
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