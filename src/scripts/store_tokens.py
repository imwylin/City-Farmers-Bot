import sys
sys.path.append('.')  # Add project root to path

from src.utils.redis_handler import RedisHandler

def store_initial_tokens():
    redis_handler = RedisHandler()
    
    # Initial tokens to store
    tokens = {
        "access_token": "YOUR_ACCESS_TOKEN",  # You'll need to provide this
        "refresh_token": "YOUR_REFRESH_TOKEN"  # And this
    }
    
    try:
        redis_handler.store_twitter_tokens("bot_user", tokens)
        print("Successfully stored tokens in Redis")
        
        # Verify storage
        stored_tokens = redis_handler.get_twitter_tokens("bot_user")
        if stored_tokens:
            print("Verified tokens are stored correctly")
        else:
            print("Failed to verify token storage")
            
    except Exception as e:
        print(f"Failed to store tokens: {str(e)}")

if __name__ == "__main__":
    store_initial_tokens() 