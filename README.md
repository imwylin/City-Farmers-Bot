# City Farmers Bot

A Twitter marketing bot for City Farmers, an innovative urban farming company. The bot generates and posts engaging content about aeroponic farming, greenhouse innovation, and open source Bubble Tech.

## Features

- Automated tweet generation using Claude AI
- Twitter OAuth 2.0 with PKCE
- Redis-based token storage
- Background task processing
- Error handling and logging

## Setup

1. Clone the repository:
```bash
git clone https://github.com/imwylin/City-Farmers-Bot.git
cd City-Farmers-Bot
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env` and fill in your credentials:
```bash
cp .env.example .env
```

5. Run the application:
```bash
uvicorn src.main:app --reload
```

## X/Twitter API Setup

1. In Twitter Developer Portal:
   - Enable OAuth 2.0
   - Set App type to "Web App"
   - Add callback URL: `https://your-domain.com/oauth/callback`
   - Verify required scopes are enabled:
     - tweet.read
     - tweet.write
     - users.read
     - offline.access

2. Configure environment variables:
```
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
REDIRECT_URI=https://your-domain.com/oauth/callback
```

3. Verify API connection:
    ```bash
    # Check system health
    curl https://your-domain.com/health

    # If tokens need reset
    curl -X POST https://your-domain.com/reset-auth

    # Visit to authenticate
    https://your-domain.com/auth/twitter
    ```

## API Endpoints

### Authentication
- `GET /auth/twitter`: Start Twitter OAuth flow
- `GET /callback`: OAuth callback handler
- `POST /reset-auth`: Clear stored tokens and PKCE credentials

### Tweet Operations
- `POST /post-tweet`: Generate and post a tweet
  - Query Parameters:
    - `content_type`: Type of content to generate
      - `educational`: Bubble Tech and growing systems
      - `decentralized`: Local farming and blockchain
      - `sustainability`: Unhinged sustainability posts

### Monitoring
- `GET /health`: Check system health status
- `GET /scheduler-status`: Check scheduler status and next run time

## Testing Commands

Test API connectivity:
```bash
curl -X POST https://city-farmers-bot.onrender.com/test-tweet
```

Check system health:
```bash
curl https://city-farmers-bot.onrender.com/health
```

Post different types of tweets:
```bash
# Educational content about Bubble Tech
curl -X POST "https://city-farmers-bot.onrender.com/post-tweet?content_type=educational"

# Decentralized agriculture content
curl -X POST "https://city-farmers-bot.onrender.com/post-tweet?content_type=decentralized"

# Sustainability content
curl -X POST "https://city-farmers-bot.onrender.com/post-tweet?content_type=sustainability"
```

Reset authentication:
```bash
curl -X POST https://city-farmers-bot.onrender.com/reset-auth
```

## Automated Posting Schedule

The bot uses a scheduler to automatically post tweets at set times (Central Time):

- 9:00 AM
- 12:00 PM
- 2:00 PM
- 4:00 PM
- 7:00 PM

Content types rotate between educational, decentralized, and shitposting themes. The scheduler automatically handles rate limits by rescheduling for the next day.

Check scheduler status:
```bash
curl https://your-app.onrender.com/scheduler-status
```

Response:
```json
{
    "running": true,
    "next_run": "2024-11-27 09:00:00 CST"
}
```

## Deployment

The application is configured for deployment on Render.com:

1. Set up Redis instance on Render
2. Create Web Service:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
3. Configure environment variables
4. Visit `/auth/twitter` to authenticate
5. Check `/health` to verify setup

## License

MIT

## Environment Variables

Required environment variables:
```
ANTHROPIC_API_KEY=your_claude_api_key
CLIENT_ID=your_twitter_client_id
CLIENT_SECRET=your_twitter_client_secret
REDIS_URL=your_redis_url
```