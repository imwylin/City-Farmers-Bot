# City Farmers Bot

A social media bot for City Farmers, an innovative urban farming company. The bot generates and posts engaging content about aeroponic farming, greenhouse innovation, and open source Bubble Tech to both Twitter and Farcaster.

## Features

- Automated tweet generation using Claude AI
- Twitter OAuth 2.0 with PKCE
- Cross-posting to Farcaster
- Redis-based token storage
- Background task processing
- Error handling and logging
- Automated scheduling with rate limit handling

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
      - `shitposting`: Elite agricultural truth bombs

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

# Elite agricultural shitposting
curl -X POST "https://city-farmers-bot.onrender.com/post-tweet?content_type=shitposting"
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
curl https://city-farmers-bot.onrender.com/scheduler-status
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
   - Health Check Path: `/health`
3. Configure environment variables
4. Visit `/auth/twitter` to authenticate
5. Check `/health` to verify setup

The health check endpoint verifies:
- Redis connection
- Twitter token presence
- Scheduler status
- Next scheduled run time

Response example:
```json
{
    "status": "healthy",
    "redis_connected": true,
    "has_tokens": true,
    "scheduler_running": true,
    "next_run": "2024-11-27 09:00:00 CST"
}
```

## License

MIT

## Environment Variables

Required environment variables:
```
ANTHROPIC_API_KEY=your_claude_api_key
CLIENT_ID=your_twitter_client_id
CLIENT_SECRET=your_twitter_client_secret
REDIS_URL=your_redis_url
LOG_LEVEL=INFO
ENVIRONMENT=production
FARCASTER_MNEMONIC=your_farcaster_mnemonic_here
```

## Application Settings

- Configure these settings in your deployment:

### Web Service
- Environment: Python
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
- Health Check Path: `/health`

### Application Settings
- LOG_LEVEL=INFO
- ENVIRONMENT=production

## Rate Limits

The bot is subject to Twitter's API rate limits:

- Daily tweet limit: 17 tweets per 24-hour period
- Current behavior on rate limits:
  - 429 (Too Many Requests): Operation fails and logs error
  - 401 (Unauthorized): Attempts token refresh
  - Rate limit resets: Daily at UTC midnight

Note: Rate limit handling improvements are planned for a future update to provide better automatic rescheduling and monitoring capabilities.

To avoid rate limits, the scheduler spaces out posts throughout the day. If you encounter rate limits, wait until the next UTC day before resuming operations.

## Farcaster Setup

1. Get your Farcaster custody account mnemonic from Warpcast
2. Add the mnemonic to your `.env` file:
   ```
   FARCASTER_MNEMONIC=your_12_word_recovery_phrase
   ```
3. The bot will automatically cross-post content to both Twitter and Farcaster
4. Farcaster errors are handled gracefully - if posting to Farcaster fails, the bot will continue operating on Twitter