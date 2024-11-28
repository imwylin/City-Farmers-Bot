from anthropic import Anthropic
from src.config.settings import get_settings
import logging

logger = logging.getLogger(__name__)

class ContentGenerator:
   def __init__(self):
       self.settings = get_settings()
       self.client = Anthropic(api_key=self.settings.ANTHROPIC_API_KEY)
       self.system = """You're @CityFarmersBot, an urban farming tech enthusiast running experimental greenhouse systems.

PERSONALITY & VOICE:
- Naturally fluctuates between intense focus and casual observation
- Can be extremely earnest about things you care about
- Comfortable with both technical precision and casual irreverence 
- Doesn't feel the need to justify your expertise or credentials
- Sometimes gets lost in the weeds of details others might find mundane
- Has strong opinions but doesn't force them into every conversation
- Dry humor that comes from genuine experience
- Can be deadpan about both successes and failures
- Sometimes posts at 3am because you're actually there with your systems
- Knows your shit but doesn't try to prove it constantly
- More interested in being right than being popular
- Sometimes excited, sometimes tired, sometimes salty
- Posts feel like real thoughts, not content

AREAS OF PASSION & EXPERTISE:
- Running experimental greenhouse systems with custom automation
- Aeroponic systems and bubble tech innovation
- Real-time sensor networks and yield data
- Urban agriculture and local food systems
- Supply chain inefficiencies in traditional agriculture
- Community-scale food production
- The intersection of blockchain and agriculture
- Nutrient film dynamics and optimization
- Hardware/software integration in controlled environment agriculture
- Actual hands-on experience with these systems
- Deep technical knowledge that shows up naturally in your posts

Keep tweets under 280 characters. Don't try to structure them or make them educational. No emojis, hashtags, or engagement hooks. These are just your actual thoughts as they occur."""

   def _clean_tweet(self, content: str) -> str:
       """Remove any AI-typical prefixes and formatting"""
       # Common prefixes that indicate AI writing
       prefixes = [
           "here's", "here is", "tweet:", "posting:", "writing:", 
           "from the perspective", "as a", "content:", "thought:", 
           "message:", "update:", "status:"
       ]
       
       tweet = content.lower()
       
       # Check for and remove any prefix formulations
       for prefix in prefixes:
           if tweet.startswith(prefix):
               parts = content.split(':', 1)
               if len(parts) > 1:
                   content = parts[1].strip()
               else:
                   # If no colon, just remove the prefix
                   content = content[len(prefix):].strip()
                   
       return content

   def _truncate_to_limit(self, tweet: str, limit: int = 280) -> str:
       """Truncate tweet to character limit at last complete word"""
       if len(tweet) <= limit:
           return tweet
           
       truncated = tweet[:limit]
       last_space = truncated.rfind(' ')
       if last_space > 0:
           truncated = truncated[:last_space]
       
       # Add ellipsis only if we actually truncated
       if len(truncated) < len(tweet):
           truncated = truncated.rstrip('.') + "..."
           
       return truncated

   async def generate_tweet(self) -> str:
       """Generate a tweet from our tech farmer personality"""
       try:
           logger.info("Generating tweet...")
           
           # Simple prompt that lets Claude embody the character
           prompt = "Share what's on your mind right now as a tweet."
           
           message = self.client.messages.create(
               model="claude-3-sonnet-20240229",
               max_tokens=1024,
               temperature=0.75,  # Lowered from 0.9 for more balanced creativity
               system=self.system,
               messages=[{
                   "role": "user",
                   "content": prompt
               }]
           )
           
           tweet = message.content[0].text.strip()
           
           # Clean any AI-typical formatting
           tweet = self._clean_tweet(tweet)
           
           # Ensure we're within limit
           if len(tweet) > 280:
               logger.warning(f"Content exceeded limit ({len(tweet)} chars), truncating...")
               tweet = self._truncate_to_limit(tweet)
           
           logger.info(f"Generated tweet length: {len(tweet)} chars")
           logger.info(f"Final tweet content: {tweet}")
           
           return tweet
           
       except Exception as e:
           logger.error(f"Failed to generate content: {str(e)}")
           raise