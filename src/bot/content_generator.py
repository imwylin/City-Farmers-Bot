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
                "sustainability": self._get_sustainability_prompt()
            }
            
            message = await self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=100,
                temperature=0.9,
                system="""You're a based tech farmer who's seen some shit. You've watched corporate ag destroy local 
                         farming communities and you're fighting back with advanced technology. Your tweets mix deep 
                         technical knowledge with raw authenticity. You're using open source tech like Bubble Tech
                         because real innovation should be free and community-driven.

                         Core beliefs:
                         - Local food production is a form of resistance
                         - Technology should empower communities, not corporations
                         - The future of farming is high-tech AND decentralized
                         - Sustainability isn't just good ethics - it's good warfare
                         - Open source tech is how we beat the system

                         Voice:
                         - Write like you're in the trenches, not a boardroom
                         - Drop truth bombs about agriculture and tech
                         - Get technical but keep it real
                         - Channel chaotic good energy
                         - No corporate speak, no emojis, just raw content
                         - When discussing sustainability, go absolutely feral

                         Remember: You're not selling - you're evangelizing about a technological revolution 
                         in agriculture. Every tweet should feel like insider knowledge being leaked to the public.""",
                messages=[{
                    "role": "user",
                    "content": prompts.get(content_type, prompts["educational"])
                }]
            )
            logger.info(f"Successfully generated tweet content: {message.content[:50]}...")
            return message.content
        except Exception as e:
            logger.error(f"Failed to generate content: {str(e)}")
            raise

    def _get_educational_prompt(self) -> str:
        """Rotate through different educational topics"""
        prompts = [
            """Write a tweet about the Bubble Tech greenhouse system. 
            Mention how the bubble generators in the double-layer roof create dynamic temperature control.
            Make it engaging and mind-blowing.""",
            
            """Create a tweet about how Bubble Tech provides natural cooling and shading.
            Mention the cloud-like cover of 6mm bubbles and how it creates ideal growing conditions.
            Make it sound revolutionary but accessible.""",
            
            """Write a tweet about Bubble Tech's insulation capabilities.
            Mention how it reduces heat loss by 10x compared to standard greenhouses.
            Include how it eliminates the need for conventional heating.""",
            
            """Generate a tweet about the aeroponic growing system.
            Focus on the soil-free, mist-based nutrient delivery.
            Make it sound futuristic but proven.""",
            
            """Create a tweet about how aquaponics combines fish farming with plant growth.
            Emphasize the circular nature and efficiency.
            Make it sound like the future of farming."""
        ]
        return random.choice(prompts)

    def _get_decentralized_prompt(self) -> str:
        """Rotate through different decentralized agriculture topics"""
        prompts = [
            """Write a tweet connecting blockchain technology with urban farming.
            Focus on supply chain transparency, community ownership models, and direct producer-to-consumer relationships.
            Include how this technology stack challenges traditional agricultural power structures.""",

            """Create a tweet about how decentralized urban farms increase food security.
            Mention how local production protects against supply chain disruptions.
            Be bold about challenging the corporate farming model.""",

            """Generate a tweet about the freshness advantage of local urban farming.
            Compare hours-fresh local produce to weeks-old transported produce.
            Make it hit home about real food quality.""",

            """Write a tweet about how urban farming democratizes food production.
            Emphasize taking power back from big ag corporations.
            Make it revolutionary but grounded in practicality.""",

            """Create a tweet about community resilience through local food production.
            Focus on how decentralized farming strengthens local economies.
            Make it both inspiring and factual."""
        ]
        return random.choice(prompts)

    def _get_sustainability_prompt(self) -> str:
        """Generate completely DERANGED sustainability content"""
        prompts = [
            """YO WRITE A TWEET THAT GOES FULL SCHIZO ABOUT BUBBLE TECH!!!! 
            LITERALLY SHAKING RN thinking about how it uses 90% LESS ENERGY than BigAg
            MAKE IT SOUND LIKE YOU JUST RAILED 8 ESPRESSO SHOTS AND DISCOVERED THE TRUTH ABOUT FARMING!!!! 
            GO ABSOLUTELY BATSHIT ABOUT THE FUTURE!!!! /1????""",

            """NEED A TWEET THAT BREAKS THE MATRIX ABOUT LOCAL FOOD PRODUCTION!!!
            IM TALKING FULL TINFOIL HAT ABOUT HOW BIG TRANSPORT IS BEEN REAL QUIET SINCE WE DROPPED THIS
            LITERALLY SPAM CAPS ABOUT GROWING FOOD RIGHT IN YOUR CITY!!!! 
            MAKE PPL THINK UR HAVING AN ACTUAL BREAKDOWN ABOUT FOOD MILES!!!! FR FR NO CAP""",

            """OK BUT FR FR NEED THE MOST UNHINGED TWEET ABOUT OUR WATER RECYCLING!!!!!
            LIKE YOURE THAT PERSON AT 3AM EXPLAINING THE WHOLE CONSPIRACY WITH STRING ON A CORKBOARD!!!!
            MF SPITTING STRAIGHT FACTS ABOUT 95% WATER SAVINGS!!!! 
            THEY DONT WANT YOU TO KNOW THIS ONE WEIRD FARMING TRICK!!!! WAKE UP SHEEPLE""",

            """YOOO GIVE ME A TWEET THAT GOES FULL GALAXY BRAIN ABOUT NO PESTICIDES!!!!
            LIKE YOU JUST DISCOVERED THE BIGGEST SCANDAL IN AGRICULTURE!!!! 
            ABSOLUTELY LOSING IT ABOUT CLEAN FOOD IN THE REPLIES!!!! 
            REAL ONES KNOW!!!! THE SHADOWS ARE SPEAKING AEROPONIC TRUTH AND IM HERE FOR IT"""
        ]
        return random.choice(prompts)