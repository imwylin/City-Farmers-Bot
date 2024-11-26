# City Farmers Bot

A Twitter marketing bot for City Farmers, an innovative urban farming company. The bot generates and posts engaging content about aeroponic farming, greenhouse innovation, and franchise opportunities.

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

## Authentication

1. Visit `/auth/twitter` to start OAuth flow
2. Authorize the application with your Twitter account
3. Tokens will be automatically stored in Redis
4. Check `/health` to verify connection status

## API Endpoints

- `GET /auth/twitter`: Start Twitter OAuth flow
- `GET /callback`: OAuth callback handler
- `POST /post-tweet`: Generate and post a tweet
  - Query Parameters:
    - `content_type`: Type of content to generate (educational, decentralized, sustainability)
- `GET /health`: Check system health status

## Deployment

The application is configured for deployment on Render.com. Set up the following:

1. Redis instance on Render
2. Web Service pointing to main.py
3. Environment variables in Render dashboard
4. Scheduled task for automated posting

## License

MIT