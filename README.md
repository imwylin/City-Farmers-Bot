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

## Testing Commands

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

The bot automatically posts at these times daily:
- 9:00 AM
- 12:00 PM
- 2:00 PM
- 4:00 PM
- 7:00 PM

Content types rotate through educational, decentralized, and sustainability themes.

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