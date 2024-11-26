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
            
            message = self.client.messages.create(
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
            # Extract just the text content from the message
            content = message.content[0].text if isinstance(message.content, list) else message.content
            logger.info(f"Successfully generated tweet content: {content[:50]}...")
            return content
        except Exception as e:
            logger.error(f"Failed to generate content: {str(e)}")
            raise

    def _get_educational_prompt(self) -> str:
        """Rotate through different educational topics"""
        prompts = [
            """Write a single tweet (max 280 chars) about the Bubble Tech greenhouse system.
            Focus on how bubble generators in the double-layer roof create dynamic temperature control.
            One complete thought, no threads, no cliffhangers.""",
            
            """Write a single tweet (max 280 chars) about how Bubble Tech handles cooling and shading.
            Focus on the cloud-like cover of 6mm bubbles creating ideal growing conditions.
            One complete thought, no threads, no cliffhangers.""",
            
            """Write a single tweet (max 280 chars) about Bubble Tech's insulation capabilities.
            Focus on how it reduces heat loss 10x compared to standard greenhouses.
            One complete thought, no threads, no cliffhangers.""",
            
            """Write a single tweet (max 280 chars) about aeroponic growing systems.
            Focus on soil-free, mist-based nutrient delivery.
            One complete thought, no threads, no cliffhangers.""",
            
            """Write a single tweet (max 280 chars) about aquaponics.
            Focus on how it combines fish farming with plant growth in a circular system.
            One complete thought, no threads, no cliffhangers."""
        ]
        return random.choice(prompts)

    def _get_decentralized_prompt(self) -> str:
        """Rotate through different decentralized agriculture topics"""
        prompts = [
            """Write a single tweet (max 280 chars) connecting blockchain with urban farming.
            Focus on supply chain transparency and community ownership models.
            One complete thought, no threads, no cliffhangers.""",

            """Write a single tweet (max 280 chars) about decentralized urban farms and food security.
            Focus on how local production protects against supply chain disruptions.
            One complete thought, no threads, no cliffhangers.""",

            """Write a single tweet (max 280 chars) about local urban farming's freshness advantage.
            Focus on the difference between hours-fresh and weeks-old transported produce.
            One complete thought, no threads, no cliffhangers.""",

            """Write a single tweet (max 280 chars) about democratizing food production.
            Focus on taking power back from big ag corporations through urban farming.
            One complete thought, no threads, no cliffhangers.""",

            """Write a single tweet (max 280 chars) about community resilience through local food.
            Focus on how decentralized farming strengthens local economies.
            One complete thought, no threads, no cliffhangers."""
        ]
        return random.choice(prompts)

    def _get_sustainability_prompt(self) -> str:
        """Generate completely DERANGED sustainability content"""
        prompts = [
            """Write a single UNHINGED tweet (max 280 chars) about Bubble Tech's energy efficiency.
            GO ABSOLUTELY FERAL about using 90% LESS ENERGY than BigAg.
            One complete thought, NO THREADS, JUST PURE ENERGY!!!!!""",

            """Write a single UNHINGED tweet (max 280 chars) about local food production.
            GO FULL CONSPIRACY about how Big Transport is sweating.
            One complete thought, NO THREADS, JUST PURE CHAOS!!!!!""",

            """Write a single UNHINGED tweet (max 280 chars) about water recycling.
            GO FULL 3AM CONSPIRACY BOARD about 95% water savings.
            One complete thought, NO THREADS, JUST PURE MADNESS!!!!!""",

            """Write a single UNHINGED tweet (max 280 chars) about pesticide-free farming.
            GO ABSOLUTELY GALAXY BRAIN about clean food production.
            One complete thought, NO THREADS, JUST PURE REVELATION!!!!!"""
        ]
        return random.choice(prompts)