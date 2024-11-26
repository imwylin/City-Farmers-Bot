import base64
import hashlib
import os
import re
import json
import logging
from flask import Flask, request, redirect, session, url_for
from requests_oauthlib import OAuth2Session
from src.bot.content_generator import ContentGenerator
from src.utils.redis_handler import RedisHandler
from src.config.settings import get_settings

settings = get_settings()
app = Flask(__name__)
app.secret_key = os.urandom(50)

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# OAuth 2.0 Configuration
auth_url = "https://twitter.com/i/oauth2/authorize"
token_url = "https://api.x.com/2/oauth2/token"
scopes = ["tweet.read", "users.read", "tweet.write", "offline.access"]

# PKCE Setup
code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
code_verifier = re.sub("[^a-zA-Z0-9]+", "", code_verifier)
code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
code_challenge = code_challenge.replace("=", "")

def make_token():
    return OAuth2Session(
        settings.TWITTER_CLIENT_ID, 
        redirect_uri=settings.TWITTER_REDIRECT_URI, 
        scope=scopes
    )

@app.route("/")
def auth():
    """Start OAuth flow"""
    twitter = make_token()
    authorization_url, state = twitter.authorization_url(
        auth_url, 
        code_challenge=code_challenge, 
        code_challenge_method="S256"
    )
    session["oauth_state"] = state
    return redirect(authorization_url)

@app.route("/callback")
def callback():
    """Handle OAuth callback and post initial tweet"""
    try:
        twitter = make_token()
        token = twitter.fetch_token(
            token_url=token_url,
            client_secret=settings.TWITTER_CLIENT_SECRET,
            code_verifier=code_verifier,
            code=request.args.get("code")
        )
        
        # Store token in Redis
        redis_handler = RedisHandler()
        redis_handler.store_twitter_tokens("bot_user", token)
        
        # Generate and post initial tweet
        content_generator = ContentGenerator()
        content = content_generator.generate_tweet("educational")
        
        response = requests.post(
            "https://api.x.com/2/tweets",
            json={"text": content},
            headers={
                "Authorization": f"Bearer {token['access_token']}",
                "Content-Type": "application/json",
            }
        )
        
        return {"message": "Successfully authenticated and posted first tweet", "response": response.json()}
    except Exception as e:
        logger.error(f"Callback failed: {str(e)}")
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(port=5000) 