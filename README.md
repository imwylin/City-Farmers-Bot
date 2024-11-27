# City Farmers Bot

An X marketing bot for City Farmers, an innovative urban farming company. The bot generates and posts engaging content about aeroponic farming, greenhouse innovation, and open source Bubble Tech.

## Features

- Automated tweet generation using Claude AI
- X OAuth 2.0 with PKCE
- Redis-based token storage
- Background task processing
- Error handling and logging
- Automated scheduling

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

## Environment Variables

Required environment variables in `.env`:
```
ANTHROPIC_API_KEY=your_claude_api_key
CLIENT_ID=your_x_client_id
CLIENT_SECRET=your_x_client_secret
REDIS_URL=your_redis_url
LOG_LEVEL=INFO
ENVIRONMENT=production
```

## X API Setup

1. In X Developer Portal:
   - Enable OAuth 2.0
   - Set App type to "Web App"
   - Add callback URL: `https://your-domain.com/oauth/callback`

2. Verify API connection:
```bash
# Check system health
curl https://your-domain.com/health

# If tokens need reset
curl -X POST https://your-domain.com/reset-auth

# Visit to authenticate
https://your-domain.com/auth/x
```

## Content Types

The bot generates three types of content:
- `educational`: Technical content about Bubble Tech and growing systems
- `decentralized`: Local farming and blockchain technology
- `shitposting`: Elite agricultural truth bombs

## Automated Schedule

Posts are made at set times (Central Time):
- 9:00 AM
- 12:00 PM
- 2:00 PM
- 4:00 PM
- 7:00 PM

Content types rotate through the schedule automatically.

## Deployment

The application is configured for deployment on Render.com:

1. Set up Redis instance on Render
2. Create Web Service:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
   - Health Check Path: `/health`
3. Configure environment variables
4. Visit `/auth/x` to authenticate
5. Check `/health` to verify setup

## API Endpoints

### Authentication
- `GET /auth/x`: Start X OAuth flow
- `GET /callback`: OAuth callback handler
- `POST /reset-auth`: Clear stored tokens

### Operations
- `POST /post-tweet`: Generate and post a tweet
- `GET /health`: Check system health
- `GET /scheduler-status`: Check scheduler status

## Testing Commands

Test API health:
```bash
curl https://city-farmers-bot.onrender.com/health
```

Response:
```json
{
    "status": "healthy",
    "redis_connected": true,
    "has_tokens": true,
    "scheduler_running": true,
    "next_run": "2024-11-27 09:00:00 CST"
}
```

Post tweets by type:
```bash
# Educational content
curl -X POST "https://city-farmers-bot.onrender.com/post-tweet?content_type=educational"

# Decentralized agriculture
curl -X POST "https://city-farmers-bot.onrender.com/post-tweet?content_type=decentralized"

# Agricultural shitposting
curl -X POST "https://city-farmers-bot.onrender.com/post-tweet?content_type=shitposting"
```

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

Reset authentication if needed:
```bash
curl -X POST https://city-farmers-bot.onrender.com/reset-auth
```

## License

MIT