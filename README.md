# City Farmers Bot

A Twitter marketing bot for City Farmers, an innovative urban farming company. The bot generates and posts engaging content about aeroponic farming, greenhouse innovation, and franchise opportunities.

## Project Structure
```
city_farmers_bot/
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── bot/
│   │   ├── __init__.py
│   │   ├── twitter_bot.py
│   │   └── content_generator.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   └── utils/
│       ├── __init__.py
│       ├── redis_handler.py
│       └── logger.py
└── tests/
    └── __init__.py
```

## Features

- Automated tweet generation using Claude AI
- Twitter integration with OAuth 2.0
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

## Environment Variables

Required environment variables in `.env`:
```
TWITTER_CLIENT_ID=your_twitter_client_id
TWITTER_CLIENT_SECRET=your_twitter_client_secret
TWITTER_REDIRECT_URI=https://city-farmers-bot.onrender.com/callback
ANTHROPIC_API_KEY=your_anthropic_api_key
REDIS_URL=your_redis_url
LOG_LEVEL=INFO
ENVIRONMENT=production
```

## API Endpoints

### POST /post-tweet
Generate and post a tweet

**Query Parameters:**
- `content_type` (optional): Type of content to generate
  - `educational` (default): Aeroponic farming innovation
  - `franchise`: Franchise opportunities
  - `sustainability`: Sustainable urban farming

**Response:**
```json
{
    "status": "Tweet generation initiated",
    "content": "Generated tweet content"
}
```

## Deployment

The application is configured for deployment on Render.com:

1. Set up a Redis instance on Render
2. Create a Web Service:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
3. Configure environment variables in Render dashboard
4. Set up a cron job to hit `/post-tweet` at desired intervals

## License

MIT