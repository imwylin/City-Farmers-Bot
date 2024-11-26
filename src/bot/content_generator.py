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
            return content
        except Exception as e:
            logger.error(f"Failed to generate content: {str(e)}")
            raise

    def _get_educational_prompt(self) -> str:
        """Rotate through different educational topics"""
        prompts = [
            """Write a single tweet (EXACTLY 280 chars or less) about the Bubble Tech greenhouse system.
            Focus on how bubble generators in the double-layer roof create dynamic temperature control.
            Return ONLY the tweet text, nothing else.""",
            
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